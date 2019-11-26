# -*- coding: utf-8 -*-
'''模型'''

from . import db
from flask import url_for,current_app
from flask_login import AnonymousUserMixin,UserMixin
import flask_sqlalchemy
from flask import request
from datetime import datetime



class User(db.Model):
    '''用户'''
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # TODO: how to get openId?
    openId = db.Column("openId", db.String(64), unique=False, nullable=False) # 改
    userName = db.Column("userName", db.String(16), unique=False, nullable=False)
    wx = db.Column("wx", db.String(64), unique=False, nullable=False) # 改
    email = db.Column("email", db.String(64), unique=False) # 改
    avatar = db.Column("avatar", db.String(128))
    schoolId = db.Column('schoolID', db.String(30), unique=False)  # 改
    phone = db.Column('phone', db.String(20))
    department = db.Column('department', db.Text)
    profile = db.Column('profile', db.Text)
    userActivities = db.relationship('UserActivity', backref='user',lazy='dynamic')
    messages = db.relationship('Message', backref='user')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py as fp
        seed()
        for i in range(count):
            u = User(
                    openId=i,
                    email=fp.internet.email_address(),
                    userName=fp.internet.user_name(True),
                    wx=fp.lorem_ipsum.word(),
                    phone=fp.address.phone(),
                    schoolId=str(fp.credit_card.number()),
                    department=fp.lorem_ipsum.word(),
                    profile=fp.lorem_ipsum.sentence(),
            )
            db.session.add(u)
            db.session.commit()

    def to_json(self):
        json_user={
            'url':url_for('api.get_user',id=self.id,_external=True),
            'openId':self.openId,
            'userName':self.userName,
            'wx':self.wx,
            'email': self.email,
            'avatar': self.avatar,
            'schoolID': self.schoolID,
            'phone':self.phone,
            'department':self.department,
            'profile': self.profile,
        }
        return json_user

    def applyedActivities(self):
        l=self.UserActivity.filter_by(type='applyed').all()
        res=[x.Activity for x in l]
        return res

    def applyingActivities(self):
        l=self.UserActivity.filter_by(type='applying').all()
        res=[x.Activity for x in l]
        return res

   def finishedActivities(self):
        l=self.UserActivity.filter_by(type='finished').all()
        res=[x.Activity for x in l]
        return res

class Team(db.Model,UserMixin):
    '''志愿团体'''
    __tablename__ = 'teams'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column("userName", db.String(64), unique=False, nullable=False)
    email = db.Column("email", db.String(64), unique=False) #改
    teamname=db.Column('teamname',db.String(64),unique=False) #改
    establishedtime=db.Column('establishedtime',db.DateTime)
    avatar = db.Column("avatar", db.String(128))
    password=db.Column('password',db.String(128))
    description=db.Column('description',db.Text)
    teamActivities = db.relationship('TeamActivity', backref='team',lazy='dynamic')
    messages = db.relationship('Message', backref='team')


    def verify_password(self,password):
        return self.password==password

    def is_administrator(self):
        return self.email==current_app.config['FLASK_ADMIN']

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py as fp
        seed()
        for i in range(count):
            t = Team(
                    email=fp.internet.email_address(),
                    userName=fp.internet.user_name(True),
                    teamname=fp.lorem_ipsum.word(),
                    establishedtime=fp.date.date(),
                    description=fp.lorem_ipsum.sentence(),
            )
            db.session.add(t)
            db.session.commit()

    def to_json(self):
        json_team={
            'url':url_for('api.get_team',id=self.id,_external=True),
            'userName':self.userName,
            'email':self.email,
            'teamname':self.teamname,
            'establishedtime':self.establishedtime,
            'description':self.description,
            'avatar':self.avatar,
        }
        return json_team

    def createdActivities(self):
        l=self.TeamActivity.filter_by(type='created').all()
        res=[x.Activity for x in l]
        return res

    def creatingActivities(self):
        l=self.TeamActivity.filter_by(type='creating').all()
        res=[x.Activity for x in l]
        return res

    def finishedActivities(self):
        l=self.TeamActivity.filter_by(type='finished').all()
        res=[x.Activity for x in l]
        return res

class Activity(db.Model):
    '''活动'''
    __tablename__ = 'activities'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    AID = db.Column('AID', db.Integer)
    thumb = db.Column('thumb', db.String(128), nullable=False)
    time = db.Column('time', db.DateTime, nullable=False)
    endtime = db.Column('endtime',db.DateTime,nullable=False)
    location = db.Column('location', db.String(50), nullable=False)
    title = db.Column('title', db.String(70), nullable=False)
    description = db.Column('description', db.String(400), nullable=False)
    content = db.Column('content', db.String(400), nullable=False)
    totalRecruits = db.Column('totalRecruits', db.Integer)
    appliedRecruits = db.Column('appliedRecruits', db.Integer)
    qrcode = db.Column('qrcode',db.String(128))
    userActivities = db.relationship('UserActivity', backref='activity',lazy='dynamic')
    teamActivities = db.relationship('TeamActivity', backref='activity',lazy='dynamic')
    messages = db.relationship('Message',backref='activity')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py as fp
        seed()
        for i in range(count):
            a = Activity(
                AID=i,
                thumb=fp.internet.domain_name(),
                time=fp.date.date(),
                endtime=fp.date.date(),
                location=fp.address.city(),
                title=fp.lorem_ipsum.title(),
                description=fp.lorem_ipsum.sentence(),
                content=fp.lorem_ipsum.sentence(),
                totalRecruits=fp.basic.number(at_least=20, at_most=100),
                appliedRecruits=fp.basic.number(at_least=0, at_most=20),
            )
            db.session.add(a)
            db.session.commit()

    def to_json(self):
        json_activity={
            'url':url_for('api.get_activity',id=self.id,_external=True),
            'AID':self.AID,
            'time':self.time,
            'endtime':self.endtime,
            'location':self.location,
            'title':self.title,
            'description':self.description,
            'content':self.content,
            'totalRecruits':self.totalRecruits,
            'appliedRecruits':self.appliedRecruits,
        }
        return json_activity


    def leader(self):
        return self.TeamActivity.first().User

    def members(self):
        l=self.UserActivity.filter_by(type='applyed').all()
        res=[x.User for x in l]
        return res


class Message(db.Model):
    '''消息'''
    __tablename__ = 'messages'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('users.id'))
    notifier = db.Column('notifier', db.Integer, db.ForeignKey('teams.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('activities.id'))
    content = db.Column('content', db.Text)
    qrCode = db.Column('qrCode', db.String(64))
    time = db.Column('time', db.DateTime)
    isRead = db.Column('isRead', db.Boolean)

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py as fp

        seed()
        user_count=User.query.count()
        notifier_count=Team.query.count()
        activity_count=Activity.query.count()
        for i in range(count):
            u=User.query.offset(randint(0,user_count-1)).first()
            t=Team.query.offset(randint(0,notifier_count-1)).first()
            a=Activity.query.offset(randint(0,activity_count-1)).first()
            m=Message(Sender=u,Notifier=t,Activity=a,content = fp.lorem_ipsum.sentence(),
                      time = fp.date.date(),isRead = fp.basic.boolean())
            db.session.add(m)
            db.session.commit()

    def to_json(self):
        json_message={
            'url':url_for('api.get_message',id=self.id,_external=True),
            'sender': url_for('api.get_user', id=self.userId, _external=True),
            'notifier':url_for('api.get_notifier',id=self.notifier,_external=True),
            'activity':url_for('api.get_activity',id=self.notifier,_external=True),
            'content':self.content,
            'qrcode':self.qrCode,
            'time':self.time,
            'isRead':self.isRead,
        }
        return json_message

class UserActivity(db.Model):
    '''个人活动'''
    __tablename__ = 'useractivities'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('users.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('activities.id'))
    type = db.Column('type', db.Enum('applying', 'applyed','finished'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py as fp

        seed()
        user_count=User.query.count()
        activity_count=Activity.query.count()
        for i in range(count):
            u=User.query.offset(randint(0,user_count-1)).first()
            a=Activity.query.offset(randint(0,activity_count-1)).first()
            t=randint(0,2)
            u_activity=UserActivity(user=u,activity=a,type='applying'if t==0 else 'applyed' if t==1 else 'finished')
            db.session.add(u_activity)
            db.session.commit()



class TeamActivity(db.Model):
    '''团队活动'''
    __tablename__ = 'teamactivities'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    teamId = db.Column('teamId', db.Integer, db.ForeignKey('teams.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('activities.id'))
    type = db.Column('type', db.Enum('creating', 'created','finished'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py as fp

        seed()
        team_count=Team.query.count()
        activity_count=Activity.query.count()
        for i in range(count):
            team=Team.query.offset(randint(0,team_count-1)).first()
            a=Activity.query.offset(randint(0,activity_count-1)).first()
            t=randint(2,4)
            t_activity=TeamActivity(team=team,activity=a,type='creating'if t==2 else 'created' if t==3 else 'finished')
            db.session.add(t_activity)
            db.session.commit()


from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Team.query.get(user_id)

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False
    

login_manager.anonymous_user=AnonymousUser

class IntroCode(db.Model):
    __tablename__="introcodes"
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    code=db.Column('code',db.String(30))

    @staticmethod
    def verify_code(code):
        return IntroCode.query.filter_by(code=code).first()