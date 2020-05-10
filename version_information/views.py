from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseBadRequest, HttpResponse
# Create your views here.

class version(APIView):
    def get(self, request,format=None):
        '''
        前端调用得到最新版本信息
        访问方法 http://127.0.0.1:8000/version/
        无参数
        返回结果：版本号，更新日期，更新公告，下载地址
        '''
        data = Version_t.objects.all()
        length = data.count()
        if length > 0 :
            return Response(data.values("version_number", "update_date",  "announcement", "download_address")[length-1])
        else:
            return Response({"version_number":"", "update_date": "",  "announcement": "", "download_address":""})
    def post(self, request, format=None):
        2
        '''
        pm调用在数据库中插入最新版本信息
        访问方法 http://127.0.0.1:8000/version/
        参数:版本号，更新日期，更新公告，下载地址
        返回结果：插入状态
        '''

        req = request.data
        if len(req) != 4:
            return Response(status=400,data={"state":"参数数量不正确"})
        if (("version_number" not in req) | ("update_date" not in req) 
            | ("announcement" not in req) | ("download_address" not in req)):
            return Response(status=400,data={"state":"参数错误"})
        
        if len(Version_t.objects.filter(version_number=req["version_number"])) > 0:
            return Response(status=400,data={"state":"新版本号已有"})

        
        Version_t(version_number=req["version_number"],update_date=req["update_date"],announcement=req["announcement"], 
                download_address=req["download_address"]).save()
        
        return  Response({"state":"成功"})