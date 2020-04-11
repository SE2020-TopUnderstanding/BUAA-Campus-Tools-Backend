from vpn import *

'''
this class is going to get messages from jiaowu.buaa.edu.cn
'''
class jiaoWuReq():
    def __init__(self, userName, password):
        VpnLogin(userName, password) # login


# for test
if __name__ == "__main__":
    jiaoWuReq('', '')
