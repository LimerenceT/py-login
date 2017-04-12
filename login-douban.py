import requests
import urllib
import http.cookiejar

filename = 'douban-cookies'
r = requests.session()
r.cookies = http.cookiejar.LWPCookieJar(filename)
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'https://www.douban.com/accounts/login'  ##开始的URL地址
try:
    r.cookies.load(filename,ignore_discard=True)
except:
    print('weijiazai')

email = ''
password = ''
data = {
          "form_email": email,
          "form_password": password,
          "source": "None",
          "remember": "on"
}

result = r.post(all_url,data=data,headers = headers)
r.cookies.save(ignore_discard=True, ignore_expires=True)
pageurl = 'https://www.douban.com/people/141130012/'
page = r.get(pageurl,headers=headers)
print(page.text)
