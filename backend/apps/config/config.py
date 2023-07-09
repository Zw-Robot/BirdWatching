#DEBUG = True

# Flask Sqlalchemy Setting
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'toor'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'birdwatching'

#mysql 不会认识utf-8,而需要直接写成utf8
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


# Flask Bcrypt Setting
BCRYPT_LOG_ROUNDS = 1