# -*- coding: utf-8 -*-
import base64
from datetime import datetime, timedelta

from sqlalchemy import Column, String, Integer, Enum, DateTime, Boolean, ForeignKey, Float
from itsdangerous import Serializer
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db
from apps.config.config import SECRET_KEY


class LogonUser(db.Model):
    """用户"""

    __tablename__ = 'logon_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    hash_password = Column(String(120), nullable=False, comment='密码')
    phone = Column(String(20), nullable=False, comment='手机号')
    email = Column(String(20), nullable=True, comment='邮箱')
    avatar = Column(String(100), nullable=True, comment='头像')
    role = Column(Enum('sysadmin', 'admin', 'others'), default='others', nullable=False,
                  comment='权限sysadmin-超级管理员，admin-管理员，others-其他')
    depart = Column(Integer, default=0, nullable=False, comment="默认0--unowned")
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    login_date = Column(DateTime, default=datetime.now, comment="最后登陆时间", nullable=False,
                        onupdate=func.now())
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除该用户')


    def __init__(self, username, hash_password, phone, email=None, avatar=None, role='others', depart=0):
        self.username = username
        self.hash_password = hash_password
        self.phone = phone
        self.email = email
        self.avatar = avatar
        self.role = role
        self.depart = depart
        self.is_lock = False
        self.update()

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
            'exp': expires.timestamp()
        }
        payload_str = s.dumps(payload)


        payload_base64 = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
        token = payload_base64
        return token

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


'''登录状态表'''


class LoginSessionCache(db.Model):
    __tablename__ = 'login_session_cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(255))  # openid
    session_key = Column(String(255))  # token
    update_at = Column(DateTime,default=datetime.now())
    # 定义对象
    def __init__(self, openid=None, session_key=None):
        self.openid = openid
        self.session_key = session_key
        self.update()  # 提交数据

    # 提交数据函数
    def update(self):
        self.update_at=datetime.now()
        db.session.add(self)
        db.session.commit()


'''基础用户数据表'''


class Userdata(db.Model):
    __tablename__ = 'userdata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(255))  # openid
    username = Column(String(255))  # username
    avatar = Column(String(255))  # avatarUrl
    gender = Column(String(255))  # gender
    country = Column(String(255))  # country
    province = Column(String(255))  # province
    city = Column(String(255))  # city
    update_at = Column(DateTime, default=datetime.now())

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
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class BirdInfos(db.Model):
    """鸟类图片声音"""

    __tablename__ = 'bird_image_sound'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_by = Column(String(40), nullable=False, comment='提供者')
    path = Column(String(100), nullable=False, comment='存储路径')
    label = Column(String(40), nullable=False, comment='类型 图片或声音')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除该目录')

    def __init__(self, order_by, path, label, is_lock=False):
        self.order_by = order_by
        self.path = path
        self.label = label
        self.is_lock = is_lock

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class BirdInventory(db.Model):
    """鸟类名录"""

    __tablename__ = 'bird_inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_en = Column(String(40), nullable=False, comment='目英文')
    order_cn = Column(String(40), nullable=False, comment='目中文')
    family_en = Column(String(40), nullable=False, comment='科英文')
    family_cn = Column(String(40), nullable=False, comment='科中文')
    genus = Column(String(40), nullable=False, comment='属')
    species = Column(String(40), nullable=False, comment='种')
    latin_name = Column(String(40), nullable=False, comment='拉丁名')
    geotype = Column(String(40),nullable=True, comment='地理型')
    seasonal = Column(String(200),nullable=True,comment='季节型 逗号分割')
    IUCN = Column(String(40),nullable=True,comment='濒危等级')
    level = Column(String(100),nullable=True,comment='保护等级')
    describe = Column(String(200), nullable=True, comment='描述')
    habitat = Column(String(200), nullable=True, comment='生境')
    behavior = Column(String(200), nullable=True, comment='习性')
    bird_info = Column(String(200), nullable=True, comment='鸟类声音图像信息id 逗号隔开添加')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_check = Column(Boolean,default=False, nullable=False,comment='是否检查')
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除该鸟')

    def __init__(self, order_en, order_cn, family_en, family_cn, genus, species, latin_name, describe=None,
                 habitat=None, behavior=None, bird_info=None):
        self.order_en = order_en
        self.order_cn = order_cn
        self.family_en = family_en
        self.family_cn = family_cn
        self.genus = genus
        self.species = species
        self.latin_name = latin_name
        self.describe = describe
        self.habitat = habitat
        self.behavior = behavior
        self.bird_info = bird_info
        self.is_lock = False

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class BirdRecords(db.Model):
    """鸟类记录"""

    __tablename__ = 'bird_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment='记录用户id')
    bird_id = Column(Integer, ForeignKey('bird_inventory.id'), nullable=False, comment='鸟类名录ID')
    record_time = Column(DateTime, nullable=False, comment='时间')
    record_location = Column(String(200), nullable=False, comment='地点')
    longitude = Column(Float,nullable=False,comment="经度")
    latitude = Column(Float,nullable=False,comment="经度")
    weather = Column(String(40),nullable=False,comment="天气")
    temperature = Column(Float,nullable=False,comment="气温")
    record_describe = Column(String(200), nullable=True, comment='描述')
    bird_info = Column(String(200), nullable=True, comment='鸟类声音图像信息 逗号隔开添加')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_check = Column(Boolean, default=False, nullable=False,comment='是否检查')
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除该记录')

    def __init__(self, user_id, bird_id, record_time, record_location, longitude,latitude,weather,temperature,record_describe=None, bird_info=None,):
        self.user_id = user_id
        self.bird_id = bird_id
        self.record_time = record_time
        self.record_location = record_location
        self.record_describe = record_describe
        self.bird_info = bird_info
        self.longitude = longitude
        self.latitude = latitude
        self.weather = weather
        self.temperature = temperature
        self.is_lock = False

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class BirdSurvey(db.Model):
    """鸟类调查"""

    __tablename__ = 'bird_survey'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment='调查人id')
    survey_name = Column(String(40), nullable=False, comment='调查名称')
    survey_desc = Column(String(200), nullable=True, comment='调查描述')
    survey_time = Column(DateTime, nullable=False, comment='调查时间')
    survey_location = Column(String(200), nullable=False, comment='调查地点')
    describe = Column(String(200), nullable=False, comment='描述')
    habitat = Column(String(200), nullable=False, comment='生境')
    behavior = Column(String(200), nullable=False, comment='习性')
    bird_info = Column(String(200), nullable=False, comment='鸟类声音图像信息,逗号分割')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_check = Column(Boolean, default=False, nullable=False,comment='是否检查')
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除调查')

    def __init__(self, user_id, survey_name, survey_desc=None, survey_time=None, survey_location=None, describe=None,
                 habitat=None, behavior=None, bird_info=None):
        self.user_id = user_id
        self.survey_name = survey_name
        self.survey_desc = survey_desc
        self.survey_time = survey_time
        self.survey_location = survey_location
        self.describe = describe
        self.habitat = habitat
        self.behavior = behavior
        self.bird_info = bird_info
        self.is_lock = False

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class BirdMatch(db.Model):
    """鸟类比赛"""

    __tablename__ = "bird_match"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_create = Column(String(200), nullable=False, comment='举办人/单位')
    match_name = Column(String(60), nullable=False, comment='比赛名称')
    match_desc = Column(String(200), nullable=True, comment='比赛描述')
    match_location = Column(String(200), nullable=False, comment='比赛地点')
    referee = Column(String(200), nullable=False, comment='裁判信息 逗号隔开添加')
    match_image = Column(String(200), nullable=True, comment='比赛banner图片')
    start_time = Column(DateTime, nullable=False, comment='开始时间')
    end_time = Column(DateTime, nullable=False, comment='结束时间')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否删除')

    def __init__(self, match_create, match_name, match_desc, match_location, referee, start_time, end_time):
        self.match_create = match_create
        self.match_name = match_name
        self.match_desc = match_desc
        self.match_location = match_location
        self.referee = referee
        self.start_time = start_time
        self.end_time = end_time
        self.is_lock = False

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()


class MatchGroup(db.Model):
    """比赛小组"""

    __tablename__ = "bird_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("bird_match.id"), nullable=False, comment="比赛id")
    group_name = Column(String(60), unique=True, nullable=False, comment='小组名称')
    group_desc = Column(String(200), nullable=True, comment='小组描述')
    group_user = Column(String(200), nullable=False, comment='小组成员 逗号隔开添加')
    rank = Column(Integer, nullable=True, comment='小组排名')
    create_at = Column(DateTime, default=datetime.now())
    update_at = Column(DateTime, default=datetime.now())
    is_lock = Column(Boolean, default=False, nullable=False, comment='是否结束小组')

    def __init__(self, match_id, group_name, group_desc, group_user):
        self.match_id = match_id
        self.group_name = group_name
        self.group_desc = group_desc
        self.group_user = group_user
        self.rank = None
        self.is_lock = False

    def update(self):
        self.update_at = datetime.now()
        db.session.add(self)
        db.session.commit()
