import requests


URL = 'https://e2.buaa.edu.cn/users/sign_in'
LIST_URL = 'https://e2.buaa.edu.cn/'
JW_URL = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome'
COURSE_URL = 'https://course.e2.buaa.edu.cn/portal/login'


class WebLogin:

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

    def get_session(self):
        return self.now

    def get_usr_name_and_pw(self):
        return self.usr_name, self.password

    def switch_to_jiaowu(self):
        """
            登录请求
            返回：  1 -> 成功
                   0 -> 登录教务网站出现错误
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
        status = self.login()
        if status != 0:
            return status
        i = 0
        web = ''
        while i < 3:
            try:
                web = self.now.get(url=JW_URL, headers=self.headers_vpn, timeout=5)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0
        # print(web.text)
        aim_web = 'https://jwxt-7001.e2.buaa.edu.cn:443/ieas2.1/welcome'
        if web != '' and web.status_code == 200 and web.url.split(';')[0] == aim_web:
            return 1
        return 0

    def switch_to_course(self):
        """
            登录请求
            返回：  1 -> 成功
                   0 -> 登录课程中心网站出现错误
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
        status = self.login()
        if status != 0:
            return status
        i = 0
        web = ''
        while i < 3:
            try:
                web = self.now.get(url=COURSE_URL, headers=self.headers_vpn, timeout=5)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0
        # print(web.text)
        aim_web = 'https://course.e2.buaa.edu.cn/portal'
        if web != '' and web.status_code == 200 and web.url == aim_web:
            return 1
        return 0


if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    WebLogin(USR_NAME, PW).switch_to_jiaowu()
