from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import queue

req_queue = queue.Queue()


class Queue(APIView):
    @staticmethod
    def get(request):
        content = []
        if req_queue.empty():
            return HttpResponse(status=204)
        cur_queue = req_queue.get()
        content.append(cur_queue)
        return Response(content)

    @staticmethod
    def post():
        return HttpResponse(status=201)
