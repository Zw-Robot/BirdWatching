from apps.auth import service
from ..auth import auth
from apps.components.common import returnData
from apps.components.middleware import requestPOST, SingAuth

'''登录接口'''
@auth.route('/sgin', methods=["GET","POST"], endpoint='auth_login')
@SingAuth
def login(request):
    code, msg, json = service.login(request)
    return returnData(code, msg, json)