from rest_framework.response import Response
from rest_framework.views import APIView

from api_exception.exceptions import ArgumentError
from .models import VERSION


class Version(APIView):
    @staticmethod
    def get(request):
        """
        前端调用得到最新版本信息
        访问方法 http://127.0.0.1:8000/version/
        无参数
        返回结果：版本号，更新日期，更新公告，下载地址
        """
        req = request.query_params.dict()

        if len(req) != 0:
            raise ArgumentError()

        data = VERSION.objects.all()
        length = data.count()
        if length > 0:
            return Response(
                data.values("version_number", "update_date", "announcement", "download_address")[length - 1])
        return Response({"version_number": "", "update_date": "", "announcement": "", "download_address": ""})

    @staticmethod
    def post(request):
        """
        pm调用在数据库中插入最新版本信息
        访问方法 http://127.0.0.1:8000/version/
        参数:版本号，更新日期，更新公告，下载地址
        返回结果：插入状态
        """

        req = request.data
        if (len(req) != 4) | (("version_number" not in req) | ("update_date" not in req) |
                              ("announcement" not in req) | ("download_address" not in req)):
            raise ArgumentError()

        if len(VERSION.objects.filter(version_number=req["version_number"])) > 0:
            raise ArgumentError()

        VERSION(version_number=req["version_number"], update_date=req["update_date"],
                announcement=req["announcement"],
                download_address=req["download_address"]).save()

        return Response({"state": "成功"})
