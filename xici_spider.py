import re
import requests
import fake_useragent

from logger import logger

log = logger()


class ProxiesSpider:
    url = 'https://www.xicidaili.com/nn/{}.html'
    re_str = r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>'

    def get_1page_html(self, page):
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
        pattern = re.compile(ProxiesSpider.re_str, re.S)
        result = pattern.findall(html)
        return [tup[0] + ':' + tup[1] for tup in result]


if __name__ == "__main__":
    p = ProxiesSpider()
    aa = p.get_1page_html(1)

