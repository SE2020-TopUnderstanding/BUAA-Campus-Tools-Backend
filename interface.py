import traceback
import sys
import json
import time
from datetime import datetime
import requests
from data import DataReq
from password_utils import Aescrypt, KEY, MODEL, ENCODE_

HOST = 'http://114.115.208.32:8000/'
HEADERS = {'Content-Type': 'application/json'}


def decrypt_string(message):
    script = Aescrypt(KEY, MODEL, '', ENCODE_)
    decode_result = script.aesdecrypt(message)
    return decode_result


def encrypt_string(message):
    script = Aescrypt(KEY, MODEL, '', ENCODE_)
    en_text = script.aesencrypt(message)
    return en_text


def send_error(error_id, usr, passw):
    encode_result = encrypt_string(passw)
    url = HOST + 'delete/'
    jsons = {'usr_name': usr, 'password': encode_result}
    jsons = json.dumps(jsons, ensure_ascii=False)      # 获取json包
    print('send error ' + str(error_id))
    # noinspection PyBroadException
    try:
        requests.post(url=url, headers=HEADERS, data=jsons.encode('utf-8'))
    except Exception:
        print('send error req fail')
        print(traceback.format_exc())
        return 0
    return 1


def get_all_stu(insect_id):
    """
    获取所有需要爬取的学生的账号密码
    返回 jsons -> 成功
    返回 -1 -> 请求失败
    """
    url = HOST + 'login/'
    params = {'password': '123', 'number': insect_id}
    # noinspection PyBroadException
    try:
        req = requests.get(url, verify=False, params=params)
    except Exception:
        print('req fail')
        return -1
    jsons = req.json()
    return jsons


def req_schedule(data_req):
    """
    获取学生课表并post给后端
    返回  1 -> 成功
    返回  0 -> 网络错误
    返回 -5 -> post错误
    返回 -6 -> ip被封
    返回 -7 -> 用户名错误或者网站要求输入验证码
    返回 -8 -> 密码错误
    返回 -9 -> 用户名或密码为空
    返回-10 -> 账号被锁
    """
    schedule = data_req.request('s')
    # 错误处理
    if schedule == -1:
        print('usr_name or password is wrong\n')
        return 0
    if schedule == -2:
        print('there is something wrong on network\n')
        return 0
    if schedule == -3:
        print('unknown errors\n')
        return 0
    if schedule == -4:
        print('error on the jiaowu web\n')
        return 0
    if schedule == -5:
        return -6
    if schedule in (-6, -7, -8, -9):
        return schedule - 1
    schedule_url = HOST + 'timetable/'
    # noinspection PyBroadException
    try:
        requests.post(url=schedule_url, headers=HEADERS, data=schedule.encode('utf-8'))
    except Exception:
        print('req fail')
        print(traceback.format_exc())
        return -5
    return 1


def req_grades(data_req):
    """
    获取学生成绩并post给后端
    返回  1 -> 成功
    返回  0 -> 网络错误
    返回 -5 -> post错误
    返回 -6 -> ip被封
    返回 -7 -> 用户名错误或者网站要求输入验证码
    返回 -8 -> 密码错误
    返回 -9 -> 用户名或密码为空
    返回-10 -> 账号被锁
    """
    grades = data_req.request('g')
    # 错误处理
    if grades == -1:
        print('usr_name or password is wrong\n')
        return 0
    if grades == -2:
        print('there is something wrong on network\n')
        return 0
    if grades == -3:
        print('unknown errors\n')
        return 0
    if grades == -4:
        print('error on the jiaowu web\n')
        return 0
    if grades == -5:
        return -6
    if grades in (-6, -7, -8, -9):
        return grades - 1
    grades_url = HOST + 'score/'
    for each in grades:
        # noinspection PyBroadException
        try:
            requests.post(url=grades_url, headers=HEADERS, data=each.encode('utf-8'))
        except Exception:
            print('req fail')
            print(traceback.format_exc())
            return -5
    return 1


def req_ddl(data_req):
    """
    获取学生ddl信息并post给后端
    返回  1 -> 成功
    返回  0 -> 网络错误
    返回 -5 -> post错误
    返回 -6 -> ip被封
    返回 -7 -> 用户名错误或者网站要求输入验证码
    返回 -8 -> 密码错误
    返回 -9 -> 用户名或密码为空
    返回-10 -> 账号被锁
    """
    ddl = data_req.request('d')
    # 错误处理
    if ddl == -1:
        print('usr_name or password is wrong\n')
        return 0
    if ddl == -2:
        print('there is something wrong on network\n')
        return 0
    if ddl == -3:
        print('unknown errors\n')
        return 0
    if ddl == -4:
        print('error on the course web\n')
        return 0
    if ddl == -5:
        return -6
    if ddl in (-6, -7, -8, -9):
        return ddl - 1
    ddl_url = HOST + 'ddl/'
    # noinspection PyBroadException
    try:
        requests.post(url=ddl_url, headers=HEADERS, data=ddl.encode('utf-8'))
        # ddlUrl = ddlUrl
    except Exception:
        print('req fail')
        print(traceback.format_exc())
        return -5
    return 1


def req_empty_classroom(data_req):
    """
    获取空教室信息并post给后端
    返回  1 -> 成功
    返回  0 -> 网络错误
    返回 -5 -> post错误
    返回 -6 -> ip被封
    返回 -7 -> 用户名错误或者网站要求输入验证码
    返回 -8 -> 密码错误
    返回 -9 -> 用户名或密码为空
    返回-10 -> 账号被锁
    """
    empty_classroom = data_req.request('e')
    # 错误处理
    if empty_classroom == -1:
        print('usr_name or password is wrong\n')
        return 0
    if empty_classroom == -2:
        print('there is something wrong on network\n')
        return 0
    if empty_classroom == -3:
        print('unknown errors\n')
        return 0
    if empty_classroom == -4:
        print('error on the jiaowu web\n')
        return 0
    if empty_classroom == -5:
        return -6
    if empty_classroom in (-6, -7, -8, -9):
        return empty_classroom - 1
    empty_classroom_url = HOST + 'classroom/'
    for each in empty_classroom:
        return_json = json.dumps(each, ensure_ascii=False)
        # noinspection PyBroadException
        try:
            requests.post(url=empty_classroom_url, headers=HEADERS, data=return_json.encode('utf-8'))
        except Exception:
            print(traceback.format_exc())
            print('req fail')
            return -5
    return 1


def deal_reqs():
    """
    处理后端发来的临时请求
    返回 1 -> 成功
    返回 0 -> 当前不存在临时请求
    返回 -1 -> 失败
    返回 -2 -> 暂时不支持空教室请求
    返回 -5 -> 与后端的get失败
    返回 -6 -> 与后端的post失败
    返回 -7 -> IP被封
    返回 -8 -> 用户名错误或者网站要求输入验证码
    返回 -9 -> 密码错误
    返回-10 -> 用户名或密码为空
    返回-11 -> 账号被锁
    """
    ask_url = HOST + 'request/'
    # noinspection PyBroadException
    try:
        req = requests.get(ask_url)
    except Exception:
        print('req get fail')
        return -5

    if req.status_code == 204:                  # if there is not any reqs
        return 0

    # 错误处理
    jsons = req.json()
    data = jsons
    user = data['usr_name']
    passw = decrypt_string(data['password'])
    req_type = data['req_type']
    data_req = DataReq(user, passw)
    success = 0
    return_id = 1
    if req_type == 's':
        i = 0
        while success != 1 and i < 3:
            success = req_schedule(data_req)
            if success == -6:
                return_id = -7
            if success in (-7, -8, -10):
                send_error(success, user, passw)
                return success - 1
            i += 1
    if req_type == 'g':
        i = 0
        while success != 1 and i < 3:
            success = req_grades(data_req)
            if success == -6:
                return_id = -7
            if success in (-7, -8, -10):
                send_error(success, user, passw)
                return success - 1
            i += 1
    if req_type == 'd':
        i = 0
        while success != 1 and i < 3:
            success = req_ddl(data_req)
            if success == -6:
                return_id = -7
            if success in (-7, -8, -10):
                send_error(success, user, passw)
                return success - 1
            i += 1

    # 空教室查询花费时间过长
    # 暂时不支持这种情况

    if req_type == 'e':
        # reqEmptyClassroom(dataReq)
        return -2
    if success == 0:
        return_id = -1
    # noinspection PyBroadException
    try:
        if return_id < 0:
            jsons = json.dumps(jsons, ensure_ascii=False)
            requests.post(url=ask_url, headers=HEADERS, data=jsons.encode('utf-8'))
        else:
            new_json = {'req_id': jsons['req_id']}
            jsons = json.dumps(new_json, ensure_ascii=False)
            requests.post(url=ask_url, headers=HEADERS, data=jsons.encode('utf-8'))
    except Exception:
        print('req post fail')
        print(traceback.format_exc())
        return -6
    return return_id


def insect_other(insect_id):
    """
    循环获取课表、成绩（空教室）信息
    """
    print('爬虫部署成功！')
    print('将进行课表、成绩、空教室的查询')
    while True:
        print('开始新一轮循环')
        now = datetime.now()                                # 获取当前时间

        all_stu = get_all_stu(insect_id)
        if all_stu == -1:
            continue
        for j in range(len(all_stu)):                        # 刷新学生信息
            usr = all_stu[j]['usr_name']
            passw = decrypt_string(all_stu[j]['usr_password'])
            cur_data_req = DataReq(usr, passw)
            if j == 0:
                success = 0
                i = 0
                while success != 1 and i < 3:
                    # success = reqEmptyClassroom(curDataReq) # 空教室只查询一次
                    if success == -6:
                        time.sleep(630)                     # ip被封, 等待10分钟
                    i += 1
            # dealReqs()
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = req_schedule(cur_data_req)
                if success == -6:
                    time.sleep(630)                        # ip被封, 等待10分钟
                if success in (-7, -8, -10):
                    send_error(success, usr, passw)
                    break
                i += 1
            if success in (-7, -8, -10):
                continue
            # dealReqs()
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = req_grades(cur_data_req)
                if success == -6:
                    time.sleep(630)                        # ip被封, 等待10分钟
                if success in (-7, -8, -10):
                    send_error(success, usr, passw)
                    break
                i += 1
            if success in (-7, -8, -10):
                continue
            # dealReqs()
        print('本轮循环完成，进入待机状态')
        while True:
            after_proc = datetime.now()                      # 获取当前时间
            deltatime = after_proc - now
            seconds = deltatime.total_seconds()
            limit_time = 60 * 60 * 24
            if seconds >= limit_time:                        # 24小时后重新开始循环
                break
            # dealReqs()
            time.sleep(10)                                  # 防止轮询占用大量cpu资源


def insect_ddl(insect_id):
    """
    循环获取ddl信息
    """
    print('爬虫部署成功！')
    print('将进行ddl的获取，刷新间隔极少，为60s')
    while True:
        print('开始新一轮循环')
        all_stu = get_all_stu(insect_id)
        if all_stu == -1:
            continue
        for j in range(len(all_stu)):                        # 刷新学生信息
            print('当前总人数：' + str(len(all_stu)))
            print('当前爬取学生序号：' + str(j + 1))
            usr = all_stu[j]['usr_name']
            passw = decrypt_string(all_stu[j]['usr_password'])
            cur_data_req = DataReq(usr, passw)
            success = 0
            i = 0
            while success != 1 and i < 3:
                success = req_ddl(cur_data_req)
                if success == -6:
                    time.sleep(630)                        # ip被封, 等待10分钟
                if success in (-7, -8, -10):
                    send_error(success, usr, passw)
                    break
                i += 1
            time.sleep(1)
        print('本轮循环结束，将进行60s待机')
        time.sleep(60)


def insect_req():
    """
    循环执行后端发出的临时请求
    """
    print('爬虫部署成功！')
    print('将进行消息队列的获取与处理')
    while True:
        print('开始新一轮循环')
        success = deal_reqs()
        if success == -7:
            time.sleep(630)                     # ip被封, 等待10分钟
        if success == 1:
            print('处理成功')
        elif success == 0:
            print('暂时没有req存在')
        else:
            print('处理出现问题，错误码为：' + str(success))
        print('本轮循环结束，将进行5s待机')
        time.sleep(5)


def test_time():
    """
    计算耗时
    结果:
    空教室查询: 0:20:41.309
    课表查询: 0:00:28.732
    成绩查询: 0.00.55.983
    ddl查询: 0.00.52.933
    """
    usr = input('user: ')
    passw = input('password: ')
    cur_data_req = DataReq(usr, passw)
    now = datetime.now()
    req_empty_classroom(cur_data_req)
    enow = datetime.now()
    req_schedule(cur_data_req)
    snow = datetime.now()
    req_grades(cur_data_req)
    gnow = datetime.now()
    req_ddl(cur_data_req)
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


# 程序开始执行
if __name__ == '__main__':
    # testTime()                                 # 计算耗时
    if len(sys.argv) != 3:
        print('请输入正确参数，-d 整数：启动ddl爬虫，-o 整数：启动其他爬虫, -r 整数：启动消息队列')
    elif sys.argv[1] == '-d':                     # 获取ddl信息
        while True:
            # noinspection PyBroadException
            try:
                insect_ddl(int(sys.argv[2]))
            except Exception as err:
                print(traceback.format_exc())
    elif sys.argv[1] == '-o':                   # 获取课表和成绩信息
        while True:
            # noinspection PyBroadException
            try:
                insect_other(int(sys.argv[2]))
            except Exception as err:
                print(traceback.format_exc())
    elif sys.argv[1] == '-r':                   # 处理后端的临时请求
        while True:
            # noinspection PyBroadException
            try:
                insect_req()
            except Exception as err:
                print(traceback.format_exc())
    else:
        print('请输入正确参数，-d：启动ddl爬虫，-o：启动其他爬虫, -r 整数：启动消息队列')
