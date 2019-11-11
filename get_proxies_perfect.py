import time
import csv
import requests
from lxml.html import etree
import fake_useragent
from multiprocessing import Process


class ProxiesSpider:
    def __init__(self):
        self.url = 'http://ip.yqie.com/proxygaoni/index_{}.htm'
        self.url2 = 'http://httpbin.org/get'
        self.i = 0

    def get_html(self):
        for i in range(1, 3423):
            url = self.url.format(i)
            headers = {'User-Agent': fake_useragent.UserAgent().random}

            res = requests.get(url,
                               headers=headers,
                               timeout=5
                               )
            html = res.content
            self.parse_html(html)
            print('第{}页抓取完成'.format(i))

    def parse_html(self, html):
        parse_obj = etree.HTML(html)
        # print(html)
        r_list = parse_obj.xpath('//tr/td/text()')
        # print(r_list)
        # ['1', '106.75.226.36', '808', '山东济南', 'HTTPS', '2018-10-02', '2', '118.190.95.43', '9001', '广西'

        r_list_ip = []  # 1,7,13,19...
        r_list_port = []  # 2,8,14,20.....
        r_list_addr = []
        for i in range(0, len(r_list), 6):
            r_list_ip.append(r_list[i + 1])
            r_list_port.append(r_list[i + 2])
            # print(r_list_ip)  # ['106.75.226.36', '118.190.95.43', '118.190.95.35',
            # print(r_list_port)  # ['808', '9001', '9001', '80', '37259', '3128',
        for i in range(len(r_list_ip)):
            r_list_addr.append(r_list_ip[i] + ':' + r_list_port[i])

        # print(r_list_addr)
        # input()
        p_list = []
        for i in range(len(r_list_addr)):
            self.i += 1
            p = Process(target=self.test_html, args=(r_list_addr[i],))
            p.daemon = True
            time.sleep(0.1)
            p_list.append(p)
            p.start()
        for p in p_list:
            p.join()

    def test_html(self, addr):
        proxies = {
            'http': 'http:' + addr,
            # 'http': 'http://61.157.206.174:37259',
            'https': 'https' + addr,
        }


        # try:
        #     res = requests.get(self.url2, proxies=proxies, timeout=8)
        #     res.encoding = 'utf-8'
        #     print(res.text)
        #     print(res.status_code)
        #     if "https://httpbin.org/get" in res.text:
        #         self.write_html(addr)
        # except Exception as e:
        #     print('failed', '     count', self.i)

        for i in range(3):
            try:
                res = requests.get(self.url2, proxies=proxies, timeout=8)
                res.encoding = 'utf-8'
                print(res.text)
                print(res.status_code)
                if "https://httpbin.org/get" in res.text:
                    self.write_html(addr)

            except Exception:
                print(addr, end='---->')
                print('failed for {}'.format(i), '   id for >>>>>>', self.i)

    def write_html(self, addr):

        with open('proxies.csv', 'r') as f:
            reader = csv.reader(f)
            for item in reader:
                if addr in item:
                    print('>>>>>>>>>addr existed<<<<<<<<<<')
                    return
        with open('proxies.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([addr])

    def run(self):
        self.get_html()


if __name__ == "__main__":
    s01 = ProxiesSpider()
    s01.run()
