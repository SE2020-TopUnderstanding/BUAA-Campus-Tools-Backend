from rest_framework.response import Response
from rest_framework.views import APIView


class Ping(APIView):
    @staticmethod
    def get():
        # windows环境下测试的时候无法使用
        with open("/root/BUAA-Campus-Tools-Backend/API/nohup.out", "r") as fp:
            info = fp.readlines()
        process = os.popen("ps -A | grep chrome")
        return Response(status=200, data={
            "后端更新时间": "",
            "后端所在PR": "",
            "爬虫上一次活跃时间（显示的是UTC时间，应将这个时间+8小时）": "None",
            "服务器上的Chrome进程": process.read().split("\n"),
            "最新的调试信息（显示最新的50条）": info[-50:]
        })
