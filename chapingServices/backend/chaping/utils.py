import hashlib
import string
import random


def create_token_by_url(url, num=6):
    return hashlib.md5(url.encode()).hexdigest()[:num]


def create_token(num=6):
    str_from = string.ascii_letters + string.digits
    return ''.join([random.choice(str_from) for _ in range(num)])