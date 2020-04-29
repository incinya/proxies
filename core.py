import asyncio

from xici_spider import XiciSpider


async def main():
    p = XiciSpider()
    tasks = [p.loop_set_list()]  # 打包任务
    done, pending = await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
