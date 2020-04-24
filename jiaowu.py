from vpn import *


class jiaoWuReq():
    '''
    this class is going to get messages from jiaowu.buaa.edu.cn
    '''
    def __init__(self, userName, password):
        self.status = 0
        vpn = ''
        for i in range(3):
            vpn = VpnLogin(userName, password)  # login
            success = vpn.switchToJiaoWu()      # switch
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
        self.browser = vpn.getBrowser()     # get the browser.

        #self.getEmptyClassroom()           # for debug
        #self.getGrade()                    # for debug
        #self.getSchedule()                 # for debug

    
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

    
    def getGrade(self):
        '''
        this func will get all the grades in a time
        a list will be returned
        data type:
        [
            # sorted by semester
            [   
                [id, semester, department, course code, course character, course type, credit, isExamed, retest mark, grade, convertion grade, grade edit]
                [id, semester, department, course code, course character, course type, credit, isExamed, retest mark, grade, convertion grade, grade edit]
                ...
                ...
            ]
            ...
        ]
        '''
        if self.status != 0:
            return self.status
        # this label cannot click, so we use js to click the label
        personalGradeLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[8]/div/a[1]/span[2]')
        self.browser.execute_script("arguments[0].click();", personalGradeLabel)
        time.sleep(0.5)                                                                         
        
        self.browser.switch_to.frame('iframename')                                              # switch to another frame to get datas
        locator = (By.XPATH, '/html/body/div/div/div[3]/div[2]/a')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        endGrage = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/a')     # search the final exam grades
        endGrage.click()
        locator = (By.XPATH, '//*[@id="xnxqid"]')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       
        except Exception:   
            print('timeout or switch to an unknown page')
            return -4
        selectDate = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))            
        allGrades = []
        for i in range(len(selectDate.options)):                                            # the first option cannot use
            if i == len(selectDate.options) - 1:
                continue
            each = selectDate.options[i + 1]
            print(str(each.text))
            selectDate.select_by_visible_text(each.text)                                        
            time.sleep(2)                                                                       
            searchButton = self.browser.find_element_by_xpath('//*[@id="queryform"]/div/table/tbody/tr[1]/td[9]/div/a')
            searchButton.click()                                                                
            locator = (By.XPATH, '/html/body/div[1]/div/div[4]/table')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            table = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/table')    
            tableRows = table.find_elements_by_tag_name('tr')[1:]
            grades = []
            for row in tableRows:                                                               # view the chart
                grade = []
                datas = row.find_elements_by_tag_name('td')                                     
                for data in datas:
                    #print(data.text)                                                           # for debug
                    grade.append(data.text)
                #print()
                grades.append(grade)
            #print()
            allGrades.append(grades)                                                            
            selectDate = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))        # reget the select options
        return allGrades

    
    def getEmptyClassroom(self):
        '''
        this func will get all the empty classrooms in a time
        a list will be returned
        data type:
        [
            sorted by weeks
            {                   time
                roomName : [1 0 0 1 ...] 1:empty 0:occupied
            }
            ...
        ]
        '''
        if self.status != 0:
            return self.status
        # this label cannot click, so we use js to click the label
        emptyClassroomLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/a[3]')
        self.browser.execute_script("arguments[0].click();", emptyClassroomLabel)
        time.sleep(0.5)                                                                         
        self.browser.switch_to.frame('iframename')                                              # switch to another frame to get datas
        locator = (By.XPATH, '//*[@id="pageZc1"]')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))       
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        selectDate1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))          # set the start week
        selectDate2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))          # set the end week
        allEmptyClassrooms = []
        for i in range(len(selectDate1.options) - 1):                                           # the first option cannot use
            each1 = selectDate1.options[i + 1]
            each2 = selectDate2.options[i + 1]
            print(each1.text)
            selectDate1.select_by_visible_text(each1.text)
            selectDate2.select_by_visible_text(each2.text)
            time.sleep(0.5)                                                                       
            searchButton = self.browser.find_element_by_xpath('//*[@id="queryform"]/table/tbody/tr/td[11]/div/a')
            searchButton.click()                                                                
            locator = (By.XPATH, '/html/body/div/div/div[5]/table')
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))   
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            classRooms = {}
            while True:                                                                         # view all the pages
                
                table = self.browser.find_element_by_xpath('/html/body/div/div/div[5]/table')   
                tableRows = table.find_elements_by_tag_name('tr')[2:]                           
                
                for row in tableRows:                                                           # view the chart
                    classRoom = []
                    rooms = row.find_elements_by_tag_name('td')[1:]
                    #print(row.find_elements_by_tag_name('td')[0].text)
                    for room in rooms:
                        s = room.get_attribute('innerHTML')                                     # check whether it is empty
                        if s == '\n\t\t\t\t\t      \t \n\t\t\t\t\t      \t <div class=""></div>\n\t\t\t\t\t      \t':
                            classRoom.append(1)                                                 
                            #print('1', end = ' ')
                        else:
                            classRoom.append(0)                                                 
                            #print('0', end = ' ')   
                    #print()                                                                    # for debug
                    classRooms[row.find_elements_by_tag_name('td')[0].text] = classRoom
                try:                                                                            # switch t0 the next page
                    nextPage = self.browser.find_element_by_xpath('/html/body/div/div/div[6]/ul/li[12]/a')    
                except Exception:
                    break                                                                       # it is the final page
                nextPage.click()
                locator = (By.XPATH, '/html/body/div/div/div[5]/table')
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -4
                time.sleep(0.5)                                                                   
            selectDate1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))      # reget the select options
            selectDate2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))      # reget the select options
            allEmptyClassrooms.append(classRooms)                                               
        return allEmptyClassrooms

         
    def getSchedule(self):
        '''
        this func will get all the class schedules in a time
        a list will be returned
        data type:
        [
            ['lesson', ' ', ' ', ' ', ' ', ' ', ' ']
            ...
            ['datas'] other lessons
        ]
        '''       
        if self.status != 0:
            return self.status
        # this label cannot click, so we use js to click the label
        scheduleLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/a[6]')
        self.browser.execute_script("arguments[0].click();", scheduleLabel)
        #time.sleep(0.5)                                                                             
        self.browser.switch_to.frame('iframename')                                                  
        locator = (By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/table')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))           
        except Exception:
            print('timeout or switch to an unknown page')
            return -4

        idPlace = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[8]/div[1]/span')
        studentId = idPlace.text
        studentId = studentId.split('(')[1]
        studentId = studentId.split(')')[0]

        table = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[8]/div[2]/table')     
        tableRows = table.find_elements_by_tag_name('tr')[1:-2]   
        schedules = []
        for row in tableRows:                                                                       # view the chart
            schedule = []     
            lessons = row.find_elements_by_tag_name('td')[2:]                                       # catch all the lessons   
            for each in lessons:
                #print(each.text)
                schedule.append(each.text)
            schedules.append(schedule)
        #print(table.find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name('td')[0].text)    # other lessons
        other = []
        other.append(table.find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name('td')[0].text)
        schedules.append(other)


        return schedules

    def getId(self):
        if self.status != 0:
            return self.status
        # this label cannot click, so we use js to click the label
        scheduleLabel = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/a[6]')
        self.browser.execute_script("arguments[0].click();", scheduleLabel)
        #time.sleep(0.5)                                                                             
        self.browser.switch_to.frame('iframename')                                                  
        locator = (By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/table')
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))           
        except Exception:
            print('timeout or switch to an unknown page')
            return -4

        idPlace = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[8]/div[1]/span')
        studentId = idPlace.text
        studentId = studentId.split('(')[1]
        studentId = studentId.split(')')[0]
        return studentId

    def quit(self):
        self.browser.quit()

# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    jiaoWuReq(userName, password)
