from django.test import TestCase, Client
from .views import Student


# Create your tests here.
class CourseGetTest(TestCase):

    def test_get_success(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.get("/timetable/?student_id=17373010&week=all")
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        client = Client()
        response = client.get("/timetable/?student_id=17373011&week=all")
        self.assertEqual(response.status_code, 401)

    def test_bad_request1(self):
        client = Client()
        response = client.get("/timetable/")
        self.assertEqual(response.status_code, 400)

    def test_bad_request2(self):
        client = Client()
        response = client.get("/timetable/?student=17373011&week=all")
        self.assertEqual(response.status_code, 400)

    def test_this_week(self):
        client = Client()
        response = client.get("/timetable/?date=2020-4-19")
        self.assertEqual(response.status_code, 200)

    def test_this_week_bad(self):
        client = Client()
        response = client.get("/timetable/?dae=2020-4-19")
        self.assertEqual(response.status_code, 400)

    def test_post2(self):
        client = Client()
        response = client.post("/timetable/", content_type='application/json',
                               data={"student_id": "17373010",
                                     "info": [["计算机网络", "(一)305", "荣文戈", "1-16", "周1 第3，4节"]]})
        self.assertEqual(response.status_code, 401)

    def test_post3(self):
        client = Client()
        student = Student(id='17373010', name='xxx', usr_name='xxx', usr_password='xxx', grade='2')
        student.save()
        response = client.post("/timetable/", content_type='application/json',
                               data={"student_id": "17373010",
                                     "info": [["(一)305", "荣文戈", "1-16", "周1 第3，4节"]]})
        self.assertEqual(response.status_code, 400)
