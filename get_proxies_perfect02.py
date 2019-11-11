import time
import re
import csv
import requests
import fake_useragent
from multiprocessing import Process


class ProxiesSpider:
    def __init__(self):
        self.url = 'https://www.xicidaili.com/nn/{}.html'
        self.url2 = 'http://httpbin.org/get'
        self.i = 0

    def get_html(self):
        for i in range(1, 3423):
            url = self.url.format(i)
            headers = {'User-Agent': fake_useragent.UserAgent().random}

            try:
                res = requests.get(url,
                                   headers=headers,
                                   timeout=5
                                   )
            except Exception:
                continue
            res.encoding = 'utf-8'
            html = res.content
            self.parse_html(html)
            print('第{}页抓取完成,休眠2秒,抓取下一页.....'.format(i))
            time.sleep(2)

    def parse_html(self, html):
        html = html.decode()
        pattern = re.compile(r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>', re.S)
        result_list = pattern.findall(html)
        # [('121.226.53.201', '61234'), ('120.83.97.81', '9999')......]

        r_list_addr = []
        for tup in result_list:
            r_list_addr.append(tup[0] + ':' + tup[1])
        # ['121.226.53.201:61234', '120.83.97.81:9999',......]
        # print(r_list)

        # print(r_list_addr)
        # ['xxx.xxx.xxx.xxx:xxxx',...]
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

        # for p in p_list:
        #     p.join()
        # self.test_html(r_list_addr[i])

    def test_html(self, addr):
        proxies = {
            'http': 'http:' + addr,
            # 'http': 'http://61.157.206.174:37259',
            'https': 'https' + addr,
        }

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

    @staticmethod
    def write_html(addr):

        with open('proxies.csv', 'r') as f:
            reader = csv.reader(f)
            for item in reader:
                if addr in item:
                    print('>>>>>>>>>addr existed<<<<<<<<<<')
                    return
        with open('proxies.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([addr])
            f.flush()

    def run(self):
        self.get_html()


if __name__ == "__main__":
    s01 = ProxiesSpider()
    s01.run()
