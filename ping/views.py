from rest_framework.response import Response
from rest_framework.views import APIView
from course_query.models import Student
from request_queue.models import RequestRecord


class Ping(APIView):
    @staticmethod
    def get(request):
        # windows环境下测试的时候无法使用
        with open("/root/BUAA-Campus-Tools-Backend/nohup.out", "r") as file:
            info = file.readlines()
        return Response(status=200, data={
            "后端更新时间": "2020-04-29",
            "后端所在PR": "#136 与爬虫新login的结合",
            "后端注册用户数": len(Student.objects.all()),
            "各项功能访问次数": RequestRecord.objects.values(),
            "最新的调试信息（显示最新的100条）": info[-100:]
        })
