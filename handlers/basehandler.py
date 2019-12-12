# coding:utf-8

import json
import tornado.web

from tornado.web import RequestHandler
from utils.session import Session


class BaseHandler(RequestHandler):
    '''所有请求处理的基类'''
    def prepare(self):
        '''预处理'''
        # 解析请求中的json数据
        if self.request.headers.get('Content-Type', '').startswith("application/json"):
            session_data = self.request.body
            self.json_args = json.loads(session_data)
        else:
            session_data = {}

    # 提供db属性的简写操作
    @property
    def db(self):
        return self.application.db

    # 提供redis的简写操作属性
    @property
    def redis(self):

        return self.application.redis

    # 设置默认的响应报文中header
    def set_default_headers(self) -> None:

        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        '''自定义写会给前端的错误信息格式'''
        # 将错误的描述信息kwargs字典直接使用write方法返回给前端,write自动转换为json
        self.write(kwargs)

    def get_current_user(self):
        '''判断用户是否登录成功'''
        self.session = Session(self)

        return self.session.session_data


class StaticFileHandler(tornado.web.StaticFileHandler):
    '''重写静态文件的处理类,补充设置xsrf  cookie的功能'''
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        # 通过获取xsrf_token的属性，可以自动设置xsrf_token
        self.xsrf_token


class OrderHandler(BaseHandler):
    ''''''