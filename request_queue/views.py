from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, Http404
from course_query.models import Student

req_id = 0
req_queue = []
pending_work = []


def delete_request(usr_name, password):
    global req_id, req_queue, pending_work
    for item in req_queue[:]:
        if item['usr_name'] == usr_name \
                and item['password'] == password:
            req_queue.remove(item)
            pending_work.remove(item['req_id'])
    return 1


def add_request(req_type, student_id):
    global req_id, req_queue, pending_work
    exist = 0
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise Http404
    for item in req_queue:
        if item['usr_name'] == student.usr_name \
                and item['password'] == student.usr_password \
                and item['req_type'] == req_type:
            exist = 1
            break
    if not exist:
        req_id += 1
        new_request = {'req_id': req_id, 'usr_name': student.usr_name, 'password': student.usr_password,
                       'req_type': req_type}
        req_queue.append(new_request)
        log = open('log.txt', 'a')
        log.write('new request: ')
        log.write(str(new_request))
        log.write('\n')
        pending_work.append(req_id)
        return req_id
    else:
        return -1


class Queue(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        # 爬虫在这里取得request
        if not req:
            if not req_queue:
                return HttpResponse(status=204)
            cur_queue = req_queue.pop(0)
            log = open('log.txt', 'a')
            log.write('request has been sent: ')
            log.write(str(cur_queue))
            log.write('\n')
            return Response(cur_queue)

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
        req = request.data
        if len(req) == 1 and 'req_id' in req.keys():
            cur_id = int(req['req_id'])
            try:
                pending_work.remove(cur_id)
            except ValueError:
                message = '没有这个任务号'
                return HttpResponse(message, status=404)
            return HttpResponse(status=200)
        elif len(req) == 4:
            req_queue.append(req)
            log = open('log.txt', 'a')
            log.write('new request: ')
            log.write(str(req))
            log.write('\n')
            pending_work.append(req['req_id'])
            return HttpResponse(status=201)
        else:
            message = '参数数量不正确，需要为4个或1个且只有\'req_id\'参数'
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
