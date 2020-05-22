from django.test import TestCase
from course_query.models import Student
from .models import Feedback


# Create your tests here.
class UserLoginTests(TestCase):
    def test_get_200(self):
        """
        检测返回状态码为200的get请求
        1.获取所有反馈
        2.获取某一天的反馈
        3。获取某一类的反馈
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        student = Student.objects.get(id="17373349")
        Feedback(student_id=student, kind="bug", content="ddl有问题").save()

        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/feedback/?date=2020-05-14')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/feedback/?kind=bug')
        self.assertEqual(response.status_code, 200)

    def test_get_400(self):
        """
        检测返回状态码位400的get请求
        1.参数数量错误
        2.参数名称错误
        :return:
        """
        response = self.client.get('/feedback/?a=1&b=2&c=3')
        self.assertEqual(response.status_code, 400)

        response = self.client.get('/feedback/?data=2020-05-14')
        self.assertEqual(response.status_code, 400)

    def test_post_200(self):
        """
        检测返回状态码为200的post请求
        1.成功登录
        """
        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()

        data = {
            "student_id": "17373349",
            "kind": "bug",
            "content": "ddl错误"
        }
        response = self.client.post('/feedback/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_400(self):
        """
        检测返回状态码为400的post请求
        1.传入json包名称错误
        2.传入json包数量错误
        """
        data = {
            "student_id": "17373349",
            "kind": "bug",
        }
        response = self.client.post('/feedback/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "student_id": "17373349",
            "kind": "bug",
            "conten": "ddl错误"
        }
        response = self.client.post('/feedback/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_401(self):
        """
        检测返回状态码为401的post请求
        1.数据库中无该学生数据
        """
        Student(usr_name="mushan", usr_password="123", id="17373348", name="hbb", grade=3).save()

        data = {
            "student_id": "17373349",
            "kind": "bug",
            "content": "ddl错误"
        }
        response = self.client.post('/feedback/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 401)
