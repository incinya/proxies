import asyncio
import re
import time
import requests
import fake_useragent

from logger import logger
from memory.memory_queue import ExpSet

log = logger()
POLLTIME = 10
POOL_SIZE = 100


class XiciSpider:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'
    count = 0
    key = 'xici:xici_proxy_set'
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
            log.debug(e)
            return []
        res.encoding = 'utf-8'
        html = res.text
        return self.parse_html(html)

    @staticmethod
    def parse_html(html):
        pattern = re.compile(XiciSpider.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]

    async def loop_get_list(self):
        mem = XiciSpider.mem
        key = XiciSpider.key
        while True:
            XiciSpider.count += 1
            res = await self.get_1page_html(XiciSpider.count)
            for item in res:
                mem.set_item(item)
                print(item)
            m = mem.get(XiciSpider.key)
            aa = 2


if __name__ == "__main__":
    p = XiciSpider()
    loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(p.get_1page_html(1))
    loop.run_until_complete(p.loop_get_list())
    vv = 1
