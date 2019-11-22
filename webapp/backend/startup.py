# -*- coding: utf-8 -*-
'''后端启动文件

web启动入口文件，封装flask-app全局设置
'''
from flask import Flask

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .Users import users

from flask_login import LoginManager

from .app_env import get_config

from .database import db
from .model import User, Team, Activity, UserActivity, TeamActivity

def create_app(config):

	env_config = get_config()
	template_folder = env_config.get('template_folder', None)
	static_folder = env_config.get('static_folder', None)

	app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )

	app.secret_key = b'admin'

	# 配置数据库
	db_config = env_config['db_config']
	app.config['SQLALCHEMY_DATABASE_URI'] = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(
		db_config['type'], db_config['driver'], db_config['username'], db_config['password'],
		db_config['host'], db_config['port'], db_config['dbname'], db_config['charset']
	)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)
	app.db = db
	with app.app_context():
		db.create_all()

	# flask-login
	login = LoginManager(app)

	# flask-admin
	admin = Admin(app)
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ModelView(Team, db.session))
	admin.add_view(ModelView(Activity, db.session))
	admin.add_view(ModelView(UserActivity, db.session))
	admin.add_view(ModelView(TeamActivity, db.session))

	app.register_blueprint(users, url_prefix="/users")

	return app
