from django.test import TestCase
from version_information.models import VERSION


# Create your tests here.
class VersionInformationTests(TestCase):
    def test_get_200(self):
        """
        检测返回状态码为200的get请求
        1.数据库中无数据
        2.数据库中有数据
        """
        response = self.client.get('/version/')
        self.assertEqual(response.status_code, 200)

        VERSION(version_number='1.01', update_date='2020-1-20', announcement="第一次",
                download_address='22/21').save()
        response = self.client.get('/version/')
        self.assertEqual(response.status_code, 200)

    def test_post_200(self):
        """
        检测返回状态码为200的post请求
        1.成功插入相应版本
        """
        data = {
            "version_number": "1.1.1",
            "update_date": "2020",
            "announcement": "hh",
            "download_address": "22"
        }
        response = self.client.post('/version/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_400(self):
        """
        检测返回状态码为400的post请求
        1.版本号已存在
        2.参数数量不对
        3.参数名称不对
        """
        data = {
            "version_number": "1.1.1",
            "update_date": "2020",
            "announcement": "hh",
            "download_address": "22"
        }
        self.client.post('/version/', content_type='application/json', data=data)
        response = self.client.post('/version/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "update_date": "2020",
            "announcement": "hh",
            "download_address": "22"
        }
        response = self.client.post('/version/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            "version_number": "1.1.1",
            "update_date": "2020",
            "announcement": "hh",
            "download_addres": "22"
        }
        response = self.client.post('/version/', content_type='application/json', data=data)
        self.assertEqual(response.status_code, 400)
