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
        '''
        # for test
        f = open('ddl.txt', 'a', encoding='utf-8')                     
        f.write(returnJson)
        f.close()
        print(returnJson)
        '''
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
            scheduleChart['semester'] = semember
            scheduleChart['info'] = aimGrades
            returnJson = json.dumps(scheduleChart, ensure_ascii=False)  # get the json package
            '''
            # for test
            f = open('grade.txt', 'a', encoding='utf-8')
            f.write(returnJson)
            f.close()
            print(returnJson)
            '''
            jsons.append(returnJson)
        return jsons

    def dealWithEmptyClassroom(self, emptyClassroom):
        '''
        data sort for empty classrooms
        '''
        aimJsons = []
        for i in range(len(emptyClassroom)):
            thisWeek = emptyClassroom[i]
            curWeek = []
            for m in range(7):
                curWeek.append([])
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
                    teaching_building = '主M'
                elif room[0] == '主' and room[1] == '北':
                    teaching_building = '主北'
                elif room[0] == '主' and room[1] == '南':
                    teaching_building = '主南'
                elif room[0] == '主':
                    teaching_building = '主楼'
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
                        if isEmpty[j] == 1:
                            section.append(13)
                            section.append(14)
                        dictCur = {}
                        dictCur['campus'] = campus
                        dictCur['teaching_building'] = teaching_building
                        dictCur['classroom'] = classroom
                        tmp = str(section.copy())
                        tmp = tmp[:-1] + ',]'
                        dictCur['section'] = tmp
                        if len(section) > 0:
                            curWeek[j // 6].append(dictCur)
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
            for m in range(7):                                          # sort all the datas in a day
                curDate = {}
                days = i * 7 + m
                originDay = datetime.strptime('2020-02-24',"%Y-%m-%d")
                date = originDay + timedelta(days = days)
                date = date.strftime("%Y-%m-%d")
                curDate['date'] = date
                curDate['classroom'] = curWeek[m].copy()
                '''
                # for test
                f = open('empty.txt', 'a', encoding='utf-8')
                f.write(returnJson)
                f.close()
                print(returnJson)
                '''
                aimJsons.append(curDate)                                # push this day to the list
        return aimJsons

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

                curStrs = curStr.split('节')                            # divide different lessons by '节'
                lessons = []
                curLesson = ''
                for k in range(len(curStrs)):                           # get all the lessons
                    if curStrs[k] == '':
                        continue
                    if curLesson == '':
                        curLesson = curLesson + curStrs[k]
                        continue
                    if curStrs[k][0] == '，':
                        curLesson = curLesson + '节' + curStrs[k]
                        if k == len(curStrs) - 2:
                            curLesson = curLesson + '节'
                            lessons.append(curLesson)
                            curLesson = ''
                            break
                    if curStrs[k][0] != '，':
                        curLesson = curLesson + '节'
                        lessons.append(curLesson)
                        curLesson = curStrs[k]
                        if k == len(curStrs) - 2:
                            curLesson = curLesson + '节'
                            lessons.append(curLesson)
                            curLesson = ''
                            break
                if curLesson != '':
                    if curLesson[-1] == '：':
                        lessons.append(curLesson)
                    else:
                        lessons.append(curLesson + '节')

                curInfos = []
                for curStr in lessons:                                  # get the datas in a lesson
                    curStrs = curStr.split('\n')
                    lesson = curStrs[0]
                    if curStrs[0] == '':
                        lesson = curStrs[1]
                        curStrs = curStrs[1:]
                    info = ''
                    for k in range(len(curStrs) - 1):
                        info = info + curStrs[k + 1]
                    infos = info.split('，')
                    types = []
                    tmpStr = ''
                    for each in infos:                                  # deal with the multi classes problem
                        tmpStr = tmpStr + each
                        if each[-1] == '节':
                            types.append(tmpStr)
                            tmpStr = ''
                        else:
                            tmpStr = tmpStr + '，'

                    for each in types:
                        info = each
                        teachers, info = info.split('[')                # get the teacher
                        week, info = info.split(']')                    # get the week
                        place, time = info.split(' ')                   # get the place and time
                        # deal with some certain problems
                        if week == '' or week == '周':
                            week = '1-16'
                        if place[0] == '单' or place[0] == '双':
                            week = week + place[0]
                            place = place[1:]
                        if time[0] == time[1]:
                            time = time[1:]
                        curInfo = []
                        curInfo.append(lesson)
                        curInfo.append(place[1:])
                        curInfo.append(teachers)
                        curInfo.append(week)
                        curInfo.append('周' + str(j + 1) + ' ' + time)
                        curInfos.append(curInfo)
                aimLessons.append(curInfos)
        scheduleChart = {}
        scheduleChart['student_id'] = studentId
        scheduleChart['info'] = aimLessons
        returnJson = json.dumps(scheduleChart, ensure_ascii=False)      # get the json package
        '''
        # for test
        f = open('schedule.txt', 'a', encoding='utf-8')
        f.write(returnJson)
        f.close()
        print(returnJson)
        '''
        return returnJson

# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    #DataReq(userName, password).request('d')
    #DataReq(userName, password).request('g')
    #DataReq(userName, password).request('e')
    #DataReq(userName, password).request('s')

