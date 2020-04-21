from data import *
from multiprocessing import Queue
import requests

host = '127.0.0.1:8000/'
#host = '114.115.208.32:8000/'                  # for local test
headers = {'Content-Type': 'application/json'}

def getAllStu():
    '''
    get all the students' usr_name and password
    '''
    url = host + 'login/'
    req = requests.get(url)
    jsons = req.json()
    data = json.loads(jsons)
    return data

def reqSchedule(dataReq):
    '''
    get the schedule's json and post it to the back 
    '''
    schedule = dataReq.request('s')
    # due with the errors
    if schedule == -1:
        print('usr_name or password is wrong\n')
        return 0
    elif schedule == -2:
        print('there is something wrong on network\n')
        return 0
    elif schedule == -3:
        print('unknown errors\n')  
        return 0
    elif schedule == -4:
        print('error on the jiaowu web\n')  
        return 0
    scheduleUrl = host + 'timetable/'
    requests.post(url=scheduleUrl, headers=headers, data=schedule)
    return 1

def reqGrades(dataReq):
    '''
    get the grade's json and post it to the back 
    '''
    grades = dataReq.request('g')
    # due with the errors
    if grades == -1:
        print('usr_name or password is wrong\n')
        return 0
    elif grades == -2:
        print('there is something wrong on network\n')
        return 0
    elif grades == -3:
        print('unknown errors\n')  
        return 0
    elif grades == -4:
        print('error on the jiaowu web\n')  
        return 0
    gradesUrl = host + 'timetable/'
    requests.post(url=gradesUrl, headers=headers, data=grades)
    return 1

def reqDdl(dataReq):
    '''
    get the ddl's json and post it to the back 
    '''
    ddl = dataReq.request('d')
    # due with the errors
    if ddl == -1:
        print('usr_name or password is wrong\n')
        return 0
    elif ddl == -2:
        print('there is something wrong on network\n')
        return 0
    elif ddl == -3:
        print('unknown errors\n')  
        return 0
    elif ddl == -4:
        print('error on the jiaowu web\n')  
        return 0
    ddlUrl = host + 'timetable/'
    requests.post(url=ddlUrl, headers=headers, data=ddl)
    return 1

def reqEmptyClassroom(dataReq):
    '''
    get the empty classroom's json and post it to the back 
    '''
    emptyClassroom = dataReq.request('e')
    # due with the errors
    if emptyClassroom == -1:
        print('usr_name or password is wrong\n')
        return 0
    elif emptyClassroom == -2:
        print('there is something wrong on network\n')
        return 0
    elif emptyClassroom == -3:
        print('unknown errors\n')  
        return 0
    elif emptyClassroom == -4:
        print('error on the jiaowu web\n')  
        return 0
    emptyClassroomUrl = host + 'timetable/'
    requests.post(url=emptyClassroomUrl, headers=headers, data=emptyClassroom)
    return 1

def dealReqs():
    '''
    due with the reqs from the background
    return 1 -> success
    return 0 -> no req exists
    return -1 -> failed
    return -2 -> empty classroom req
    '''
    askUrl = host + 'request/'
    req = requests.get(askUrl)
    
    if req.status_code == 204:                  # if there is not any reqs
        return 0

    # due with the reqs
    jsons = req.json()
    data = json.loads(jsons)
    user = data['usr_name']
    password = data['password']
    reqType = data['req_type']
    dataReq = DataReq(user, password)
    success = 0
    if reqType == 's':
        i = 0
        while success == 0 and i < 3:
            success = reqSchedule(dataReq)
            i += 1
    if reqType == 'g':
        i = 0
        while success == 0 and i < 3:
            success = reqGrades(dataReq)
            i += 1
    if reqType == 'd':
        i = 0
        while success == 0 and i < 3:
            success = reqDdl(dataReq)
            i += 1
    '''
    it cost too much time
    so we won't let it happen
    '''
    if reqType == 'e':
        #reqEmptyClassroom(dataReq)
        return -2
    if success == 0:
        return -1
    requests.post(url=askUrl, headers=headers, data=jsons)
    return 1

def insect():
    '''
    the main func
    circle and circle again to get all the datas
    '''
    while True:
        now = datetime.now()                                # get the cur time
        allStu = getAllStu()
        for j in range(len(allStu)):                        # flush all the students' datas
            usr = allStu[j]['usr_name']
            pw = allStu[j]['usr_password']
            curDataReq = DataReq(usr, pw)
            if j == 0:
                success = 0
                i = 0
                while success == 0 and i < 3:
                    success = reqEmptyClassroom(curDataReq)           # empty classroom checked once
                    i += 1
            success = 0
            i = 0
            while success == 0 and i < 3:
                success = reqEmptyClassroom(curDataReq)               
                i += 1
            success = 0
            i = 0
            while success == 0 and i < 3:
                success = reqEmptyClassroom(curDataReq)               
                i += 1
            success = 0
            i = 0
            while success == 0 and i < 3:
                success = reqEmptyClassroom(curDataReq)               
                i += 1
            reqSchedule(curDataReq)
            reqGrades(curDataReq)
            reqDdl(curDataReq)
            dealReqs()

        while True:
            afterProc = datetime.now()                      # get the cur time
            deltatime = afterProc - now
            seconds = deltatime.total_seconds()
            if seconds >= 7200 and dealReqs() == 0:         # will not flush the datas until 2h later and no reqs exist
                break
            dealReqs()                                      # deal with the reqs in the waiting time
            time.sleep(5)                                   # avoid the cpu from circling all the time

def testTime():
    '''
    test the time cost
    result:
    empty classroom: 0:20:41.309
    schedule: 0:00:28.732
    grades: 0.00.55.983
    ddls: 0.00.52.933
    '''
    usr = input('user: ')
    pw = input('password: ')
    curDataReq = DataReq(usr, pw)
    now = datetime.now() 
    reqEmptyClassroom(curDataReq)   
    enow = datetime.now() 
    reqSchedule(curDataReq)
    snow = datetime.now() 
    reqGrades(curDataReq)
    gnow = datetime.now() 
    reqDdl(curDataReq)
    dnow = datetime.now() 
    deltatime = enow - now
    print('empty ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = snow - enow
    print('schedule ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = gnow - snow
    print('grade ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = dnow - gnow
    print('ddl ' + str(deltatime.total_seconds()))
    print(deltatime)


# start the program                
if __name__ == '__main__':
    #testTime()
    insect()