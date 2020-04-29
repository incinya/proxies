import asyncio
import re
import time
import requests
import fake_useragent

from logger import log
from memory.memory_queue import ExpSet
from proxy_checker import ProxyChecker


class XiciSpider:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    count = 0
    key = 'xici:xici_proxy_set'
    poll_time = 10
    pool_size = 100
    mem = ExpSet(key)

    async def get_1page_html(self, page):
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
        pattern = re.compile(XiciSpider.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]

    async def loop_set_list(self):
        mem = XiciSpider.mem
        while True:
            XiciSpider.count += 1
            res = await self.get_1page_html(XiciSpider.count)
            for item in res:
                size = len(mem.get_all())
                while size >= XiciSpider.pool_size:
                    log.info(
                        'pool_size over {},sleeping for pool_time {}'.format(XiciSpider.pool_size,
                                                                             XiciSpider.poll_time))
                    time.sleep(XiciSpider.poll_time)
                p = ProxyChecker()
                if await p.check_proxy(item) is False:
                    continue
                mem.set(item)
                log.info(item)


if __name__ == "__main__":
    x = XiciSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(x.loop_set_list())
    vv = 1
