import time
import requests
from bs4 import BeautifulSoup
from web import WebLogin
from log import Log

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'


class JiaoWuReq:
    """
    本类将从 jiaowu.buaa.edu.cn 网站获取信息
    """
    def __init__(self, usr_name, pw):
        # 登陆用的网页地址、user_agent、header等
        self.schedule_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryGrkb'
        self.headers_jw = {
            'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome',
            'User-Agent': USER_AGENT
        }
        self.empty_classroom_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kjscx/queryKjs'
        self.final_exam_grade_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
        self.all_lesson_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryXsxkXq'

        self.status = 1
        self.now = ''                                                                       # 整个爬取过程的session
        login = ''
        for i in range(3):
            login = WebLogin(usr_name, pw)                                                  # 登录
            success = login.switch_to_jiaowu()                                              # 切换到教务
            # 错误处理
            if success == -4:
                if i == 2:
                    self.status = -4
                    break
            elif success == 1:
                self.now = login.get_session()
                break
            else:
                self.status = success
                break
        if login == '':
            self.status = -11
            Log('教务登陆失败，login == '', usr_name = ' + usr_name)
            return

        # self.get_empty_classroom()          # debug用
        # self.get_grade()                    # debug用
        # self.get_schedule()                 # debug用
        # self.get_id()                       # debug用
        # self.get_all_lessons()              # debug用

    def get_status(self):
        """
        初始化的结果
        status =   1 : 成功
        status =   0 : 登录教务网站出现未知错误，通常是超时问题
        status =  -1 : 登陆时出现未知错误，请参考log信息
        status =  -2 : 登录状态码是2XX，但不是200
        status =  -3 : 跳转到未知网页
        status =  -4 : 超时3次
        status =  -5 : 登陆或访问教务状态码是4XX或5XX
        status =  -6 : IP被封
        status =  -7 : 用户名错误或者网站要求输入验证码
        status =  -8 : 密码错误
        status =  -9 : 用户名或密码为空
        status = -10 : 账号被锁
        status = -11 : 极度奇怪的错误（可以认为不可能发生）
        status = -12 : 在教务网站请求失败
        """
        return self.status

    @ staticmethod
    def check_status(html):
        """
        用于检查登录是否成功
        成功返回  0
        失败返回 -1
        """
        try:
            if html != '':
                html.raise_for_status()
            else:
                return -1
        except requests.exceptions.RequestException as err:
            print(err)
            return -1
        return 0

    def get_grade(self):
        """
        该函数返回该学生的所有成绩
        将返回一个列表
        列表数据格式:
        [
            # 按照学期排列
            [
                [序号, 学年学期, 开课院系, 课程代码, 课程名称, 课程性质, 课程类别, 学分, 是否考试课, 补考重修标记, 总成绩, 折算成绩, 备注]
                [序号, 学年学期, 开课院系, 课程代码, 课程名称, 课程性质, 课程类别, 学分, 是否考试课, 补考重修标记, 总成绩, 折算成绩, 备注]
                ...
                ...
            ]
            ...
        ]
        """
        if self.status != 1:
            return self.status
        grade = ''
        i = 0
        while i < 3:
            try:
                grade = self.now.get(url=self.final_exam_grade_url, headers=self.headers_jw)    # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(grade) == -1:
            return -12

        search_list = []
        soup = BeautifulSoup(grade.text, 'lxml')
        table = soup.select('table > tr > td > select[class="XNXQ_CON"] > option')              # 获取选项的值
        for each in table:
            # print(each.get_text())
            # print(each.attrs['value'])
            if each.attrs['value'] != '':
                search_list.append(each.attrs['value'])
        grades = []
        for k in range(len(search_list)):
            semester = []
            print('cur_year: ' + search_list[k])
            grade = ''
            i = 0
            params = {
                'pageXnxq': search_list[k],                                                     # 借助params进行requests
                'pageBkcxbj': '',
                'pageSfjg': '',
                'pageKcmc': ''
            }
            headers_grades = {
                'User-Agent': USER_AGENT,
                'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
            }
            while i < 3:
                try:
                    grade = self.now.post(url=self.final_exam_grade_url, headers=headers_grades,
                                          params=params)
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(grade) == -1:
                return -12
            time.sleep(1)
            soup = BeautifulSoup(grade.text, 'lxml')
            table = soup.select('table[class="bot_line"] > tr > td')                            # 借助bs4分析网页，获取信息
            iterator = 0
            texts = []
            for each in table:
                iterator += 1
                strs = each.get_text()
                # print(strs)

                strs = strs.replace('\t', '')
                strs = strs.replace('\n', '')
                strs = strs.replace('\r', '')
                strs = strs.replace(' ', '')

                texts.append(strs)
                if iterator == 14:
                    # print(texts)
                    semester.append((texts.copy()))
                    iterator = 0
                    texts.clear()
            grades.append(semester)
        # print(grades)
        return grades

    def get_empty_classroom(self):
        """
        该函数一次性返回全部空教室的数据
        将数据以列表的形式返回
        数据格式:
        [
            按照周排列
            {                   时间
                教室名 : [1 0 0 1 ...] 1:空闲 0:占用
            }
            ...
        ]
        """
        if self.status != 1:
            return self.status
        empty_classroom = ''
        i = 0
        while i < 3:
            try:
                empty_classroom = self.now.get(url=self.empty_classroom_url, headers=self.headers_jw)   # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(empty_classroom) == -1:
            return -12

        soup = BeautifulSoup(empty_classroom.text, 'lxml')
        table = soup.select('table > tr > td > select[class="XNXQ_CON"] > option')
        semester = ''
        for each in table:
            # print(each.get_text())
            # print(each.attrs['value'])
            if each.attrs['value'] != '' and 'selected' in each.attrs.keys():                   # 获取当前学期选项
                semester = each.attrs['value']

        if semester == '':
            return -12

        empty_classrooms = []
        for k in range(19):
            print('week: ' + str(k + 1))
            cur_dict = {}
            for j in range(9):
                # print('page: ' + str(j + 1))
                empty_classroom = ''
                i = 0
                params = {
                    'pageNo': str(j + 1),
                    'pageSize': str(20),
                    'pageCount': str(9),
                    'pageXnxq': semester,                                                       # 借助params进行requests
                    'pageZc1': str(k + 1),
                    'pageZc2': str(k + 1),
                    'pageXiaoqu': '',
                    'pageLhdm': '',
                    'pageCddm': ''
                }
                headers_ec = {
                    'User-Agent': USER_AGENT,
                    'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kjscx/queryKjs'
                }
                while i < 3:
                    try:
                        empty_classroom = self.now.post(url=self.empty_classroom_url, headers=headers_ec,
                                                        params=params)
                        break
                    except requests.exceptions.RequestException as err:
                        print(err)
                        i += 1
                        if i == 3:
                            return 0

                if self.check_status(empty_classroom) == -1:
                    return -12

                time.sleep(1)
                soup = BeautifulSoup(empty_classroom.text, 'lxml')
                table = soup.select('table[class="dataTable"] > tr > td')                       # 通过BeautifulSoup分析
                occupied = []
                last_strs = ''
                for each in table:
                    strs = each.get_text()
                    if strs == '\n\n':
                        icon = each.contents[1].attrs
                        if len(icon['class']) == 2:
                            occupied.append(0)
                        else:
                            occupied.append(1)
                    else:

                        if last_strs == '':
                            last_strs = strs
                            continue
                        # print(last_strs)
                        cur_dict[last_strs] = occupied.copy()
                        # print(occupied)
                        occupied.clear()
                        last_strs = strs
                # print(last_strs)
                cur_dict[last_strs] = occupied.copy()
                # print(occupied)
                occupied.clear()
            empty_classrooms.append(cur_dict)
        # print(empty_classrooms)
        return empty_classrooms

    def get_schedule(self, choose=1):
        """
        该函数一次性返回该学生当前学期课表
        将数据以列表的形式返回
        数据格式:
        [
            ['课程1', '课程2', '课程3', '课程4', '课程5', '课程6', '课程7']
            ...
        ]
        """
        if self.status != 1:
            return self.status
        schedule = ''
        i = 0
        while i < 3:
            try:
                schedule = self.now.get(url=self.schedule_url, headers=self.headers_jw)     # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(schedule) == -1:
            return -12

        soup = BeautifulSoup(schedule.text, 'lxml')
        table = soup.select('table > tr > td > select[class="XNXQ_CON"] > option')
        semester = []
        for each in table:
            # print(each.get_text())
            # print(each.attrs['value'])
            if choose == 1 and each.attrs['value'] != '' and 'selected' in each.attrs.keys():  # 获取当前学期选项
                semester.append(each.attrs['value'])
            elif choose == 0 and each.attrs['value'] != '':
                semester.append(each.attrs['value'])

        if len(semester) == 0:
            return -12

        all_schedules = []
        for k in range(len(semester)):
            print('cur_year: ' + semester[k])
            page = ''
            i = 0
            params = {
                'fhlj': 'kbcx/queryGrkb',
                'xnxq': semester[k]
            }
            headers_grades = {
                'User-Agent': USER_AGENT,
                'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryGrkb'
            }
            while i < 3:
                try:
                    page = self.now.post(url=self.schedule_url, headers=headers_grades,
                                         params=params)
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(page) == -1:
                return -12
            time.sleep(1)

            soup = BeautifulSoup(page.text.replace('</br>', '\n'), 'lxml')                  # 这里相当关键
            table = soup.select('table[class="addlist_01"] > tr > td')                      # 使用BeautifulSoup分析网页
            schedules = []
            schedule = []
            for each in table:
                strs = each.get_text()
                # print(strs)
                if strs in ('上午', '下午', '晚上'):
                    continue
                if strs.find('其它课程：') != -1:
                    continue
                if strs[0] == '第' and (strs[2] == '，' or strs[3] == '，' or strs[2] == ',' or strs[3] == ','):
                    if len(schedule) != 0:
                        schedules.append(schedule.copy())
                    schedule.clear()
                    continue
                if strs[0] == '&':
                    schedule.append('')
                    continue
                schedule.append(strs)
            schedules.append((schedule.copy()))
            all_schedules.append(schedules)
        # print(schedules)
        if choose == 1:
            return all_schedules[0]
        return all_schedules

    def get_id(self):
        """
        该函数返回该学生的学号
        """
        if self.status != 1:
            return self.status
        schedule = ''
        i = 0
        while i < 3:
            try:
                schedule = self.now.get(url=self.schedule_url, headers=self.headers_jw)     # 获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(schedule) == -1:
            return -12

        soup = BeautifulSoup(schedule.text, 'lxml')
        table = soup.select('span[class="ml10 bold"]')                                      # 使用BeautifulSoup分析网页
        stu_id = '10000000'
        for each in table:
            stu_id = each.get_text()
            left = stu_id.find('(')
            right = stu_id.find(')', left)
            stu_id = stu_id[left + 1:right]
        # print(stu_id)
        return stu_id

    def get_all_lessons(self, choose=0):
        """
        该函数返回该学生的所有已选课程
        将返回一个列表
        列表数据格式:
        [
            # 按照学期排列
            [
                [学年学期, 课程代码, 课程名称, 课序号, 课程类别, 课程性质, 开课院系, 上课老师, 上课地点, 学分, 总学时, 教参数量, 备注]
                [学年学期, 课程代码, 课程名称, 课序号, 课程类别, 课程性质, 开课院系, 上课老师, 上课地点, 学分, 总学时, 教参数量, 备注]
                ...
                ...
            ]
            ...
        ]
        """
        if self.status != 1:
            return self.status
        lesson = ''
        i = 0
        while i < 3:
            try:
                lesson = self.now.get(url=self.all_lesson_url, headers=self.headers_jw)         # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(lesson) == -1:
            return -12
        soup = BeautifulSoup(lesson.text, 'lxml')
        search_list = []
        table = soup.select('table > tr > td > select[class="XNXQ_CON"] > option')              # 获取所有选项的值
        for each in table:
            # print(each.get_text())
            # print(each.attrs['value'])
            if choose == 1 and each.attrs['value'] != '' and 'selected' in each.attrs.keys():  # 获取当前学期选项
                search_list.append(each.attrs['value'])
            elif choose == 0 and each.attrs['value'] != '':
                search_list.append(each.attrs['value'])

        lessons = []
        for k in range(len(search_list)):
            semester = []
            print('cur_year: ' + search_list[k])
            lesson = ''
            i = 0
            params = {
                'fhlj': 'kbcx/queryXsxkXq',
                'pageRwh': '',
                'xnxq': search_list[k]                                                          # 借助params进行requests
            }
            headers_grades = {
                'User-Agent': USER_AGENT,
                'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
            }
            while i < 3:
                try:
                    lesson = self.now.post(url=self.all_lesson_url, headers=headers_grades,
                                           params=params)
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(lesson) == -1:
                return -12
            time.sleep(1)
            if lesson.text.find("alert('课程查询暂未开放！');") != -1:
                continue
            soup = BeautifulSoup(lesson.text, 'lxml')
            table = soup.select('table[class="bot_line"] > tr > td')                        # 使用BeautifulSoup分析网页
            iterator = 0
            texts = []
            for each in table:
                iterator += 1
                strs = each.get_text()
                # print(strs)

                strs = strs.replace('\t', '')
                strs = strs.replace('\n', '')
                strs = strs.replace('\r', '')
                strs = strs.replace(' ', '')

                texts.append(strs)
                if iterator == 13:
                    # print(texts)
                    semester.append((texts.copy()))
                    iterator = 0
                    texts.clear()
            lessons.append(semester)
        # print(lessons)
        if choose == 1:
            return lessons[0]
        return lessons

    def quit(self):
        """
        该函数结束整个session访问过程
        """
        self.now.close()


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    JiaoWuReq(USR_NAME, PW)
