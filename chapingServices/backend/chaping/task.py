import requests
from bs4 import BeautifulSoup

from .headers import get_header_ua

"""update
2020.6.8 
- update class to gl-item
- add headers

"""

def create_task(start_url):
    r = requests.get(start_url, headers={'User-Agent': get_header_ua()})  # need headers
    sp =BeautifulSoup(r.text, 'lxml')
    sku_list = [i['data-sku'] for i in sp.findAll(class_='gl-item')]
    return sku_list


def main():
    start_url = 'https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'
    task_list = create_task(start_url)

    print(task_list)


if __name__ == "__main__":
    main()