import traceback
import sys
import json
import time
from datetime import datetime
import requests
from data import DataReq
from password_utils import Aescrypt, KEY, MODEL, ENCODE_, SERVER_PW
from log import Log

HOST = 'http://hangxu.sharinka.top:8000/'
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
    url = HOST + 'spider/delete/'
    if error_id == -7:
        error_type = 1
    else:
        error_type = 0
    err_json = {'usr_name': usr, 'password': encode_result, 'error_type': error_type}
    err_json = json.dumps(err_json, ensure_ascii=False)      # 获取json包
    print('send error ' + str(error_id))
    # noinspection PyBroadException
    try:
        req = requests.post(url=url, headers=HEADERS, data=err_json.encode('utf-8'))
        req.raise_for_status()
    except Exception:
        print('send error req fail')
        print(traceback.format_exc())
        return 0
    return 1


def get_all_stu(insect_id):
    """
    获取所有需要爬取的学生的账号密码
    返回 stu_json -> 成功
    返回 -1 -> 请求失败
    """
    url = HOST + 'login/'
    if insect_id == -1:
        params = {'password': SERVER_PW}
    else:
        params = {'password': SERVER_PW, 'number': insect_id}
    # noinspection PyBroadException
    try:
        req = requests.get(url, verify=False, params=params)
    except Exception:
        print('req fail')
        return -1
    stu_json = req.json()
    return stu_json


def req_jiaowu_msg(data_req):
    """
    获取学生课表以及成绩并post给后端
    返回 =  1 : 成功
    返回 =  0 : 登录被拒绝，错误信息已传至log
    返回 = -1 : 访问超时
    返回 = -2 : 访问失败，网络可能存在问题
    返回 = -3 : IP被封
    返回 = -4 : 用户名错误或者网站要求输入验证码
    返回 = -5 : 密码错误
    返回 = -6 : 用户名或密码为空
    返回 = -7 : 账号被锁
    返回 = -8 : 服务器请求出错
    """
    grades, schedule = data_req.request('j')

    if schedule == '':
        print('无效代码')

    # 错误处理
    if grades == -1:
        print('登录被拒绝，错误信息已传至log\n')
        return 0
    if grades in (0, -4):
        print('访问超时')
        return -1
    if grades in (-2, -3, -5, -11, -12):
        print('访问失败，网络可能存在问题')
        return -2
    if grades in (-6, -7, -8, -9, -10):
        return grades + 3

    # 暂时关闭课程爬取
    # """
    # schedule_url = HOST + 'timetable/'
    # noinspection PyBroadException
    # try:
    #     req = requests.post(url=schedule_url, headers=HEADERS, data=schedule.encode('utf-8'))
    #     req.raise_for_status()
    # except Exception:
    #     print('req fail')
    #     print(traceback.format_exc())
    #     return -8
    # """
    grades_url = HOST + 'score/'
    for each in grades:
        # noinspection PyBroadException
        try:
            req = requests.post(url=grades_url, headers=HEADERS, data=each.encode('utf-8'))
            req.raise_for_status()
        except Exception:
            print('req fail')
            print(traceback.format_exc())
            return -8
    return 1


def req_ddl(data_req):
    """
    获取学生ddl信息并post给后端
    返回 =  1 : 成功
    返回 =  0 : 登录被拒绝，错误信息已传至log
    返回 = -1 : 访问超时
    返回 = -2 : 访问失败，网络可能存在问题
    返回 = -3 : IP被封
    返回 = -4 : 用户名错误或者网站要求输入验证码
    返回 = -5 : 密码错误
    返回 = -6 : 用户名或密码为空
    返回 = -7 : 账号被锁
    返回 = -8 : 服务器请求出错
    """
    ddl = data_req.request('d')[0]

    # 错误处理
    if ddl == -1:
        print('登录被拒绝，错误信息已传至log\n')
        return 0
    if ddl in (0, -4):
        print('访问超时')
        return -1
    if ddl in (-2, -3, -5, -11, -12):
        print('访问失败，网络可能存在问题')
        return -2
    if ddl in (-6, -7, -8, -9, -10):
        return ddl + 3

    ddl_url = HOST + 'ddl/'
    # noinspection PyBroadException
    try:
        req = requests.post(url=ddl_url, headers=HEADERS, data=ddl.encode('utf-8'))
        req.raise_for_status()
    except Exception:
        print('req fail')
        print(traceback.format_exc())
        return -8
    return 1


def req_lessons(data_req):
    """
    获取学生已选课程信息并post给后端
    返回 =  1 : 成功
    返回 =  0 : 登录被拒绝，错误信息已传至log
    返回 = -1 : 访问超时
    返回 = -2 : 访问失败，网络可能存在问题
    返回 = -3 : IP被封
    返回 = -4 : 用户名错误或者网站要求输入验证码
    返回 = -5 : 密码错误
    返回 = -6 : 用户名或密码为空
    返回 = -7 : 账号被锁
    返回 = -8 : 服务器请求出错
    """
    lessons = data_req.request('l')[0]

    # 错误处理
    if lessons == -1:
        print('登录被拒绝，错误信息已传至log\n')
        return 0
    if lessons in (0, -4):
        print('访问超时')
        return -1
    if lessons in (-2, -3, -5, -11, -12):
        print('访问失败，网络可能存在问题')
        return -2
    if lessons in (-6, -7, -8, -9, -10):
        return lessons + 3

    lessons_url = HOST + 'timetable/add_course/'
    # noinspection PyBroadException
    try:
        req = requests.post(url=lessons_url, headers=HEADERS, data=lessons.encode('utf-8'))
        req.raise_for_status()
    except Exception:
        print('req fail')
        print(traceback.format_exc())
        return -8
    return 1


def req_empty_classroom(data_req):
    """
    获取空教室信息并post给后端
    返回 =  1 : 成功
    返回 =  0 : 登录被拒绝，错误信息已传至log
    返回 = -1 : 访问超时
    返回 = -2 : 访问失败，网络可能存在问题
    返回 = -3 : IP被封
    返回 = -4 : 用户名错误或者网站要求输入验证码
    返回 = -5 : 密码错误
    返回 = -6 : 用户名或密码为空
    返回 = -7 : 账号被锁
    返回 = -8 : 服务器请求出错
    """
    empty_classroom = data_req.request('e')[0]

    # 错误处理
    if empty_classroom == -1:
        print('登录被拒绝，错误信息已传至log\n')
        return 0
    if empty_classroom in (0, -4):
        print('访问超时')
        return -1
    if empty_classroom in (-2, -3, -5, -11, -12):
        print('访问失败，网络可能存在问题')
        return -2
    if empty_classroom in (-6, -7, -8, -9, -10):
        return empty_classroom + 3

    empty_classroom_url = HOST + 'classroom/'
    for each in empty_classroom:
        return_json = json.dumps(each, ensure_ascii=False)
        # noinspection PyBroadException
        try:
            req = requests.post(url=empty_classroom_url, headers=HEADERS, data=return_json.encode('utf-8'))
            req.raise_for_status()
        except Exception:
            print(traceback.format_exc())
            print('req fail')
            return -8
    return 1


def deal_reqs():
    """
    处理后端发来的临时请求
    返回   1 -> 成功
    返回   0 -> 当前不存在临时请求
    返回  -1 -> 登录被拒绝，错误信息已传至log
    返回  -2 -> 访问超时
    返回  -3 -> 访问失败，网络可能存在问题
    返回  -4 -> 服务器请求出错
    返回  -5 -> 与后端的get失败
    返回  -6 -> 与后端的post失败
    返回  -7 -> IP被封
    返回  -8 -> 用户名错误或者网站要求输入验证码
    返回  -9 -> 密码错误
    返回 -10 -> 用户名或密码为空
    返回 -11 -> 账号被锁
    返回 -12 -> 请求的格式错误
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
    return_id = -12
    if req_type == 'l':
        i = 0
        while success != 1 and i < 3:
            success = req_lessons(data_req)
            if success == -3:
                return_id = -7
                break
            if success in (-4, -5, -6, -7):
                send_error(success, user, passw)
                return success - 4
            if success in (0, -1, -2):
                return_id = success - 1
            if success == -8:
                return_id = -4
            if success == 1:
                return_id = 1
            i += 1
    if req_type == 'j':
        i = 0
        while success != 1 and i < 3:
            success = req_jiaowu_msg(data_req)
            if success == -3:
                return_id = -7
                break
            if success in (-4, -5, -6, -7):
                send_error(success, user, passw)
                return success - 4
            if success in (0, -1, -2):
                return_id = success - 1
            if success == -8:
                return_id = -4
            if success == 1:
                return_id = 1
            i += 1
    if req_type == 'd':
        i = 0
        while success != 1 and i < 3:
            success = req_ddl(data_req)
            if success == -3:
                return_id = -7
                break
            if success in (-4, -5, -6, -7):
                send_error(success, user, passw)
                return success - 4
            if success in (0, -1, -2):
                return_id = success - 1
            if success == -8:
                return_id = -4
            if success == 1:
                return_id = 1
            i += 1

    # 空教室查询花费时间过长
    # 不支持这种情况

    # noinspection PyBroadException
    try:
        if return_id < 0:
            jsons = json.dumps(jsons, ensure_ascii=False)
            req = requests.post(url=ask_url, headers=HEADERS, data=jsons.encode('utf-8'))
            req.raise_for_status()
        else:
            new_json = {'req_id': jsons['req_id']}
            jsons = json.dumps(new_json, ensure_ascii=False)
            req = requests.post(url=ask_url, headers=HEADERS, data=jsons.encode('utf-8'))
            req.raise_for_status()
    except Exception:
        print('req post fail')
        print(traceback.format_exc())
        return -6
    return return_id


def insect_jiaowu(insect_id):
    """
    循环获取课表、成绩信息
    """
    print('爬虫部署成功！')
    print('将进行课表、成绩的查询')
    while True:
        print('开始新一轮循环')
        now = datetime.now()                                # 获取当前时间

        all_stu = get_all_stu(insect_id)
        if all_stu == -1:
            print('请求学生信息失败')
            time.sleep(5)
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
                success = req_jiaowu_msg(cur_data_req)
                if success == -3:
                    time.sleep(630)                        # ip被封, 等待10分钟
                if success in (-4, -5, -6, -7):
                    send_error(success, usr, passw)
                    break
                i += 1

        print('本轮循环完成，进入待机状态')
        while True:
            after_proc = datetime.now()                      # 获取当前时间
            deltatime = after_proc - now
            seconds = deltatime.total_seconds()
            # limit_time = 60 * 60 * 24
            limit_time = 60
            if seconds >= limit_time:                        # 24小时后重新开始循环，暂时改为1分钟
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
            print('请求学生信息失败')
            time.sleep(5)
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
                if success == -3:
                    time.sleep(630)                        # ip被封, 等待10分钟
                if success in (-4, -5, -6, -7):
                    send_error(success, usr, passw)
                    break
                i += 1
            time.sleep(1)
        print('本轮循环结束，将进行60s待机')
        time.sleep(60)


def insect_all_lessons():
    """
    获取已选课程信息
    返回请求失败的用户名的列表
    """
    print('爬虫部署成功！')
    print('将进行已选课程信息的获取')

    all_stu = get_all_stu(-1)
    failed = []
    if all_stu == -1:
        print('请求学生信息失败')
        return 0
    for j in range(len(all_stu)):  # 刷新学生信息
        print('当前总人数：' + str(len(all_stu)))
        print('当前爬取学生序号：' + str(j + 1))
        usr = all_stu[j]['usr_name']
        passw = decrypt_string(all_stu[j]['usr_password'])
        cur_data_req = DataReq(usr, passw)

        success = 0
        i = 0
        while success != 1 and i < 3:
            success = req_lessons(cur_data_req)
            if success == -3:
                time.sleep(630)  # ip被封, 等待10分钟
            if success in (-4, -5, -6, -7):
                send_error(success, usr, passw)
                break
            i += 1
        if success != 1:
            failed.append(usr)
    if len(failed) != 0:
        print('爬取失败的用户名如下：')
        print(failed)
    return failed


def insect_empty_classroom():
    """
    获取空教室信息
    成功返回：True
    失败返回：False
    """
    print('爬虫部署成功！')
    print('将进行空教室信息的获取')
    all_stu = get_all_stu(-1)
    failed = False
    if all_stu == -1:
        print('请求学生信息失败')
        return 0
    for j in range(len(all_stu)):  # 刷新学生信息
        print('当前总人数：' + str(len(all_stu)))
        print('当前爬取学生序号：' + str(j + 1))
        usr = all_stu[j]['usr_name']
        passw = decrypt_string(all_stu[j]['usr_password'])
        cur_data_req = DataReq(usr, passw)

        success = 0
        i = 0
        while success != 1 and i < 3:
            success = req_empty_classroom(cur_data_req)
            if success == -3:
                time.sleep(630)  # ip被封, 等待10分钟
            if success in (-4, -5, -6, -7):
                send_error(success, usr, passw)
                break
            i += 1
        if success == 1:
            print('爬取成功，爬虫退出')
            return True
    return failed


def insect_req():
    """
    循环执行后端发出的临时请求
    错误码  -1 -> 登录被拒绝，错误信息已传至log
    错误码  -2 -> 访问超时
    错误码  -3 -> 访问失败，网络可能存在问题
    错误码  -4 -> 服务器请求出错
    错误码  -5 -> 与后端的get失败
    错误码  -6 -> 与后端的post失败
    错误码  -7 -> IP被封
    错误码  -8 -> 用户名错误或者网站要求输入验证码
    错误码  -9 -> 密码错误
    错误码 -10 -> 用户名或密码为空
    错误码 -11 -> 账号被锁
    错误码 -12 -> 请求的格式错误
    """
    print('爬虫部署成功！')
    print('将进行消息队列的获取与处理')
    while True:
        success = deal_reqs()
        if success == -7:
            time.sleep(630)                     # ip被封, 等待10分钟
        if success == 1:
            print('处理成功')
        elif success == 0:
            print('暂时没有req存在')
        else:
            print('处理出现问题，错误码为：' + str(success))
        time.sleep(5)


def test_time():
    """
    计算耗时
    结果:
    alpha版本如下：
    空教室查询: 0:20:41.309
    课表查询: 0:00:28.732
    成绩查询: 0.00.55.983
    ddl查询: 0.00.52.933
    beta版本
    空教室查询: 0:07:47.332
    课表成绩查询: 0:00:14.684
    已选课程查询: 0.00.15.285 (尚未完成老师补全)
    ddl查询: 0.00.34.670
    """
    usr = input('user: ')
    passw = input('password: ')
    cur_data_req = DataReq(usr, passw)
    start_now = datetime.now()
    req_empty_classroom(cur_data_req)
    empty_now = datetime.now()
    req_lessons(cur_data_req)
    lesson_now = datetime.now()
    req_jiaowu_msg(cur_data_req)
    jiaowu_now = datetime.now()
    req_ddl(cur_data_req)
    ddl_now = datetime.now()
    deltatime = empty_now - start_now
    print('空教室查询耗费时间: ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = lesson_now - empty_now
    print('已选课表查询耗费时间: ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = jiaowu_now - lesson_now
    print('课表成绩查询耗费时间: ' + str(deltatime.total_seconds()))
    print(deltatime)
    deltatime = ddl_now - jiaowu_now
    print('ddl查询耗费时间: ' + str(deltatime.total_seconds()))
    print(deltatime)


# 程序开始执行
if __name__ == '__main__':
    # testTime()                                 # 计算耗时
    if len(sys.argv) != 3:
        print('请输入正确参数')
    elif sys.argv[1] == '-d':                     # 获取ddl信息
        while True:
            # noinspection PyBroadException
            try:
                insect_ddl(int(sys.argv[2]))
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    elif sys.argv[1] == '-j':                   # 获取课表和成绩信息
        while True:
            # noinspection PyBroadException
            try:
                insect_jiaowu(int(sys.argv[2]))
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    elif sys.argv[1] == '-l':                   # 处理后端的临时请求
        while True:
            # noinspection PyBroadException
            try:
                insect_all_lessons()
                break
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    elif sys.argv[1] == '-e':                   # 处理后端的临时请求
        while True:
            # noinspection PyBroadException
            try:
                insect_empty_classroom()
                break
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    elif sys.argv[1] == '-r':                   # 处理后端的临时请求
        while True:
            # noinspection PyBroadException
            try:
                insect_req()
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    elif sys.argv[1] == '-t':                   # 处理后端的临时请求
        while True:
            # noinspection PyBroadException
            try:
                test_time()
                break
            except Exception as err:
                print(traceback.format_exc())
                Log('运行过程中出现问题，错误信息: ' + traceback.format_exc())
    else:
        print('请输入正确参数')
