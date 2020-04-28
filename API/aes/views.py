from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseBadRequest, HttpResponse
from user_login.LoginRequest.Password import *
# Create your views here.

password = "123"

class aes(APIView):
    def get(self, request, format=None):
        '''
        给定一个文本，和调用aes方法的密码，返回加密后的文本
        调用方法http://127.0.0.1:8000/aes/?text=17373349&password=123

        密码错误或参数错误都返回错误状态500
        '''
        req = request.query_params.dict()

        if (len(req) != 2) | ("text" not in req) | ("password" not in req):
            return HttpResponse(status=500)
        if (req["password"] != password):
            return HttpResponse(status=500)
        
        pr = aescrypt(key,model,iv,encode_)
        text = pr.aesencrypt(req["text"])

        return Response({"text":text})