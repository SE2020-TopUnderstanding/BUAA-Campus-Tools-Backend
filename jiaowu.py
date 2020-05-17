import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from vpn import VpnLogin
from web import WebLogin


class JiaoWuReq:
    """
    本类将从 jiaowu.buaa.edu.cn 网站获取信息
    """
    def __init__(self, usr_name, pw):
        # """
        self.status = 0
        vpn = ''
        for i in range(3):
            vpn = VpnLogin(usr_name, pw)  # 登录
            success = vpn.switch_to_jiao_wu()      # 切换到教务
            # 错误处理
            if success == -1:
                self.status = -1
                break
            if success in (-2, -5):
                if i == 2:
                    self.status = -2
                    break
                vpn.get_browser().quit()
            if success in (-3, -4):
                self.status = -3
                break
            if -6 >= success >= -10:
                self.status = success + 1
                break
            if success == 0:
                break
        if vpn == '':
            self.status = -11
            return
        self.browser = vpn.get_browser()     # 获取浏览器.
        # """

        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        self.schedule_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kbcx/queryGrkb'
        self.headers_jw = {
            'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome',
            'User-Agent': self.user_agent
        }

        self.empty_classroom_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kjscx/queryKjs'
        # self.final_exam_grade_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
        self.status = 1
        self.now = ''
        login = ''
        for i in range(3):
            login = WebLogin(usr_name, pw)  # 登录
            success = login.switch_to_jiaowu()      # 切换到教务
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
            return

        # self.get_empty_classroom()           # debug用
        self.get_grade()                    # debug用
        # self.get_schedule()                 # debug用

    def get_status(self):
        """
        初始化的结果
        status =  1 : 成功
        status =  0 : 登录教务网站出现未知错误，通常是超时问题
        status = -1 : 登陆时出现未知错误，请参考log信息
        status = -2 : 登录状态码是2XX，但不是200
        status = -3 : 跳转到未知网页
        status = -4 : 超时3次
        status = -5 : 登陆或访问教务状态码是4XX或5XX
        status = -6 : IP被封
        status = -7 : 用户名错误或者网站要求输入验证码
        status = -8 : 密码错误
        status = -9 : 用户名或密码为空
        status =-10 : 账号被锁
        status =-11 : 账号被锁
        status =-12 : 在教务网站请求失败
        """
        return self.status

    @ staticmethod
    def check_status(html):
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
        final_exam_grade_url = 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
        if self.status != 1:
            return self.status
        grade = ''
        i = 0
        while i < 3:
            try:
                grade = self.now.get(url=final_exam_grade_url, headers=self.headers_jw)
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
        table = soup.select('table > tr > td > select[class="XNXQ_CON"] > option')
        for each in table:
            # print(each.get_text())
            # print(each.attrs['value'])
            if each.attrs['value'] != '':
                search_list.append(each.attrs['value'])

        for k in range(19):
            print('cur_year: ' + search_list[k])
            grade = ''
            i = 0
            params = {
                'pageXnxq': search_list[k],
                'pageBkcxbj': '',
                'pageSfjg': '',
                'pageKcmc': ''
            }
            headers_grades = {
                'User-Agent': self.user_agent,
                'Referer': 'https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj'
            }
            while i < 3:
                try:
                    grade = self.now.post(url=final_exam_grade_url, headers=headers_grades,
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
            table = soup.select('table[class="bot_line"] > tr > td')
            iterator = 0
            texts = []
            for each in table:
                iterator += 1
                strs = each.get_text()
                # print(strs)
                texts.append(strs)
                if iterator == 14:
                    print(texts)
                    iterator = 0
                    texts.clear()
        return ''

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
                empty_classroom = self.now.get(url=self.empty_classroom_url, headers=self.headers_jw)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(empty_classroom) == -1:
            return -12

        empty_classrooms = []
        for k in range(19):
            print('week: ' + str(k + 1))
            cur_dict = {}
            for j in range(9):
                print('page: ' + str(j + 1))
                empty_classroom = ''
                i = 0
                params = {
                    'pageNo': str(j + 1),
                    'pageSize': str(20),
                    'pageCount': str(9),
                    'pageXnxq': '2019-20202',
                    'pageZc1': str(k + 1),
                    'pageZc2': str(k + 1),
                    'pageXiaoqu': '',
                    'pageLhdm': '',
                    'pageCddm': ''
                }
                headers_ec = {
                    'User-Agent': self.user_agent,
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
                table = soup.select('table[class="dataTable"] > tr > td')
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

    def get_schedule(self):
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
                schedule = self.now.get(url=self.schedule_url, headers=self.headers_jw)
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(schedule) == -1:
            return -12

        soup = BeautifulSoup(schedule.text, 'lxml')
        table = soup.select('table[class="addlist_01"] > tr > td')
        schedules = []
        schedule = []
        for each in table:
            strs = each.get_text()
            # print(strs)
            if strs in ('上午', '下午', '晚上'):
                continue
            if strs.find('其它课程：') != -1:
                continue
            if strs[0] == '第' and (strs[2] == '，' or strs[3] == '，'):
                if len(schedule) != 0:
                    schedules.append(schedule.copy())
                schedule.clear()
                continue
            if strs[0] == '&':
                schedule.append('')
                continue
            schedule.append(strs)
        schedules.append((schedule.copy()))
        # print(schedules)
        return schedules

    def get_id(self):
        if self.status != 0:
            return self.status
        # 这个按钮不能直接按，需要使用js来按
        schedule_label = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[6]/div/a[6]')
        self.browser.execute_script("arguments[0].click();", schedule_label)
        # time.sleep(0.5)
        self.browser.switch_to.frame('iframename')
        locator = (By.XPATH, '/html/body/div[1]/div/div[8]/div[2]/table')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            print('timeout or switch to an unknown page')
            return -4

        id_place = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[8]/div[1]/span')
        student_id = id_place.text
        student_id = student_id.split('(')[1]
        student_id = student_id.split(')')[0]
        self.browser.switch_to.default_content()
        return student_id

    def quit(self):
        self.browser.quit()


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    JiaoWuReq(USR_NAME, PW)
