from flask import jsonify

from apps.auth import service
from ..auth import auth
from apps.components.common import returnData
from apps.components.middleware import requestPOST, SingAuth, login_required, requestGET
from ..models import LogonUser

'''登录接口'''


@auth.route('/sgin', methods=["GET", "POST"], endpoint='auth_login')
@SingAuth
def login(request):
    code, msg, json = service.login(request)
    return returnData(code, msg, json)




@auth.route('/login', methods=['GET'])
def login():
    # TODO:完成网页端用户的登陆操作
    '''
    接受参数并校验参数，返回token
    :return:
    # '''
    # 生成token
    # z_token = LogonUser.create_token(1,"username","admin")
    # #
    # return z_token
    pass

@auth.route('/create_user', methods=['POST'])
@login_required('admin')
@requestPOST
def create_user(request):
    # TODO:完成网页端用户创建接口
    pass

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


