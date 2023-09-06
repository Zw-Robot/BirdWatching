import requests

# 微信SDK 密匙 和 id
class Choices:
    AppID, AppSecret = 'wxbee80c3c4c5036d4', 'd7d8738ad5d998720620412f6e5b9936'

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
