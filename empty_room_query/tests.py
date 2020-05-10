from django.test import TestCase


# Create your tests here.

class emptyRoomModelTests(TestCase):
    def testGet_200(self):
        '''
        检测返回状态码为200的get请求
        '''
        response = self.client.get('/classroom/?campus=学院路校区&date=2020-04-20&section=1,')
        self.assertEqual(response.status_code, 200)

    def testGet_500(self):
        '''
        检测返回状态码为500的get请求
        '''
        response = self.client.get('/classroom/?camus=学院路校区&date=2020-04-20&section=1,')
        self.assertEqual(response.status_code, 500)

        response = self.client.get('/classroom/')
        self.assertEqual(response.status_code, 500)

    def testPost_200(self):
        '''
        检测返回状态码为200的post请求
        '''
        data = {
            "date": "2020-04-20",
            "classroom": [
                {
                    "campus": "学院路校区",
                    "teaching_building": "一号楼",
                    "classroom": "(一)203",
                    "section": "1,2,3,4,5,7,"
                },
                {
                    "campus": "学院路校区",
                    "teaching_building": "一号楼",
                    "classroom": "(一)204",
                    "section": "1,2,3,4,7,"
                },
                {
                    "campus": "学院路校区",
                    "teaching_building": "三号楼",
                    "classroom": "(三)202",
                    "section": "3,4,5,7,8,"
                },
                {
                    "campus": "学院路校区",
                    "teaching_building": "三号楼",
                    "classroom": "(三)202",
                    "section": "3,4,5,7,8,"
                }
            ]
        }
        response = self.client.post('/classroom/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)

    def testPost_500(self):
        '''
        检测返回状态码为500的post请求
        '''
        data = {
            "date": "2020-04-20",
            "clasroom": [
                {
                    "campus": "学院路校区",
                    "teaching_building": "一号楼",
                    "classroom": "(一)203",
                    "section": "1,2,3,4,5,7,"
                }
            ]
        }
        response = self.client.post('/classroom/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 500)
