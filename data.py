from jiaowu import *
from course import *

'''
this class is goint to arrange the data 
and create interface for background
'''

class DataReq():
    def __init__(self, userName, password):
        self.userName = userName
        self.password = password

    def request(self, requestType):
        getStuId = jiaoWuReq(self.userName, self.password)
        stuId = getStuId.getId()
        getStuId.quit()
        if requestType == 'd':          # get ddl
            course = courseReq(self.userName, self.password)
            ddls = course.getDdl()
            course.quit()
            if ddls == -1 or ddls == -2 or ddls == -3 or ddls == -4:
                return ddls
            else:
                return self.dealWithDdl(ddls, stuId) 
        elif requestType == 'g':        # get grades
            jiaowu = jiaoWuReq(self.userName, self.password)
            grades = jiaowu.getGrade()
            jiaowu.quit()
            if grades == -1 or grades == -2 or grades == -3 or grades == -4:
                return grades
            else:
                return self.dealWithGrades(grades, stuId) 
        elif requestType == 'e':        # get empty classrooms
            jiaowu = jiaoWuReq(self.userName, self.password)
            emptyClassroom = jiaowu.getEmptyClassroom()
            jiaowu.quit()
            if emptyClassroom == -1 or emptyClassroom == -2 or emptyClassroom == -3 or emptyClassroom == -4:
                return emptyClassroom
            else:
                return self.dealWithEmptyClassroom(emptyClassroom) 
        elif requestType == 's':        # get schedules
            jiaowu = jiaoWuReq(self.userName, self.password)
            schedules = jiaowu.getSchedule()
            jiaowu.quit()
            if schedules == -1 or schedules == -2 or schedules == -3 or schedules == -4:
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
            for each in allDdl:
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
        returnJson = json.dumps(aimJson, ensure_ascii=False)
        print(returnJson)
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
                lessonCode = curData[3]
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
            returnJson = json.dumps(scheduleChart, ensure_ascii=False)
            print(returnJson)
            jsons.append(returnJson)
        return jsons

    def dealWithEmptyClassroom(self, emptyClassroom):
        '''
        data sort for empty classrooms
        it is difficult to finish it in time
        '''
        aimJson = []
        for i in range(len(emptyClassroom)):
            thisWeek = emptyClassroom[i]
            for room, isEmpty in thisWeek.items():
                campus = ''
                teaching_building = ''
                classroom = ''
                if room[0] == 'J':
                    campus = '沙河校区'
                else:
                    campus = '学院路校区'
                classroom = room
                if room[0] == 'J' and room[1] == '1':
                    teaching_building = '教一'
                elif room[0] == 'J' and room[1] == '2':
                    teaching_building = '教二'
                elif room[0] == 'J' and room[1] == '3':
                    teaching_building = '教三'
                elif room[0] == 'J' and room[1] == '4':
                    teaching_building = '教四'
                elif room[0] == 'J' and room[1] == '5':
                    teaching_building = '教五'
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
                for j in range(len(isEmpty)):
                    if j % 6 == 5:
                        # TODO: use i and j to getCurDate
                        date = ''
                        if isEmpty[j] == 1:
                            section.append(13)
                            section.append(14)
                        # TODO: data insert

                        section.clear()
                    else:
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
        # TODO: data sort and return
        return ''

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
                lesson, info = curStr.split('\n')
                teachers, info = info.split('[')
                week, info = info.split(']')
                place, time = info.split(' ')
                curInfo = []
                curInfo.append(lesson)
                curInfo.append(place[1:])
                curInfo.append(teachers)
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
                curInfo.append(week)
                curInfo.append('周' + str(j + 1) + ' ' + time)
                aimLessons.append(curInfo)
        scheduleChart = {}
        scheduleChart['student_id'] = studentId
        scheduleChart['info'] = aimLessons
        returnJson = json.dumps(scheduleChart, ensure_ascii=False)
        print(returnJson)
        return returnJson

# for test
if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    DataReq(userName, password).request('d')
    #DataReq(userName, password).request('g')
    #DataReq(userName, password).request('e')
    #DataReq(userName, password).request('s')

