from vpn import *

'''
this class is going to get messages from course.buaa.edu.cn
'''
class courseReq():
    def __init__(self, userName, password):
        vpn = VpnLogin(userName, password)  # login
        success = vpn.switchToJiaoWu()      # switch
        #TODO: handle errors
        self.browser = vpn.getBrowser()     # get a browser. it's current page is https://course.e2.buaa.edu.cn/portal 


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    courseReq(userName, password)