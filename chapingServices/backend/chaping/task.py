import requests
from bs4 import BeautifulSoup

from .headers import get_header_ua
from .utils import get_proxy, de8ug_log, delete_proxy

"""update
2020.6.8 
- update class to gl-item
- add headers

"""

logger = de8ug_log(__name__)

def create_task(start_url):
    count = 5
    while count > 0:
        proxy = get_proxy().get("proxy")
        logger.info(f'第[ {count} ]次 create task from {start_url}')
        proxies = {"http": "http://{}".format(proxy)}
        headers = {
            'User-agent': get_header_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Connection": "keep-alive",
            "cache-control": "max-age=0",
            "dnt": "1",
            "referer": "https://www.jd.com/allSort.aspx",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
            } 
        r = requests.get(start_url, 
                        proxies=proxies,
                        headers=headers)  # need headers
        logger.info(f'第[ {count} ]次 response {r.text[:30]}')
        
        if not r.text:
            delete_proxy(proxy)
            count -= 1
        else:
            break
    if r.text:
        sp = BeautifulSoup(r.text, 'lxml')
        sku_list = [i['data-sku'] for i in sp.findAll(class_='gl-item')]
        return sku_list


def main():
    start_url = 'https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_commentcount_desc&trans=1&JL=4_5_0#J_main'
    task_list = create_task(start_url)

    print(task_list)


if __name__ == "__main__":
    main()