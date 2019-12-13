import os

from handlers import verifycode, passport
from handlers.basehandler import StaticFileHandler

urls = [
    # 用户管理功能部分
    (r'/api/piccode', verifycode.PictureCodeHandler),   # 图片验证码
    (r'/api/smscode', verifycode.SMSCodeHandler),  # 短信验证码
    (r'/api/register', passport.RegisterHandler),   # 用户注册
    (r'/api/login', passport.LoginHandler),  # 用户登录
    (r"/(.*)", StaticFileHandler,
     {"path": os.path.join(os.path.dirname(__file__), "html"), "default_filename": "register.html"})

]