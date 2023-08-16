from flask_cors import CORS
from flask_migrate import Migrate

from apps.config import config
from flask import Flask  # flask
from flask_sqlalchemy import SQLAlchemy  # sql

app = Flask(__name__)
CORS(app)

# 引入全局配置
app.config.from_object(config)

# 跨域密匙
app.secret_key = 'sda2&*FSWee12@s*$MMK1023('
db = SQLAlchemy(app)

migrate = Migrate(app, db)
