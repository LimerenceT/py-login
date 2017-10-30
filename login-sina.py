import requests
import base64
import re
import urllib
import urllib.parse
import rsade
import json
import binascii
from bs4 import BeautifulSoup
import time
import urllib.request

unix_time = str(int(time.time()*1000))
headers = {'User-Agent': '*iaskspider/2.0(+http://iask.com/help/help_index.html”) *Mozilla/5.0 (compatible; iaskspider/1.0; MSIE 6.0)'}
pre_su = base64.b64encode('13038305792'.encode(encoding='utf-8'))
prelogin_url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su='+urllib.request.quote(pre_su.decode(encoding = 'utf-8'))+'&rsakt=mod&client=ssologin.js(v1.4.18)&_='+unix_time
post_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_='+unix_time
print(prelogin_url)
r = requests.session()
pre_page = r.get(prelogin_url,headers = headers)
print(pre_page.text)

post_data = {
            "entry":"weibo",
            "gateway":"1",
            "from":"",
            "savestate":"7",
            "useticket":"1",
            "pagerefer":"http%3A%2F%2Flogin.sina.com.cn%2Fsso%2Flogout.php%3Fentry%3Dminiblog%26r%3Dhttp%253A%252F%252Fweibo.com%252Flogout.php%253Fbackurl%253D%25252F",
            "vsnf":"1",
            "su":pre_su,
            "service":"miniblog",
            "servertime":unix_time,
            "nonce":'F7D34H',
            "pwencode":"rsa2",
            "rsakv":'1330428213',
            "sp":'',
            "sr":"1920*1080",
            "encoding":"UTF-8",
            "prelt":"109",
            "domain":"weibo.com",
            "cdult":"2",
            "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype":"TEXT"
        }
# r.post(url=post_url,headers=headers,data=post_data)
#respond = r.get(url='http://weibo.com/3529741811/profile?topnav=1&wvr=6&is_all=1',headers= headers)
res = requests.get('http://weibo.com',headers)
print(res.text)
