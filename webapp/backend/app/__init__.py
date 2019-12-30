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
from flask_babelex import Babel

mail = Mail()
db = SQLAlchemy()
bootstrap=Bootstrap()
babel = Babel()
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
    babel.init_app(app)
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
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
        column_labels=dict(id="序号",userName="用户名",email="邮箱",schoolId="学号",   
            phone="手机号",department="院系",profile="个人简介",messages="审批消息",userActivities="关联活动")

    class MyTeamView(MyBaseView):
        column_list=['id','teamName','email','phone']
        column_searchable_list=['id','teamName','email','phone']
        form_excluded_columns=['avatar']
        column_labels=dict(id="序号",teamName="团体名",email="邮箱",phone="手机号",activities="活动",
            establishedTime="成立时间",password_hash="密码",description="团队简介")
        
        def on_model_change(self, form, team, is_created):
            team.password = form.password_hash.data

    class MyActivityView(MyBaseView):
        column_list=['id','AID','title','starttime','location','managePhone','type','isApplyFinish']
        column_labels={'isApplyFinish':'isApplyFinish'}
        column_searchable_list=['id','AID','title']
        form_excluded_columns=['managePhone','managePerson','manageEmail','thumb','starttime','endtime','qrcode','AID','isMessage','isRead','time']
        column_labels=dict(id="序号",AID="活动编号",title="活动标题",starttime="开始时间",location="活动地点",managePhone="负责人电话",
            type="活动状态",isApplyFinish="是否申请结项",userActivities="关联用户",messages="审批消息",content="活动内容",totalRecruits="总人数",
            appliedRecruits="已报名人数",team="团队")

    class MyUserActivityView(MyBaseView):
        column_list=['id','activityId','content','applyTime','type','hours']
        column_searchable_list=['id','activityId']
        column_labels=dict(id="序号",activityId="活动编号",content="申请理由",applyTime="申请时间",type="申请状态",hours="志愿工时",
            isRead="是否已审批",isSignIn="是否已签到",user="志愿者",activity="活动")

    class MyMessageView(MyBaseView):
        column_list=['id','content','time']
        column_searchable_list=['id']
        column_labels=dict(id="序号",content="审批消息内容",time="审批时间",isRead="是否已阅读",user="志愿者",activity="活动")

    class MyIntroCodeView(MyBaseView):
        column_list=['id','code']
        column_searchable_list=['id']
        column_labels=dict(id="序号",code="邀请码",time="生成时间")

    class MySuggestionView(MyBaseView):
        column_list=['id','content']
        column_searchable_list=['id']
        column_labels=dict(id="序号",content="意见内容")

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
    admin.add_view(MyUserView(User, db.session,name="志愿者"))
    admin.add_view(MyTeamView(Team, db.session,name="志愿团队"))
    admin.add_view(MyActivityView(Activity, db.session,name="活动"))
    admin.add_view(MyIntroCodeView(IntroCode, db.session,name="邀请码"))
    admin.add_view(MyUserActivityView(UserActivity, db.session,name="志愿者-活动"))
    admin.add_view(MyMessageView(Message, db.session,name="审批消息"))
    admin.add_view(MySuggestionView(Suggestion,db.session,name="意见反馈"))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
