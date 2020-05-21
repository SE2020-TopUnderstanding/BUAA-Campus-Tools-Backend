from django.test import TestCase, Client
from course_query.models import Student
from .views import add_request


class RequestTest(TestCase):

    def test_get(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        request = client.get('/request/')
        self.assertEqual(request.status_code, 200)

    def test_post(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        data = {"req_id": "1"}
        request = client.post("/request/", content_type='application/json',
                              data=data)
        self.assertEqual(request.status_code, 200)

    def test_post2(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        data = {"req_id": "1", "usr_name": "xxx", "password": "xxx", "req_type": "xxx"}
        request = client.post("/request/", content_type='application/json',
                              data=data)
        self.assertEqual(request.status_code, 201)

    def test_post3(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        data = {"student_id": "17373010"}
        request = client.post("/request/add_course/?student_id=17373010", content_type='application/json',
                              data=data)
        self.assertEqual(request.status_code, 200)

    def test_post4(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        data = {"student_id": "17373010"}
        request = client.post("/request/ddl/?student_id=17373010", content_type='application/json',
                              data=data)
        self.assertEqual(request.status_code, 200)

    def test_post5(self):
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        add_request('s', '17373010')
        client = Client()
        data = {"student_id": "17373010"}
        request = client.post("/request/score_course/?student_id=17373010", content_type='application/json',
                              data=data)
        self.assertEqual(request.status_code, 200)
