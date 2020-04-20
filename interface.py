from data import *
from multiprocessing import Queue
import requests

host = '127.0.0.1:8000/'
host = '114.115.208.32:8000/'
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
        return
    elif schedule == -2:
        print('there is something wrong on network\n')
        return
    elif schedule == -3:
        print('unknown errors\n')  
        return
    elif schedule == -4:
        print('error on the jiaowu web\n')  
        return
    scheduleUrl = host + 'timetable/'
    requests.post(url=scheduleUrl, headers=headers, data=schedule)

def reqGrades(dataReq):
    '''
    get the grade's json and post it to the back 
    '''
    grades = dataReq.request('g')
    # due with the errors
    if grades == -1:
        print('usr_name or password is wrong\n')
        return
    elif grades == -2:
        print('there is something wrong on network\n')
        return
    elif grades == -3:
        print('unknown errors\n')  
        return
    elif grades == -4:
        print('error on the jiaowu web\n')  
        return
    gradesUrl = host + 'timetable/'
    requests.post(url=gradesUrl, headers=headers, data=grades)

def reqDdl(dataReq):
    '''
    get the ddl's json and post it to the back 
    '''
    ddl = dataReq.request('d')
    # due with the errors
    if ddl == -1:
        print('usr_name or password is wrong\n')
        return
    elif ddl == -2:
        print('there is something wrong on network\n')
        return
    elif ddl == -3:
        print('unknown errors\n')  
        return
    elif ddl == -4:
        print('error on the jiaowu web\n')  
        return
    ddlUrl = host + 'timetable/'
    requests.post(url=ddlUrl, headers=headers, data=ddl)

def reqEmptyClassroom(dataReq):
    '''
    get the empty classroom's json and post it to the back 
    '''
    emptyClassroom = dataReq.request('e')
    # due with the errors
    if emptyClassroom == -1:
        print('usr_name or password is wrong\n')
        return
    elif emptyClassroom == -2:
        print('there is something wrong on network\n')
        return
    elif emptyClassroom == -3:
        print('unknown errors\n')  
        return
    elif emptyClassroom == -4:
        print('error on the jiaowu web\n')  
        return
    emptyClassroomUrl = host + 'timetable/'
    requests.post(url=emptyClassroomUrl, headers=headers, data=emptyClassroom)

def dealReqs():
    '''
    due with the reqs from the background
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
    if reqType == 's':
        reqSchedule(dataReq)
    if reqType == 'g':
        reqGrades(dataReq)
    if reqType == 'd':
        reqDdl(dataReq)
    '''
    it cost too much time
    so we won't let it happen
    '''
    if reqType == 'e':
        #reqEmptyClassroom(dataReq)
        return 0
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
        for i in range(len(allStu)):                        # flush all the students' datas
            usr = allStu[0]['usr_name']
            pw = allStu[0]['usr_password']
            curDataReq = DataReq(usr, pw)
            if i == 0:
                reqEmptyClassroom(curDataReq)               # empty classroom checked once
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