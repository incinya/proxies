import requests
from requests import ConnectTimeout

from logger import logger
from memory.memory_queue import ExpSet

time_out = 8
log = logger()


class ProxyChecker:
    def __init__(self):
        self.e = ExpSet(set_name='poll', level='xici:')

    @staticmethod
    def check_proxy(url):
        to = 'http://httpbin.org/get'
        proxies = {
            'http': 'http://' + url,
            'https': 'https://' + url,
        }
        try:
            res = requests.get(to, proxies=proxies, timeout=time_out)
        except ConnectTimeout:
            log.debug('连接超时' + url)
            return False
        if url.split(':')[0] in res.text:
            return True
        return False

    def mem_proxy(self, url):
        self.e.set_item(url)

    def check_and_mem_proxy(self, url):
        if self.check_proxy(url):
            self.mem_proxy(url)
            return True
        log.debug('无效ip')
        return False


if __name__ == '__main__':
    p = ProxyChecker()
    p.check_proxy('121.237.148.101:3000')
