# -*- coding: utf-8 -*-
'''后端启动文件

web启动入口文件，封装flask-app全局设置
'''
from flask import Flask

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

from .model import User, Team, Activity, UserActivity, TeamActivity

from flask_login import UserMixin, LoginManager, current_user, login_user

from .app_map import blueprints
from .app_env import get_config

from .utils import get_engine

from .core.database import db


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
	# 数据库类型
	db_type = db_config['type']
	db_config.pop('type')
	db_kwargs = config.get('db_kwargs', {})
	engine = get_engine(db_type, user_config=db_config, **db_kwargs)
	# Flask-SQLAlchemy配置
	app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	# 关联Flask-SQLAlchemy到当前app
	db.init_app(app)
	app.db = db
	with app.app_context():
		db.create_all()

	# flask-login
	login = LoginManager(app)


	# flask-admin
	# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
	admin = Admin(app)
	admin.add_view(ModelView(User, db.session))
	admin.add_view(ModelView(Team, db.session))
	admin.add_view(ModelView(Activity, db.session))
	admin.add_view(ModelView(UserActivity, db.session))
	admin.add_view(ModelView(TeamActivity, db.session))



	# @app.route('/login')
	# def login():
	# 	admin_user = AdminUser.query.get(1)





	# 注册蓝图(子应用)
	for item in blueprints:
		app.register_blueprint(item[1], url_prefix=item[0])

	return app
