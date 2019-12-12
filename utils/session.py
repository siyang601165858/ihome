

# 1. 保存session数据
#  session_id
#  session_data = {
#
#  }

# 2.  生成session_id

# 3.  设置前端 cookie   session_id

# 4.  自动完成获取cookie, 从redis中读取对应的session数据
import json
import logging
import uuid


class Session(object):

    def __init__(self, request_handler_obj):
        self.request_handler_obj = request_handler_obj
         # 从请求中读取cookie获取session_id
        self.session_id = request_handler_obj.get_secure_cookie('session_id')
        # 如果用户没有session_id, 需要重新生成一个session_id与其对应
        if not self.session_id:
            self.session_id = uuid.uuid4().hex
            self.session_data = {}
            request_handler_obj.set_secure_cookie('session_id', self.session_id)
        else:
            try:
                session_data = request_handler_obj.redis.get('sess_%s' % self.session_id)
            except Exception as e:
                logging.error(e)
                raise e
            # session_data已经过期，返回为None
            if not session_data:
                self.session_data = {}
            else:
                self.session_data = json.loads(session_data)

    def save(self):
        '''保存session_data的数据'''
        # 将session_data序列化为json字符串
        session_data = json.dumps(self.session_data)

        # 将session_data写入redis
        try:
            self.request_handler_obj.redis.setex("sess_%s" % self.session_id, 3600, session_data)

        except Exception as e:
            logging.error(e)
            raise e

    def clear(self):
        '''删除session数据'''
        try:
            self.request_handler_obj.redis.delete('sess_%s' % self.session_id)
        except Exception as e:
            logging.error(e)
            raise e
