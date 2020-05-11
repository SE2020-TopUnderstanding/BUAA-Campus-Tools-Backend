from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

VPN_URL = 'https://e2.buaa.edu.cn/users/sign_in'


class VpnLogin:
    """
    这个类将创建一个浏览器并登录BUAA vpn页面
    IP地址不会改变，因此可能会被封IP
    """
    def __init__(self, usr_name, pw):

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                    ' Chrome/80.0.3987.163 Safari/537.36'
        opt = webdriver.ChromeOptions()
        opt.add_argument('--headless')                 # 隐藏浏览器，release版本使用
        opt.add_argument('--disable-gpu')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--user-agent=%s' % user_agent)
        opt.add_argument('--lang=zh-cn')
        self.browser = webdriver.Chrome(options=opt)
        self.login_success = self.login(usr_name, pw)
        self.usr = usr_name
        self.passw = pw

    def login(self, usr_name, passw):
        """
        登录请求
        返回 0   -> 成功
        返回 -1  -> 登陆错误
        返回 -2  -> 超时或网络错误
        返回 -3  -> 未知错误
        返回 -6  -> IP被封
        返回 -7  -> 用户名错误或者网站要求输入验证码
        返回 -8  -> 密码错误
        返回 -9  -> 用户名或密码为空
        返回 -10 -> 账号被锁
        """
        self.browser.get(VPN_URL)
        # self.browser.maximize_window()                  # 用于debug

        # 找到并填充用户名和密码框，提交登录请求
        # noinspection PyBroadException
        try:
            input_user_name = self.browser.find_element_by_xpath('//*[@id="user_login"]')
            input_password = self.browser.find_element_by_xpath('//*[@id="user_password"]')
            commit = self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')
            input_user_name.send_keys(usr_name)
            input_password.send_keys(passw)
            commit.click()
        except Exception:
            print('network load exception')
            return -2

        locator = (By.XPATH, '/html/body/div[5]/div/ul')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            # noinspection PyBroadException
            try:
                # 检查是否出现错误信息

                # 可能的信息如下
                # 用户名或密码错误, 超过五次将被锁定。
                # 用户名,密码或验证码错误。
                # 此IP登录尝试次数过多，请10分钟后再试
                # 用户名密码不能为空
                # 您的帐号已被锁定, 请在十分钟后再尝试

                error_text = self.browser.find_element_by_xpath('//*[@id="canvas"]/div[2]/div[2]/div[1]').text
                print(error_text)
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
            except Exception:
                if self.browser.current_url == VPN_URL:  # 如果我们仍在登陆页面上
                    print('timeout')                     # 请求应该是超时了
                    return -2
                print('some unknown errors happened')    # 如果我们不在登陆界面上，鬼知道出了什么错
                return -3
        return 0

    def switch_to_jiao_wu(self):
        if self.login_success != 0:
            return self.login_success
        push_button = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[5]/a')
        push_button.click()
        windows = self.browser.window_handles           # 得到所有页面
        if len(windows) == 1:                           # 如果只有一个页面
            print('there is only one page')
            return -4
        self.browser.switch_to.window(windows[-1])      # 切换到最后一个页面
        locator = (By.XPATH, '//*[@id="menu_6"]/span')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            # noinspection PyBroadException
            try:
                input_id = self.browser.find_element_by_xpath('//*[@id="username"]')
                input_pw = self.browser.find_element_by_xpath('//*[@id="password"]')
                commit = self.browser.find_element_by_xpath('//*[@id="fm1"]/div[3]/input[4]')
                input_id.send_keys(self.usr)
                input_pw.send_keys(self.passw)
                commit.click()
                # noinspection PyBroadException
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -5
            except Exception:
                print('timeout or switch to an unknown page')
                return -5
        return 0

    def switch_to_course(self):
        if self.login_success != 0:
            return self.login_success
        push_button = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[3]/a')
        push_button.click()
        windows = self.browser.window_handles           # 得到所有页面
        if len(windows) == 1:                           # 如果只有一个页面
            print('there is only one page')
            return -4
        self.browser.switch_to.window(windows[-1])      # 切换到最后一个页面
        locator = (By.XPATH, '//*[@id="toolMenu"]/ul/li[5]/a/span[2]')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            # noinspection PyBroadException
            try:
                input_id = self.browser.find_element_by_xpath('//*[@id="username"]')
                input_pw = self.browser.find_element_by_xpath('//*[@id="password"]')
                commit = self.browser.find_element_by_xpath('//*[@id="fm1"]/div[3]/input[4]')
                input_id.send_keys(self.usr)
                input_pw.send_keys(self.passw)
                commit.click()
                # noinspection PyBroadException
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -5
            except Exception:
                print('timeout or switch to an unknown page')
                return -5
        return 0

    def get_browser(self):
        return self.browser


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    VpnLogin(USR_NAME, PW)
