from rest_framework.exceptions import APIException


class ArgumentError(APIException):
    status_code = 400
    default_detail = "参数数量或者名称错误"
    default_code = 'BadRequest'


class UnAuthorizedError(APIException):
    status_code = 401
    default_detail = "数据库中没有这个学生的信息或账号密码错误"
    default_code = 'UnAuthorized'


class NotFoundError(APIException):
    status_code = 404
    default_detail = "未找到请求的资源"
    default_code = "NotFound"


class AccountLockedError(APIException):
    status_code = 460
    default_detail = "学生学生账号重复登录次数过多被锁定"
    default_code = "AccountLocked"


class IPBannedError(APIException):
    status_code = 461
    default_detail = "爬虫服务器ip被锁"
    default_code = "IPIsBanned"


class DatabasePasswordError(APIException):
    status_code = 462
    default_detail = "爬虫访问数据库密码错误"
    default_code = "PasswordError"


class DatabaseNotExitError(APIException):
    status_code = 463
    default_detail = "数据库中无该学年数据"
    default_code = "non-existent"


class InternalServerError(APIException):
    status_code = 500
    default_detail = "服务器内部错误"
    default_code = "InternalServerError"
