import requests
from bs4 import BeautifulSoup
import datetime
import time

url = 'https://e2.buaa.edu.cn/users/sign_in'
list_url = 'https://e2.buaa.edu.cn/'
jiaowu_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome'
course_url = 'https://course.e2.buaa.edu.cn/portal/login'


class WebGetId():

    def __init__(self, userName, password):
        self.usr_name = userName
        self.password = password
        self.now = requests.session()
        self.headersVpn = {
            'Referer': 'https://e2.buaa.edu.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        self.headersLogin = {
            'Referer': 'https://e2.buaa.edu.cn/users/sign_in',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }

    def login(self):
        '''
        login request
        return 0 -> success
              -1 -> login error, unknown, please refer to the log
              -2 -> login request status code is 2XX, but not 200
              -3 -> jump to unknown page
              -4 -> request exception, timeout or network error
              -5 -> login request status code is 4XX or 5XX
              -6 -> IP is banned from the buaa
              -7 -> usr_name is wrong or there is a CAPTCHA
              -8 -> password is wrong
              -9 -> usr_name or password is empty
             -10 -> account is locked
        '''

        i = 0
        while i < 3:
            try:
                page = self.now.get(url=url, headers=self.headersVpn, timeout=5)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
                if i == 3:
                    return -4

        text = page.text
        codeStart = text.find('csrf-token') + 21
        codeEnd = text.find('" />', codeStart)
        code = text[codeStart:codeEnd]

        params = {
            'utf8': True,
            'authenticity_token': code,
            'user[login]': self.usr_name,
            'user[password]': self.password,
            'user[dymatice_code]': 'unknown',
            'commit': '登录 Login'
        }
        i = 0
        while i < 3:
            try:
                page = self.now.post(url=url, headers=self.headersLogin, params=params, timeout=5)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
                if i == 3:
                    return -4
        try:
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            return -5

        if page.status_code == 200:
            if page.url == list_url:
                return 0
            elif page.url.find('sign_in') != -1:
                warning_start = page.text.find('data-dismiss="alert">&times;</button>') + 37
                warning_end = page.text.find('</div>', warning_start)
                print(page.text[warning_start:warning_end])
                error_text = page.text[warning_start:warning_end]
                if error_text.find('此IP') != -1:
                    return -6
                if error_text.find('验证码') != -1:
                    return -7
                if error_text.find('超过五次') != -1:
                    return -8
                if error_text.find('不能为空') != -1:
                    return -9
                if error_text.find('已被锁定') != -1:
                    return -10
                return -1
            else:
                return -3
        else:
            return -2

    def getStudentInfo(self):
        '''
        get students' information
        return: [stu_id, usr_name, name, grade] -> success
                 0 -> request error when login the jiaowu web
                -1 -> login error, unknown, please refer to the log
                -2 -> login request status code is 2XX, but not 200
                -3 -> jump to unknown page
                -4 -> request exception, timeout or network error
                -5 -> login request status code is 4XX or 5XX
                -6 -> IP is banned from the buaa
                -7 -> usr_name is wrong or there is a CAPTCHA
                -8 -> password is wrong
                -9 -> usr_name or password is empty
               -10 -> account is locked
        password and major cannot be returned
        the grade may be wrong, cause it is calculated by the student's id
        '''
        success = self.login()
        if success < 0:
            return success

        i = 0
        while i < 3:
            try:
                web = self.now.get(url=jiaowu_url, headers=self.headersVpn, timeout=5)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
                if i == 3:
                    return 0

        name_start = web.text.find('<div class="welcome">您好！') + 24
        name_end = web.text.find('同学</div>', name_start)
        name = web.text[name_start:name_end]

        table_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryGrkb'
        headersJiaowu = {
            'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }

        i = 0
        while i < 3:
            try:
                schedule = self.now.get(url=table_url, headers=headersJiaowu)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
                if i == 3:
                    return 0

        soup = BeautifulSoup(schedule.text, 'lxml')
        table = soup.get_text()
        id_end = table.find(name) - 1
        id_start = table.find('(', id_end - 10) + 1
        stuId = table[id_start:id_end]

        year = int(datetime.datetime.now().year) - 2000
        month = int(datetime.datetime.now().month)
        inYear = int(stuId[0:2])
        offset = 0
        if month > 6:
            offset = 1
        grade = year - inYear + offset

        ans = []
        ans.append(stuId)
        ans.append(self.usr_name)
        ans.append(name)
        ans.append(grade)
        return ans


if __name__ == "__main__":
    userName = input('Your username: ')
    password = input('Your password: ')
    WebGetId(userName, password).getStudentInfo()
