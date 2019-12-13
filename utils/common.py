import functools

from utils.response_code import RET


def required_login(funcs):
    """登录状态保持的装饰器"""
    @functools.wraps(funcs)
    def wrapper(request_handler_obj, *args, **kwargs):
        # 根据　get_current_user 方法判断用户是否烟瘴成功,是的话表示登录
        if request_handler_obj.get_current_user():
            funcs(request_handler_obj, *args, **kwargs)
        else:
            # 验证不成功，返回错误信息
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg='请重回新登录'))

    return wrapper