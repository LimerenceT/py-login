import requests
from bs4 import BeautifulSoup
import os
import time
from multiprocessing import Process, Queue


COOKiES = dict(
    d_c0="ACACjETgnQuPTp4jSXJidx_Z5R1ohS4w_dY=|1492353443",
    _zap="3f1d95db-5eee-4356-bed0-8ba5925fd39c",
    q_c1="080deed681264a71bbd850b772645dde|1507733437000|1492353441000",
    __utma="51854390.1535220193.1504863675.1508812203.1508831766.5",
    __utmz="51854390.1508831766.5.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/26921730",
    __utmv="51854390.100-1|2=registration_date=20150809=1^3=entry_date=20150809=1",
    l_cap_id="YjI5M2UyMDExNjEzNDRkNDlkM2Q2MjE0YjJkNDE1YWE=|1514548791|c59609bfa761cee9cb91285d197b37db9c61a69a",
    r_cap_id="MWYxMTFlZWY3NjQ3NDdkOWIyNDUxMWJlY2M2M2EyMDQ=|1514548791|6eaaf80fb56c1126d598584a2bb4fd17dc5b7491",
    cap_id="ZWRjMWY3NWIyZGNiNGZjYTlmN2QxMjY0NTIxNTdjNGM=|1514548791|c0501105d3f8c13b0a3a1fa8f282168c06ffd0de",
    capsion_ticket="2|1:0|10:1514548792|14:capsion_ticket|44:MjE5NTliYzFmZGU1NGMyODhkNTMzMGNmYTNlZWIxNjU=|abc9f5f3fe71eb98fd436d403eb68f688e1aaa28e825a12b9e770a4380ee4037",
    z_c0="2|1:0|10:1514548794|4:z_c0|92:Mi4xaThuMUFRQUFBQUFBSUFLTVJPQ2RDeVlBQUFCZ0FsVk5Pbnd6V3dEV29objdMbml2MHJWd25zMWtPV21uUU9Qem5n|26f1bd2496451d521b74eaa34010340bbbb538dd59876ef99cdf58f458b14f28",
    aliyungf_tc="AQAAAOUmAQ0K8QwAGGYKb1WGcaHwD5AB",
    _xsrf="098a76e3-fbe4-4c9f-9bba-9a9184dc4f34",
)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}


def crawl_question_url(topic_url):
    questions = {}
    response_json = requests.get(topic_url, headers=HEADERS).json()
    for question in response_json['messages']:
        question_dir = '/Users/ql/Desktop/ss/' + question['content'] + '/'
        if os.path.exists(question_dir):
            continue
        questions[question['content']] = question['linkUrl'][31:39]
        print(question['linkUrl'])
    return questions


def crawl_pic_url(questions):
    if questions == {}:
        print('没有更新')
        return
    for question_title, question_num in questions.items():
        q = Process(target=zhihu, args=(question_num, question_title))
        q.start()


def zhihu(question_num, question_title):
    offset = 0
    while True:
        url_queue = Queue()
        api = 'https://www.zhihu.com/api/v4/questions/' + question_num + \
              ('/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,'
               'annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,'
               'can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,'
               'created_time,updated_time,review_info,'
               'relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,'
               'upvoted_followees;data[*].mark_infos[*].url;data[*].author.'
               'follower_count,badge[?(type=best_answerer)].topics&limit=20&offset='
               ) + str(offset) + '&sort_by=default'
        time.sleep(1)
        if requests.get(api, headers=HEADERS).status_code == 404:
            break
        response_json = requests.get(api, cookies=COOKiES, headers=HEADERS).json()

        for answer in response_json['data']:
            question_soup = BeautifulSoup(answer['content'].encode('utf-8'), 'lxml')
            for src_link in question_soup.find_all('img', 'origin_image zh-lightbox-thumb lazy'):
                url_queue.put(src_link['data-actualsrc'])
                print(src_link['data-actualsrc'])
        url_queue.put('over')

        q = Process(target=download_pic, args=(url_queue, question_title))
        q.start()
        if response_json['paging']['is_end']:
            break
        offset += 20


def download_pic(url_queue, question_title):
    question_dir = '/Users/ql/Desktop/ss/' + question_title + '/'
    if os.path.exists(question_dir):
        pass
    else:
        os.mkdir(question_dir)

    while True:
        pic_url = url_queue.get()
        if pic_url == 'over':
            print('完成下载' + question_title)
            break

        pic_name = question_dir + pic_url[-20:-4] + '.jpg'
        if os.path.exists(pic_name):
            pass
        else:
            pic = requests.get(pic_url, headers=HEADERS)

            if pic.status_code == 200:
                with open(pic_name, 'wb') as fp:
                    fp.write(pic.content)
            else:
                print('【错误】当前图片无法下载')
                continue


if __name__ == '__main__':
    topic_url = 'https://app.jike.ruguoapp.com/1.0/messages/showDetail?topicId=57281cf75f0ba71200ffde92'
    questions = crawl_question_url(topic_url)
    p = Process(target=crawl_pic_url, args=(questions,))
    p.start()
    p.join()
