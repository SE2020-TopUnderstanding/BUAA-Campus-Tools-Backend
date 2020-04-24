from .vpn import *
from .Password import *
def loginJudge(username, password):
    '''
    Input: username, password
    return: 1 -> success
            0 -> failed, username or password is wrong
           -1 -> failed, request timeout
           -2 -> failed, unknown exception
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
    except Exception:
        if vpn == '':
            return -2
        vpn.getBrowser().quit()
        return -2

def getStudentInfo(username, password):
    '''
    Input: username, password
    return: [stu_id, usr_name, name, grade] -> success
            0 -> failed, username or password is wrong
           -1 -> failed, request timeout
           -2 -> failed, unknown exception
           -4 -> failed, others
    password and major cannot be returned
    '''
    password = decrypt_string(password)
    vpn = ''
    try:
        for i in range(3):
            vpn = VpnLogin(username, password)
            success = vpn.getStatus()
            if success == -1:
                vpn.getBrowser().quit()
                return 0
            elif success == 0:
                break
            elif success == -2:
                if i == 2:
                    vpn.getBrowser().quit()
                    return -1
                else:
                    vpn.getBrowser().quit()
            elif success == -3:
                vpn.getBrowser().quit()
                return -2
        success = vpn.switchToJiaoWu()              # switch
        browser = vpn.getBrowser()
        name = browser.find_element_by_xpath('//*[@id="north"]/div/div/div[2]')
        name = name.text.split('！')[1][0:-2]       # get student's name
        # use lesson inquire page to get student id
        # this label cannot click, so we use js to click the label
        scheduleLabel = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/a[6]')
        browser.execute_script("arguments[0].click();", scheduleLabel)                                                                           
        browser.switch_to.frame('iframename')                                                  
        locator = (By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/table')
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located(locator))           
        except Exception:
            print('timeout or switch to an unknown page')
            vpn.getBrowser().quit()
            return -4

        idPlace = browser.find_element_by_xpath('/html/body/div[1]/div/div[8]/div[1]/span')
        studentId = idPlace.text
        studentId = studentId.split('(')[1]
        studentId = studentId.split(')')[0]
        stu_id = studentId
        usr_name = username

        #usr_password = ''                          # to avoid datas get stolen 
        #major = ''                                 # it is difficult to get

        # get user's grade by the student id
        year = int(datetime.datetime.now().year) - 2000
        month = int(datetime.datetime.now().month)
        inYear = int(stu_id[0:2])
        offset = 0
        if month > 6:
            offset = 1

        grade = year - inYear + offset
        #print(stu_id)                              # for debug
        #print(usr_name)
        #print(name)
        #print(grade)
        ans = []
        ans.append(stu_id)
        ans.append(usr_name)
        ans.append(name)
        ans.append(grade)
        print(ans)
        vpn.getBrowser().quit()
        return ans
    except Exception:
        if vpn == '':
            return -2
        vpn.getBrowser().quit()
        return -2


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    print(loginJudge(userName, password))
    getStudentInfo(userName, password)
    