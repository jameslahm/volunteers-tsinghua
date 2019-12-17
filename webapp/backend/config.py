import os
basedir = os.path.abspath(os.path.dirname(__file__))
from redis import Redis

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or "hard to guess"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[SE]'
    FLASKY_MAIL_SENDER = os.getenv('FLASKY_MAIL_SENDER') or 'SE'
    FLASK_ADMIN = os.getenv('FLASKY_ADMIN') or 'volunteers-tsinghua@example.com'
    FLASK_ADMIN_PASSWORD = os.getenv('FLASKY_ADMIN_PASSWORD') or '123456'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','bmp'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE=20
    FLASKY_COMMENTS_PER_PAGE=20
    UPLOAD_FOLDER=basedir+'/app/static/img/'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'jameslahm17@gmail.com'
    MAIL_PASSWORD = 'dkcqjdrpmswxrjtw'
    SESSION_TYPE='redis'
    appid='wxf3aa74b41b1f555c'
    appsecret='669223961b70204ffbd023015ea9decb'


    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    ENV='development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:Waqing121!@localhost:3306/volunteers?charset=utf8'
    SESSION_REDIS=Redis(host='127.0.0.1',port=6379)
    

class TestConfig(Config):
    TESTING = True
    ENV='development'
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:Waqing121!@localhost:3306/test?charset=utf8'
    SESSION_REDIS=Redis(host='127.0.0.1',port=6379)

class ProductionConfig(Config):
    ENV='production'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:zhizaitsinghua@mysql:3306/volunteers?charset=utf8'
    SESSION_REDIS=Redis(host='redis',port=6379)

config = {
    'development': Development,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Development
}
