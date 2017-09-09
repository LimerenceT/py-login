import requests
import http.cookiejar
import re
from PIL import Image
import time
from bs4 import BeautifulSoup

filename = 'zhihu-cookies'
login_url = 'https://www.zhihu.com/login/phone_num'
r = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
r.cookies = http.cookiejar.LWPCookieJar(filename=filename)

try:
    r.cookies.load(filename=filename, ignore_discard=True)
except:
    print('Cookie未加载！')
#获取——xsrf参数
def get_xsrf():
    index_url = 'http://www.zhihu.com'
    rep = r.get(index_url,headers = headers)

    html = rep.text
    get_xsrf_pattern = re.compile(r'name="_xsrf" value="(.*?)"')
    _xsrf = re.findall(get_xsrf_pattern,html)[0]
    return _xsrf
#获取验证码
def get_captcha():
    cap_url = 'https://www.zhihu.com/captcha.gif?r='+str(int(time.time()*1000))+'&type=login'
    r.request.urlretrieve(cap_url, 'cptcha.gif')
    im = Image.open('cptcha.gif')
    im.show()
    captcha = input('输入验证码：')
    return captcha

#登陆
def login(username,password):
    print(get_xsrf())
    data = {
        "_xsrf": get_xsrf(),
        "captcha_type":"cn",
        "password": password,
        "phone_num": username,
    }
    try:
        ss = r.post(login_url,data=data,headers=headers)
        print(ss.json())
    except:
        data["captcha"] = get_captcha()
#cookies保存
    # r.cookies.save(ignore_discard=True, ignore_expires=True)
    # rr = 'https://www.zhihu.com/api/v4/questions/62587148/answers?sort_by=default&include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata[*].mark_infos[*].url%3Bdata[*].author.follower_count%2Cbadge[%3F(type%3Dbest_answerer)].topics&limit=20&offset=0'
    # x = r.get(rr,headers=headers)
    # print(x)

if __name__ == '__main__':
    #username = input("输入账号：")
    #password = input("输入密码：")
    login(username='13038305792',password='q936611560q')
    ss = r.get('https://www.zhihu.com/topic',headers=headers)
    print(ss.text)
    # user_url = 'https://www.zhihu.com/people/asd-98-69/activities'
    # # allow_redirects=False 禁止重定向
    # resp = r.get(user_url, headers=headers,allow_redirects=False)
    # print(resp.text)
