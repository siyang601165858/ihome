import os

from handlers import verifycode
from handlers.basehandler import StaticFileHandler

urls = [
    # 用户管理功能部分
    (r'/api/piccode', verifycode.PictureCodeHandler),   # 图片验证码
    (r'/api/smscode', verifycode.SMSCodeHandler),  # 短信验证码
    (r"/(.*)", StaticFileHandler,
     {"path": os.path.join(os.path.dirname(__file__), "html"), "default_filename": "index.html"})

]