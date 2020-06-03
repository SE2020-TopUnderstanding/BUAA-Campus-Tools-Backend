import traceback
import json
import re
from datetime import datetime, timedelta
from jiaowu import JiaoWuReq
from course import CourseRequest
from password_utils import Aescrypt, KEY, MODEL, ENCODE_
from log import Log


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
        # 有待补充
        self.special_lessons = ['体育（', '大英B', '大英A', '汽车构造及拆装实习', '面向对象程序设计(JAVA)', '英语读说写',
                                '批判阅读与写作', '英语听说写', '学业英语阅读与写作', '高级英语听说写', '理解与辩论', '高级英语读说写']

    def request(self, request_type):
        """
        获取所有的查询请求
        爬取信息
        请求格式: {'d':'ddl查询', 'j':'成绩课表查询', 'e':'空教室查询', 'l':'已选课程查询'}
        """
        print('start to get the data, usr_name: ' + self.usr_name)
        print('requestType: ' + request_type)
        print('当前时间：' + str(datetime.now()))

        if request_type == 'd':
            session = CourseRequest(self.usr_name, self.password)      # 获取该学生的学号
            stu_id = session.get_id()
        else:
            session = JiaoWuReq(self.usr_name, self.password)          # 获取该学生的学号
            stu_id = session.get_id()
        print('studentId: ' + str(stu_id))

        wrong_message = [
            '登录课程中心出现未知错误，通常是超时问题',
            '登陆时出现未知错误，请参考log信息',
            '登录状态码是2XX，但不是200',
            '跳转到未知网页',
            '超时3次',
            '登陆或访问教务状态码是4XX或5XX',
            'IP被封',
            '用户名错误或者网站要求输入验证码',
            '密码错误',
            '用户名或密码为空',
            '账号被锁',
            '账号被锁',
            '在课程中心请求失败'
        ]

        if stu_id == '':
            print('错误!!!')
            print('usr_name: ' + self.usr_name)
            print(wrong_message[-1 * stu_id])
            return stu_id, ''

        if isinstance(stu_id, int) and -12 <= int(stu_id) <= 0:
            print('错误!!!')
            print('usr_name: ' + self.usr_name)
            print(wrong_message[-1 * stu_id])
            return stu_id, ''

        stu_id = encrypt_string(stu_id)

        if request_type == 'd':                                          # 获取ddl信息
            ddls = session.get_ddl()
            session.quit()
            if isinstance(ddls, int) and -12 <= int(ddls) <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: ddl')
                print(wrong_message[-1 * ddls])
                return ddls, ''
            if isinstance(ddls, int) and ddls == -13:
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
                return ddls, ''
            return self.deal_with_ddl(ddls, stu_id), ''

        if request_type == 'j':                                        # 获取成绩及课表信息
            grades = session.get_grade()
            if isinstance(grades, int) and -12 <= int(grades) <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: jiaowu')
                print(wrong_message[-1 * grades])
                return grades, ''
            schedules = session.get_schedule()
            if isinstance(schedules, int) and -12 <= int(schedules) <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: jiaowu')
                print(wrong_message[-1 * schedules])
                return schedules, ''
            lesson_ids = session.get_all_lessons(1)
            session.quit()
            if isinstance(lesson_ids, int) and -12 <= int(lesson_ids) <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: jiaowu')
                print(wrong_message[-1 * lesson_ids])
                return schedules, ''
            sorted_grades = self.deal_with_grades(grades, stu_id)
            sorted_schedules = self.deal_with_schedules(schedules, lesson_ids, stu_id)
            # with open("special_lessons.txt", "w") as out_file:
            #    out_file.write(str(self.special_lessons))
            return sorted_grades, sorted_schedules

        if request_type == 'e':                                        # 获取空教室信息
            empty_classroom = session.get_empty_classroom()
            session.quit()
            if isinstance(empty_classroom, int) and -12 <= empty_classroom <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: empty_classroom')
                print(wrong_message[-1 * empty_classroom])
                return empty_classroom, ''
            return self.deal_with_empty_classroom(empty_classroom), ''

        if request_type == 'l':                                        # 获取课表信息
            teachers = session.get_schedule(0)
            if isinstance(teachers, int) and -12 <= teachers <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: lesson')
                print(wrong_message[-1 * teachers])
                return teachers, ''
            lessons = session.get_all_lessons()
            session.quit()
            if isinstance(lessons, int) and -12 <= lessons <= 0:
                print('错误!!!')
                print('usr_name: ' + self.usr_name)
                print('requestType: lesson')
                print(wrong_message[-1 * lessons])
                return lessons, ''
            return self.deal_with_lessons(lessons, teachers), ''

    @staticmethod
    def analysis_lesson(schedules, i, j):
        section_dict = {0: '1，2', 1: '3，4', 2: '6，7', 3: '8，9', 4: '11，12', 5: '13，14'}
        abandon_list = ['第1,2节', '第3,4节', '第5,6节', '第7,8节', '第9,10节', '第11,12节']
        # noinspection PyBroadException
        try:
            cur_str = schedules[i][j]
            if cur_str in abandon_list:
                return []
            if cur_str in ('', ' '):
                return []
            if cur_str.find('考试时间:') != -1:
                start = cur_str.find('考试时间:')
                mid = cur_str.find('考试时间:', start + 1)
                end = cur_str.find('考试时间:', mid + 1)
                if end not in (start, -1):
                    cur_str = cur_str[:start] + abandon_list[i] + cur_str[end + 5:]
                else:
                    cur_str = cur_str.replace('考试时间:', abandon_list[i])
            cur_str = cur_str.replace('节节', '节')
            pattern = r'(\d节)'
            cur_strs = re.split(pattern, cur_str)  # 使用‘节’来划分不同的课
            # print(cur_strs)
            for k in range(len(cur_strs) - 1):
                if re.match(pattern, cur_strs[k + 1]) is not None:
                    cur_strs[k] += cur_strs[k + 1][0]
            for each in cur_strs[::-1]:
                if re.match(pattern, each) is not None:
                    cur_strs.remove(each)
            lessons = []
            cur_lesson = ''
            for k in range(len(cur_strs)):  # 获取所有课程
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
            splited_lesson = ['航空发动机结构设', '模式识别与智能系']
            for cur_str in lessons:  # 获取这个课程的信息
                cur_strs = cur_str.split('\n')
                lesson = cur_strs[0]
                if cur_strs[0] == '':
                    lesson = cur_strs[1]
                    if lesson in splited_lesson:
                        lesson += cur_strs[2]
                        cur_strs = cur_strs[2:]
                    else:
                        cur_strs = cur_strs[1:]
                elif lesson in splited_lesson:
                    lesson += cur_strs[1]
                    cur_strs = cur_strs[1:]
                info = ''
                for k in range(len(cur_strs) - 1):
                    info = info + cur_strs[k + 1]
                infos = info.split('，')
                types = []
                tmp_str = ''
                for each in infos:  # 处理多课程问题
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

                        pattern = r'([单双\]]周)'
                        divide_weeks = re.split(pattern, info)
                        # print(divide_weeks)
                        for ite in range(len(divide_weeks) - 1):
                            if re.match(pattern, divide_weeks[ite + 1]) is not None:
                                divide_weeks[ite] += divide_weeks[ite + 1][0]
                        for each_item in divide_weeks[::-1]:
                            if re.match(pattern, each_item) is not None:
                                divide_weeks.remove(each_item)

                        for k in range(len(divide_weeks) - 1):
                            strs = divide_weeks[k] + '周' + divide_weeks[-1]
                            if strs[0] == '，':
                                strs = strs[1:]
                            another_types.append(strs)
                    else:
                        another_types = types
                types = another_types
                save_teacher = ''
                for each in types:
                    info = each
                    teachers, info = info.split('[')  # 获取老师信息
                    if teachers == '' and save_teacher != '':
                        teachers = save_teacher
                    save_teacher = teachers
                    week, info = info.split(']')  # 获取周数信息
                    if info.find(' ') != -1:
                        place, aim_time = info.split(' ')  # 获取时间地点信息
                    else:
                        info = info.replace('第第', '第')
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
        except Exception:
            print(traceback.format_exc())
            print('解析课表信息出错')

            Log('解析课表信息出错')
            Log('信息内容：' + schedules[i][j])
            Log(traceback.format_exc())
            cur_str = schedules[i][j]
            cur_infos = []
            cur_info = [cur_str.split('\n')[0], '未知', '未知', '1-16']
            section = section_dict[i]
            cur_info.append('周' + str(j + 1) + ' 第' + section + '节')
            cur_infos.append(cur_info)
        return cur_infos

    def match(self, str1, str2):
        new_str1 = str1.replace(' ', '').replace('，', ',').lower()
        new_str2 = str2.replace(' ', '').replace('，', ',').lower()
        for each in self.special_lessons:
            if str1.find(each) != -1 and new_str1.find(new_str2) != -1:
                return True
        if new_str1 == new_str2:
            return True
        return False

    def deal_with_lessons(self, lessons, teachers):
        """
        进行已选课程信息的数据整理
        """
        ignore_list = ['仪光科技基础综合训练（3）', '高等代数（1）', '高等代数（2）', '物理学实验（1）']
        info = []
        for i in teachers[::-1]:
            if i[0][0] == '没有数据!':
                teachers.remove(i)

        for sememter in range(len(teachers)):
            sememter_teacher = teachers[sememter]
            sememter_lessons = lessons[sememter]
            aim_lessons = []
            for i in range(len(sememter_teacher)):
                for j in range(len(sememter_teacher[i])):
                    cur_infos = self.analysis_lesson(sememter_teacher, i, j)
                    if len(cur_infos) == 0:
                        continue
                    aim_lessons.append(cur_infos)

            for lesson in sememter_lessons:
                sign = 0
                if lesson[7] == '':
                    sign = 1
                for tmp_lessons in aim_lessons:
                    for each in tmp_lessons:
                        if self.match(each[0], lesson[2]):
                            teachers_name = each[2].split('，')
                            for teacher_name in teachers_name:
                                if lesson[7].replace(' ', '').find(teacher_name.replace(' ', '')) == -1:
                                    lesson[7] += '，' + teacher_name
                            sign = 1

                if sign == 0:
                    out_sign = 0
                    for each in ignore_list:
                        if each == lesson[2].replace(' ', '').replace('(', '（').replace(')', '）'):
                            out_sign = 1
                            break
                    for tmp_lessons in aim_lessons:
                        for each in tmp_lessons:
                            if self.match(each[0], lesson[2] + '(实验)'):
                                self.special_lessons.append(lesson[2])
                                teachers_name = each[2].split('，')
                                for teacher_name in teachers_name:
                                    if lesson[7].replace(' ', '').find(teacher_name.replace(' ', '')) == -1:
                                        lesson[7] += '，' + teacher_name
                                out_sign = 1
                    if not out_sign:
                        print('向已选课程中补充教师信息失败')
                        Log('向已选课程中补充教师信息失败')
                        Log('所需补充的课程：' + str(lesson))
                        Log('用户名: ' + self.usr_name)
                        Log('相关课程')
                        for tmp_lessons in aim_lessons:
                            for each in tmp_lessons:
                                new_str1 = each[0].replace(' ', '').replace('，', ',')
                                new_str2 = lesson[2].replace(' ', '').replace('，', ',')
                                if new_str1.find(new_str2) != -1:
                                    Log('可能相关的课程：' + each[0])
                                if new_str2.find(new_str1) != -1:
                                    Log('可能相关的课程：' + each[0])
                        Log('相关课程结束')
                cur_lesson = [lesson[2], lesson[1], lesson[9],
                              lesson[10], lesson[6], lesson[4], lesson[7].replace(' ', '')]
                info.append(cur_lesson)
        aim_json = {'info': info}
        return_json = json.dumps(aim_json, ensure_ascii=False)  # 使用json打包
        return_json = return_json.replace('，', ',')
        # 测试用
        # f = open('ddl.txt', 'a', encoding='utf-8')
        # f.write(returnJson)
        # f.close()
        # print(return_json)

        return return_json

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
        # print(return_json)

        return return_json

    @staticmethod
    def deal_with_grades(ori_grades, student_id):
        """
        data sort for grades
        """
        aim_jsons = []
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
            # print(return_json)

            aim_jsons.append(return_json)
        return aim_jsons

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

    def deal_with_schedules(self, schedules, lesson_ids, student_id):
        """
        data sort for schedules
        """
        aim_lessons = []
        for i in range(len(schedules)):
            for j in range(len(schedules[i])):
                cur_infos = self.analysis_lesson(schedules, i, j)
                if len(cur_infos) == 0:
                    continue
                for each in cur_infos:
                    sign = 0
                    for lesson in lesson_ids:
                        if self.match(each[0], lesson[2]):
                            each.insert(0, lesson[1])
                            sign = 1
                            break
                    if sign == 0:
                        each.insert(0, '')
                for aim in cur_infos:
                    if aim[0] == '':
                        for each in cur_infos:
                            if each[0] != '' and aim[1].replace(' ', '') == each[1].replace(' ', ''):
                                aim[0] = each[0]
                                break
                        if aim[1].find('(实验)') != -1:
                            pattern = r'(\(实验\))'
                            add_item = re.split(pattern, aim[1])[0]
                            self.special_lessons.append(add_item)
                            for lesson in lesson_ids:
                                if self.match(aim[1], lesson[2]):
                                    aim[0] = lesson[1]
                                    break
                        if aim[0] == '':
                            print('向课表整合课程代码失败')
                            Log('向课表整合课程代码失败')
                            Log('所需整合的课程：' + str(aim))
                            Log('用户名: ' + self.usr_name)
                aim_lessons.append(cur_infos)
        schedule_chart = {'student_id': student_id, 'info': aim_lessons}
        return_json = json.dumps(schedule_chart, ensure_ascii=False)      # 使用json进行打包
        return_json = return_json.replace('，', ',')
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
    # DataReq(USR_NAME, PW).request('d')
    # DataReq(USR_NAME, PW).request('j')
    # DataReq(USR_NAME, PW).request('e')
    # DataReq(USR_NAME, PW).request('l')
