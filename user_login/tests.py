from django.test import TestCase

# Create your tests here.
class user_loginTests(TestCase):
    def testGet_200(self):
        '''
        检测返回状态码为200的get请求
        1.爬取所有用户的信息
        2.爬取某一个服务器上用户的信息
        '''
        response = self.client.get('/login/?password=123')
        self.assertEquals(response.status_code, 200)

        response = self.client.get('/login/?password=123&number=1')
        self.assertEquals(response.status_code, 200)
    
    def testGet_500(self):
        '''
        检测返回状态码为500的get请求
        1.密码错误
        '''
        response = self.client.get('/login/?password=12')
        self.assertEquals(response.status_code, 500)
    

    def testPost_200(self):
        '''
        检测返回状态码为200的post请求
        1.成功登录
        '''
        data = {
	        "usr_name":"mushan",
	        "usr_password":"wEYiPWtqkBw4BQQQXfEH2w=="
        }
        response = self.client.post('/login/', content_type= 'application/json', data=data)
        self.assertEquals(response.status_code, 200)

    def testPost_500(self):
        '''
        检测返回状态码为500的post请求
        1.参数数量错误
        2.参数名称错误
        '''
        data = {
	        "usr_name":"mushan",
        }
        response = self.client.post('/login/', content_type= 'application/json', data=data)
        self.assertEquals(response.status_code, 500)

        data = {
	        "usr_name":"mushan",
            "usr_passwor":"zI4MS1ylntJ3TVE32dsImw=="
        }
        response = self.client.post('/login/', content_type= 'application/json', data=data)
        self.assertEquals(response.status_code, 500)

    def testPost_401(self):
        '''
        检测返回状态码为401的post请求
        1.账号密码错误
        '''
        data = {
	        "usr_name":"musha",
	        "usr_password":"wEYiPWtqkBw4BQQQXfEH2w=="
        }
        response = self.client.post('/login/', content_type= 'application/json', data=data)
        self.assertEquals(response.status_code, 401)
    def testPost_402(self):
        '''
        检测返回状态码为402的post请求
        1.账号被锁//未测试因为情况不易出现
        '''

    def testPost_403(self):
        '''
        检测返回状态码为403的post请求
        1.服务器ip被锁//未测试因为情况不易出现
        '''