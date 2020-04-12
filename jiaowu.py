from vpn import *

'''
this class is going to get messages from jiaowu.buaa.edu.cn
'''
class jiaoWuReq():
    def __init__(self, userName, password):
        vpn = VpnLogin(userName, password)  # login
        success = vpn.switchToJiaoWu()      # switch
        #TODO: handle errors
        self.browser = vpn.getBrowser()     # get a browser. it's current page is https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    jiaoWuReq(userName, password)
