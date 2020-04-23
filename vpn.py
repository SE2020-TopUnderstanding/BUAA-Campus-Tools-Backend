from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select 

import time
import json
from datetime import datetime, date, timedelta

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
        opt.add_argument('--headless')                 # hide the chrome, it's for the release version
        opt.add_argument('--disable-gpu')               
        opt.add_argument('--no-sandbox')                
        opt.add_argument('--user-agent=%s' % userAgent) 
        opt.add_argument('--lang=zh-cn')
        self.browser = webdriver.Chrome(options=opt)    
        self.loginSuccess = self.login(userName, password) 
        self.usr = userName
        self.pw = password

    def login(self, userName, password):
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
                error_text = self.browser.find_element_by_xpath('//*[@id="canvas"]/div[2]/div[2]/div[1]').text 
                print(error_text)                       
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

# for test 
if __name__ == "__main__": 
    userName = input('Your username: ') 
    password = input('Your password: ')
    VpnLogin(userName, password)
