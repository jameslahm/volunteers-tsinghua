import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or "hard to guess"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = os.getenv('FLASKY_MAIL_SENDER')
    FLASK_ADMIN = os.getenv('FLASKY_ADMIN') or 'volunteers-tsinghua@example.com'
    FLASK_ADMIN_PASSWORD = os.getenv('FLASKY_ADMIN_PASSWORD') or '123456'

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE=20
    FLASKY_COMMENTS_PER_PAGE=20


    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    ENV='development'
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') 
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') 
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:zhizaitsinghua@localhost:3306/volunteers?charset=utf8'

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:Waqing121!@localhost:3306/volunteers?charset=utf8'


class ProductionConfig(Config):
    ENV='production'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://  \
                            root:zhizaitsinghua@mysql:3306/volunteers?charset=utf8'


config = {
    'development': Development,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Development
}
