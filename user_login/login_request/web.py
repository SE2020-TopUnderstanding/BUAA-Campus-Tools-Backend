import datetime
import requests
from bs4 import BeautifulSoup


URL = 'https://e2.buaa.edu.cn/users/sign_in'
LIST_URL = 'https://e2.buaa.edu.cn/'
JW_URL = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome'
COURSE_URL = 'https://course.e2.buaa.edu.cn/portal/login'


class WebGetId:

    def __init__(self, usr_name, pw):
        self.usr_name = usr_name
        self.password = pw
        self.now = requests.session()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        self.headers_vpn = {
            'Referer': 'https://e2.buaa.edu.cn/',
            'User-Agent': user_agent
        }
        self.headers_login = {
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
                page = self.now.get(url=URL, headers=self.headers_vpn, timeout=5)
                break
            except requests.exceptions.RequestException as err:
                print(err)
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
                page = self.now.post(url=URL, headers=self.headers_login, params=params, timeout=5)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return -4
        try:
            page.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
            return -5

        error_dict = {'此IP': -6, '验证码': -7, '超过五次': -8, '不能为空': -9, '已被锁定': -10}

        if page.status_code == 200:
            if page.url == LIST_URL:
                return 0
            if page.url.find('sign_in') != -1:
                warning_start = page.text.find('data-dismiss="alert">&times;</button>') + 37
                warning_end = page.text.find('</div>', warning_start)
                print(page.text[warning_start:warning_end])
                error_text = page.text[warning_start:warning_end]
                for key, value in error_dict.items():
                    if error_text.find(key) != -1:
                        return value
                return -1
            return -3
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
                web = self.now.get(url=JW_URL, headers=self.headers_vpn, timeout=5)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        web = self.secondary_login(web)
        if web == 0:
            return web

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
            except requests.exceptions.RequestException as err:
                print(err)
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

    def secondary_login(self, web):
        if web.url.find('login') != -1:
            print('进行二次登录')
            soup = BeautifulSoup(web.text, 'lxml')
            table = soup.select('div[class="clearfix login_btncont"] > input')  # 获取选项的值
            code = ''
            for each in table:
                if each.attrs['name'] == 'lt':
                    code = each.attrs['value']
            if code == '':
                return 0
            params = {
                'username': self.usr_name,
                'password': self.password,
                'code': '',
                'lt': code,
                'execution': 'e1s1',
                '_eventId': 'submit',
                'submit': '登录'
            }
            i = 0
            this_url = web.url.split('?')[0]
            web = ''
            while i < 3:
                try:
                    web = self.now.post(url=this_url, headers=self.headers_vpn, params=params, timeout=20)
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

        if web == '':
            return 0
        return web


if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    WebGetId(USR_NAME, PW).get_student_info()
