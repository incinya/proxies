import asyncio
import aiohttp

from spider.proxy_model import ProxyStack
from spider.xici_ip_model import XiciQueue
from utils.logger import log


class AsyncSpider:
    """only support http proxy"""

    def __init__(self, queue, stack):
        self.queue = queue
        self.stack = stack

    sem = 20
    stack_size = 50
    poll_time = 60
    stack_exp = 10 * 60
    time_out = 10

    async def loop_send_req(self):
        while True:
            url1 = 'http://httpbin.org/get'
            url2 = self.queue.de_queue()
            proxy = 'http://' + url2
            # 信号量，控制协程数，防止爬的过快
            async with asyncio.Semaphore(AsyncSpider.sem):
                print('url', url1, 'proxy', proxy)
                # async with是异步上下文管理器
                async with aiohttp.ClientSession() as session:  # 获取session
                    try:
                        async with session.get(url1, proxy=proxy) as resp:  # 提出请求
                            html = await resp.read()  # 可直接获取bytes
                            if url2 in html.decode():
                                self.stack.en_stack(url1)
                                log.info(('in stack 1', url2))
                    except Exception as e:
                        log.debug(e)

    def main(self):
        loop = asyncio.get_event_loop()  # 获取事件循环
        tasks = [self.loop_send_req() for _ in range(AsyncSpider.sem)]  # 把所有任务放到一个列表中
        while True:
            loop.run_until_complete(asyncio.wait(tasks, timeout=AsyncSpider.time_out))  # 激活协程


if __name__ == "__main__":
    # DEBUG:root:b'{ "origin": "39.137.107.98", \n  "url": "http://httpbin.org/get"\n}\n'
    x2 = AsyncSpider(XiciQueue, ProxyStack)
    x2.main()
