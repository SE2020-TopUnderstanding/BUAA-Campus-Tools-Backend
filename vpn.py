from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By  

import time

vpnUrl = 'https://e2.buaa.edu.cn/users/sign_in'

'''
this class will create a browser and login the Buaa vpn page
ip address won't change, so it may be banned from the network
and I have not handled certain errors 
more efforts are needed
'''
class VpnLogin:

    def __init__(self, userName, password, userAgent = '', randomIpAddress = False):
        
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        opt = webdriver.ChromeOptions()                 # Chrome options
        #opt.add_argument('--headless')                 # hide the chrome, it's for the release version
        opt.add_argument('--disable-gpu')               # google says it can avoid some bugs
        opt.add_argument('--no-sandbox')                # avoid DevToolsActivePort Not Exist error
        opt.add_argument('--user-agent=%s' % userAgent) # user agent may be different in other computers
        self.browser = webdriver.Chrome(options=opt)    # start the chrome
        self.login(userName, password)

    def login(self, userName, password):
        self.browser.get(vpnUrl)                        # open the login page
        self.browser.maximize_window()                  # Used for debugging
        
        #find and fill the username and password text box and commit
        inputUserName = self.browser.find_element_by_xpath('//*[@id="user_login"]')         # find the username text box
        inputPassword = self.browser.find_element_by_xpath('//*[@id="user_password"]')      # find the password text box
        commit = self.browser.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')   # find the commit pushbutton
        inputUserName.send_keys(userName)               # fill the username text box
        inputPassword.send_keys(password)               # fill the password text box
        commit.click()                                  # push the login button


# for test 
if __name__ == "__main__": 
    userName = input('Your username: ') 
    password = input('Your password: ')
    VpnLogin(userName, password)
