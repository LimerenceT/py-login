import requests
import re
import json
import time
from html.parser import HTMLParser

class HTML_Parser(HTMLParser):
    a = False
    result_str = []
    def handle_starttag(self, tag, attrs):
        if attrs:
            if tag=='li'and attrs[0][0]=='title':
                self.a = True
    def handle_data(self, data):
        if self.a:
            self.result_str.append(data)
    def handle_endtag(self, tag):
        if tag == 'li':
            self.a = False
    def show_result(self):
        return '\n'.join(self.result_str)
def search_taobao():
    headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',

                }
    search='围城'
    api_url = 'https://s.taobao.com/search?q='+search
    session = requests.session()
    res = session.get(api_url,headers=headers)
    goods_urls = []
    html_paser = HTML_Parser()
    result = ''
    res_json = json.loads(re.findall(r'g_page_config = (.*);', res.text)[0])
    try:
        for dd in res_json['mods']['itemlist']['data']['auctions']:
            goods_urls.append(dd['detail_url'])

        for page in range(1):#想要输出的商品搜索结果数量
            try:
                response = requests.get(goods_urls[page], headers=headers)
            except:
                response = requests.get(u'https:'+goods_urls[page],headers=headers)
            html_paser.feed(response.text)
        result = html_paser.show_result()
    except:
        result = '没有搜到结果'
    print(result)

if __name__ == '__main__':
    start = time.clock()
    search_taobao()
    end = time.clock()
    print (str(end-start))