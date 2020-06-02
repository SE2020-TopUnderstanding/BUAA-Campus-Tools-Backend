import time
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from web import WebLogin
from log import Log

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'


class CourseRequest:
    """
    本类将从 course.buaa.edu.cn 网站获取信息
    """
    def __init__(self, user_name, pw):
        # 登陆用的网页地址、user_agent、header等
        self.course_url = 'https://course.e2.buaa.edu.cn/portal'
        self.headers_course = {
            'Referer': 'https://course.e2.buaa.edu.cn/portal',
            'User-Agent': USER_AGENT
        }

        self.status = 1
        self.now = ''                           # 整个爬取过程的session
        login = ''
        for i in range(3):
            login = WebLogin(user_name, pw)     # 登录
            success = login.switch_to_course()  # 切换到课程中心
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
            Log('课程中心登陆失败，login == '', usr_name = ' + user_name)
            return

        # self.get_ddl()                        # debug用
        # self.get_id()                         # debug用

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
        status = -13 : 该学生课程中心设置有问题
        """
        return self.status

    @staticmethod
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

    def get_ddl(self):
        """
        该函数将从 course.buaa.edu.cn 网页获取ddl
        将返回一个列表
        列表数据格式:
        {
            当前课程 : [[作业名, 作业状态, 开放日期, 截止日期], [作业名, 作业状态, 开放日期, 截止日期], ...]
            当前课程 : [[作业名, 作业状态, 开放日期, 截止日期], [作业名, 作业状态, 开放日期, 截止日期], ...]
            ...
        }
        """
        if self.status != 1:
            return self.status
        page = ''
        i = 0
        while i < 3:
            try:
                page = self.now.get(url=self.course_url, headers=self.headers_course, timeout=20)  # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(page) == -1:
            return -12

        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.select('div #otherSitesCategorWrap > ul')                         # 获取所有课程的名称和网址
        lessons = {}

        if len(table) < 1:                                                             # 站点不存在其他站点标签
            return -13

        for each in table[0].contents:
            if each == '\n':
                continue
            lessons[each.contents[1].attrs['title']] = each.contents[1].attrs['href']

        ddls = {}

        for lesson_title, url in lessons.items():
            this_ddls = []
            lesson = ''
            i = 0
            while i < 3:
                try:
                    lesson = self.now.get(url=url, headers=self.headers_course, timeout=20)         # 访问该课程的主页
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(lesson) == -1:
                return -12

            soup = BeautifulSoup(lesson.text, 'lxml')
            table = soup.select('a[class="toolMenuLink"]')                              # 获取该课程的作业的网址
            info_url = ''
            for each in table:
                # print(each.attrs['title'])
                if each.attrs['title'].find('在线发布、提交和批改作业') != -1:
                    info_url = each.attrs['href']
                    break
            if info_url == '':
                continue

            i = 0
            while i < 3:
                try:
                    lesson = self.now.get(url=info_url, headers=self.headers_course, timeout=20)    # 访问作业部分
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(lesson) == -1:
                return -12

            soup = BeautifulSoup(lesson.text, 'lxml')
            table = soup.select('div[class="portletMainWrap"] > iframe')                # 获取iframe的网址
            iframe_url = ''
            for each in table:
                iframe_url = each.attrs['src']
                break

            if iframe_url == '':
                return -12

            i = 0
            while i < 3:
                try:
                    lesson = self.now.get(url=iframe_url, headers=self.headers_course, timeout=20)  # 访问iframe
                    break
                except requests.exceptions.RequestException as err:
                    print(err)
                    i += 1
                    if i == 3:
                        return 0

            if self.check_status(lesson) == -1:
                return -12

            soup = BeautifulSoup(lesson.text, 'lxml')
            table = soup.select('table[class="listHier lines nolines"] > tr')           # 获取所有作业的信息
            for each in table[1:]:
                # print(each.get_text())
                sign = 0
                title = ''
                state = ''
                begin = ''
                end = ''
                for each_cont in each.children:
                    if isinstance(each_cont, Tag):
                        if sign == 1:
                            title = each_cont.get_text().replace('  ', '')
                            title = title.replace('\n', '')
                            title = title.replace('\t', '').lstrip()
                        if sign == 2:
                            state = each_cont.get_text().replace('  ', '')
                            state = state.replace('\n', '')
                            state = state.replace('\t', '').lstrip()
                        if sign == 3:
                            begin = each_cont.get_text().replace('  ', '')
                            begin = begin.replace('\n', '')
                            begin = begin.replace('\t', '').lstrip()
                        if sign == 4:
                            end = each_cont.get_text().replace('  ', '')
                            end = end.replace('\n', '')
                            end = end.replace('\t', '').lstrip()
                        sign += 1
                work_ddls = [title, state, begin, end]
                this_ddls.append(work_ddls)
            ddls[lesson_title] = this_ddls
            time.sleep(1)
        # print(ddls)
        return ddls

    def get_id(self):
        """
        该函数返回该学生的学号
        """
        if self.status != 1:
            return self.status
        page = ''
        i = 0
        while i < 3:
            try:
                page = self.now.get(url=self.course_url, headers=self.headers_course, timeout=20)   # 先获取完整网页
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(page) == -1:
            return -12

        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.select('a[class="toolMenuLink"]')                                  # 获取个人信息的网址
        info_url = ''
        for each in table:
            # print(each.attrs['title'])
            if each.attrs['title'].find('查看和修改我的个人信息') != -1:
                info_url = each.attrs['href']
                break

        if info_url == '':
            return -12
        i = 0
        while i < 3:
            try:
                page = self.now.get(url=info_url, headers=self.headers_course, timeout=20)          # 访问个人信息网址
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(page) == -1:
            return -12

        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.select('div[class="portletMainWrap"] > iframe')                    # 获取iframe的网址
        iframe_url = ''
        for each in table:
            iframe_url = each.attrs['src']
            break

        if iframe_url == '':
            return -12
        i = 0
        while i < 3:
            try:
                page = self.now.get(url=iframe_url, headers=self.headers_course, timeout=20)        # 访问iframe
                break
            except requests.exceptions.RequestException as err:
                print(err)
                i += 1
                if i == 3:
                    return 0

        if self.check_status(page) == -1:
            return -12

        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.select('div[class="shorttext"]')                                   # 获取学号
        stu_id = ''
        for each in table:
            # print(each.get_text())
            strs = each.get_text()
            label = strs.split('\n')[1]
            stu_id = strs.split('\n')[2].replace(' ', '')
            if label == '用户ID':
                break
            stu_id = ''
        if stu_id == '':
            return -12
        return stu_id

    def quit(self):
        """
        该函数结束整个session访问过程
        """
        self.now.close()


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    CourseRequest(USR_NAME, PW)
