import math

from apps.auth import service, auth
from apps.components.common import required_attrs_validator
from apps.models import LogonUser, Userdata, LoginSessionCache
from apps.components.middleware import requestPOST, SingAuth, login_required, requestGET
from apps.components.responser import Responser, FileResponser

'''登录接口'''


def calculate_level(score):
    level = math.floor(math.sqrt(score))
    return level


@auth.route('/sgin', methods=["GET", "POST"], endpoint='auth_login')
@requestPOST
# @SingAuth
def auth_login(request):
    code, msg, json = service.login(request)
    if code == 200:
        return Responser.response_success(data=json, msg=msg)
    else:
        return Responser.response_error(msg=msg)


@auth.route('/get_score', methods=["POST"])
@requestPOST
@SingAuth
def get_score(request):
    tmp = request.json
    openid = tmp.get("openid")  # openid
    user = Userdata.query.filter_by(openid=openid).first()
    if user:
        return Responser.response_success(data={"id": user.id, "level": calculate_level(user.score)}, msg="success")
    else:
        return Responser.response_error("尚未登陆！")


@auth.route('/info', methods=["GET", "POST"], endpoint='info')
@requestPOST
def get_info(request):
    tmp = request.json
    openid = tmp.get("openid")  # openid
    # try:
    #     params = getWXInfo(sessionKey=secession, encryptedData=encryptedData, iv=iv)
    # except:
    params = tmp.get("userInfo")
    username = params.get("nickName")  # username
    avatar = params.get("avatarUrl")  # avatarUrl
    gender = params.get("gender")  # gender
    country = params.get("country")  # country
    province = params.get("province")  # province
    city = params.get("city")
    name = tmp.get("name", '')  # name
    phone = tmp.get("phone", '')  # city
    email = tmp.get("email", '')  # city
    user = Userdata.query.filter_by(openid=openid).first()
    if user:
        user.openid = openid
        user.username = username
        user.avatar = avatar
        user.gender = gender
        user.country = country
        user.province = province
        user.city = city
        user.name = name
        user.phone = phone
        user.email = email
        user.is_lock = False
        user.update()
    else:
        user = Userdata(openid=openid, username=username, avatar=avatar, gender=gender, country=country,
                        province=province, city=city, name=name, phone=phone, email=email)
    return Responser.response_success(data={"id": user.id, "level": calculate_level(user.score)}, msg="success")

@auth.route('/delete_info',methods=["POST"])
@requestPOST
@SingAuth
def delete_info(request):
    openid = request.json.get("openid")  # openid
    user = Userdata.query.filter_by(openid=openid).first()
    user.is_lock = True
    user.update()
    return Responser.response_success(msg='退出成功！')

@auth.route('/check_info', methods=["POST"])
@requestPOST
@SingAuth
def check_info(request):
    tmp = request.json
    openid = tmp.get("openid")  # openid
    user = Userdata.query.filter_by(openid=openid).first()
    if not user:
        return Responser.response_error('尚未登陆')
    if not (user.name and user.phone and user.email):
        return Responser.response_error('尚未完善信息，请先完善信息')
    if user.is_lock == True:
        return Responser.response_error('尚未完善信息，请先完善信息')
    return Responser.response_success('检查通过')


@auth.route('/login', methods=['POST'])
@requestPOST
def login(request):
    # 完成网页端用户的登陆操作
    """
    接受参数并校验参数，返回token
    :return:
    # """
    # 生成token
    username = request.json.get("username")
    password = request.json.get("password")
    lost_attrs = required_attrs_validator([username, password])
    if lost_attrs:
        return Responser.response_error('参数缺失')
    user = LogonUser.query.filter_by(username=username, is_lock=False).first()
    if user.check_password(password):
        z_token = LogonUser.create_token(user.id, "username", user.role)
    else:
        return Responser.response_error('用户名或密码错误！')
    data = {
        "auth": z_token
    }
    return Responser.response_success(data=data, msg='success')


@auth.route('/create_user', methods=['POST'])
@requestPOST
@login_required('sysadmin')
def create_user(request):
    # 完成网页端用户创建接口
    username = request.json.get("username")
    password = request.json.get("password")
    phone = request.json.get("phone", "")
    email = request.json.get("email", "")
    role = request.json.get("role")
    depart = request.json.get("depart_id", 0)
    image = request.files.get("image", "")
    isExist = LogonUser.query.filter_by(username=username).first()
    if isExist:
        return Responser.response_error('已存在该用户')
    avatar = FileResponser.image_save(image)
    lost_attrs = required_attrs_validator([username, password, phone, email, role, depart])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    user = LogonUser(
        username=username,
        hash_password=password,
        phone=phone,
        email=email,
        role=role,
        depart=depart,
        avatar=avatar
    )

    user.update()
    return Responser.response_success(msg="创建成功")


@auth.route('/update_user', methods=['POST'])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def update_user(request):
    # 完成网页端用户更新信息接口
    userid = request.json.get("userid")
    username = request.json.get("username")
    password = request.json.get("password")
    phone = request.json.get("phone", "")
    email = request.json.get("email", "")
    role = request.json.get("role")
    depart = request.json.get("depart_id", 0)
    image = request.files.get("image", "")
    user = LogonUser.query.filter_by(id=userid).first()
    if not user:
        return Responser.response_error('没有该用用户')
    isExist = LogonUser.query.filter_by(username=username).first()
    if isExist:
        return Responser.response_error('已存在该用户')
    avatar = FileResponser.image_save(image)
    lost_attrs = required_attrs_validator([username, password, phone, email, role, depart])
    if lost_attrs:
        return Responser.response_error('缺少参数')
    user = LogonUser(
        username=username,
        hash_password=password,
        phone=phone,
        email=email,
        role=role,
        depart=depart,
        avatar=avatar
    )

    user.update()
    return Responser.response_success(msg="修改成功")


@auth.route('/delete_user', methods=['GET'])
@requestGET
@login_required(['sysadmin', 'admin'])
def delete_user(request):
    # 完成网页端用户删除接口
    userid = request.json.get("id")
    user = LogonUser.query.filter_by(id=userid).first()
    if not user:
        return Responser.response_error('没有该用用户')
    user.is_lock = True
    user.update()
    return Responser.response_success("删除成功！")


@auth.route('/get_all_users', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin'])
def get_all_users(request):
    # 获取所有用户信息
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    users = LogonUser.query.filter_by(is_lock=False)
    total_pages = math.ceil(users.count() / per_page)

    users_paginated = users.paginate(page=page, per_page=per_page, error_out=False)
    user_list = []
    for user in users_paginated:
        # if user.role == 'sysadmin':
        #     continue
        user_dict = {
            'id': user.id,
            'username': user.username,
            'phone': user.phone,
            'email': user.email,
            'avatar': user.avatar,
            'role': user.role,
            'depart': user.depart,
            'create_at': user.create_at,
            'update_at': user.update_at,
            'login_date': user.login_date,
            'is_lock': user.is_lock
        }
        user_list.append(user_dict)
    return Responser.response_page(data=user_list, page=page, page_size=per_page, count=total_pages)


@auth.route('/get_all_wxusers', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin'])
def get_all_wxusers(request):
    # 获取所有用户信息
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    users = Userdata.query.filter_by(is_lock=False)
    total_pages = math.ceil(users.count() / per_page)

    users_paginated = users.paginate(page=page, per_page=per_page, error_out=False)
    user_list = []
    for user in users_paginated:
        user_dict = {
            'id': user.id,
            'username': user.username,
            'openid': user.openid,
            'avatar': user.avatar,
            'gender': user.gender,
            'country': user.country,
            'province': user.province,
            'city': user.city,
            'name': user.name,
            'phone': user.phone,
            'email': user.email,
            'update_at': user.update_at,
            'score': user.score,
            'limit': user.limit
        }
        user_list.append(user_dict)
    print(user_dict)
    return Responser.response_page(data=user_list, page=page, page_size=per_page, count=total_pages)

@auth.route('/wx_get_single_wxusers', methods=["POST"])
@requestPOST
@SingAuth
def wx_get_single_wxusers(request):
    # 获取所有用户信息
    openid = request.json.get('openid')

    user = Userdata.query.filter_by(openid=openid).first()

    user_dict = {
        'id': user.id,
        'username': user.username,
        'avatar': user.avatar,
        'gender': user.gender,
        'country': user.country,
        'province': user.province,
        'city': user.city,
        'name': user.name,
        'phone': user.phone,
        'email': user.email,
        'update_at': user.update_at,
        'score': user.score
    }
    return Responser.response_success(data=user_dict)


@auth.route('/get_simple_users', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'others'])
def get_simple_users(request):
    # 获取单个用户信息
    userid = request.json.get("id")
    user = LogonUser.query.filter_by(id=userid).first()
    user_dict = {
        'id': user.id,
        'username': user.username,
        'phone': user.phone,
        'email': user.email,
        'avatar': user.avatar,
        'role': user.role,
        'depart': user.depart,
        'create_at': user.create_at,
    }
    return Responser.response_success(data=user_dict)

@auth.route('/get_user_list', methods=["GET"])
@requestGET
@login_required(['sysadmin', 'admin', 'others'])
def get_user_list(request):
    # 获取单个用户信息
    users = Userdata.query.filter_by(is_lock=False).all()
    res = []
    for user in users:
        if user.name:
            dic = {
                "user_id":user.id,
                "user_name":user.name,
                "user_username":user.username
            }
            res.append(dic)
    return Responser.response_success(data=res)

@auth.route('/change_limit', methods=["POST"])
@requestPOST
@login_required(['sysadmin', 'admin', 'others'])
def change_limit(request):
    userid = request.json.get("id")
    user = Userdata.query.filter_by(id=userid).first()
    if user.limit == 0:
        user.limit = 1
    else:
        user.limit = 0
    user.update()
    return Responser.response_success(msg='修改成功！')