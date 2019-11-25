# -*- coding: utf-8 -*-
'''
web启动入口文件，封装flask-app全局设置
'''
from flask import Flask, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_user import UserManager, SQLAlchemyAdapter, current_user
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
user_manager = UserManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    app.db = db

    with app.app_context():
        db.create_all()

    # flask-admin
    from .model import User, Team, Activity, UserActivity, TeamActivity, AdminUser

    # flask-user
    from .model import AdminUser
    db_adapter = SQLAlchemyAdapter(db, AdminUser)
    user_manager.init_app(app, db_adapter)

    class MyUserView(ModelView):
        def is_accessible(self):
            # return True
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return url_for("admin.index")

    admin = Admin(app)
    admin.add_view(MyUserView(User, db.session))
    admin.add_view(MyUserView(Team, db.session))
    admin.add_view(MyUserView(Activity, db.session))
    admin.add_view(MyUserView(UserActivity, db.session))
    admin.add_view(MyUserView(TeamActivity, db.session))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
