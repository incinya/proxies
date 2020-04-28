import asyncio
import time
from unittest import TestCase

import requests


class ProxyTest(TestCase):
    a = 1

    def setUp(self) -> None:
        ...

    def test_proxy(self):
        url = '117.88.176.42:3000'

        to = 'http://httpbin.org/get'
        time_out = 8
        proxies = {
            'http': 'http://' + url,
            'https': 'https://' + url,
        }
        res = requests.get(to, proxies=proxies, timeout=time_out)
        print(url.split(':')[0] in res.text)
        print(res.text)

    def test_a(self):
        ProxyTest.a += 1
        print(self.a)
        print(ProxyTest.a)

    def test_asnic(self):
        def f1():
            print(998)
            time.sleep(1)
            print(998)
            time.sleep(1)
            print(998)
            time.sleep(1)

        async def hello():
            print("Hello world!")
            await f1()
            print("Hello again!")

        loop = asyncio.get_event_loop()
        tasks = [hello(), hello()]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def test_yield1(self):
        def num():
            yield 1
            yield 2
            yield 3
            yield 4

        c = num()
        while True:
            print(c.send(None))
            time.sleep(1)

    def test_yield2(self):
        def num():
            a = yield 1
            while True:
                a = yield a

        c = num()

        print(c.send(None))
        time.sleep(4)
        print(c.send(10))

    def test_yield3(self):
        def a():
            next_val = yield print('start!')
            while True:
                next_val += 1
                next_val = yield next_val

        def b(gen):
            gen.send(None)
            bb = 0
            for i in range(5):
                bb = gen.send(bb)
                print(bb)
                time.sleep(1.5)

        b(a())

    def test_yiled4(self):
        def generator_1(titles):
            yield titles

        def generator_2(titles):
            yield from titles

        titles = ['Python', 'Java', 'C++']

        a = generator_1(titles)
        print(a.send(None))

        b = generator_2(titles)
        print(b.send(None))
        print(b.send(None))
        print(b.send(None))

    def test_yiled5(self):
        def generator_1():
            total = 0
            while True:
                x = yield
                print('加', x)
                if not x:
                    break
                total += x
            return total

        def generator_2():  # 委托生成器
            while True:
                total = yield from generator_1()  # 子生成器
                print('加和总数是:', total)

        def main():  # 调用方
            # g1 = generator_1()
            # g1.send(None)
            # g1.send(2)
            # g1.send(3)
            # g1.send(None)
            g2 = generator_2()
            g2.send(None)
            g2.send(2)
            g2.send(3)
            g2.send(None)

        main()

    def test_yield6(self):
        # 使用同步方式编写异步功能
        import time
        import asyncio

        async def taskIO_1():
            print('开始运行IO任务1...')
            await asyncio.sleep(2)  # 假设该任务耗时2s
            print('IO任务1已完成，耗时2s')
            return taskIO_1.__name__

        async def taskIO_2():
            print('开始运行IO任务2...')
            await asyncio.sleep(3)  # 假设该任务耗时3s
            print('IO任务2已完成，耗时3s')
            return taskIO_2.__name__

        async def main():  # 调用方
            tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
            done, pending = await asyncio.wait(tasks)  # 子生成器
            for r in done:  # done和pending都是一个任务，所以返回结果需要逐个调用result()
                print('协程无序返回值：' + r.result())

        start = time.time()
        loop = asyncio.get_event_loop()  # 创建一个事件循环对象loop
        try:
            loop.run_until_complete(main())  # 完成事件循环，直到最后一个任务结束
        finally:
            loop.close()  # 结束事件循环
        print('所有IO任务总耗时%.5f秒' % float(time.time() - start))
