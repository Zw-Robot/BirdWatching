from apps.auth import service
from apps.models import LogonUser
from ..auth import auth
from apps.components.common import returnData, required_attrs_validator
from apps.components.middleware import requestPOST, SingAuth, login_required, requestGET
from ..components.responser import Responser

'''登录接口'''


@auth.route('/sgin', methods=["GET", "POST"], endpoint='auth_login')
@SingAuth
def login(request):
    code, msg, json = service.login(request)
    return returnData(code, msg, json)


@auth.route('/login', methods=['GET'])
@requestGET
def login(request):
    # TODO:完成网页端用户的登陆操作
    '''
    接受参数并校验参数，返回token
    :return:
    # '''
    # 生成token
    username = request.json.get("username")
    password = request.json.get("password")
    lost_attrs = required_attrs_validator([username, password])
    if lost_attrs:
        return Responser.response_error('E001')
    user = LogonUser.query.filter_by(username=username).first()
    if user.check_password(password):
        z_token = LogonUser.create_token(user.id, "username", user.role)
    else:
        return Responser.response_error('密码错误')
    data = {
        "auth": z_token
    }
    return Responser.response_success(data=data, msg='success')


@auth.route('/create_user', methods=['POST'])
@requestPOST
@login_required('sysadmin')
def create_user(request):
    # TODO:完成网页端用户创建接口
    username = request.json.get("username")
    password = request.json.get("password")
    phone = request.json.get("phone","")
    email = request.json.get("email","")
    role = request.json.get("role")
    depart = request.json.get("depart_id",0)
    image = request.json.get("image","")
    isExist = LogonUser.query.filter_by(username=username).first()
    if isExist:
        return Responser.response_error('已存在该用户，请q')
    if image:
        avatar = '/var/birdwatching/avatar/{}.png'.format(username)
        image.save(avatar)
    else:
        avatar = '/var/birdwatching/example.png'
    lost_attrs = required_attrs_validator([username,password,phone,email,role,depart])
    if lost_attrs:
        return Responser.response_error('E001')
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


@auth.route('/update_user', methods=['GET'])
@requestGET
@login_required('sysadmin', 'admin')
def update_user():
    # TODO:完成网页端用户更新接口
    pass


@auth.route('/delete_user', methods=['GET'])
@requestGET
def delete_user():
    # TODO:完成网页端用户删除接口
    pass


@auth.route('/get_all_users', methods=["GET"])
@requestGET
def get_all_users():
    # TODO:获取所有用户信息
    pass
