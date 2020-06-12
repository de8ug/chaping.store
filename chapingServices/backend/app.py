import json

from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from celery import Celery
import pymongo

from chaping.utils import create_token_by_url, de8ug_log
from chaping.task import create_task
from chaping.chaping import download_all
from chaping.status import ResultStatus, redis_db1
from chaping.analysis_jd import get_result
from settings import mongo_params, tokens, ce_broker



app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": '*'}})
api = Api(app)


auth = HTTPTokenAuth(scheme='Token')



@auth.verify_token
def verify_token(token):  
    print('验证。。。', token)
    if token in tokens:
        # g.current_user = tokens[token]
        return True
    return False


# 创建异步的任务
celery = Celery(app.name, broker=ce_broker)

# log
logger = de8ug_log()

# 调用download_all(task_list, save_type='csv', db_client=None, db_name='chaping'):
@celery.task
def run_download(task_list, db_name, save_type='mongodb'):
    logger.debug('run_download...')
    
    try:
        client = pymongo.MongoClient(**mongo_params)
        logger.info('run_download with celery...\n')
        download_all(task_list, save_type, client, db_name)
    except Exception as e:
        print(e)
        logger.debug(e)

class TaskApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='give a name')  
        self.parser.add_argument('url', type=str, help='give a url')  

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        for k, v in args.items():
            print(k, v)
        # 通过url，计算一个token作为任务的标识符
        url = args['url']

        token = create_token_by_url(url)
        logger.info(url)
        result = {'status': 0, 'statusText': '创建成功', 'token': token}

        # save token and hot words
        name = args['name']
        status = ResultStatus('hot')
        status.save_status(token, {'url':url, 
                                    'words':name,
                                    'token':token})

        # create task
        sku_list = create_task(url)
        print(f'sku_list: {sku_list}')

        if sku_list:
            result['sku_list'] = sku_list  # SAVE FOR FRONT USE

            # 执行异步任务
            # 测试可以少一点
            # sku_list = sku_list[:5]
            logger.info('开始异步执行任务...')
            run_download.delay(sku_list, db_name='chaping-' + token)
        else:
            result['status'] = 1
            result['statusText'] = '创建失败'

        return result, 200


class StatusApi(Resource):

    @auth.login_required
    def get(self):
        token = request.args.get('token', '')
        logger.debug(f'checking status: {token}')

        if token:
            status = ResultStatus(token)
            return status.show_all(task_pattern=f'{token}*')
        else:
            return {}


def get_paginated_list(results, url, start, limit):
    """自定义分页
    """
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


class ResultApi(Resource):
    def __init__(self):
        self.client = pymongo.MongoClient(**mongo_params)
        super().__init__()

    def get(self):
        """ 注意: 不用返回所有数据！！！
        - 分页！
        - 先从缓存取数据没有再从数据库取
        """
        token = request.args.get('token', '')
        key = request.args.get('key', '')  # sum, chaping
        update = request.args.get('update', '')  # update
        logger.debug(f'{token} - {key} - {update}')
        
        if key == 'sum':
            token = f'{key}-{token}'
            print(f'get {key}, now, token={token}')
        
        # using cache first
        results = redis_db1.get(token)
        if results and not update:
            # print('使用缓存数据：', results)
            results = json.loads(results)
        else:
            if key == 'sum':
                db = self.client.get_database(token)  # already sum
                results = []
                try:
                    name_list = sorted(db.list_collection_names())
                    print('sum result:', name_list)

                    for name in name_list:
                        col = db.get_collection(name)
                        dic = col.find()[0] 
                        del dic['_id']  # we don't need this id
                        # print({name:dic})
                        results.append(dic)
                except Exception as e:
                    print(e)
                    logger.debug(e)

            else:
                db = self.client.get_database(f'chaping-{token}')   # 1st 
                results = get_result(db)                   # 1st
            # print('使用数据库数据: ', results)
            if token and results:  # saving to redis
                print(token)
                redis_db1.set(token, json.dumps(results))
                redis_db1.expire(token, 60*60*24)  # 缓存过期时间
        
        return jsonify(get_paginated_list(
                        results, 
                        '/api/v1/results', 
                        start=request.args.get('start', 1), 
                        limit=request.args.get('limit', 10)
                    ))


api.add_resource(TaskApi, '/api/v1/task')
api.add_resource(StatusApi, '/api/v1/status')
api.add_resource(ResultApi, '/api/v1/results', endpoint='results')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)  # need call from outside
    app.run(host="0.0.0.0")  # need call from outside
    logger.debug(f'\n\nstart to run flask .............\n\n')
