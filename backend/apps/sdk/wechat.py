import requests

# 微信SDK 密匙 和 id
class Choices:
    AppID, AppSecret = 'wx34396991c4ea8e2c', '843092735a9268a4bbf66ae5a93c2de1'

# 微信SDK auth.code2Session
def WXSDK_jscode2session(code):
    print(code)
    wechat_url = 'https://api.weixin.qq.com/sns/jscode2session'
    wechat_data = {
        'appid': Choices.AppID,
        'secret': Choices.AppSecret,
        'js_code': code,
        'grant_type': 'authorization_code',
    }
    return requests.get(url=wechat_url, params=wechat_data).json()

# # 微信SDK userinfo
# def WXSDK_userinfo(openid, access_token):
#     wechat_url = 'https://api.weixin.qq.com/sns/userinfo'
#     wechat_data = {
#         'openid': openid,
#         'access_token': access_token,
#     }
#     result = requests.get(wechat_url, params=wechat_data).encoding = 'UTF-8'
#     print(result)
#     return result.json()
