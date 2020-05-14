import re
import time
import fake_useragent
import requests

from memory.redis_memory import RedisExpSet
from utils.logger import log


class XiciQueue:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    count = 0
    key = 'xici:xici_proxy_queue'
    poll_heart_beat = 4
    queue_exp = 10 * 60
    queue_size = 100
    mem_set = RedisExpSet(key)

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
        pattern = re.compile(XiciQueue.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]

    def loop_en_queue(self):
        mem = XiciQueue.mem_set
        while True:
            X = XiciQueue
            X.count += 1

            res = self.get_1page_html(X.count)
            for item in res:
                size = len(mem.get_all())
                while size >= X.queue_size:
                    mem.flush(X.queue_exp)
                    size = len(mem.get_all())
                    log.debug(
                        'queue_size over {},sleeping for poll_time {}'.format(X.queue_size,
                                                                              X.poll_heart_beat))
                    time.sleep(X.poll_heart_beat)
                mem.set(item)

    @staticmethod
    def de_queue():
        res = XiciQueue.mem_set.get_oldest()[0]
        XiciQueue.mem_set.delete(res)
        return res


if __name__ == "__main__":
    x1 = XiciQueue()
    x1.loop_en_queue()
