from jiaowu import *
from course import *

class DataReq():
    '''
    this class is goint to arrange the data 
    '''
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password

    def request(self, requestType):
        '''
        catch all the reqs 
        get and sort the datas
        requestType: {'d':'ddls', 'g':'grades', 'e':'empty classrooms', 's':'schedule'}
        '''
        print('start to get the data, usr_name: ' + self.userName)
        print('requestType: ' + requestType)
        getStuId = jiaoWuReq(self.userName, self.password)              # get the student's id
        stuId = getStuId.getId()
        print('studentId: ' + str(stuId))
        getStuId.quit()
        if stuId == -1 or stuId == -2 or stuId == -3 or stuId == -4:    # if there is something wrong
            print('something wrong')
            print('usr_name: ' + self.userName)
            print('requestType: ' + 'getStuId')
            return stuId
        if requestType == 'd':                                          # get ddl
            course = courseReq(self.userName, self.password)
            ddls = course.getDdl()
            course.quit()
            if ddls == -1 or ddls == -2 or ddls == -3 or ddls == -4:    # if there is something wrong
                print('something wrong')
                print('usr_name: ' + self.userName)
                print('requestType: ddl')
                return ddls
            else:
                return self.dealWithDdl(ddls, stuId) 
        elif requestType == 'g':                                        # get grades
            jiaowu = jiaoWuReq(self.userName, self.password)
            grades = jiaowu.getGrade()
            jiaowu.quit()
            if grades == -1 or grades == -2 or grades == -3 or grades == -4:
                print('something wrong')
                print('usr_name: ' + self.userName)
                print('requestType: grades')
                return grades
            else:
                return self.dealWithGrades(grades, stuId) 
        elif requestType == 'e':                                        # get empty classrooms
            jiaowu = jiaoWuReq(self.userName, self.password)
            emptyClassroom = jiaowu.getEmptyClassroom()
            jiaowu.quit()
            if emptyClassroom == -1 or emptyClassroom == -2 or emptyClassroom == -3 or emptyClassroom == -4:
                print('something wrong')
                print('usr_name: ' + self.userName)
                print('requestType: empty calssroom')
                return emptyClassroom
            else:
                return self.dealWithEmptyClassroom(emptyClassroom) 
        elif requestType == 's':                                        # get schedules
            jiaowu = jiaoWuReq(self.userName, self.password)
            schedules = jiaowu.getSchedule()
            jiaowu.quit()
            if schedules == -1 or schedules == -2 or schedules == -3 or schedules == -4:
                print('something wrong')
                print('usr_name: ' + self.userName)
                print('requestType: schedule')
                return schedules
            else:
                return self.dealWithSchedules(schedules, stuId) 

    def dealWithDdl(self, ddls, studentId):
        '''
        data sort for ddls
        '''
        aimJson = {}
        aimJson['student_id'] = studentId
        ddl = []
        for lesson, allDdl in ddls.items():
            curLessonDdl = {}
            content = []
            for each in allDdl:                                         # get all the needed items
                curDdl = {}
                if len(each) >= 4:
                    curDdl['ddl'] = each[3]
                else:
                    curDdl['ddl'] = ''
                curDdl['homework'] = each[0]
                curDdl['state'] = each[1]
                content.append(curDdl)
            curLessonDdl['content'] = content
            curLessonDdl['name'] = lesson
            ddl.append(curLessonDdl)
        aimJson['ddl'] = ddl
        returnJson = json.dumps(aimJson, ensure_ascii=False)            # get the json package
        #print(returnJson)
        return returnJson
    
    def dealWithGrades(self, oriGrades, studentId):
        '''
        data sort for grades
        '''
        jsons = []
        for i in range(len(oriGrades)):
            aimGrades = []
            semember = ''
            for j in range(len(oriGrades[i])):
                curData = oriGrades[i][j]
                lessonCode = curData[3]                                 # get all the needed datas
                lessonName = curData[4]
                credit = curData[7]
                grades = curData[11]
                semember = curData[1]
                curInfo = []
                curInfo.append(lessonCode)
                curInfo.append(lessonName)
                curInfo.append(credit)
                curInfo.append(grades)
                aimGrades.append(curInfo)
            
            scheduleChart = {}
            scheduleChart['student_id'] = studentId
            scheduleChart['semember'] = semember
            scheduleChart['info'] = aimGrades
            #returnJson = json.dumps(scheduleChart, ensure_ascii=False)  # get the json package
            #print(returnJson)
            jsons.append(scheduleChart)
        returnJson = json.dumps(jsons, ensure_ascii=False)            # get the json package
        return returnJson

    def dealWithEmptyClassroom(self, emptyClassroom):
        '''
        data sort for empty classrooms
        '''
        aimJson = []
        dictXueYuan = {}
        dictXueYuan['campus'] = '学院路校区'
        xueYuan = []
        dictShaHe = {}
        dictShaHe['campus'] = '沙河校区'
        shaHe = []
        for i in range(len(emptyClassroom)):
            thisWeek = emptyClassroom[i]
            for room, isEmpty in thisWeek.items():
                campus = ''
                teaching_building = ''
                classroom = ''
                if room[0] == 'J':                                      # get the campus
                    campus = '沙河校区'
                else:
                    campus = '学院路校区'
                classroom = room
                if room[0] == 'J' and room[1] == '1':                   # get the building
                    teaching_building = '教一'
                elif room[0] == 'J' and room[1] == '2':
                    teaching_building = '教二'
                elif room[0] == 'J' and room[1] == '3':
                    teaching_building = '教三'
                elif room[0] == 'J' and room[1] == '4':
                    teaching_building = '教四'
                elif room[0] == 'J' and room[1] == '5':
                    teaching_building = '教五'
                elif room[0] == 'J' and room[1] == '0':
                    teaching_building = '教零'
                elif room[0] == '(' and room[1] == '一':
                    teaching_building = '一号楼'
                elif room[0] == '(' and room[1] == '二':
                    teaching_building = '二号楼'
                elif room[0] == '(' and room[1] == '三':
                    teaching_building = '三号楼'
                elif room[0] == '(' and room[1] == '四':
                    teaching_building = '四号楼'
                elif room[0] == '主' and room[1] == 'M':
                    teaching_building = '主M楼'
                elif room[0] == '主' and room[1] == '北':
                    teaching_building = '主北楼'
                elif room[0] == '主' and room[1] == '南':
                    teaching_building = '主南楼'
                elif room[0] == 'A':
                    teaching_building = '新主楼A座'   
                elif room[0] == 'B':
                    teaching_building = '新主楼B座'  
                elif room[0] == 'C':
                    teaching_building = '新主楼C座'    
                elif room[0] == 'D':
                    teaching_building = '新主楼D座'    
                elif room[0] == 'E':
                    teaching_building = '新主楼E座'    
                elif room[0] == 'F':
                    teaching_building = '新主楼F座'    
                elif room[0] == 'G':
                    teaching_building = '新主楼G座'   
                elif room[0] == 'H':
                    teaching_building = '新主楼H座'   
                section = []
                for j in range(len(isEmpty)):                           # get the date and section
                    if j % 6 == 5:                                      # if it is end of a day
                        days = i * 7 + j / 6
                        originDay = datetime.strptime('2020-02-24',"%Y-%m-%d")
                        date = originDay + timedelta(days = days)
                        date = date.strftime("%Y-%m-%d")
                        if isEmpty[j] == 1:
                            section.append(13)
                            section.append(14)
                        dictCur = {}
                        dictCur['teaching_building'] = teaching_building
                        dictCur['classroom'] = classroom
                        dictCur['date'] = date
                        tmp = str(section.copy())
                        tmp = tmp[:-1] + ',]'
                        dictCur['section'] = tmp

                        if campus == '沙河校区':
                            shaHe.append(dictCur)
                        else:
                            xueYuan.append(dictCur)
                        section.clear()
                    else:                                               # it is still in a single day
                        if isEmpty[j] == 1:
                            if j % 6 == 0:
                                section.append(1)
                                section.append(2)
                            if j % 6 == 1:
                                section.append(3)
                                section.append(4)
                                section.append(5)
                            if j % 6 == 2:
                                section.append(6)
                                section.append(7)
                            if j % 6 == 3:
                                section.append(8)
                                section.append(9)
                                section.append(10)
                            if j % 6 == 4:
                                section.append(11)
                                section.append(12)
        dictShaHe['content'] = shaHe
        dictXueYuan['content'] = xueYuan
        aimJson.append(dictShaHe)
        aimJson.append(dictXueYuan)
        returnJson = json.dumps(aimJson, ensure_ascii=False)            # get the json package
        #print(returnJson)
        return returnJson

    def dealWithSchedules(self, schedules, studentId):
        '''
        data sort for schedules
        '''
        aimLessons = []
        for i in range(len(schedules) - 1):
            for j in range(len(schedules[i])):
                curStr = schedules[i][j]
                if curStr == ' ':
                    continue
                # TODO: data sort
                curStrs = curStr.split('\n')
                lesson = curStrs[0]
                info = ''
                for k in range(len(curStrs) - 1):
                    info = info + curStrs[k + 1]
                infos = info.split('，')
                types = []
                tmpStr = ''
                for each in infos:
                    tmpStr = tmpStr + each
                    if each[-1] == '节':
                        types.append(tmpStr)
                        tmpStr = ''
                    else:
                        tmpStr = tmpStr + '，'
                curInfos = []
                for each in types:
                    info = each
                    teachers, info = info.split('[')                        # some special conditions cannot be unpacked easily
                    week, info = info.split(']')
                    place, time = info.split(' ')
                    curInfo = []
                    curInfo.append(lesson)
                    curInfo.append(place[1:])
                    curInfo.append(teachers)
                    curInfo.append(week)
                    curInfo.append('周' + str(j + 1) + ' ' + time)
                    curInfos.append(curInfo)
                '''
                this feature cannot be achieved easily

                if len(week.split('-')) == 2:
                    weeksStart = int(week.split('-')[0])
                    weeksEnd = int(week.split('-')[1])
                    weeksInt = []
                    for k in range(weeksStart, weeksEnd + 1):
                        weeksInt.append(k)
                    curInfo.append(weeksInt)
                elif len(week.split('-')) == 1:
                    curInfo.append(int(week))
                '''
                aimLessons.append(curInfos)
        scheduleChart = {}
        scheduleChart['student_id'] = studentId
        scheduleChart['info'] = aimLessons
        returnJson = json.dumps(scheduleChart, ensure_ascii=False)      # get the json package
        #print(returnJson)
        return returnJson

# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    #DataReq(userName, password).request('d')
    #DataReq(userName, password).request('g')
    #DataReq(userName, password).request('e')
    DataReq(userName, password).request('s')

