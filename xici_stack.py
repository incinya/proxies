import asyncio
import aiohttp
from utils.logger import log
from memory.memory_queue import ExpSet
from xici_queue import XiciProxyQueue


class XiciProxyStack:
    queue = 'xici:xici_proxy_queue'
    stack = 'xici:xici_proxy_stack'
    mem_q = ExpSet(queue)
    mem_s = ExpSet(stack)
    sem = 10
    stack_size = 50
    poll_time = 60
    stack_exp = 10 * 60
    time_out = 10

    @staticmethod
    async def loop_send_req():
        while True:
            url = 'http://httpbin.org/get'
            proxy = 'http://' + XiciProxyQueue.de_queue()
            # 信号量，控制协程数，防止爬的过快
            async with asyncio.Semaphore(XiciProxyStack.sem):
                print(url, proxy)
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
        tasks = [self.loop_send_req() for _ in range(XiciProxyStack.sem)]  # 把所有任务放到一个列表中
        while True:
            loop.run_until_complete(asyncio.wait(tasks, timeout=XiciProxyStack.time_out))  # 激活协程


if __name__ == "__main__":
    # DEBUG:root:b'{ "origin": "39.137.107.98", \n  "url": "http://httpbin.org/get"\n}\n'
    x2 = XiciProxyStack()
    x2.main()
