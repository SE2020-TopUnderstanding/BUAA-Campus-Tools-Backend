from django.test import TestCase
from .models import DDL_t
from course_query.models import Student


# Create your tests here.
class ddlTests(TestCase):
    def testGet_200(self):
        '''
        检测返回状态码为200的get请求
        成功的请求
        '''
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        student = Student.objects.get(id="17373349")
        DDL_t(student_id=student, ddl="2020-03-19 23:55:00", homework="第一次作业",
              state="已提交", course="计算机科学").save()

        response = self.client.get('/ddl/?student_id=17373349')
        self.assertEquals(response.status_code, 200)

    def testGet_401(self):
        '''
        检测返回状态码为401的get请求
        1.查询用户不存在
        '''
        response = self.client.get('/ddl/?student_id=17373349')
        self.assertEquals(response.status_code, 401)

    def testGet_500(self):
        '''
        检测返回状态码为500的get请求
        1.参数名称错误
        2.参数数量错误
        '''
        response = self.client.get('/ddl/')
        self.assertEquals(response.status_code, 500)

        response = self.client.get('/ddl/?studentid=17373349')
        self.assertEquals(response.status_code, 500)

    def testPost_200(self):
        '''
        检测返回状态码为200的post请求
        1.成功返回
        '''
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
        self.assertEquals(response.status_code, 200)

    def testPost_400(self):
        '''
        检测返回状态码为400的post请求
        1.json包中参数不正确
        '''
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
                }
            ]
        }
        response = self.client.post('/ddl/', content_type='application/json', data=data)
        self.assertEquals(response.status_code, 400)

    def testPost_500(self):
        '''
        检测返回状态码为500的post请求
        1.json包中无key:ddl
        2.ddl时间格式问题
        '''
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
        self.assertEquals(response.status_code, 500)

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
        self.assertEquals(response.status_code, 500)
