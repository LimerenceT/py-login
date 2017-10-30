import requests
login_url = 'http://aqjy.swu.edu.cn/j_spring_security_check'
test_url = 'http://aqjy.swu.edu.cn/exam/studentexame/studentExameAction!gotoExame.do'
answer_url = 'http://aqjy.swu.edu.cn/exam/studentexame/studentExameAction!saveAnswerAndGetNextExameTheme.do'
headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',

            }
login_data = {
    'j_password':'',
    'j_username':''
}
test_data = {
    'exameid':'712540'
}
#answr_list = ['A','C','A','B','C','C','A','A','C','S','']
swu = requests.session()
swu.post(login_url,headers=headers,data=login_data)
res = swu.post(test_url,headers=headers,data=test_data).text
print(res)

