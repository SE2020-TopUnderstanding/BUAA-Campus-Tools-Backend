from data import *
from multiprocessing import Queue
import requests
import traceback
import sys

host = 'http://114.115.208.32:8000/'                  
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
        print(traceback.format_exc())
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
        print('error on the course web\n')  
        return 0
    ddlUrl = host + 'ddl/'
    try:
        requests.post(url=ddlUrl, headers=headers, data=ddl.encode('utf-8'))
    except Exception:
        print('req fail')
        print(traceback.format_exc())
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
        returnJson = json.dumps(each, ensure_ascii=False)
        try:
            requests.post(url=emptyClassroomUrl, headers=headers, data=returnJson.encode('utf-8'))
        except Exception:
            print(traceback.format_exc())
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
    user = data['usr_name']
    password = decrypt_string(data['password'])
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

def insect_other():
    '''
    the main func
    circle and circle again to get the other datas
    '''
    print('爬虫部署成功！')
    print('将进行课表、成绩、空教室的查询')
    while True:
        print('开始新一轮循环')
        now = datetime.now()                                # get the cur time
        '''
        this part will start to get the data at 3:00 am, but it cannot start at this time,
        because more situations need to be discussed and considered

        time_begin = datetime.strptime(str(datetime.now().date()) + '3:00',"%Y-%m-%d%H:%M")
        time_end = datetime.strptime(str(datetime.now().date()) + '3:30',"%Y-%m-%d%H:%M")
        while now > time_end or now < time_begin:
            dealReqs()                                      # deal with the reqs in the waiting time
            time.sleep(5)                                   # avoid the cpu from circling all the time
            now = datetime.now()
        '''
        allStu = getAllStu()
        if allStu == -1:
            continue
        for j in range(len(allStu)):                        # flush all the students' datas
            usr = allStu[j]['usr_name']
            pw = decrypt_string(allStu[j]['usr_password'])
            curDataReq = DataReq(usr, pw)
            if j == 0:
                success = 0
                i = 0
                while success != 1 and i < 3:
                    #success = reqEmptyClassroom(curDataReq)           # empty classroom checked once
                    i += 1
            #dealReqs()
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqSchedule(curDataReq)          
                i += 1
            #dealReqs()
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqGrades(curDataReq)          
                i += 1          
            #dealReqs()
        print('本轮循环完成，进入待机状态')
        while True:
            afterProc = datetime.now()                      # get the cur time
            deltatime = afterProc - now
            seconds = deltatime.total_seconds()
            limitTime = 60 * 60 * 24
            if seconds >= limitTime:                        # will not flush the datas until 24h later
                break
            #dealReqs()                                     # deal with the reqs in the waiting time
            time.sleep(10)                                  # avoid the cpu from circling all the time

def insect_ddl():
    '''
    the main func
    circle and circle again to get the ddl datas
    '''
    print('爬虫部署成功！')
    print('将进行ddl的获取，刷新间隔极少，为60s')
    while True:
        print('开始新一轮循环')
        allStu = getAllStu()
        if allStu == -1:
            continue
        for j in range(len(allStu)):                        # flush all the students' datas
            usr = allStu[j]['usr_name']
            pw = decrypt_string(allStu[j]['usr_password'])
            curDataReq = DataReq(usr, pw)
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = reqDdl(curDataReq)           
                i += 1  
            time.sleep(1)    
        print('本轮循环结束，将进行60s待机')
        time.sleep(60)        

def insect_req():
    '''
    the main func
    circle and circle again to get the req datas
    '''
    print('爬虫部署成功！')
    print('将进行消息队列的获取与处理')
    while True:
        print('开始新一轮循环')
        success = dealReqs()
        if success == 1:
            print('处理成功')
        elif success == 0:
            print('暂时没有req存在')
        else:
            print('处理出现问题，错误码为：' + str(success))
        print('本轮循环结束，将进行5s待机')
        time.sleep(5)  

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
    #testTime()                                 # test the average cost time
    if len(sys.argv) < 2:
        print('请输入参数，-d：启动ddl爬虫，-o：启动其他爬虫, -r：启动消息队列')
    elif len(sys.argv) > 2:
        print('输入参数过多')
    elif sys.argv[1] == '-d':                     # get the ddl data
        try:
            insect_ddl()
        except Exception as e:
            print(traceback.format_exc())
            insect_ddl()
    elif sys.argv[1] == '-o':                   # get the schedule, grade and emptyclassroom(current can not do that) data
        try:
            insect_other()
        except Exception as e:
            print(traceback.format_exc())
            insect_other()
    elif sys.argv[1] == '-r':                   # get the schedule, grade and emptyclassroom(current can not do that) data
        try:
            insect_req()
        except Exception as e:
            print(traceback.format_exc())
            insect_req()
    else:
        print('请输入正确参数，-d：启动ddl爬虫，-o：启动其他爬虫, -r：启动消息队列')