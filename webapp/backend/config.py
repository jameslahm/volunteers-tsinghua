import os
basedir = os.path.abspath(os.path.dirname(__file__))
from redis import Redis

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or "hard to guess"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[SE]'
    FLASKY_MAIL_SENDER = os.getenv('FLASK_MAIL_SENDER') 
    FLASK_ADMIN = os.getenv('FLASK_ADMIN') or 'volunteers-tsinghua@example.com'
    FLASK_ADMIN_PASSWORD = os.getenv('FLASK_ADMIN_PASSWORD') or '123456'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','bmp'])
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ACTIVITY_PER_PAGE=5
    FLASK_WX_PER_PAGE=20
    UPLOAD_FOLDER=basedir+'/app/static/img/'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    TESTING=False


    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    ENV='development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:password@localhost:3306/volunteers?charset=utf8'
    SESSION_TYPE='redis'
    SESSION_REDIS=Redis(host='127.0.0.1',port=6379)
    

class TestConfig(Config):
    TESTING = True
    ENV='development'
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:password!@localhost:3306/test?charset=utf8'
    SESSION_TYPE='redis'
    SESSION_REDIS=Redis(host='127.0.0.1',port=6379)

class ProductionConfig(Config):
    ENV='production'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:password@mysql:3306/volunteers?charset=utf8'
    SESSION_TYPE='redis'
    SESSION_REDIS=Redis(host='redis',port=6379)


config = {
    'development': Development,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Development
}
