from user_login.login_request.web import WebGetId
from user_login.login_request.password_utils import Aescrypt, KEY, MODEL, IV, ENCODE_


def get_student_info(username, pswd):
    """
        获取学生基本信息
        输入: 用户名, 密码
        返回:     [stu_id, usr_name, name, grade] -> 成功
                 0 -> 登录教务时请求错误
                -1 -> 不可预知的错误，请参考log信息
                -2 -> 登录状态码是2XX，但不是200
                -3 -> 跳转到未知网页
                -4 -> 请求错误，超时或网络错误
                -5 -> 登陆状态码是4XX或5XX
                -6 -> IP被北航屏蔽
                -7 -> 用户名错误，或者出现验证码
                -8 -> 密码错误
                -9 -> 用户名或密码为空
               -10 -> 账户被锁定了
        密码和专业暂时不能返回
        年级的计算可能出现问题，因为年级是根据学号计算的，请一定注意
    """
    script = Aescrypt(KEY, MODEL, IV, ENCODE_)
    pswd = script.aesdecrypt(pswd)
    return WebGetId(username, pswd).get_student_info()


# 测试用代码
if __name__ == "__main__":
    USR_NAME = input('Your username: ')
    PW = input('Your password: ')
    print(get_student_info(USR_NAME, PW))
