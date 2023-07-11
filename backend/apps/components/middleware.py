import base64
from datetime import datetime

from flask import request, jsonify
from functools import wraps

from itsdangerous import Serializer

from apps.components.common import returnData
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
                return returnData(400, '参数缺失', '')

            '''判断两个key的值是否为空'''
            if openid == '' or session_key == '':
                return returnData(400, '参数缺失', '')

            else:

                '''获取openid 和 token 一致的记录'''
                if LoginSessionCache.query.filter_by(openid=openid, session_key=session_key).first():

                    '''查询该用户的openid'''
                    if Userdata.query.filter_by(openid=openid).first():
                        return func(request, *args, **kwargs)

                    else:
                        return returnData(403, '未授权', '')

                else:
                    return returnData(401, '未登录', '')

        else:
            '''禁止get请求'''
            return returnData(404, '请求方式不正确', '')

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
                return returnData(400, '参数缺失', 'Authorization')
            s = Serializer(SECRET_KEY)
            try:
                payload = s.loads(payload_base64)

                # 提取用户信息
                user_id = payload['user_id']
                username = payload['username']
                user_role = payload['role']
                expires = payload['exp']
                if user_role:

                    # 获取token中的权限列表如果在参数列表中则表示有权限，否则就表示没有权限
                    result = True if user_role in role else False
                    if not result:
                        return returnData(400, "权限不够","")
                if expires < datetime.utcnow().timestamp():
                    # 令牌已过期

                    return returnData(400, "登录已过期", "")

            except Exception as e:
                return returnData(500,"其他错误","")
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
            return returnData(404, '请求方式不正确', '')
    return wrapper

# GET
def requestGET(func=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'GET':
            return func(request, *args, **kwargs)
        else:
            return returnData(404, '该接口不支持POST方式请求', '')
    return wrapper