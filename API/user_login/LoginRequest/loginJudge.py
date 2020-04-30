from .vpn import *
from .web import *
from .Password import *

def loginJudge(username, password):
    '''
    Input: username, password
    return: 1 -> success
            0 -> failed, an unexcepted error on the login page
           -1 -> failed, request timeout
           -2 -> failed, unknown exception
           -3 -> IP is banned from the buaa
           -4 -> usr_name is wrong or there is a CAPTCHA
           -5 -> password is wrong
           -6 -> usr_name or password is empty
           -7 -> account is locked
    '''
    vpn = ''
    try:
        for i in range(3):
            vpn = VpnLogin(username, password)
            success = vpn.getStatus()
            if success == -1:
                vpn.getBrowser().quit()
                return 0
            elif success == 0:
                vpn.getBrowser().quit()
                return 1
            elif success == -2:
                if i == 2:
                    vpn.getBrowser().quit()
                    return -1
                else:
                    vpn.getBrowser().quit()
            elif success == -3:
                vpn.getBrowser().quit()
                return -2
            elif success <= -6:
                vpn.getBrowser().quit()
                return success + 3
    except Exception:
        if vpn == '':
            return -2
        vpn.getBrowser().quit()
        return -2

def getStudentInfo(username, password):
    '''
        get students' information
        Input: username, password
        return: [stu_id, usr_name, name, grade] -> success
                 0 -> request error when login the jiaowu web
                -1 -> login error, unknown, please refer to the log
                -2 -> login request status code is 2XX, but not 200
                -3 -> jump to unknown page
                -4 -> request exception, timeout or network error
                -5 -> login request status code is 4XX or 5XX
                -6 -> IP is banned from the buaa
                -7 -> usr_name is wrong or there is a CAPTCHA
                -8 -> password is wrong
                -9 -> usr_name or password is empty
               -10 -> account is locked
        password and major cannot be returned
        the grade may be wrong, cause it is calculated by the student's id
    '''
    pr = aescrypt(key,model,iv,encode_)
    password = pr.aesdecrypt(password)
    return WebGetId(username, password).getStudentInfo()


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    print(getStudentInfo(userName, password))
    