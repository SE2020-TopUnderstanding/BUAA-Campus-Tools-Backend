from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import queue

req_id = 0
req_queue = queue.Queue()
pending_work = []


class Queue(APIView):
    @staticmethod
    def get(request):
        # 爬虫在这里取得request
        content = []
        if req_queue.empty():
            return HttpResponse(status=204)
        cur_queue = req_queue.get()
        content.append(cur_queue)
        return Response(content)

    @staticmethod
    def post(request):
        # 爬虫执行完成时返回完成的request id
        cur_id = int(request.data['req_id'])
        try:
            pending_work.remove(cur_id)
        except ValueError:
            return HttpResponse(status=404)

        return HttpResponse(status=200)
