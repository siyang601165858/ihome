import hashlib
import logging
import re

import config
from handlers.basehandler import BaseHandler
from utils.response_code import RET
from utils.session import Session


class RegisterHandler(BaseHandler):
    '''注册'''

    def post(self):
        ''''''
        # 接收参数
        # 手机号
        mobile = self.json_args.get('mobile')
        # 短信验证码
        smscode = self.json_args.get('phonecode')
        # 密码
        password = self.json_args.get('password')

        # 校验参数
        if not all([mobile, smscode, password]):

            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺少'))

        if not re.match(r'^1\d{10}$', mobile):
            return self.write((dict(errcode=RET.PARAMERR, errmsg='手机号码格式错误')))

        # 为方便调试，不用每次发送短信,留一个万能验证码
        if '123456' != smscode:
            # 业务逻辑
            # 校验短信啊验证码
            try:

                real_smscode = self.redis.get('smscode_%s' % mobile)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errcode=RET.PARAMERR, errmsg='redis读取验证码错误'))
            # 判断验证码是否过期
            if not real_smscode:
                return self.write(dict(errcode=RET.PARAMERR, errmsg='验证码过期'))

            # 判断验证码是否正确
            print(real_smscode, smscode)
            if real_smscode.decode() != smscode:
                return self.write(dict(errcode=RET.PARAMERR, errmsg='验证码输入有误'))

            # 删除redis中的smscode
            try:
                self.redis.delete('smscode_%s' % mobile)
            except Exception as e:
                logging.error(e)

        # 操作数据库，保存用户信息
        sql = "insert ih_user_profile(up_name, up_mobile, up_passwd) values(%(name)s, %(mobile)s, %(password)s);"
        password = hashlib.sha256((password+config.password_secret).encode()).hexdigest()
        try:
            user_id = self.db.execute(sql, name=mobile, mobile=mobile, password=password)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DATAERR, errmsg='用户已经注册'))

        # 保存用户登录状态
        try:
            session = Session(self)
            session.session_data['user_id'] = user_id
            session.session_data['name'] = mobile
            session.session_data['mobile'] = mobile
            print(session)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.LOGINERR, errmsg='session数据保存失败'))

        return self.write(dict(errcode=RET.OK, errmsg='注册成功', user_id=user_id))


class LoginHandler(BaseHandler):
    """登录"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get('mobile')
        password = self.json_args.get('password')

        # 检查参数
        if not all([mobile, password]):

            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数缺失'))

        if not re.match(r'^[1]\d{10}$', mobile):

            return self.write(dict(errcode=RET.DATAERR, errmsg='手机号格式错误'))

        # 检查密码是否正确
        res = self.db.get("select up_user_id,up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s",
                          mobile=mobile)
        password = hashlib.sha256((password+config.password_secret).encode()).hexdigest()
        print(password, res['up_passwd'])
        print(res)
        if res and res['up_passwd'] == password:
            # 生成session数据
            # 返回客户端
            try:
                self.session = Session(self)
                self.session.session_data['user_id'] = res['up_user_id']
                self.session.session_data['name'] = res['up_name']
                self.session.session_data['mobile'] = mobile
                self.session.save()

            except Exception as e:
                logging.error(e)
            else:
                return self.write(dict(errcode=RET.OK, errmsg='成功'))
        else:
            return self.write(dict(errcode=RET.DATAERR, errmsg='密码输入错误'))

