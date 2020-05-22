from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from course_query.models import Student
from api_exception.exceptions import ArgumentError, UnAuthorizedError, NotFoundError

REQ_ID = 0
REQ_QUEUE = []
PENDING_WORK = []


def delete_request(usr_name, password):
    global REQ_ID, REQ_QUEUE, PENDING_WORK
    for item in REQ_QUEUE[:]:
        if item['usr_name'] == usr_name \
                and item['password'] == password:
            REQ_QUEUE.remove(item)
            PENDING_WORK.remove(item['req_id'])
    return 1


def add_request(req_type, student_id):
    global REQ_ID, REQ_QUEUE, PENDING_WORK
    exist = 0
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise UnAuthorizedError()
    for item in REQ_QUEUE:
        if item['usr_name'] == student.usr_name \
                and item['password'] == student.usr_password \
                and item['req_type'] == req_type:
            exist = 1
            break
    if not exist:
        REQ_ID += 1
        new_request = {'req_id': REQ_ID, 'usr_name': student.usr_name, 'password': student.usr_password,
                       'req_type': req_type}
        REQ_QUEUE.append(new_request)
        log = open('log.txt', 'a')
        log.write('new request: ')
        log.write(str(new_request))
        log.write('\n')
        PENDING_WORK.append(REQ_ID)
        return REQ_ID
    return -1


class Queue(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        # 爬虫在这里取得request
        if not req:
            if not REQ_QUEUE:
                return HttpResponse(status=204)
            cur_queue = REQ_QUEUE.pop(0)
            log = open('log.txt', 'a')
            log.write('request has been sent: ')
            log.write(str(cur_queue))
            log.write('\n')
            return Response(cur_queue)

        # 前端在这里取得对应任务是否完成的信息, true为已完成
        if len(req) == 1 and 'id' in req:
            return Response([{'status': int(req['id']) not in PENDING_WORK}])

        # 其他非法请求
        raise ArgumentError()

    @staticmethod
    def post(request):
        # 爬虫执行完成时返回完成的request id
        req = request.data
        if len(req) == 1 and 'req_id' in req.keys():
            cur_id = int(req['req_id'])
            try:
                PENDING_WORK.remove(cur_id)
            except ValueError:
                raise NotFoundError(detail='没有这个任务号')
            return HttpResponse(status=200)
        if len(req) == 4:
            REQ_QUEUE.append(req)
            log = open('log.txt', 'a')
            log.write('new request: ')
            log.write(str(req))
            log.write('\n')
            PENDING_WORK.append(req['req_id'])
            return HttpResponse(status=201)
        raise ArgumentError()


class AddCourseRequest(APIView):
    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1:
            request_id = add_request('l', req['student_id'])
            return Response([{"id": request_id}])
        raise ArgumentError()


class DDLRequest(APIView):
    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('d', req['student_id'])
            return Response([{"id": request_id}])
        raise ArgumentError()


class ScoreOrCourseRequest(APIView):

    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('j', req['student_id'])
            return Response([{"id": request_id}])
        raise ArgumentError()


class TestsRequest(APIView):

    @staticmethod
    def post(request):
        req = request.query_params.dict()
        if len(req) == 1 and 'student_id' in req.keys():
            request_id = add_request('t', req['student_id'])
            return Response([{"id": request_id}])
        raise ArgumentError()
