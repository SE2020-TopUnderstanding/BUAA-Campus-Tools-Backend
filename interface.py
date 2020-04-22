from data import *
from multiprocessing import Queue
import requests
import traceback

#host = '127.0.0.1:8000/'
host = 'http://114.115.208.32:8000/'                  # for local test
headers = {'Content-Type': 'application/json'}

def decrypt_string(message):
    decode_result = ""
    for char in message:
        char_int = ord(char)                          # 返回ascall值
        if  (char_int >= 97) & (char_int <= 122):     # 小写字母
            decode_result += chr(122-(char_int-97))
        elif (char_int >= 69) & (char_int <= 78):     # E-N
            decode_result += chr(57-char_int+69)
        elif (char_int >= 48) & (char_int <= 57):     # 0-9
            decode_result += chr(69+char_int-48)
        else:
            decode_result += char
    return decode_result

def getAllStu():
    '''
    get all the students' usr_name and password
    return jsons -> success
    return -1 -> req fail
    '''
    url = host + 'login/'
    params = {'password' : '123'}
    try:
        req = requests.get(url, verify=False, params=params)
    except Exception:
        print('req fail')
        return -1
    jsons = req.json()
    #data = json.loads(jsons)
    return jsons

def reqSchedule(dataReq):
    '''
    get the schedule's json and post it to the back 
    return 1 -> success
    return 0 -> web fail
    return -5 -> req fail
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
    try:
        requests.post(url=scheduleUrl, headers=headers, data=schedule.encode('utf-8'))
    except Exception:
        print('req fail')
        return -5
    return 1

def reqGrades(dataReq):
    '''
    get the grade's json and post it to the back 
    return 1 -> success
    return 0 -> web fail
    return -5 -> req fail
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
    gradesUrl = host + 'score/'
    for each in grades:
        try:
            requests.post(url=gradesUrl, headers=headers, data=each.encode('utf-8'))
        except Exception:
            print('req fail')
            print(traceback.format_exc())
            return -5
    return 1

def reqDdl(dataReq):
    '''
    get the ddl's json and post it to the back 
    return 1 -> success
    return 0 -> web fail
    return -5 -> req fail
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
    ddlUrl = host + 'ddl/'
    try:
        requests.post(url=ddlUrl, headers=headers, data=ddl.encode('utf-8'))
    except Exception:
        print('req fail')
        return -5
    return 1

def reqEmptyClassroom(dataReq):
    '''
    get the empty classroom's json and post it to the back 
    return 1 -> success
    return 0 -> web fail
    return -5 -> req fail
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
    emptyClassroomUrl = host + 'classroom/'
    for each in emptyClassroom:
        try:
            requests.post(url=emptyClassroomUrl, headers=headers, data=each.encode('utf-8'))
        except Exception:
            print('req fail')
            return -5
    return 1

def dealReqs():
    '''
    due with the reqs from the background
    return 1 -> success
    return 0 -> no req exists
    return -1 -> failed
    return -2 -> empty classroom req
    return -5 -> req get fail
    return -6 -> req post fail
    '''
    askUrl = host + 'request/'
    try:
        req = requests.get(askUrl)
    except Exception:
        print('req get fail')
        return -5
        
    
    if req.status_code == 204:                  # if there is not any reqs
        return 0

    # due with the reqs
    jsons = req.json()
    data = jsons
    #data = json.loads(jsons)
    user = data['usr_name']
    password = data['password']
    reqType = data['req_type']
    dataReq = DataReq(user, password)
    success = 0
    if reqType == 's':
        i = 0
        while success != 1 and i < 3:
            success = reqSchedule(dataReq)
            i += 1
    if reqType == 'g':
        i = 0
        while success != 1 and i < 3:
            success = reqGrades(dataReq)
            i += 1
    if reqType == 'd':
        i = 0
        while success != 1 and i < 3:
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
    try:
        requests.post(url=askUrl, headers=headers, data=jsons.encode('utf-8'))
    except Exception:
        print('req post fail')
        return -6
    return 1

def insect():
    '''
    the main func
    circle and circle again to get all the datas
    '''
    print('爬虫部署成功！')
    while True:
        print('开始新一轮循环')
        now = datetime.now()                                # get the cur time
        allStu = getAllStu()
        if allStu == -1:
            continue
        for j in range(len(allStu)):                        # flush all the students' datas
            usr = allStu[j]['usr_name']
            pw = decrypt_string(allStu[j]['usr_password'])
            #pw = allStu[j]['usr_password']
            curDataReq = DataReq(usr, pw)
            if j == 0:
                success = 0
                i = 0
                while success != 1 and i < 3:
                    #success = reqEmptyClassroom(curDataReq)           # empty classroom checked once
                    #success = 1
                    i += 1
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqSchedule(curDataReq)  
                #success = 1           
                i += 1
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqGrades(curDataReq)    
                #success = 1       
                i += 1
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqDdl(curDataReq)    
                #success = 1         
                i += 1            
            dealReqs()

        while True:
            afterProc = datetime.now()                      # get the cur time
            deltatime = afterProc - now
            seconds = deltatime.total_seconds()
            limitTime = len(allStu) * 3.5 + 20
            if seconds >= 0 and dealReqs() == 0:         # will not flush the datas until 2h later and no reqs exist
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
    try:
        insect()
    except Exception as e:
        print(traceback.format_exc())
        insect()