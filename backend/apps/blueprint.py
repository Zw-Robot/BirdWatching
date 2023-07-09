from apps import app
from apps.auth import auth

# 微信登录验证
from apps.test import test

app.register_blueprint(auth, url_prefix='/auth', name='auth')
app.register_blueprint(test,url_prefix='/test', name='test')
