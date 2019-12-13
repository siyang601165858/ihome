import os


settings = dict(
    debug=True,
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    cookie_secret="F3fv87mzTI6fKbP13gUNZI+eZrL1VEzguyX1+AVsRdI=",
    xsrf_cookies=False
)


# Mysql配置参数
mysql_options = dict(
    host='127.0.0.1',
    database='ihome',
    user='root',
    password='mysql'
)


# Redis配置参数
redis_options = dict(host='127.0.0.1')

# 日志文件
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

# 日志等级
log_level = 'debug'

# 密码加秘钥
password_secret = "F3fv87mzTI6fKbP13gUNZI+eZrL1VEzguyX1+AVsRdI="
