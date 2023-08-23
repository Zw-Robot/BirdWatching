from apps import app
from apps.auth import auth

# 微信登录验证
from apps.competition import competition
from apps.inventory import inventory
from apps.notice import notice
from apps.test import test

app.register_blueprint(auth, url_prefix='/auth', name='auth')
app.register_blueprint(test,url_prefix='/test', name='test')
app.register_blueprint(inventory,url_prefix='/inventory', name='inventory')
app.register_blueprint(competition,url_prefix='/competition',name='competition')
app.register_blueprint(notice,url_prefix='/notice',name='notice')