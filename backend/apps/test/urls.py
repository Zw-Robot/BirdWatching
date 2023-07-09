from flask import jsonify

from . import views, test
from ..components.middleware import requestPOST

'''登录接口'''
@test.route('/test', methods=["GET","POST"])
@requestPOST
def test(request):
    if request.method == 'POST':
        # 处理 POST 请求
        data = request.json  # 获取请求中的 JSON 数据
        # 处理数据并返回响应
        response = {
            'code': 200,
            'message': 'Success',
            'data': data
        }
        return jsonify(response)
    else:
        # 处理 GET 请求
        # 返回一个简单的响应
        response = {
            'code': 200,
            'message': 'Success',
            'data': 'Hello, GET request!'
        }
        return jsonify(response)