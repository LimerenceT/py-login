import requests
import re
import time
from bs4 import BeautifulSoup
import queue
import threading
urls_queue = queue()
out_queue = queue()

class ThreadCrawl(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
    def run(self):
        while True:
            item = self.queue.get()
            self.queue.task_down()

class ZhiHu(object):
    def __init__(self):
        self.cookies = dict(
                q_c1="28f6c24badd04adc957563f319727083|1504849432000|1504849432000",
                r_cap_id="NmE1YWI4YzVkMTAzNGI5N2E4YzNjMjA4ZDQzNzBjMmU=|1504849432|ea8e6613f05a11d5d2e9b90162cf8e7a7eac1224",
                cap_id="NzQ4YTM0ZWI3Mzc4NGZhYWI1OTY1NzdlNWI2MDFjNDg=|1504849432|db78b0b8b65cc626e0699af784645e4f1648af72",
                d_c0="AIBCNLAUWAyPTjqhDhhkMev7dHwGz-z481c=|1504849433",
                _zap="57844534-0d68-4f19-abe5-77fea7674bf4",
                l_n_c="1",
                z_c0="Mi4xaThuMUFRQUFBQUFBZ0VJMHNCUllEQmNBQUFCaEFsVk5JcnZaV1FCSUNjN0pzSk9KWk0zTlRQX1l6QlVOMkNZYXRR|1504849442|212c4e85274e545ac879b039077055b3d27d2b64",
                _xsrf="b86c20d1f76e413d51486c1fc1cc6e2e",
                __utma="51854390.152042317.1504849434.1504849434.1504849434.1",
                __utmb="51854390.0.10.1504849434",
                __utmc="51854390",
                __utmz="51854390.1504849434.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
                __utmv="51854390.100 - 1 | 2 = registration_date = 20150809 = 1 ^ 3 = entry_date = 20150809 = 1",

               )
        self.r = requests.Session()

        self.headers = {
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                            'Host':'www.zhihu.com'

                        }


    # 登陆
    def login(self):
            i = 0;
            self.r.headers.clear()
            self.r.get('https://www.zhihu.com',cookies=self.cookies)

            root_url = 'https://www.zhihu.com/topic/19584431/hot'
            page_hot = self.r.get(root_url,headers=self.headers)
            pat = re.compile('data-score="(\d+.\d+)\"+?')
            first_offset = pat.findall(page_hot.text)[0]

            pdata = {
                'offset': first_offset,
                'start': '0',
            }
            html_json = {'msg': [0, 1]}
            pattern = re.compile('data-score="(\d+.\d+)\"+?')
            while (html_json['msg'][1]):
                time.sleep(1)
                print("加载下一个页面\n")
                resp = self.r.post(root_url, data=pdata, headers=self.headers)
                html_json = resp.json()
                # try:
                if pattern.findall(html_json['msg'][1]):
                    next_offset = pattern.findall(html_json['msg'][1])[-1]
                    pdata['offset'] = next_offset
                    html_doc = html_json['msg'][1]
                    soup = BeautifulSoup(html_doc, 'lxml')


                    for link in soup.find_all('a', 'question_link'):
                        print(link.get_text())
                        question_next_url = 'https://www.zhihu.com/api/v4/questions' + link['href'][9:] + '/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
                        #print(question_next_url)
                        xx = False
                        while (xx==False) :
                            #print('ssssssssssssss')
                            question_url_response = self.r.get(question_next_url, cookies=self.cookies)
                            question_json = question_url_response.json()
                            question_next_url = question_json['paging']['next']
                            xx = question_json['paging']['is_end']
                            for x in question_json['data']:
                                #print(x['author'])
                                #print(x['content'])
                                question_soup = BeautifulSoup(x['content'].encode('utf-8'), 'lxml')
                                for src_link in question_soup.find_all('img', 'origin_image zh-lightbox-thumb lazy'):

                                    try:
                                        pic = requests.get(src_link['data-actualsrc'])
                                    except requests.exceptions.ConnectionError:
                                        print('【错误】当前图片无法下载')
                                        continue
                                    string = '/Users/ql/Desktop/pic/' + str(i) + '.jpg'
                                    fp = open(string, 'wb')
                                    fp.write(pic.content)
                                    fp.close()
                                    i += 1


                            time.sleep(1)

                else:
                    print("最后一个了")
               # 隔
                time.sleep(1)





a = ZhiHu()
a.login()


