import hashlib
import string
import random

import requests


def create_token_by_url(url, num=6):
    return hashlib.md5(url.encode()).hexdigest()[:num]


def create_token(num=6):
    str_from = string.ascii_letters + string.digits
    return ''.join([random.choice(str_from) for _ in range(num)])

# proxy
def get_proxy():
    return requests.get("http://proxy_pool:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://proxy_pool:5010/delete/?proxy={}".format(proxy))

# log
import logging

def de8ug_log(logger_name='== DE8UG-LOG ==', log_file='logs/de8ug.log', level=logging.DEBUG):
    # 创建 logger对象
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 添加等级

    # 创建控制台 console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # 创建文件 handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')

    # 创建 formatter
    formatter = logging.Formatter('%(asctime)s == %(filename)s [line:%(lineno)d] %(name)s %(levelname)s == %(message)s')

    # 添加 formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 把 ch， fh 添加到 logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger