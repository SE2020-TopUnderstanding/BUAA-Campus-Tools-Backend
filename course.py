import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from vpn import VpnLogin


class CourseRequest:
    """
    本类将从 course.buaa.edu.cn 网站获取信息
    """
    def __init__(self, user_name, pw):
        self.status = 0
        vpn = ''
        for i in range(3):
            vpn = VpnLogin(user_name, pw)  # 登录
            success = vpn.switch_to_course()      # 切换到课程中心
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
        self.browser = vpn.get_browser()         # 获取浏览器.
        # self.getDdl()                           # debug用

    def get_status(self):
        """
        初始化的结果
        status =  0 : 成功
        status = -1 : 登陆错误
        status = -2 : 超时3次
        status = -3 : 未知错误
        status = -5 : IP被封
        status = -6 : 用户名错误或者网站要求输入验证码
        status = -7 : 密码错误
        status = -8 : 用户名或密码为空
        status = -9 : 账号被锁
        """
        return self.status

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
        if self.status != 0:
            return self.status
        # noinspection PyBroadException
        try:
            cur_lessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
        except Exception:
            print('timeout or this guy redefined the network')
            time.sleep(5)
            # noinspection PyBroadException
            try:
                cur_lessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
            except Exception:
                print('this guy redefined the network')
                return -10
        lessons = cur_lessons.find_elements_by_xpath('li')                                       # 获取所有课程
        ddls = {}
        for i in range(len(lessons)):
            link = lessons[i].find_elements_by_xpath('a')[0]
            # print(link.get_attribute('href'))
            cur_lesson = link.get_attribute('title')                                             # 获取课程名字
            # print(curLesson)
            link = link.get_attribute('href')

            self.browser.get(link)                                                              # 切换到该课程页面
            locator = (By.XPATH, '//*[@id="toolMenu"]/ul')
            # noinspection PyBroadException
            try:
                WebDriverWait(self.browser, 5).until(Ec.presence_of_element_located(locator))
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            work_buttons = self.browser.find_element_by_xpath('//*[@id="toolMenu"]/ul')
            work_buttons = work_buttons.find_elements_by_tag_name('a')
            work_button = 0
            for each in work_buttons:
                if each.get_attribute('title') == '在线发布、提交和批改作业':
                    work_button = each
                    break
            if work_button == 0:
                self.browser.switch_to.default_content()                                            # 重新获取下一个课程
                cur_lessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
                lessons = cur_lessons.find_elements_by_xpath('li')
                continue

            work_button.click()
            frame = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div/div/div[2]/iframe')
            self.browser.switch_to.frame(frame)                                                 # 切换到另一个frame获取数据
            locator = (By.XPATH, '/html/body/div')
            # noinspection PyBroadException
            try:
                WebDriverWait(self.browser, 5).until(Ec.presence_of_element_located(locator))
            except Exception:
                print('timeout or switch to an unknown page')
                return -4
            # noinspection PyBroadException
            try:
                self.browser.find_element_by_xpath('/html/body/div/form/table')                 # 检查是否存在作业
            except Exception:
                # noinspection PyBroadException
                try:
                    self.browser.find_element_by_xpath('/html/body/div/p')
                    # print('no homework founded\n')
                    ddls[cur_lesson] = []

                    self.browser.switch_to.default_content()
                    time.sleep(0.5)
                    cur_lessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
                    lessons = cur_lessons.find_elements_by_xpath('li')                           # 如果没有作业

                    continue
                except Exception:
                    print('timeout or switch to an unknown page')
                    return -4
            table = self.browser.find_element_by_xpath('/html/body/div/form/table')
            table_rows = table.find_elements_by_tag_name('tr')[1:]
            jobs = []
            for row in table_rows:                                                               # 获取作业信息
                datas = row.find_elements_by_tag_name('td')[1:]
                work = []
                if len(datas) >= 1:
                    title = datas[0].find_elements_by_tag_name('a')
                    if title:
                        title = title[0]
                    else:
                        title = datas[0].find_elements_by_tag_name('span')[0]
                    title = title.text
                    # print(title)
                    work.append(title)
                if len(datas) >= 2:
                    status = datas[1].text
                    # print(status)
                    work.append(status)
                if len(datas) >= 3:
                    opendate = datas[2].text
                    # print(opendate)
                    work.append(opendate)
                if len(datas) >= 4:
                    duedate = datas[3].find_elements_by_tag_name('span')
                    if duedate:
                        duedate = duedate[0].text
                    else:
                        duedate = datas[3].text
                    # print(duedate)
                    work.append(duedate)
                while len(work) < 4:
                    work.append('')
                # print()
                jobs.append(work)
            ddls[cur_lesson] = jobs

            self.browser.switch_to.default_content()                                            # 重新获取下一个课程
            time.sleep(0.5)
            cur_lessons = self.browser.find_element_by_xpath('//*[@id="otherSitesCategorWrap"]/ul[1]')
            lessons = cur_lessons.find_elements_by_xpath('li')
        return ddls

    def get_id(self):
        if self.status != 0:
            return self.status
        # noinspection PyBroadException
        try:
            name_button = self.browser.find_element_by_xpath('//*[@id="toolMenu"]/ul/li[9]/a')
        except Exception:
            print('timeout or switch to an unknown page')
            return -4
        name_button.click()
        frame = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div/div/div[2]/iframe')
        self.browser.switch_to.frame(frame)                                                 # 切换到另一个frame获取数据
        time.sleep(0.5)
        stu_id = self.browser.find_element_by_xpath('//*[@id="userViewForm"]/fieldset/div[1]')
        stu_id = stu_id.text
        self.browser.switch_to.default_content()
        time.sleep(0.5)
        return stu_id.split(' ')[1]

    def quit(self):
        self.browser.quit()


# 测试用
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    CourseRequest(USR_NAME, PW)
