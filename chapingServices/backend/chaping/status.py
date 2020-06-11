#coding: utf-8
#author: de8ug

# 通过redis缓存状态信息

import json
import redis


redis_db0 = redis.StrictRedis(host='redis', port=6379, db=0)
redis_db1 = redis.StrictRedis(host="redis", port=6379, db=1)

STATUS_READY = 0
STATUS_CRAWLING = 1
STATUS_CRAWLING_ERROR = 2
STATUS_SAVING = 3
STATUS_SAVING_ERROR = 4
STATUS_SUCCESS = 100


class ResultStatus:
    def __init__(self, prefix='jd'):
        self.prefix = prefix

    def delete(self):
        for task_name in redis_db0.keys(f'{self.prefix}-*'):
            redis_db0.delete(task_name)  # delete the same key name

    def save_status(self, task_id, status):
        redis_db0.set(f'{self.prefix}-{task_id}', json.dumps(status))
        redis_db0.expire('{self.prefix}-{task_id}', 60*60*24)  # 缓存过期时间

    def get_status(self, task_name):
        status = redis_db0.get(task_name)
        return None if status is None else json.loads(status)

    def show_all(self, task_pattern='jd-*'):
        return [self.get_status(task_name) for task_name in redis_db0.keys(task_pattern)]


def main():
    status =  {'status': 1, 'statusText': 'csv ok good'}
    r = ResultStatus('de8ug')
    # r.save_status(888, status)
    # print(r.get_status('de8ug-666'))

    for i, v in enumerate(r.show_all('de8ug-*')):
        print(i, v)

if __name__ == "__main__":
    main()