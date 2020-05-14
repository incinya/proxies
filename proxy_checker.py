import requests
from utils.logger import log
from memory.memory_queue import RedisExpSet

time_out = 8


class ProxyChecker:
    def __init__(self):
        self.exp_set = RedisExpSet(set_name='poll', level='xici:')

    @staticmethod
    def check_proxy(url) -> bool:
        to = 'http://httpbin.org/get'
        proxies = {
            'http': 'http://' + url,
            'https': 'https://' + url,
        }
        try:
            log.info('start connection to {}'.format(url))
            res = requests.get(to, proxies=proxies, timeout=time_out)
        except Exception as e:
            log.debug('连接错误' + e.__str__())
            return False
        if url.split(':')[0] in res.text:
            return True
        return False

    def mem_proxy(self, url):
        self.exp_set.set_items(url)

    def check_and_mem_proxy(self, url):
        if self.check_proxy(url):
            self.mem_proxy(url)
            return True
        log.debug(('无效ip', url))
        return False


if __name__ == '__main__':
    p = ProxyChecker()
    p.check_proxy('121.237.148.101:3000')
