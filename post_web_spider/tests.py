from django.test import TestCase
from course_query.models import Student


# Create your tests here.
class ErrorHandlingTests(TestCase):
    def test_post_200(self):
        """
        检测返回状态码为200的post请求
        1.如果数据库中无该学生，返回0
        2.如果数据库中密码不相同，返回-1
        3.如果成功删除返回1
        """
        data = {
            "usr_name": "mushan",
            "password": "2020",
        }
        response = self.client.post('/spider/delete/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], 0)

        Student(usr_name="mushan", usr_password="123", id="17373349", name="hbb", grade=3).save()
        response = self.client.post('/spider/delete/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], -1)

        Student(usr_name="mushan", usr_password="2020", id="17373349", name="hbb", grade=3).save()
        response = self.client.post('/spider/delete/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], 1)

    def test_post_400(self):
        """
        检测返回状态码为400的post请求
        1.参数数量不正确
        2.参数名称不正确
        """
        data = {
            "usr_nam": "mushan",
            "password": "2020",
        }
        response = self.client.post('/spider/delete/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "password": "2020",
        }
        response = self.client.post('/spider/delete/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)
