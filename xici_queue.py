import re
import time
import fake_useragent
import requests
from memory.memory_queue import ExpSet
from utils.logger import log


class XiciProxyQueue:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    count = 0
    key = 'xici:xici_proxy_queue'
    poll_time = 4
    queue_exp = 10 * 60
    queue_size = 100
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

    def loop_en_queue(self):
        mem = XiciProxyQueue.mem
        while True:
            X = XiciProxyQueue
            X.count += 1

            res = self.get_1page_html(X.count)
            for item in res:
                size = len(mem.get_all())
                while size >= X.queue_size:
                    mem.flush(X.queue_exp)
                    size = len(mem.get_all())
                    log.info(
                        'queue_size over {},sleeping for poll_time {}'.format(X.queue_size,
                                                                              X.poll_time))
                    time.sleep(X.poll_time)
                mem.set(item)

    @staticmethod
    def de_queue():
        res = XiciProxyQueue.mem.get_oldest()[0]
        XiciProxyQueue.mem.delete(res)
        return res


if __name__ == "__main__":
    x1 = XiciProxyQueue()
    x1.loop_en_queue()
