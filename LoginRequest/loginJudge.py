from vpn import *

'''
Input: username, password
return: 1 -> success
        0 -> failed, username or password is wrong
       -1 -> failed, request timeout
       -2 -> failed, unknown exception
'''
def loginJudge(username, password):
    try:
        for i in range(3):
            vpn = VpnLogin(username, password)
            success = vpn.getStatus()
            if success == -1:
                return 0
            elif success == 0:
                return 1
            elif success == -2:
                if i == 2:
                    return -1
            elif success == -3:
                return -2
    except Exception:
        return -2

if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    print(loginJudge(userName, password))