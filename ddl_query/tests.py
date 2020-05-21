from django.test import TestCase
from course_query.models import Student
from .models import DDL, SchoolYear


class DdlTests(TestCase):
    def test_get_200(self):
        """
        检测返回状态码为200的get请求
        成功的请求
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        student = Student.objects.get(id="17373349")
        DDL(student_id=student, ddl="2020-03-19 23:55:00", homework="第一次作业",
            state="已提交", course="计算机科学").save()

        response = self.client.get('/ddl/?student_id=17373349')
        self.assertEqual(response.status_code, 200)

    def test_get_401(self):
        """
        检测返回状态码为401的get请求
        1.查询用户不存在
        """
        response = self.client.get('/ddl/?student_id=17373349')
        self.assertEqual(response.status_code, 401)

    def test_get_400(self):
        """
        检测返回状态码为400的get请求
        1.参数名称错误
        2.参数数量错误
        """
        response = self.client.get('/ddl/')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/ddl/?studentid=17373349')
        self.assertEqual(response.status_code, 400)

    def test_post_200(self):
        """
        检测返回状态码为200的post请求
        1.成功返回
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()

        data = {
            "student_id": "17373349",
            "ddl": [
                {
                    "content": [
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第一次作业",
                            "state": "提交"
                        },
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第二次作业",
                            "state": "未提交"
                        }
                    ],
                    "name": "计算机科学方法论"
                },
                {
                    "content": [
                        {
                            "ddl": "",
                            "homework": "第一次作业",
                            "state": "提交"
                        }
                    ],
                    "name": "计算机图形学"
                }
            ]
        }

        response = self.client.post('/ddl/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_400(self):
        """
        检测返回状态码为400的post请求
        1.json包中无key:ddl
        2.ddl时间格式问题
        3.json包中参数不正确
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        data = {
            "student_id": "17373349",
            "dd": [
                {
                    "content": [
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第一次作业",
                            "state": "提交"
                        },
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第二次作业",
                            "state": "未提交"
                        }
                    ],
                    "name": "计算机科学方法论"
                }
            ]
        }
        response = self.client.post('/ddl/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "student_id": "17373349",
            "ddl": [
                {
                    "content": [
                        {
                            "ddl": "2020--3-19 下午11:55",
                            "homework": "第一次作业",
                            "state": "提交"
                        },
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第二次作业",
                            "state": "未提交"
                        }
                    ],
                    "name": "计算机科学方法论"
                }
            ]
        }
        response = self.client.post('/ddl/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "student_id": "17373349",
            "ddl": [
                {
                    "content": [
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第一次作业",
                            "state": "提交"
                        },
                        {
                            "ddl": "2020-3-19 下午11:55",
                            "homework": "第二次作业",
                            "state": "未提交"
                        }
                    ],
                }
            ]
        }
        response = self.client.post('/ddl/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)


class CalendarTests(TestCase):
    def test_get_200(self):
        """
        检测返回状态码为200的get请求
        成功的请求
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        SchoolYear(school_year="2019-2020", first_semester="2019-09-02",
                   winter_semester="2020-01-13", second_semester="2020-02-24",
                   third_semester="2020-06-29", end_semester="2020-09-06").save()
        response = self.client.get('/ddl/Calendar/?student_id=17373349&school_year=2019-2020')
        self.assertEqual(response.status_code, 200)

    def test_get_400(self):
        """
        检测返回状态码为400的get请求
        1.参数名称错误
        2.参数数量错误
        """
        response = self.client.get('/ddl/Calendar/?student_id=17373349&schoo_year=2019-2020')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/ddl/Calendar/?student=17373349')
        self.assertEqual(response.status_code, 400)

    def test_get_401(self):
        """
        检测返回状态码为401的get请求
        数据库中无该用户
        """
        SchoolYear(school_year="2019-2020", first_semester="2019-09-02",
                   winter_semester="2020-01-13", second_semester="2020-02-24",
                   third_semester="2020-06-29", end_semester="2020-09-06").save()
        response = self.client.get('/ddl/Calendar/?student_id=17373349&school_year=2019-2020')
        self.assertEqual(response.status_code, 401)

    def test_get_463(self):
        """
        检测返回状态码为463的get请求
        数据库中无该学年信息
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        SchoolYear(school_year="2018-2019", first_semester="2019-09-02",
                   winter_semester="2020-01-13", second_semester="2020-02-24",
                   third_semester="2020-06-29", end_semester="2020-09-06").save()
        response = self.client.get('/ddl/Calendar/?student_id=17373349&school_year=2019-2020')
        self.assertEqual(response.status_code, 463)

    def test_post_200(self):
        """
        检测返回状态码为200的post请求
        1.成功插入
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()

        data = {
            "school_year": "2019-2020",
            "first_semester": "2019-09-02",
            "winter_semester": "2020-01-13",
            "second_semester": "2020-02-24",
            "third_semester": "2020-06-29",
            "end_semester": "2020-09-06",
            "content": []
        }

        response = self.client.post('/ddl/Calendar/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/ddl/Calendar/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_400(self):
        """
        检测返回状态码为400的post请求
        1.插入的json包格式有问题
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()

        data = {
            "school_year": "2019-2020",
            "first_semester": "2019-09-02",
            "winter_semester": "2020-01-13",
            "second_semester": "2020-02-24",
            "third_semester": "2020-06-29",
            "end_semester": "2020-09-06",
            "contet": [
                {
                    "semester": "2019-2020第一学期",
                    "date": "2019-09-13",
                    "holiday": "中秋节"
                }
            ]
        }

        response = self.client.post('/ddl/Calendar/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)
