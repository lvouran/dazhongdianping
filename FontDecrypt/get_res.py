# -*- coding:utf-8 -*-
# author:lvao
# datetime:2019/5/30 11:00
# software: PyCharm

import requests
from settings import HEADERS
from requests.exceptions import ConnectionError


def retry(max_num=1):
    def warpper(func):
        def _war(*args, **kwargs):
            for num in range(max_num):
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    pass
        return _war
    return warpper


@retry(max_num=3)
def get_response(url):
    assert url, f'url {url}不能为空'
    if 'http' not in url:
        url = 'http:' + url
    print(url)
    res = requests.get(url, headers=HEADERS)
    return res


if __name__ == '__main__':
    get_response('https://baidu.com')
