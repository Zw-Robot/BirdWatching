# -*- coding: utf-8 -*-
import base64
from datetime import datetime, timedelta

from itsdangerous import Serializer
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db
from apps.config.config import SECRET_KEY, COOKIE_EXPIRATION


class LogonUser(db.Model):
    """用户"""

    __tablename__ = 'logon_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash_password = db.Column(db.String(120), nullable=False, comment='密码')
    phone = db.Column(db.String(20), nullable=False, comment='手机号')
    email = db.Column(db.String(20), nullable=True, comment='邮箱')
    avatar = db.Column(db.String(100), nullable=True, comment='头像')
    role = db.Column(db.Enum('spuadmin','admin','others'), server_default='2', nullable=False,
                      comment='权限0-超级管理员，1-管理员，2-其他无权限')
    depat_id = db.Column(db.Integer, server_default='0',nullable=False,comment="默认0用户无法登陆")
    is_lock = db.Column(db.Boolean, server_default='false', nullable=False, comment='是否删除该用户')
    create_at = db.Column(db.Date, default=datetime.now)
    update_at = db.Column(db.Date, default=datetime.now)
    login_date = db.Column(db.TIMESTAMP, comment="最后登陆时间", nullable=False,
                           onupdate=func.now())
    # 明文密码（只读）
    @property
    def password(self):
        raise AttributeError('不可读')

    # 写入密码，同时计算hash值，保存到模型中
    @password.setter
    def password(self, value):
        self.hash_password = generate_password_hash(value)

    # 检查密码是否正确
    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    # 生成token
    @staticmethod
    def create_token(user_id, user_name, role, expires_in=3600):
        now = datetime.utcnow()
        # 计算过期时间
        expires = now + timedelta(seconds=expires_in)
        print(expires)
        '''
        生成token
        :return: token
        '''
        s = Serializer(SECRET_KEY)
        payload = {
            'user_id': user_id,
            'username': user_name,
            'role': role,
            'exp': expires.timestamp()  # 将过期时间转换为时间戳
        }
        payload_str = s.dumps(payload)

        # 使用 base64 编码负载字符串
        payload_base64 = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')

        # 生成令牌
        token = payload_base64
        return token


'''登录状态表'''
class LoginSessionCache(db.Model):
    __tablename__ = 'login_session_cache'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(255))  # openid
    session_key = db.Column(db.String(255))  # token

    # 定义对象
    def __init__(self, openid=None, session_key=None):
        self.openid = openid
        self.session_key = session_key
        self.update()  # 提交数据

    # 提交数据函数
    def update(self):
        db.session.add(self)
        db.session.commit()


'''基础用户数据表'''
class Userdata(db.Model):
    __tablename__ = 'userdata'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(255))  # openid
    username = db.Column(db.String(255))  # username
    avatar = db.Column(db.String(255))  # avatarUrl
    gender = db.Column(db.String(255))  # gender

    country = db.Column(db.String(255))  # country
    province = db.Column(db.String(255))  # province
    city = db.Column(db.String(255))  # city

    # 定义对象
    def __init__(self, openid=None, username=None, avatar=None, gender=None, country=None, province=None, city=None):
        self.openid = openid
        self.username = username
        self.avatar = avatar
        self.gender = gender
        self.country = country
        self.province = province
        self.city = city
        self.update()  # 提交数据

    # 提交数据函数
    def update(self):
        db.session.add(self)
        db.session.commit()
