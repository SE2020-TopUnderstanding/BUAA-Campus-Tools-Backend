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
        req = request.query_params.dict()
        # 爬虫在这里取得request
        if len(req) == 0:
            content = []
            if req_queue.empty():
                return HttpResponse(status=204)
            cur_queue = req_queue.get()
            content.append(cur_queue)
            return Response(content)

        # 前端在这里取得对应任务是否完成的信息, true为已完成
        elif len(req) == 1 and 'id' in req:
            return Response([{'status': req['id'] not in pending_work}])

        # 其他非法请求
        else:
            return HttpResponse(status=400)

    @staticmethod
    def post(request):
        # 爬虫执行完成时返回完成的request id
        if 'req_id' in request.data.keys():
            cur_id = int(request.data['req_id'])
            try:
                pending_work.remove(cur_id)
            except ValueError:
                return HttpResponse(status=404)

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
