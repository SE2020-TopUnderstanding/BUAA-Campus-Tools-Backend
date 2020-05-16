import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
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

        self.get_empty_classroom()           # debug用
        # self.getGrade()                    # debug用
        # self.get_schedule()                 # debug用

    def get_status(self):
        """
        初始化的结果
        status =  1 : 成功
        status =  0 : 登录教务网站出现未知错误
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
        """
        return self.status

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
        if self.status != 0:
            return self.status
        # 这个按钮不能直接按，需要使用js来按
        person_grade_label = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[8]/div/a[1]/span[2]')
        self.browser.execute_script("arguments[0].click();", person_grade_label)
        time.sleep(0.5)

        self.browser.switch_to.frame('iframename')                                              # 切换到另一个frame获取数据
        locator = (By.XPATH, '/html/body/div/div/div[3]/div[2]/a')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        end_grage = self.browser.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/a')     # 搜索期末成绩
        end_grage.click()
        locator = (By.XPATH, '//*[@id="xnxqid"]')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        select_date = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))
        all_grades = []
        for i in range(len(select_date.options)):                                            # 第一个选项不能用
            if i == len(select_date.options) - 1:
                continue
            each = select_date.options[i + 1]
            print(str(each.text))
            select_date.select_by_visible_text(each.text)
            time.sleep(2)
            search_button = self.browser.find_element_by_xpath('//*[@id="queryform"]/div/table/tbody/tr[1]/td[9]/div/a')
            search_button.click()
            locator = (By.XPATH, '/html/body/div[1]/div/div[4]/table')
            # noinspection PyBroadException
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            table = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[4]/table')
            table_rows = table.find_elements_by_tag_name('tr')[1:]
            grades = []
            for row in table_rows:                                                               # 浏览表格
                grade = []
                datas = row.find_elements_by_tag_name('td')
                for data in datas:
                    # print(data.text)                                                           # debug用
                    grade.append(data.text)
                # print()
                grades.append(grade)
            # print()
            all_grades.append(grades)
            select_date = Select(self.browser.find_element_by_xpath('//*[@id="xnxqid"]'))        # 重新选择选项
        return all_grades

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
        if self.status != 0:
            return self.status
        # 这个按钮不能直接按，需要使用js来按
        empty_classroom_label = self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div/a[3]')
        self.browser.execute_script("arguments[0].click();", empty_classroom_label)
        time.sleep(0.5)
        self.browser.switch_to.frame('iframename')                                              # 切换到另一个frame获取数据
        locator = (By.XPATH, '//*[@id="pageZc1"]')
        # noinspection PyBroadException
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        select_date1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))          # 设定起始周
        select_date2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))          # 设定末尾周
        all_empty_classrooms = []
        for i in range(len(select_date1.options) - 1):                                           # 第一个选项不能用
            each1 = select_date1.options[i + 1]
            each2 = select_date2.options[i + 1]
            print(each1.text)
            select_date1.select_by_visible_text(each1.text)
            select_date2.select_by_visible_text(each2.text)
            time.sleep(0.5)
            search_button = self.browser.find_element_by_xpath('//*[@id="queryform"]/table/tbody/tr/td[11]/div/a')
            search_button.click()
            locator = (By.XPATH, '/html/body/div/div/div[5]/table')
            # noinspection PyBroadException
            try:
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            classrooms = {}
            while True:                                                                         # 浏览所有页面

                table = self.browser.find_element_by_xpath('/html/body/div/div/div[5]/table')
                table_rows = table.find_elements_by_tag_name('tr')[2:]

                for row in table_rows:                                                           # 浏览表格
                    classroom = []
                    rooms = row.find_elements_by_tag_name('td')[1:]
                    # print(row.find_elements_by_tag_name('td')[0].text)
                    for room in rooms:
                        sstr = room.get_attribute('innerHTML')                                     # 检查是否为空
                        if sstr == '\n\t\t\t\t\t      \t \n\t\t\t\t\t      \t <div class=""></div>\n\t\t\t\t\t      \t':
                            classroom.append(1)
                        else:
                            classroom.append(0)
                    # print()                                                                    # debug用
                    classrooms[row.find_elements_by_tag_name('td')[0].text] = classroom
                # noinspection PyBroadException
                try:                                                                            # 切到下一页
                    next_page = self.browser.find_element_by_xpath('/html/body/div/div/div[6]/ul/li[12]/a')
                except Exception:
                    break                                                                       # 如果是最后一页
                next_page.click()
                locator = (By.XPATH, '/html/body/div/div/div[5]/table')
                # noinspection PyBroadException
                try:
                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located(locator))
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -4
                time.sleep(0.5)
            select_date1 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc1"]'))      # 重新选择选项
            select_date2 = Select(self.browser.find_element_by_xpath('//*[@id="pageZc2"]'))      # 重新选择选项
            all_empty_classrooms.append(classrooms)
        return all_empty_classrooms
        """
        if self.status != 1:
            return self.status
        for k in range(2):
            for j in range(2):
                empty_classroom = ''
                i = 0
                params = {
                    'pageNo': j,
                    'pageSize': 20,
                    'pageCount': 9,
                    'pageXnxq': '2019 - 20202',
                    'pageZc1': k,
                    'pageZc2': k
                }
                headers_ec = {
                    'User-Agent': self.user_agent
                }
                while i < 3:
                    try:
                        empty_classroom = self.now.get(url=self.empty_classroom_url, headers=headers_ec,
                                                       params=params)
                        break
                    except requests.exceptions.RequestException as err:
                        print(err)
                        i += 1
                        if i == 3:
                            return 0
                soup = BeautifulSoup(empty_classroom.text, 'lxml')
                print(soup.text)
                table = soup.select('table[class="dataTable"] > tr > td')
                # print(table)
                for each in table:
                    strs = each.get_text()
                    print(strs)

        # print(schedules)
        return ''

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
        soup = BeautifulSoup(schedule.text, 'lxml')
        table = soup.select('table[class="addlist_01"] > tr > td')
        # print(table)
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
