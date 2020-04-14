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

        #self.getEmptyClassroom()           # for debug
        #self.getGrade()                    # for debug

    '''
    this func will get all the grades in a time
    an list will be returned
    '''
    def getGrade(self):
        # this label cannot click, so we use js to click the label
        personalGradeLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[8]/div/a[1]/span[2]')
        self.browser.execute_script("arguments[0].click();", personalGradeLabel)
        time.sleep(0.5)                                                                         # slow down, avoid too much afford
        
        self.browser.switch_to.frame('iframename')                                              # switch to another frame to get datas
        locator = (By.XPATH, '/html/body/div/div/div[3]/div[2]/a')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       # wait until the item appears
        except Exception:
            print('timeout or switch to an unknown page')
            return -1
        endGrage = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/a')     # search the final exam grades
        endGrage.click()
        locator = (By.XPATH, '//*[@id="xnxqid"]')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       # wait until the item appears
        except Exception:   
            print('timeout or switch to an unknown page')
            return -1
        selectDate = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))            # all the semester
        allGrades = []
        for i in range(len(selectDate.options) - 1):                                            # the first option cannot use
            each = selectDate.options[i + 1]
            print(each.text)
            selectDate.select_by_visible_text(each.text)                                        # select cur semester
            time.sleep(2)                                                                       # slow down, avoid too much afford
            searchButton = self.browser.find_element_by_xpath('//*[@id="queryform"]/div/table/tbody/tr[1]/td[9]/div/a')
            searchButton.click()                                                                # begin searching
            locator = (By.XPATH, '/html/body/div[1]/div/div[4]/table')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   # wait until the item appears
            except Exception:
                print('timeout or switch to an unknown page')
                return -1
            table = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/table')    # get into the chart
            tableRows = table.find_elements_by_tag_name('tr')[1:]
            grades = []
            for row in tableRows:                                                               # view the chart
                grade = []
                datas = row.find_elements_by_tag_name('td')                                     # get all the datas in a row
                for data in datas:
                    #print(data.text)                                                           # for debug
                    grade.append(data.text)
                #print()
                grades.append(grade)
            #print()
            allGrades.append(grades)                                                            # store the datas
            selectDate = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))        # reget the select options
        return allGrades

    '''
    this func will get all the empty classrooms in a time
    an list will be returned
    '''
    def getEmptyClassroom(self):
        # this label cannot click, so we use js to click the label
        emptyClassroomLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/a[3]')
        self.browser.execute_script("arguments[0].click();", emptyClassroomLabel)
        time.sleep(0.5)                                                                         # slow down, avoid too much afford
        self.browser.switch_to.frame('iframename')                                              # switch to another frame to get datas
        locator = (By.XPATH, '//*[@id="pageZc1"]')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       # wait until the item appears
        except Exception:
            print('timeout or switch to an unknown page')
            return -1
        selectDate1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))          # set the start week
        selectDate2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))          # set the end week
        allEmptyClassrooms = []
        for i in range(len(selectDate1.options) - 1):                                           # the first option cannot use
            each1 = selectDate1.options[i + 1]
            each2 = selectDate2.options[i + 1]
            print(each1.text)
            selectDate1.select_by_visible_text(each1.text)
            selectDate2.select_by_visible_text(each2.text)
            time.sleep(2)                                                                       # slow down, avoid too much afford
            searchButton = self.browser.find_element_by_xpath('//*[@id="queryform"]/table/tbody/tr/td[11]/div/a')
            searchButton.click()                                                                # begin to search
            locator = (By.XPATH, '/html/body/div/div/div[5]/table')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   # wait until the item appears
            except Exception:
                print('timeout or switch to an unknown page')
                return -1
            classRooms = {}
            while True:                                                                         # view all the pages
                
                table = self.browser.find_element_by_xpath('/html/body/div/div/div[5]/table')   # get the chart
                tableRows = table.find_elements_by_tag_name('tr')[2:]                           
                
                for row in tableRows:                                                           # view the chart
                    classRoom = []
                    rooms = row.find_elements_by_tag_name('td')[1:]
                    print(row.find_elements_by_tag_name('td')[0].text)
                    for room in rooms:
                        s = room.get_attribute('innerHTML')                                     # check whether it is empty
                        if s == '\n\t\t\t\t\t      \t \n\t\t\t\t\t      \t <div class=""></div>\n\t\t\t\t\t      \t':
                            classRoom.append(1)                                                 # empty
                            #print('1', end = ' ')
                        else:
                            classRoom.append(0)                                                 # occupied
                            #print('0', end = ' ')   
                    #print()                                                                    # for debug
                    classRooms[row.find_elements_by_tag_name('td')[0].text] = classRoom
                try:                                                                            # switch t0 the next page
                    nextPage = self.browser.find_element_by_xpath('/html/body/div/div/div[6]/ul/li[12]/a')
                    nextPage.click()
                except Exception:
                    break                                                                       # it is the final page
                time.sleep(1)                                                                   # slow down, avoid too much afford
            selectDate1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))      # reget the select options
            selectDate2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))      # reget the select options
            allEmptyClassrooms.append(classRooms)                                               # store the datas
        return allEmptyClassrooms
                


# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    jiaoWuReq(userName, password)
