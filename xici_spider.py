import re
import time
import requests
import fake_useragent
from logger import log
from memory.memory_queue import ExpSet


class XiciProxyQueue:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    count = 0
    key = 'xici:xici_proxy_queue'
    poll_time = 60
    queue_exp = 10 * 60
    queue_size = 50
    mem = ExpSet(key)

    def get_1page_html(self, page):
        url = self.url.format(page)
        headers = {'User-Agent': fake_useragent.UserAgent().random}
        try:
            res = requests.get(url,
                               headers=headers,
                               timeout=5
                               )
        except Exception as e:
            log.error(e)
            return []
        res.encoding = 'utf-8'
        html = res.text
        return self.parse_html(html)

    @staticmethod
    def parse_html(html):
        pattern = re.compile(XiciProxyQueue.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]

    def loop_set_list(self):
        mem = XiciProxyQueue.mem
        while True:
            X = XiciProxyQueue
            X.count += 1
            res = self.get_1page_html(X.count)
            for item in res:
                size = len(mem.get_all())
                while size >= XiciProxyQueue.queue_size:
                    size = len(mem.get_all())
                    mem.flush(X.poll_time)
                    log.info(
                        'pool_size over {},sleeping for pool_time {}'.format(X.queue_size,
                                                                             X.poll_time))
                    time.sleep(X.poll_time)
                mem.set(item)


if __name__ == "__main__":
    x = XiciProxyQueue()
    x.loop_set_list()
