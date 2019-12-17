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
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_session import Session
from datetime import datetime

mail = Mail()
db = SQLAlchemy()
bootstrap=Bootstrap()
sess=Session()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['BASE_DIR']=os.path.abspath(os.path.dirname(__file__))
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    app.db = db

    # flask-admin
    from .model import User, Team, Activity, UserActivity,IntroCode,Message,Suggestion

    # flask-user

    class MyBaseView(ModelView):
        
        def is_accessible(self):
            return current_user.is_administrator()

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for("auth.login"))

    class MyUserView(MyBaseView):
        column_list=['id','userName','email','schoolId','phone','department']
        column_searchable_list=['id','userName','email','schoolId']
        form_excluded_columns=['openId','avatar','wx']

    class MyTeamView(MyBaseView):
        column_list=['id','teamName','email','phone']
        column_searchable_list=['id','teamName','email','phone']
        form_excluded_columns=['avatar']
        
        def on_model_change(self, form, team, is_created):
            team.password = form.password_hash.data

    class MyActivityView(MyBaseView):
        column_list=['id','AID','title','starttime','location','managePhone','isApplyFinish']
        column_labels={'isApplyFinish':'isApplyFinish'}
        column_searchable_list=['id','AID','title']
        form_excluded_columns=['managePhone','managePerson','manageEmail','thumb','starttime','endtime','qrcode','AID','isMessage','isRead','time']

    class MyUserActivityView(MyBaseView):
        column_list=['id','activityId','content','applyTime','type','hours']
        column_searchable_list=['id','activityId']

    class MyMessageView(MyBaseView):
        column_list=['id','content','time']
        column_searchable_list=['id']

    class MyIntroCodeView(MyBaseView):
        column_list=['id','code']
        column_searchable_list=['id']

    class MySuggestionView(MyBaseView):
        column_list=['id','content']
        column_searchable_list=['id']

    class MyAdminIndexView(AdminIndexView):

        @expose('/')
        def index(self):
            if not current_user.is_administrator():
                return redirect(url_for('auth.login'))
            return super(MyAdminIndexView, self).index()

        @expose('/logout/')
        def logout_view(self):
            logout_user()
            return redirect(url_for('auth.login'))

    admin = Admin(app,name="admin",template_mode="bootstrap3",index_view=MyAdminIndexView())
    admin.add_view(MyUserView(User, db.session))
    admin.add_view(MyTeamView(Team, db.session))
    admin.add_view(MyActivityView(Activity, db.session))
    admin.add_view(MyIntroCodeView(IntroCode, db.session))
    admin.add_view(MyUserActivityView(UserActivity, db.session))
    admin.add_view(MyMessageView(Message, db.session))
    admin.add_view(MySuggestionView(Suggestion,db.session))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
