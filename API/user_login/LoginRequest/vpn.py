from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select 
import sys

import datetime
import time

vpnUrl = 'https://e2.buaa.edu.cn/users/sign_in'


class VpnLogin:
    '''
    this class will create a browser and login the Buaa vpn page
    ip address won't change, so it may be banned from the network
    more efforts are needed
    '''
    def __init__(self, userName, password, userAgent = '', randomIpAddress = False):
        
        

        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        opt = webdriver.ChromeOptions()                 
        opt.add_argument('--headless')                  # hide the chrome, it's for the release version
        opt.add_argument('--disable-gpu')               
        opt.add_argument('--no-sandbox')                
        opt.add_argument('--user-agent=%s' % userAgent) 
        opt.add_argument('--lang=zh-cn')
        self.browser = webdriver.Chrome(options=opt)    
        self.loginSuccess = self.login(userName, password) 
        self.usr = userName
        self.pw = password

    def login(self, userName, password):
        '''
        login request
        return 0 -> success
        return -1 -> login in error, pw or usrname
        return -2 -> timeout or netword load error
        return -3 -> unknown error
        return -6 -> IP is banned from the buaa
        return -7 -> usr_name is wrong or there is a CAPTCHA
        return -8 -> password is wrong
        return -9 -> usr_name or password is empty
        return -10 -> account is locked
        '''

        self.browser.get(vpnUrl)                        
        #self.browser.maximize_window()                  # Used for debugging
        
        #find and fill the username and password text box and commit
        try:
            inputUserName = self.browser.find_element_by_xpath('//*[@id="user_login"]')         
            inputPassword = self.browser.find_element_by_xpath('//*[@id="user_password"]')      
            commit = self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')   
            inputUserName.send_keys(userName)               
            inputPassword.send_keys(password)               
            commit.click()                                  
        except Exception:
            print('network load exception')
            return -2

        locator = (By.XPATH, '/html/body/div[5]/div/ul')                                    
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
        except Exception:
            try:
                # check whether we get the error message on the login page or not
                '''
                possible reply
                用户名或密码错误, 超过五次将被锁定。
                用户名,密码或验证码错误。
                此IP登录尝试次数过多，请10分钟后再试
                用户名密码不能为空
                您的帐号已被锁定, 请在十分钟后再尝试
                '''
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
                if self.browser.current_url == vpnUrl:  # if we are still on the login page
                    print('timeout')                    # the request should be timeout
                    return -2
                else:                                   # if we are on another page, maybe God knows what happened
                    print('some unknown errors happened')
                return -3
        return 0
            

    def switchToJiaoWu(self):
        if self.loginSuccess != 0:                     
            return self.loginSuccess
        pushButton = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[5]/a') 
        pushButton.click()                              
        windows = self.browser.window_handles           # get all the windows
        if len(windows) == 1:                           # if there are only one window
            print('there is only one page')
            return -4
        self.browser.switch_to_window(windows[-1])      # switch to the latest window
        locator = (By.XPATH, '//*[@id="menu_6"]/span')  
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
        except Exception:
            try:
                input_id = self.browser.find_element_by_xpath('//*[@id="username"]')
                input_pw = self.browser.find_element_by_xpath('//*[@id="password"]')
                commit = self.browser.find_element_by_xpath('//*[@id="fm1"]/div[3]/input[4]')
                input_id.send_keys(self.usr)               
                input_pw.send_keys(self.pw)               
                commit.click()
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -5
            except Exception:
                print('timeout or switch to an unknown page')
                return -5
        return 0                                        

    def switchToCourse(self):
        if self.loginSuccess != 0:
            return self.loginSuccess
        pushButton = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[3]/a') 
        pushButton.click()                              
        windows = self.browser.window_handles           # get all the windows
        if len(windows) == 1:                           # if there are only one window
            print('there is only one page')
            return -4
        self.browser.switch_to_window(windows[-1])      # switch to the latest window
        locator = (By.XPATH, '//*[@id="toolMenu"]/ul/li[5]/a/span[2]')                      
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
        except Exception:
            try:
                input_id = self.browser.find_element_by_xpath('//*[@id="username"]')
                input_pw = self.browser.find_element_by_xpath('//*[@id="password"]')
                commit = self.browser.find_element_by_xpath('//*[@id="fm1"]/div[3]/input[4]')
                input_id.send_keys(self.usr)               
                input_pw.send_keys(self.pw)               
                commit.click()
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -5
            except Exception:
                print('timeout or switch to an unknown page')
                return -5
        return 0                                        

    def getBrowser(self):
        return self.browser

    def getStatus(self):
        return self.loginSuccess

# for test 
if __name__ == "__main__": 
    userName = input('Your username: ') 
    password = input('Your password: ')
    VpnLogin(userName, password)
