import asyncio
import aiohttp
from memory.redis_memory import RedisExpSet
from utils.logger import log
from xici_queue import XiciEnQueue


class XiciStack:
    queue = 'xici:xici_proxy_queue'
    stack = 'xici:xici_proxy_stack'
    queue_mem_set = RedisExpSet(queue)
    stack_mem_set = RedisExpSet(stack)
    sem = 10
    stack_size = 50
    poll_time = 60
    stack_exp = 10 * 60
    time_out = 10

    @staticmethod
    async def loop_send_req():
        while True:
            url = 'http://httpbin.org/get'
            proxy = 'http://' + XiciEnQueue.de_queue()
            # 信号量，控制协程数，防止爬的过快
            async with asyncio.Semaphore(XiciStack.sem):
                print('url', url, 'proxy', proxy)
                # async with是异步上下文管理器
                async with aiohttp.ClientSession() as session:  # 获取session
                    try:
                        async with session.get(url, proxy=proxy) as resp:  # 提出请求
                            html = await resp.read()  # 可直接获取bytes
                            log.debug(html)
                    except Exception as e:
                        log.debug(e)

    def main(self):
        loop = asyncio.get_event_loop()  # 获取事件循环
        tasks = [self.loop_send_req() for _ in range(XiciStack.sem)]  # 把所有任务放到一个列表中
        while True:
            loop.run_until_complete(asyncio.wait(tasks, timeout=XiciStack.time_out))  # 激活协程


if __name__ == "__main__":
    # DEBUG:root:b'{ "origin": "39.137.107.98", \n  "url": "http://httpbin.org/get"\n}\n'
    x2 = XiciStack()
    x2.main()
