# coding=utf-8

from libs.yuntongxiong.CCPRestSDK import REST

import ConfigParser

# 主帐号
accountSid = '8aaf0708568d4143015697b0f4960888';

# 主帐号Token
accountToken = '42d3191f0e6745d6a9ddc6c795da0bed';

# 应用Id
appId = '8aaf0708568d4143015697b0f56e088f';

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com';

# 请求端口
serverPort = '8883';

# REST版本号
softVersion = '2013-12-26';


class CCP(object):
    """发送短信的辅助类"""

    def __new__(cls, *args, **kwargs):
        # 判断是否存在类属性_instance，_instance是类CCP的唯一对象，即单例
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    # @classmethod
    # def instance(cls):
    #     """"""
    #     if not hasattr(CCP, "_instance"):
    #         cls._instance = CCP()
    #         cls._instance.rest = REST(serverIP, serverPort, softVersion)
    #         cls._instance.rest.setAccount(accountSid, accountToken)
    #         cls._instance.rest.setAppId(appId)
    #     return  cls._instance



    def send_template_sms(self, to, datas, temp_id):
        """发送模板短信"""
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id

        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        return result.get("statusCode", -1)


# 云通讯官方提供的使用demo案例
# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
#
#             # sendTemplateSMS(手机号码,内容数据,模板Id)

if __name__ == '__main__':
    ccp = CCP()
    ccp.send_template_sms("1851695265", ["888888", "5"], 1)