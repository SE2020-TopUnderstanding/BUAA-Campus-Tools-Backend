from rest_framework.response import Response
from rest_framework.views import APIView

class Ping(APIView):
    @staticmethod
    def get(request):
        return Response(status=200, data={
            "后端更新时间": "",
            "后端所在PR": "",
            "爬虫上一次活跃时间": 
        })
