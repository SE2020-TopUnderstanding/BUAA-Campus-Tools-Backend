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
        if requestType == 'd':          # get ddl
            course = courseReq(self.userName, self.password)
            ddls = course.getDdl()
            if ddls == -1 or ddls == -2 or ddls == -3 or ddls == -4:
                return ddls
            else:
                return self.dealWithDdl(ddls) 
        elif requestType == 'g':        # get grades
            jiaowu = jiaoWuReq(self.userName, self.password)
            stuId = '17373010'
            grades = jiaowu.getGrade()
            if grades == -1 or grades == -2 or grades == -3 or grades == -4:
                return grades
            else:
                return self.dealWithGrades(grades, stuId) 
        elif requestType == 'e':        # get empty classrooms
            jiaowu = jiaoWuReq(self.userName, self.password)
            emptyClassroom = jiaowu.getEmptyClassroom()
            if emptyClassroom == -1 or emptyClassroom == -2 or emptyClassroom == -3 or emptyClassroom == -4:
                return emptyClassroom
            else:
                return self.dealWithEmptyClassroom(emptyClassroom) 
        elif requestType == 's':        # get schedules
            jiaowu = jiaoWuReq(self.userName, self.password)
            schedules, stuId = jiaowu.getSchedule()
            if schedules == -1 or schedules == -2 or schedules == -3 or schedules == -4:
                return schedules
            else:
                return self.dealWithSchedules(schedules, stuId) 

    def dealWithDdl(self, ddls):
        return ''
    
    def dealWithGrades(self, grades, studentId):
        '''
        this feature still has some bugs
        and have some problems to deal with
        '''
        jsons = []
        for i in range(len(grades)):
            aimGrades = []
            aimGrades.append(studentId)
            semember = ''
            for j in range(len(grades[i])):
                curData = grades[i][j]
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

if __name__ == "__main__":
    userName = input('Your username: ') 
    password = input('Your password: ')
    DataReq(userName, password).request('g')

