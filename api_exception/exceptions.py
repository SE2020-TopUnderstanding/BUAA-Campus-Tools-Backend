from rest_framework.exceptions import APIException


class ArgumentError(APIException):
    status_code = 400
    default_detail = "参数数量或者名称错误"
    default_code = 'BadRequest'


class UnAuthorizedError(APIException):
    status_code = 401
    default_detail = "数据库中没有这个学生的信息"
    default_code = 'UnAuthorized'


class NotFoundError(APIException):
    status_code = 404
    default_detail = "未找到请求的资源"
    default_code = "NotFound"


class InternalServerError(APIException):
    status_code = 500
    default_detail = "服务器内部错误"
    default_code = "InternalServerError"
