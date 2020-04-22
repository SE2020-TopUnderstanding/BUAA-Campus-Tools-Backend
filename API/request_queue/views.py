from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from course_query.models import Student
from request_queue.models import TimeInfo
import queue

req_id = 0
req_queue = queue.Queue()
pending_work = []


def add_request(req_type, student_id):
    global req_id, req_queue, pending_work
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise Http404
    req_id += 1
    req_queue.put(
        {'req_id': req_id, 'usr_name': student.usr_name, 'password': student.usr_password,
         'req_type': req_type})
    pending_work.append(req_id)
    return req_id


class Queue(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        # 爬虫在这里取得request
        if len(req) == 0:
            timeinfo = TimeInfo.objects.filter(id=1)
            if timeinfo.exists():
                timeinfo[0].save()
            else:
                time = TimeInfo()
                time.save()
            content = []
            if req_queue.empty():
                return HttpResponse(status=204)
            cur_queue = req_queue.get()
            content.append(cur_queue)
            return Response(content)

        # 前端在这里取得对应任务是否完成的信息, true为已完成
        elif len(req) == 1 and 'id' in req:
            return Response([{'status': int(req['id']) not in pending_work}])

        # 其他非法请求
        else:
            message = '参数数量个数或名称错误，只能为0个，或1个且是\'id\''
            return HttpResponse(message, status=400)

    @staticmethod
    def post(request):
        # 爬虫执行完成时返回完成的request id
        if 'req_id' in request.data.keys():
            cur_id = int(request.data['req_id'])
            try:
                pending_work.remove(cur_id)
            except ValueError:
                message = '没有这个任务号'
                return HttpResponse(message, status=404)

            return HttpResponse(status=200)
        else:
            message = '没有\'req_id\'参数'
            return HttpResponse(message, status=400)


class CourseRequest(APIView):
    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('s', req['student_id'])
            return Response([{"id": request_id}])
        else:
            message = '参数数量或名称错误，只能为1个且为\'student_id\''
            return HttpResponse(message, status=400)


class RoomRequest(APIView):
    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('e', req['student_id'])
            return Response([{"id": request_id}])
        else:
            message = '参数数量或名称错误，只能为1个且为\'student_id\''
            return HttpResponse(message, status=400)


class DDLRequest(APIView):
    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('d', req['student_id'])
            return Response([{"id": request_id}])
        else:
            message = '参数数量或名称错误，只能为1个且为\'student_id\''
            return HttpResponse(message, status=400)


class ScoreRequest(APIView):

    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('g', req['student_id'])
            return Response([{"id": request_id}])
        else:
            message = '参数数量或名称错误，只能为1个且为\'student_id\''
            return HttpResponse(message, status=400)


class TestsRequest(APIView):

    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('t', req['student_id'])
            return Response([{"id": request_id}])
        else:
            message = '参数数量或名称错误，只能为1个且为\'student_id\''
            return HttpResponse(message, status=400)
