from vpn import *


class courseReq():
    '''
    this class is going to get messages from course.buaa.edu.cn
    '''
    def __init__(self, userName, password):
        self.status = 0
        vpn = ''
        for i in range(3):
            vpn = VpnLogin(userName, password)  # login
            success = vpn.switchToCourse()      # switch
            # handle errors
            if success == -1:
                self.status = -1
                break
            elif success == -2 or success == -5:
                if i == 2:
                    self.status = -2
                    break
                else:
                    vpn.getBrowser().quit()
            elif success == -3 or success == -4:
                self.status = -3
                break
            elif success == -6:
                self.status = -5
                break
            elif success == 0:
                break
        if vpn == '':
            raise Exception('vpn not exists')
        self.browser = vpn.getBrowser()         # get the browser.
        #self.getDdl()                           # for debug

    def getStatus(self):
        '''
        init step's result
        status = 0 : success
        status = -1 : error occur on the network, usually due to username and password
        status = -2 : timeout for 3 times
        status = -3 : unknown error
        status = -5 : IP is banned
        '''
        return self.status

    def getDdl(self):
        '''
        this func will return ddls from the course.buaa.edu.cn
        a list will be returned
        data type:
        {
            curLesson : [[title, status, opendate, duedate], [title, status, opendate, duedate], ...]
            curLesson : [[title, status, opendate, duedate], [title, status, opendate, duedate], ...]
            ...
        }
        '''
        if self.status != 0:
            return self.status
        try:
            curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
        except Exception:
            print('timeout or this guy redefined the network')
            time.sleep(5)
            try:
                curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
            except Exception:
                print('this guy redefined the network')
                return -6
        lessons = curLessons.find_elements_by_xpath('li')                                       # get all the lessons
        ddls = {}
        for i in range(len(lessons)):
            link = lessons[i].find_elements_by_xpath('a')[0]
            #print(link.get_attribute('href'))
            curLesson = link.get_attribute('title')                                             # get lesson's name
            #print(curLesson)
            link = link.get_attribute('href')
            
            self.browser.get(link)                                                              # switch to the lesson
            workButtons = self.browser.find_element_by_xpath('//*[@id="toolMenu"]/ul')
            workButtons = workButtons.find_elements_by_tag_name('a')
            workButton = 0
            for each in workButtons:
                if each.get_attribute('title') == '在线发布、提交和批改作业':
                    workButton = each
                    break
            if workButton == 0:
                self.browser.switch_to.default_content()                                            # reget the lessons
                curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
                lessons = curLessons.find_elements_by_xpath('li')
                continue

            workButton.click()
            frame = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div/div/div[2]/iframe')
            self.browser.switch_to.frame(frame)                                                 # switch to another frame to get datas  
            locator = (By.XPATH, '/html/body/div')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            try: 
                self.browser.find_element_by_xpath('/html/body/div/form/table')                 # judge if there are some jobs
            except Exception:
                try:
                    self.browser.find_element_by_xpath('/html/body/div/p')
                    #print('no homework founded\n')
                    ddls[curLesson] = []

                    self.browser.switch_to.default_content()
                    curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
                    lessons = curLessons.find_elements_by_xpath('li')                           # do not have any jobs

                    continue
                except:
                    print('timeout or switch to an unknown page')
                    return -4
            table = self.browser.find_element_by_xpath('/html/body/div/form/table')
            tableRows = table.find_elements_by_tag_name('tr')[1:]
            jobs = []
            for row in tableRows:                                                               # get the information of the job
                datas = row.find_elements_by_tag_name('td')[1:]
                work = []
                if len(datas) >= 1:
                    title = datas[0].find_elements_by_tag_name('a')[0]
                    title = title.text
                    #print(title)
                    work.append(title)
                if len(datas) >= 2:
                    status = datas[1].text
                    #print(status)
                    work.append(status)
                if len(datas) >= 3:
                    opendate = datas[2].text
                    #print(opendate)
                    work.append(opendate)
                if len(datas) >= 4:
                    duedate = datas[3].find_elements_by_tag_name('span')
                    if len(duedate) == 0:
                        duedate = ''
                    else:
                        duedate = duedate[0].text
                    #print(duedate)
                    work.append(duedate)
                while len(work) < 4:
                    work.append('')
                #print()
                jobs.append(work)
            ddls[curLesson] = jobs

            self.browser.switch_to.default_content()                                            # reget the lessons
            curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
            lessons = curLessons.find_elements_by_xpath('li')
        return ddls  

    def quit(self):
        self.browser.quit()         


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    courseReq(userName, password)