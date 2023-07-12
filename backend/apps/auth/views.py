from apps.auth import service
from .models import LogonUser
from ..auth import auth
from apps.components.common import returnData
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
    user = LogonUser.query.filter_by(username=username).first()
    print(user.check_password(password))
    if user.check_password(password):
        z_token = LogonUser.create_token(1,"username","admin")
    # #
    else:
        return Responser.response_error(code='E0001',msg='密码错误')
    data = {
        "auth":z_token
    }
    return Responser.response_success(data=data,msg='success')

@auth.route('/create_user', methods=['POST'])
# @login_required('admin')
@requestPOST
def create_user(request):
    # TODO:完成网页端用户创建接口
    username = request.json.get("username")
    password = request.json.get("password")
    user = LogonUser()
    user.username = username
    user.password = password
    user.phone ='111'
    user.update()
    return Responser.response_success(data={},msg="")

@auth.route('/update_user', methods=['GET'])
@requestGET
def update_user():
    # TODO:完成网页端用户更新接口
    pass


@auth.route('/delete_user', methods=['GET'])
@requestGET
def delete_user():
    # TODO:完成网页端用户删除接口
    pass


@auth.route('/get_all_users',methods=["GET"])
@requestGET
def get_all_users():
    # TODO:获取所有用户信息
    pass


