import traceback
import json
from datetime import datetime, timedelta
from jiaowu import JiaoWuReq
from course import CourseRequest
from password_utils import Aescrypt, KEY, MODEL, ENCODE_


def encrypt_string(message):
    script = Aescrypt(KEY, MODEL, '', ENCODE_)
    en_text = script.aesencrypt(message)
    return en_text


class DataReq:
    """
    这个类对爬取的数据进行处理
    """
    def __init__(self, user_name, pw):
        self.usr_name = user_name
        self.password = pw

    def request(self, request_type):
        """
        获取所有的查询请求
        爬取信息
        请求格式: {'d':'ddl查询', 'g':'成绩查询', 'e':'空教室查询', 's':'课表查询'}
        """
        print('start to get the data, usr_name: ' + self.usr_name)
        print('requestType: ' + request_type)

        if request_type == 'd':
            get_stu_id = CourseRequest(self.usr_name, self.password)      # 获取该学生的学号
            stu_id = get_stu_id.get_id()
        else:
            get_stu_id = JiaoWuReq(self.usr_name, self.password)          # 获取该学生的学号
            stu_id = get_stu_id.get_id()
        print('studentId: ' + str(stu_id))
        get_stu_id.quit()

        if stu_id == -5:
            print('something wrong')
            print('IP is banned')
            return stu_id
        if stu_id in (-1, -2, -3, -4, ''):                                # 如果出现错误
            print('something wrong')
            print('usr_name: ' + self.usr_name)
            print('requestType: ' + 'getStuId')
            return stu_id
        if stu_id == -6:
            print('something wrong')
            print('usr_name is wrong or there is a CAPTCHA')
            return stu_id
        if stu_id == -7:
            print('something wrong')
            print('password is wrong')
            return stu_id
        if stu_id == -8:
            print('something wrong')
            print('usr_name or password is empty')
            return stu_id
        if stu_id == -9:
            print('something wrong')
            print('account is locked')
            return stu_id
        stu_id = encrypt_string(stu_id)
        if request_type == 'd':                                          # 获取ddl信息
            course = CourseRequest(self.usr_name, self.password)
            ddls = course.get_ddl()
            course.quit()
            if ddls in (-1, -2, -3, -4):    # 如果出现错误
                print('something wrong')
                print('usr_name: ' + self.usr_name)
                print('requestType: ddl')
                return ddls
            if ddls == -5:
                print('something wrong')
                print('IP is banned')
                return ddls
            if ddls == -6:
                print('something wrong')
                print('usr_name is wrong or there is a CAPTCHA')
                return ddls
            if ddls == -7:
                print('something wrong')
                print('password is wrong')
                return ddls
            if ddls == -8:
                print('something wrong')
                print('usr_name or password is empty')
                return ddls
            if ddls == -9:
                print('something wrong')
                print('account is locked')
                return ddls
            if ddls == -10:
                ddls = {'student_id': stu_id}
                wrong_list = []
                wrong_dict = {}
                message = '抱歉，我们暂时无法获取您的ddl信息。\n为解决此问题，请在课程中心的用户偏好标签页面保证您所需' \
                          '爬取的课程都属于收藏站点或活跃站点，并且活跃站点不要为空'
                content = []
                content_dict = {'ddl': '',
                                'homework': message,
                                'state': '错误'}
                content.append(content_dict)
                wrong_dict['name'] = '错误'
                wrong_dict['content'] = content
                wrong_list.append(wrong_dict)
                ddls['ddl'] = wrong_list
                ddls = json.dumps(ddls, ensure_ascii=False)            # 使用json打包
                return ddls
            return self.deal_with_ddl(ddls, stu_id)
        if request_type == 'g':                                        # 获取成绩信息
            jiaowu = JiaoWuReq(self.usr_name, self.password)
            grades = jiaowu.get_grade()
            jiaowu.quit()
            if grades in (-1, -2, -3, -4):
                print('something wrong')
                print('usr_name: ' + self.usr_name)
                print('requestType: grades')
                return grades
            if grades == -5:
                print('something wrong')
                print('IP is banned')
                return grades
            if grades == -6:
                print('something wrong')
                print('usr_name is wrong or there is a CAPTCHA')
                return grades
            if grades == -7:
                print('something wrong')
                print('password is wrong')
                return grades
            if grades == -8:
                print('something wrong')
                print('usr_name or password is empty')
                return grades
            if grades == -9:
                print('something wrong')
                print('account is locked')
                return grades
            return self.deal_with_grades(grades, stu_id)
        if request_type == 'e':                                        # 获取空教室信息
            jiaowu = JiaoWuReq(self.usr_name, self.password)
            empty_classroom = jiaowu.get_empty_classroom()
            jiaowu.quit()
            if empty_classroom in (-1, -2, -3, -4):
                print('something wrong')
                print('usr_name: ' + self.usr_name)
                print('requestType: empty calssroom')
                return empty_classroom
            if empty_classroom == -5:
                print('something wrong')
                print('IP is banned')
                return empty_classroom
            if empty_classroom == -6:
                print('something wrong')
                print('usr_name is wrong or there is a CAPTCHA')
                return empty_classroom
            if empty_classroom == -7:
                print('something wrong')
                print('password is wrong')
                return empty_classroom
            if empty_classroom == -8:
                print('something wrong')
                print('usr_name or password is empty')
                return empty_classroom
            if empty_classroom == -9:
                print('something wrong')
                print('account is locked')
                return empty_classroom
            return self.deal_with_empty_classroom(empty_classroom)
        if request_type == 's':                                        # 获取课表信息
            jiaowu = JiaoWuReq(self.usr_name, self.password)
            schedules = jiaowu.get_schedule()
            jiaowu.quit()
            if schedules in (-1, -2, -3, -4):
                print('something wrong')
                print('usr_name: ' + self.usr_name)
                print('requestType: schedule')
                return schedules
            if schedules == -5:
                print('something wrong')
                print('IP is banned')
                return schedules
            if schedules == -6:
                print('something wrong')
                print('usr_name is wrong or there is a CAPTCHA')
                return schedules
            if schedules == -7:
                print('something wrong')
                print('password is wrong')
                return schedules
            if schedules == -8:
                print('something wrong')
                print('usr_name or password is empty')
                return schedules
            if schedules == -9:
                print('something wrong')
                print('account is locked')
                return schedules
            return self.deal_with_schedules(schedules, stu_id)

    @staticmethod
    def deal_with_ddl(ddls, student_id):
        """
        进行ddl信息的数据整理
        """
        aim_json = {'student_id': student_id}
        ddl = []
        for lesson, all_ddl in ddls.items():
            cur_lesson_ddl = {}
            content = []
            for each in all_ddl:                                         # 获取所有后端所需的数据
                cur_ddl = {}
                if len(each) >= 4:
                    cur_ddl['ddl'] = each[3]
                else:
                    cur_ddl['ddl'] = ''
                cur_ddl['homework'] = each[0]
                cur_ddl['state'] = each[1]
                content.append(cur_ddl)
            cur_lesson_ddl['content'] = content
            cur_lesson_ddl['name'] = lesson
            ddl.append(cur_lesson_ddl)
        aim_json['ddl'] = ddl
        return_json = json.dumps(aim_json, ensure_ascii=False)            # 使用json打包

        # 测试用
        # f = open('ddl.txt', 'a', encoding='utf-8')
        # f.write(returnJson)
        # f.close()
        # print(returnJson)

        return return_json

    @staticmethod
    def deal_with_grades(ori_grades, student_id):
        """
        data sort for grades
        """
        jsons = []
        for i in range(len(ori_grades)):
            aim_grades = []
            semember = ''
            for j in range(len(ori_grades[i])):
                cur_data = ori_grades[i][j]
                lesson_code = cur_data[3]                                 # 获取所有后端所需的数据
                lesson_name = cur_data[4]
                credit = cur_data[7]
                mark = cur_data[9]
                origin_grade = cur_data[10]
                grades = cur_data[11]
                semember = cur_data[1]
                cur_info = [lesson_code, lesson_name, credit, mark, origin_grade, grades]
                aim_grades.append(cur_info)

            schedule_chart = {'student_id': student_id, 'semester': semember, 'info': aim_grades}
            return_json = json.dumps(schedule_chart, ensure_ascii=False)   # 使用json打包

            # 测试用
            # f = open('grade.txt', 'a', encoding='utf-8')
            # f.write(returnJson)
            # f.close()
            # print(returnJson)

            jsons.append(return_json)
        return jsons

    @staticmethod
    def deal_with_empty_classroom(empty_classroom):
        """
        data sort for empty classrooms
        """
        aim_jsons = []
        for i in range(len(empty_classroom)):
            this_week = empty_classroom[i]
            cur_week = []
            for week in range(7):
                cur_week.append([])
            for room, is_empty in this_week.items():
                teaching_building = ''
                if room[0] == 'J':                                      # 获取校区
                    campus = '沙河校区'
                else:
                    campus = '学院路校区'
                classroom = room
                if room[0] == 'J' and room[1] == '1':                   # 获取教学楼
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
                for j in range(len(is_empty)):                          # 获取时间和节数
                    if j % 6 == 5:                                      # 如果是这一天的最后一节
                        if is_empty[j] == 1:
                            section.append(13)
                            section.append(14)
                        dict_cur = {'campus': campus, 'teaching_building': teaching_building, 'classroom': classroom}
                        tmp = str(section.copy())
                        tmp = tmp[:-1] + ',]'
                        dict_cur['section'] = tmp
                        if section:
                            cur_week[j // 6].append(dict_cur)
                        section.clear()
                    else:                                               # 如果不是这一天的最后一节
                        if is_empty[j] == 1:
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
            for week in range(7):                                             # 整理这一周的所有数据
                cur_datedict = {}
                days = i * 7 + week
                origin_day = datetime.strptime('2020-02-24', "%Y-%m-%d")
                cur_date = origin_day + timedelta(days=days)
                cur_date = cur_date.strftime("%Y-%m-%d")
                cur_datedict['date'] = cur_date
                cur_datedict['classroom'] = cur_week[week].copy()

                # 测试用
                # f = open('empty.txt', 'a', encoding='utf-8')
                # f.write(str(curDate))
                # f.close()
                # print(curDate)

                aim_jsons.append(cur_datedict)                                # 将这一周的数据整理好放入列表
        return aim_jsons

    @staticmethod
    def deal_with_schedules(schedules, student_id):
        """
        data sort for schedules
        """
        aim_lessons = []
        section_dict = {0: '1，2', 1: '3，4', 2: '6，7', 3: '8，9', 4: '11，12', 5: '13，14'}
        for i in range(len(schedules) - 1):
            for j in range(len(schedules[i])):
                # noinspection PyBroadException
                try:
                    cur_str = schedules[i][j]
                    if cur_str == ' ':
                        continue

                    cur_strs = cur_str.split('节')                            # 使用‘节’来划分不同的课
                    lessons = []
                    cur_lesson = ''
                    for k in range(len(cur_strs)):                            # 获取所有课程
                        if cur_strs[k] == '':
                            continue
                        if cur_lesson == '':
                            cur_lesson = cur_lesson + cur_strs[k]
                            continue
                        if cur_strs[k][0] == '，':
                            cur_lesson = cur_lesson + '节' + cur_strs[k]
                            if k == len(cur_strs) - 2:
                                cur_lesson = cur_lesson + '节'
                                lessons.append(cur_lesson)
                                cur_lesson = ''
                                break
                        if cur_strs[k][0] != '，':
                            cur_lesson = cur_lesson + '节'
                            lessons.append(cur_lesson)
                            cur_lesson = cur_strs[k]
                            if k == len(cur_strs) - 2:
                                cur_lesson = cur_lesson + '节'
                                lessons.append(cur_lesson)
                                cur_lesson = ''
                                break
                    if cur_lesson != '':
                        if cur_lesson[-1] == '：':
                            lessons.append(cur_lesson)
                        else:
                            lessons.append(cur_lesson + '节')

                    cur_infos = []
                    for cur_str in lessons:                                  # 获取这个课程的信息
                        cur_strs = cur_str.split('\n')
                        lesson = cur_strs[0]
                        if cur_strs[0] == '':
                            lesson = cur_strs[1]
                            cur_strs = cur_strs[1:]
                        info = ''
                        for k in range(len(cur_strs) - 1):
                            info = info + cur_strs[k + 1]
                        infos = info.split('，')
                        types = []
                        tmp_str = ''
                        for each in infos:                                  # 处理多课程问题
                            tmp_str = tmp_str + each
                            if each[-1] == '节':
                                types.append(tmp_str)
                                tmp_str = ''
                            else:
                                tmp_str = tmp_str + '，'
                        another_types = []
                        for each in types:
                            info = each
                            if len(info.split('[')) > 2:
                                divide_weeks = info.split('周')
                                for k in range(len(divide_weeks) - 1):
                                    strs = divide_weeks[k] + '周' + divide_weeks[-1]
                                    if strs[0] == '，':
                                        strs = strs[1:]
                                    another_types.append(strs)
                            else:
                                another_types = types
                        types = another_types
                        for each in types:
                            info = each
                            teachers, info = info.split('[')                    # 获取老师信息
                            week, info = info.split(']')                        # 获取周数信息
                            if info.find(' ') != -1:
                                place, aim_time = info.split(' ')               # 获取时间地点信息
                            else:
                                place, aim_time = info.split('第')
                                aim_time = '第' + aim_time
                            # deal with some certain problems
                            if week in ('', '周'):
                                week = '1-16'
                            if place[0] == '单' or place[0] == '双':
                                week = week + place[0]
                                place = place[1:]
                            if aim_time[0] == aim_time[1]:
                                aim_time = aim_time[1:]
                            cur_info = [lesson, place[1:], teachers, week, '周' + str(j + 1) + ' ' + aim_time]
                            cur_infos.append(cur_info)
                    aim_lessons.append(cur_infos)
                except Exception:
                    print(traceback.format_exc())
                    print('解析课表信息出错')
                    cur_str = schedules[i][j]
                    cur_infos = []
                    cur_info = [cur_str.split('\n')[0], '未知', '未知', '1-16']
                    section = section_dict[i]
                    cur_info.append('周' + str(j + 1) + ' 第' + section + '节')
                    cur_infos.append(cur_info)
                    aim_lessons.append(cur_infos)
        schedule_chart = {'student_id': student_id, 'info': aim_lessons}
        return_json = json.dumps(schedule_chart, ensure_ascii=False)      # 使用json进行打包

        # 测试用
        # f = open('schedule.txt', 'a', encoding='utf-8')
        # f.write(returnJson)
        # f.close()
        # print(return_json)

        return return_json


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    # DataReq(userName, password).request('d')
    # DataReq(userName, password).request('g')
    # DataReq(userName, password).request('e')
    # DataReq(userName, password).request('s')
