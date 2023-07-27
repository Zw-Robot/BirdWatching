from apps.auth import service,auth
from apps.components.common import required_attrs_validator
from apps.models import LogonUser, Userdata, LoginSessionCache
from apps.components.middleware import requestPOST, SingAuth, login_required, requestGET
from apps.components.responser import Responser, FileResponser

'''登录接口'''


@auth.route('/sgin', methods=["GET", "POST"], endpoint='auth_login')
@requestPOST
# @SingAuth
def auth_login(request):
    code, msg, json = service.login(request)
    if code == 200:
        return Responser.response_success(data=json,msg=msg)
    else:
        return Responser.response_error(msg=msg)


@auth.route('/info', methods=["GET", "POST"], endpoint='info')
@requestPOST
@SingAuth
def get_info(request):
    params = request.json()
    openid = params.get("openid")  # openid
    log = LoginSessionCache.query.filter_by(openid=openid).first()
    if not log:
        return Responser.response_error(msg="未登录")
    username = params.get("username")  # username
    avatar = params.get("avatar")  # avatarUrl
    gender = params.get("gender")   # gender
    country = params.get("country")  # country
    province = params.get("province")   # province
    city = params.get("city") # city
    Userdata(openid=openid,username=username,avatar=avatar,gender=gender,country=country,province=province,city=city)
    return Responser.response_success(data={},msg="success")

@auth.route('/login', methods=['GET'])
@requestGET
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
    user = LogonUser.query.filter_by(username=username,is_lock=False).first()
    if not user.check_password(password):
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
    avatar = FileResponser.image_save(image, 'avatar', username)
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
    avatar = FileResponser.image_save(image, 'avatar', username)
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
@login_required(['sysadmin','admin'])
def delete_user(request):
    #完成网页端用户删除接口
    userid = request.json.get("id")
    user = LogonUser.query.filter_by(id=userid).first()
    if not user:
        return Responser.response_error('没有该用用户')
    user.is_lock = True
    user.update()
    return Responser.response_success("删除成功！")


@auth.route('/get_all_users', methods=["GET"])
@requestGET
@login_required(['sysadmin','admin'])
def get_all_users():
    # 获取所有用户信息
    users = LogonUser.query.filter_by().all()
    user_list = []
    for user in users:
        if user.role == 'sysadmin':
            continue
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
    return Responser.response_success(data=user_list)


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
