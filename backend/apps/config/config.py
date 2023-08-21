#DEBUG = True

# Flask Sqlalchemy Setting
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'Ld1ss6H94iu'
HOST = '43.138.33.82'
PORT = '3306'
DATABASE = 'birdwatching'

#mysql 不会认识utf-8,而需要直接写成utf8
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

COOKIE_EXPIRATION = 30 * 24 * 3600  # 秒（到期浏览器自动删除）
TOKEN_EXPIRATION = 30 * 24 * 3600  # 秒（到期报错SignatureExpired）
SECRET_KEY = 'k#S6@1%8)a#D5WS01'


# Flask Bcrypt Setting
BCRYPT_LOG_ROUNDS = 1