import logging
import random
import re

import constants
from handlers.basehandler import BaseHandler
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP

from utils.response_code import RET


class PictureCodeHandler(BaseHandler):
    '''图片验证码'''

    def get(self):
        # 获取前端传回来的图片验证码编号
        cur_pic_id = self.get_argument('cur_pic_id')
        pre_pic_id = self.get_argument('pre_pic_id')

        # 生成图片验证码
        text, pic = captcha.generate_captcha()
        # 将验证码对应文本放入redis缓存中
        print(text)
        print(cur_pic_id)
        try:
            self.redis.setex('piccode_%s' % cur_pic_id, 360, text)
            # print(self.redis.expires(cur_pic_id))
        except Exception as e:
            logging.error(e)
            self.write('')

        else:
            try:
                self.delete('piccode_%s' % pre_pic_id)
            except Exception as e:
                logging.error(e)
            self.write(pic)
            self.set_header('Content-Type', 'image/jpg')


class SMSCodeHandler(BaseHandler):
    '''短信验证码'''
    def post(self):

        # 获取参数
        mobile = self.json_args.get('mobile')
        piccode_id = self.json_args.get('piccode_id')
        piccode_text = self.json_args.get('piccode_text')

        print(mobile)
        print(piccode_text)
        # 参数校验
        if not all([mobile, piccode_id, piccode_text]):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='缺少参数'))

        # 手机格式校验
        if not re.match(r'^[1]([3-9])[0-9]{9}$', mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='手机号格式错误'))

        # 验证图片验证码
        try:
            real_piccode_text = self.redis.get("piccode_%s" % piccode_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='查询redis出错'))

        # 验证验证码是否过期
        if not real_piccode_text:
            return self.write(dict(errcode=RET.PARAMERR, errmsg='验证码过期'))

        # 判断验证码是否正确
        if real_piccode_text.lower().decode() != piccode_text.lower():
            return self.write(dict(errcode=RET.PARAMERR, errmsg='验证码输入错误'))

        # 验证完成后删除redis中的图片验证码数据
        try:
            self.redis.delete('piccode_%s' % piccode_id)
        except Exception as e:
            logging.error(e)

        #判断手机是否注册过
        try:
            sql = 'select count(*) counts from ih_user_profile where up_mobile=%s'
            ret = self.db.get(sql, mobile)
            print(ret)
            print(ret['counts'])
        except Exception as e:
            logging.error(e)
        else:
            if ret['counts'] > 0:

                return self.write(dict(errcode=RET.DATAERR, errmsg='该手机号已经注册过'))

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        print(sms_code)

        # 发送短信验证码
        try:
            ccp = CCP()
            result = ccp.send_template_sms(mobile, [sms_code, str(constants.SMS_CODE_REDIS_EXPIRES/60)], 1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg='发送短信验证码失败'))

        try:
            self.redis.setex('smscode_%s' % mobile, 360, sms_code)
            # print(self.redis.expires(cur_pic_id))
        except Exception as e:
            logging.error(e)
            self.write('')

        if '000000' == result:
            return self.write(dict(errcode=RET.OK, errmsg='发送成功'))
        else:
            return self.write(dict(errcode=RET.THIRDERR, errmsg='发送出现了问题' ))