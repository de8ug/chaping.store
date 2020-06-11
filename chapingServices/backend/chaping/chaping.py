#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# 爬取评论数据，并对差评进行分析

import json
import re
import time
import random
import csv
from urllib.parse import urlparse
from datetime import datetime, timedelta
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

from .task import create_task
from .headers import get_header_ua
from .timeit import DecoTime
from .status import *  # 确认一下啥时候用*



class Throttle:
    """阀门类，对相同域名的访问添加延迟时间，避免访问过快
    """
    def __init__(self, delay):
        # 延迟时间，避免访问过快
        self.delay = delay
        # 用字典保存访问某域名的时间
        self.domains = {}
        
    def wait(self, url):
        """对访问过的域名添加延迟时间
        """
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


class Downloader:
    """下载类，根据url返回内容
    """
    def __init__(self, headers=None, num_retries=3, proxies=None, delay=2, timeout=30):
        self.headers = headers
        self.num_retries = num_retries
        self.proxies = proxies
        self.throttle = Throttle(delay)
        self.timeout = timeout

    def download(self, url, is_json=False):
        print('下载页面:', url)
        self.throttle.wait(url)
        try:
            response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            print(response.status_code)

            if response.status_code == 200 and response.content:
                if is_json:
                    return response.json()
                else:
                    return response.content
            return None
        except RequestException as e:
            print('error:', e.response)
            html = ''
            if hasattr(e.response, 'status_code'):
                code = e.response.status_code
                print('error code:', code)
                if self.num_retries > 0 and 500 <= code < 600:
                    # 遇到5XX 的错误就重试
                    html = self.download(url)
                    self.num_retries -= 1
            else:
                code = None
        return html


class Recorder:
    """记录类，根据不同保存类型使用相应方法。
    通过类对象使用回掉函数方式直接调用
    """
    def __init__(self, save_type='csv', db_client=None):
        """
            如果db_client存在，则使用mongodb，把save_type='mongodb'
        """
        self.save_type = save_type
        self.db_client = db_client

    def __call__(self, filename, fields, all_list):
        if hasattr(self, self.save_type):
            func = getattr(self, self.save_type)
            return func(filename, fields, all_list)
        else:
            return {'status': 1, 'statusText': 'no record function'}

    def csv(self, filename, fields, all_list):
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                # fields = ('id', '名称', '价格', '评价人数', '好评率')
                writer.writerow(fields)
                for row in all_list:
                    writer.writerow(row)
            return {'status': 0, 'statusText': 'csv saved'}
        except Exception as e:
            print(e)
            return {'status': 1, 'statusText': 'csv error'}

    def mongodb(self, db_name, collection_name, all_list):
        db = self.db_client[db_name]
        collection = db[collection_name]
        try:
            collection.drop()  # clear first
            ret = collection.insert_many(all_list)
            if ret:
                return {'status': 0, 'statusText': 'db saved'}
        except Exception as e:
            print(e)
            return {'status': 1, 'statusText': 'db error'}


class ItemCommentSpider:
    """抓取商品评价信息
    """
    def __init__(self, headers=None, num_retries=3, proxies=None, delay=2, timeout=30, task_id=None, token=''):
        self.headers = headers
        self.num_retries = num_retries
        self.proxies = proxies
        self.throttle = Throttle(delay)
        self.timeout = timeout
        
        self.task_id = task_id
        self.token = token  # for save hot words as a db name
        self.status = ResultStatus(prefix=token)
        self.result = {'_id': task_id, 'status':STATUS_READY, 'statusText':'准备中'}
        
        self.download = Downloader(headers, num_retries, proxies, delay, timeout)

            
    def get_comment_by_json(self, url):
        # http://sclub.jd.com/comment/productPageComments.action?productId=6946647&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1

        self.status.save_status(self.task_id, self.result)
        data = self.download.download(url, is_json=True)

        self.result['status'] = STATUS_CRAWLING
        self.result['statusText'] = '爬取中'
        self.status.save_status(self.task_id, self.result)

        data_list = []
        if not isinstance(data, dict):
            self.result['status'] = STATUS_CRAWLING_ERROR
            self.result['statusText'] = '爬取出错，内容为空'
            self.status.save_status(self.task_id, self.result)
            return data_list

        # update：summary comments also return，2020.6.8
        comments, commentsSum = data['comments'], data['productCommentSummary']
        return comments, commentsSum
        # for c in comments:
        #     row = []
        #     try:
        #         row.append(c['creationTime'])
        #         row.append(c['userClientShow'])
        #         row.append(c['userLevelName'])

        #         row.append(c['referenceName'])
        #         row.append(c['productSize'])
        #         row.append(c['productColor'])
        #         row.append(c['productSales'][0]['saleValue'])
        #         row.append(c['content'])
        #     except Exception as e:
        #         print(e, c['productSales'])

        #     data_list.append(row)
        # return data_list

    def fetch_data(self, url, filename, page_start, page_end, page_offset, callback=None):
        all_list = []
        commentsSum = {}
        page_num = 1
        for page in range(page_start, page_end, page_offset):
            data_list, commentsSum = self.get_comment_by_json(url.format(page))
            all_list += data_list
            print(f'完成第{page_num}页')
            page_num += 1

        # save commentsSum in sum- db name
        # we need a list to save...
        callback(f'sum-{self.token}', self.task_id, [commentsSum])

        # if callback:
        #     callback(filename, ('creationTime', 'userClientShow', 'userLevelName', 'productSize', "productColor", 'saleValue', "content"), all_list)
        if callback:
            self.result['status'] = STATUS_SAVING
            self.result['statusText'] = '保存中'
            # self.status.save_status(self.task_id, self.result)

            back_result = callback(filename, self.task_id, all_list)
            if back_result['status']:
                self.result['status'] = STATUS_SAVING_ERROR
                self.result['statusText'] = back_result['statusText']
            else:
                self.result['status'] = STATUS_SUCCESS
                self.result['statusText'] = '成功'

        self.status.save_status(self.task_id, self.result)

        return self.result


def download_by_id(task_id, save_type='csv', db_client=None, db_name='chaping'):
    headers = {
        'User-agent': get_header_ua(),
        "referer": f"https://item.jd.com/{task_id}.html"
        } 

    delay = random.randint(2,8)
    # spider = ItemCommentSpider(headers=headers, delay=delay, task_id=task_id, token=db_name)
    spider = ItemCommentSpider(headers=headers, delay=delay, task_id=task_id, token=db_name.split('-')[-1]) # token根据db_name进行截取:db_name-token -> token

    url = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + task_id + '&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'
    # ret = spider.get_comment_by_json(url)
    # print(len(ret))
    # return spider.fetch_data(url, f'db/db-{task_id}.csv', 0, 5, 1, Recorder('csv'))
    return spider.fetch_data(url, db_name,  0, 5, 1, Recorder(save_type, db_client))


@DecoTime()
def download_all(task_list, save_type='csv', db_client=None, db_name='chaping'):
    """使用线程池处理多个任务
    41s
    """
    print('download_all')

    # clear status db first
    token = db_name.split('-')[-1]
    status = ResultStatus(prefix=token)
    status.delete()

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_id = {executor.submit(download_by_id, task_id, save_type, db_client, db_name): task_id for task_id in task_list}
        for future in concurrent.futures.as_completed(future_to_id):
            task_id = future_to_id[future]
            print(task_id, future.result())

    print(f'共执行了{len(task_list)}个任务')


@DecoTime()
def download_all_old(start_url):
    """
    10个任务，每个5页== 161s
    """
    task_list = create_task(start_url)
    for task_id in task_list[:10]:
        download_by_id(task_id)
    print(f'共执行了{len(task_list)}个任务')


def main():
    start_url = 'https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'

    # download_all(start_url)
    import pymongo
    client = pymongo.MongoClient()
    db_name = 'chaping-888'

    task_list = create_task(start_url)    
    download_all(task_list[:10], 'mongodb', client, db_name)

   


if __name__ == '__main__':
    main()