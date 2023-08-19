import base64
from datetime import datetime

from flask import request, jsonify
from functools import wraps

from itsdangerous import Serializer

from apps.components.responser import Responser
from apps.config.config import SECRET_KEY
from apps.models import LoginSessionCache, Userdata

# 登录验证
def SingAuth(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            #检验参数
            '''获取openid和token 如果不存在返回None'''
            openid, session_key = request.json.get("openid"), request.json.get("token")
            '''判断是否存在None的jsonkey'''
            if openid == None or session_key == None:
                return Responser.response_error( '参数缺失', 400)

            '''判断两个key的值是否为空'''
            if openid == '' or session_key == '':
                return Responser.response_error( '参数缺失', 400)
            else:
                '''获取openid 和 token 一致的记录'''
                if LoginSessionCache.query.filter_by(openid=openid, session_key=session_key).first():
                    '''查询该用户的openid'''
                    if Userdata.query.filter_by(openid=openid).first():
                        return func(*args, **kwargs)
                    else:
                        return Responser.response_error('未授权', 403)
                else:
                    return Responser.response_error('未登录',401)
        else:
            '''禁止get请求'''
            return Responser.response_error( '请求方式不正确',404)

    return wrapper


def login_required(*role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            try:
                # 在请求头上拿到token
                token = request.headers["Authorization"]
                payload_base64 = base64.b64decode(token.encode('utf-8')).decode('utf-8')
            except Exception as e:
                # 没接收的到token,给前端抛出错误
                return Responser.response_error('参数缺失',401)
            s = Serializer(SECRET_KEY)
            try:
                payload = s.loads(payload_base64)
                # 提取用户信息
                user_id = payload['user_id']
                username = payload['username']
                user_role = payload['role']
                expires = payload['exp']
                if expires < datetime.utcnow().timestamp():
                    # 令牌已过期

                    return Responser.response_error("登录已过期",400)
                if user_role:

                    # 获取token中的权限列表如果在参数列表中则表示有权限，否则就表示没有权限
                    result = True if user_role in role else False
                    if not result:
                        return Responser.response_error("权限不够",400)


            except Exception as e:
                return Responser.response_error("其他错误",500)
            return func(*args, **kw)

        return wrapper
    return decorator


# POST
def requestPOST(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        else:
            return Responser.response_error('请求方式错误', 404)
    return wrapper

# GET
def requestGET(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            return func(request, *args, **kwargs)
        else:
            return Responser.response_error('请求方式错误', 404)
    return wrapper