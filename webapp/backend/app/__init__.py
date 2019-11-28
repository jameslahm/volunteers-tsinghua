# -*- coding: utf-8 -*-
'''
web启动入口文件，封装flask-app全局设置
'''
from flask import Flask, url_for,redirect
from flask_login import current_user,LoginManager,logout_user
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap=Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    app.db = db


    # flask-admin
    from .model import User, Team, Activity, UserActivity,IntroCode

    # flask-user

    class MyUserView(ModelView):
        def is_accessible(self):
            return current_user.is_administrator()

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for("auth.login"))

    class MyAdminIndexView(AdminIndexView):

        @expose('/')
        def index(self):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            return super(MyAdminIndexView, self).index()

        @expose('/logout/')
        def logout_view(self):
            logout_user()
            return redirect(url_for('auth.login'))

    admin = Admin(app,name="admin",template_mode="bootstrap3",index_view=MyAdminIndexView())
    admin.add_view(MyUserView(User, db.session))
    admin.add_view(MyUserView(Team, db.session))
    admin.add_view(MyUserView(Activity, db.session))
    admin.add_view(MyUserView(IntroCode, db.session))
    admin.add_view(MyUserView(UserActivity, db.session))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
