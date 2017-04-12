import requests
import http.cookiejar
import re
from PIL import Image
import time

filename = 'zhihu-cookies'
login_url = 'https://www.zhihu.com/#signin'
r = requests.session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}
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
    get_xsrf_pattern = re.compile(r'<input type="hidden" name="_xsrf" value="(.*?)"')
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
    data = {
        "_xsrf": get_xsrf(),
        "password": password,
        "phone_num": username,
    }
    try:
        r.post(login_url,data=data,headers=headers)
    except:
        data["captcha"] = get_captcha()
#cookies保存
    r.cookies.save(ignore_discard=True, ignore_expires=True)

if __name__ == '__main__':
    #username = input("输入账号：")
    #password = input("输入密码：")
    login(username='',password='')
    user_url = 'https://www.zhihu.com/people/asd-98-69/activities'
    # allow_redirects=False 禁止重定向
    resp = r.get(user_url, headers=headers,allow_redirects=False)
    print(resp.text)