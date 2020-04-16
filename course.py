from vpn import *

'''
this class is going to get messages from course.buaa.edu.cn
'''
class courseReq():
    def __init__(self, userName, password):
        vpn = VpnLogin(userName, password)  # login
        success = vpn.switchToCourse()      # switch
        #TODO: handle errors
        self.browser = vpn.getBrowser() 
        self.getDdl()

    def getDdl(self):
        curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
        lessons = curLessons.find_elements_by_xpath('li')
        ddls = {}
        for i in range(len(lessons)):
            link = lessons[i].find_elements_by_xpath('a')[0]
            print(link.get_attribute('href'))
            curLesson = link.get_attribute('title')
            print(curLesson)
            link = link.get_attribute('href')
            
            self.browser.get(link)
            workButton = self.browser.find_element_by_xpath('//*[@id="toolMenu"]/ul/li[6]/a')
            workButton.click()
            frame = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div/div/div[2]/iframe')
            self.browser.switch_to.frame(frame)     
            locator = (By.XPATH, '/html/body/div')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            try: 
                self.browser.find_element_by_xpath('/html/body/div/form/table')
            except Exception:
                try:
                    self.browser.find_element_by_xpath('/html/body/div/p')
                    print('no homework founded\n')
                    ddls[curLesson] = []

                    self.browser.switch_to.default_content()
                    curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
                    lessons = curLessons.find_elements_by_xpath('li')

                    continue
                except:
                    print('timeout or switch to an unknown page')
                    return -4
            table = self.browser.find_element_by_xpath('/html/body/div/form/table')
            tableRows = table.find_elements_by_tag_name('tr')[1:]
            jobs = []
            for row in tableRows:
                datas = row.find_elements_by_tag_name('td')[1:]
                work = []
                if len(datas) >= 1:
                    title = datas[0].find_elements_by_tag_name('a')[0]
                    title = title.text
                    print(title)
                    work.append(title)
                if len(datas) >= 2:
                    status = datas[1].text
                    print(status)
                    work.append(status)
                if len(datas) >= 3:
                    opendate = datas[2].text
                    print(opendate)
                    work.append(opendate)
                if len(datas) >= 4:
                    duedate = datas[3].find_elements_by_tag_name('span')
                    if len(duedate) == 0:
                        duedate = ''
                    else:
                        duedate = duedate[0].text
                    print(duedate)
                    work.append(duedate)
                while len(work) < 4:
                    work.append('')
                print()
                jobs.append(work)
            ddls[curLesson] = jobs

            self.browser.switch_to.default_content()
            curLessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
            lessons = curLessons.find_elements_by_xpath('li')
        return ddls           


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    courseReq(userName, password)