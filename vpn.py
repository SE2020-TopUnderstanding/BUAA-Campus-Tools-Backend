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
        self.loginSuccess = self.login(userName, password) 

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

        locator = (By.XPATH, '/html/body/div[5]/div/ul')                                    # an item on https://e2.buaa.edu.cn/
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   # wait until the item appears
        except Exception:
            try:
                # check whether we get the error message on the login page or not
                error_text = self.browser.find_element_by_xpath('//*[@id="canvas"]/div[2]/div[2]/div[1]').text 
                print(error_text)                       # print the message if we get it
            except Exception:
                if self.browser.current_url == vpnUrl:  # if we are still on the login page
                    print('timeout')                    # the request should be timeout
                else:                                   # if we are on another page, maybe God knows what happened
                    print('some unknown errors happened')
            return -1
        return 0
            

    def switchToJiaoWu(self):
        if self.loginSuccess == -1:                     # if we failed to login the vpn pages
            return -1
        pushButton = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[5]/a') # find the jiaowu push button
        pushButton.click()                              # open the https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome link
        windows = self.browser.window_handles           # get all the windows
        if len(windows) == 1:                           # if there are only one window
            print('there is only one page')
            return -2
        self.browser.switch_to_window(windows[-1])      # switch to the latest window
        locator = (By.XPATH, '//*[@id="menu_6"]/span')  # an item on https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   # wait until the item appears
        except Exception:
            print('timeout or switch to an unknown page')
            return -3
        return 0                                        # return success

    def switchToCourse(self):
        if self.loginSuccess == -1:
            return -1
        pushButton = self.browser.find_element_by_xpath('/html/body/div[5]/div/ul/li[3]/a') # find the course push button
        pushButton.click()                              # open the https://course.e2.buaa.edu.cn/portal link
        windows = self.browser.window_handles           # get all the windows
        if len(windows) == 1:                           # if there are only one window
            print('there is only one page')
            return -2
        self.browser.switch_to_window(windows[-1])      # switch to the latest window
        locator = (By.XPATH, '//*[@id="toolMenu"]/ul/li[5]/a/span[2]')                      # an item on https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   # wait until the item appears
        except Exception:
            print('timeout or switch to an unknown page')
            return -3
        return 0                                        # return success

    def getBrowser(self):
        return self.browser

# for test 
if __name__ == "__main__": 
    userName = input('Your username: ') 
    password = input('Your password: ')
    VpnLogin(userName, password)
