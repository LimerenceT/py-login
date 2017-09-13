import requests
import re
import time
from bs4 import BeautifulSoup
import queue
import threading
import os



class Thread_Crawl(threading.Thread):
    def __init__(self,queue,r,cookies):
        threading.Thread.__init__(self)
        self.pages_queue = queue
        self.r = r
        self.cookies = cookies

    def run(self):
        self.login()

    # 登陆
    def login(self):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                'Host': 'www.zhihu.com'

            }

            r.headers.clear()
            r.get('https://www.zhihu.com',cookies=cookies)

            root_url = 'https://www.zhihu.com/topic/19551671/hot'
            page_hot = r.get(root_url,headers=headers)
            pat = re.compile('data-score="(\d+.\d+)\"+?')
            first_offset = pat.findall(page_hot.text)[0]

            pdata = {
                'offset': first_offset,
                'start': '0',
            }
            html_json = {'msg': [0, 1]}
            pattern = re.compile('data-score="(\d+.\d+)\"+?')

            while (html_json['msg'][1]):
                time.sleep(3)
                resp = r.post(root_url, data=pdata, headers=headers)#请求下一页问题
                html_json = resp.json()

                if pattern.findall(html_json['msg'][1]):
                    next_offset = pattern.findall(html_json['msg'][1])[-1]
                    pdata['offset'] = next_offset
                    html_doc = html_json['msg'][1]
                    soup = BeautifulSoup(html_doc, 'lxml')


                    for link in soup.find_all('a', 'question_link'):#每个问题编号
                        self.pages_queue.put('next_question')
                        self.pages_queue.put(link.get_text())
                        #print(link.get_text())
                        #从第一页开始，请求下一页回答，一页20个回答
                        question_next_url = 'https://www.zhihu.com/api/v4/questions' + link['href'][9:] + '/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0'
                        pages_queue.put(question_next_url)
                else:
                    print("最后一个了")
               # 隔
                time.sleep(2)

class Thread_Parser(threading.Thread):
    def __init__(self,pagequeue,urlqueue,cookies,r):
        threading.Thread.__init__(self)
        self.pages_queue = pagequeue
        self.urls_queue = urlqueue
        self.cookies = cookies
        self.r = r
    def run(self):
        self.parser()
    def parser(self):
        while True:
                next_page = pages_queue.get()
                urls_queue.put(next_page)
                urls_queue.put(pages_queue.get())
                next_page = pages_queue.get()

                question_url_response = r.get(next_page, cookies=cookies)
                question_json = question_url_response.json()
                is_end = question_json['paging']['is_end']
                #is_end = False  # 判断是否是结束页
                while (is_end == False):
                    time.sleep(2)
                    for x in question_json['data']:
                        question_soup = BeautifulSoup(x['content'].encode('utf-8'), 'lxml')
                        for src_link in question_soup.find_all('img', 'origin_image zh-lightbox-thumb lazy'):
                            urls_queue.put(src_link['data-actualsrc'])
                    #pages_queue.put(question_json['paging']['next'])
                    print('请求下一页')
                    try:
                        question_url_response = r.get(question_json['paging']['next'], cookies=cookies)
                    except:
                        time.sleep(10)
                        question_url_response = r.get(question_json['paging']['next'], cookies=cookies)

                    question_json = question_url_response.json()
                    is_end = question_json['paging']['is_end']
                #urls_queue.task_done()
                print('一个问题结束了')

class Thread_Download(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.urls_queue = queue
    def run(self):
        self.download()
    def download(self):
        i = 0;
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',

        }
        while True:

            next = self.urls_queue.get()
            if next == 'next_question':
                dir = '/Users/ql/Desktop/pic/' + self.urls_queue.get()+'/'
                if os.path.exists(dir):
                    pass
                else:
                    os.mkdir(dir)

            else:
                string = dir + str(i) + '.jpg'
                if os.path.exists(string):
                    pass
                else:
                    pic = requests.get(next,headers=headers)

                    if pic.status_code ==200:
                        with open(string, 'wb') as fp:
                            fp.write(pic.content)
                    else:
                        print('【错误】当前图片无法下载')
                        print(next)
                        continue
                i += 1


if __name__ == '__main__':
    cookies = dict(
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
    r = requests.Session()
    urls_queue = queue.Queue()
    pages_queue = queue.Queue()
    t1 = Thread_Crawl(pages_queue,r,cookies)
    t2 = Thread_Parser(pages_queue,urls_queue,cookies,r)
    t3 = Thread_Download(urls_queue)
    Threads=[]
    Threads.append(t1)
    Threads.append(t2)
    Threads.append(t3)
    for T in Threads:
        T.start()
    for T in Threads:
        T.join()



