import requests
from bs4 import BeautifulSoup
import datetime

url = 'https://e2.buaa.edu.cn/users/sign_in'
list_url = 'https://e2.buaa.edu.cn/'
jw_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome'
course_url = 'https://course.e2.buaa.edu.cn/portal/login'


class WebGetId:

    def __init__(self, user_name, pw):
        self.usr_name = user_name
        self.password = pw
        self.now = requests.session()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        self.headersVpn = {
            'Referer': 'https://e2.buaa.edu.cn/',
            'User-Agent': user_agent
        }
        self.headersLogin = {
            'Referer': 'https://e2.buaa.edu.cn/users/sign_in',
            'User-Agent': user_agent
        }

    def login(self):
        """
        登录请求
        返回：  0 -> 成功
              -1 -> 不可预知的错误，请参考log信息
              -2 -> 登录状态码是2XX，但不是200
              -3 -> 跳转到未知网页
              -4 -> 请求错误，超时或网络错误
              -5 -> 登陆状态码是4XX或5XX
              -6 -> IP被北航屏蔽
              -7 -> 用户名错误，或者出现验证码
              -8 -> 密码错误
              -9 -> 用户名或密码为空
             -10 -> 账户被锁定了
        """
        page = ''
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
        code_start = text.find('csrf-token') + 21
        code_end = text.find('" />', code_start)
        code = text[code_start:code_end]

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

    def get_student_info(self):
        """
        获取学生基本信息
        返回:     [stu_id, usr_name, name, grade] -> 成功
                 0 -> 登录教务时请求错误
                -1 -> 不可预知的错误，请参考log信息
                -2 -> 登录状态码是2XX，但不是200
                -3 -> 跳转到未知网页
                -4 -> 请求错误，超时或网络错误
                -5 -> 登陆状态码是4XX或5XX
                -6 -> IP被北航屏蔽
                -7 -> 用户名错误，或者出现验证码
                -8 -> 密码错误
                -9 -> 用户名或密码为空
               -10 -> 账户被锁定了
        密码和专业暂时不能返回
        年级的计算可能出现问题，因为年级是根据学号计算的，请一定注意
        """
        success = self.login()
        if success < 0:
            return success

        web = ''
        i = 0
        while i < 3:
            try:
                web = self.now.get(url=jw_url, headers=self.headersVpn, timeout=5)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
                if i == 3:
                    return 0

        name_start = web.text.find('<div class="welcome">您好！') + 24
        name_end = web.text.find('同学</div>', name_start)
        name = web.text[name_start:name_end]
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        table_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryGrkb'
        headers_jw = {
            'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome',
            'User-Agent': user_agent
        }

        schedule = ''
        i = 0
        while i < 3:
            try:
                schedule = self.now.get(url=table_url, headers=headers_jw)
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
        stu_id = table[id_start:id_end]

        year = int(datetime.datetime.now().year) - 2000
        month = int(datetime.datetime.now().month)
        in_year = int(stu_id[0:2])
        offset = 0
        if month > 6:
            offset = 1
        grade = year - in_year + offset

        ans = [stu_id, self.usr_name, name, grade]
        return ans


if __name__ == "__main__":
    userName = input('Your username: ')
    password = input('Your password: ')
    WebGetId(userName, password).get_student_info()
