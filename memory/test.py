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

    def test_loggin(self):
        ...
