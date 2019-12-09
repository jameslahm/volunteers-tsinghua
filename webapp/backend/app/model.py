# -*- coding: utf-8 -*-
'''模型'''

from . import db
from flask import url_for,current_app
from flask_login import AnonymousUserMixin,UserMixin
import flask_sqlalchemy
from flask import request
import datetime
from werkzeug.security import check_password_hash,generate_password_hash
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from uuid import uuid1


class User(db.Model):
    '''用户'''
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # TODO: how to get openId?
    openId = db.Column("openId", db.String(64), unique=False) # 改
    userName = db.Column("userName", db.String(16), unique=False, nullable=False)
    wx = db.Column("wx", db.String(64), unique=False) # 改
    email = db.Column("email", db.String(64), unique=False) # 改
    avatar = db.Column("avatar", db.String(128))
    schoolId = db.Column('schoolID', db.String(30), unique=False)  # 改
    phone = db.Column('phone', db.String(20))
    department = db.Column('department', db.Text)
    profile = db.Column('profile', db.Text)
    userActivities = db.relationship('UserActivity', backref='user',lazy='dynamic',cascade='all, delete-orphan')
    messages = db.relationship('Message', backref='user',cascade='all, delete-orphan')

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
            'id':self.id,
            'openId':self.openId,
            'userName':self.userName,
            'wx':self.wx,
            'email': self.email,
            'avatar': self.avatar,
            'schoolId': self.schoolId,
            'phone':self.phone,
            'department':self.department,
            'profile': self.profile,
        }
        return json_user

    def generate_auth_token(self,expiration):
        s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps(self.id).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            id=s.loads(token.encode('utf-8'))
        except:
            return False
        return User.query.filter_by(id=id).first()




class Team(db.Model,UserMixin):
    '''志愿团体'''
    __tablename__ = 'teams'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String(64), unique=False) #改
    teamName=db.Column('teamname',db.String(64),unique=False) #改
    establishedTime=db.Column('establishedtime',db.DateTime)
    avatar = db.Column("avatar", db.String(128))
    password_hash=db.Column('password_hash',db.String(128))
    description=db.Column('description',db.Text)
    phone=db.Column('phone',db.String(64))
    activities = db.relationship('Activity', backref='team',lazy='dynamic',cascade='all, delete-orphan')


    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
                    teamName=fp.internet.user_name(True),
                    establishedTime=fp.date.date(),
                    description=fp.lorem_ipsum.sentence(),
                    password=fp.basic.password()
            )
            db.session.add(t)
            db.session.commit()


    def to_json(self):
        json_team={
            'teamName':self.teamName,
            'email':self.email,
            'establishedtime':self.establishedTime,
            'description':self.description,
            'avatar':self.avatar,
        }
        return json_team

    def finishedActivities(self):
        return Activity.query.filter_by(teamId=self.id,type='finished').all()

    def createdActivities(self):
        return Activity.query.filter_by(teamId=self.id,type='created').all()
    
    def creatingActivities(self):
        return Activity.query.filter_by(teamId=self.id,type='creating').all()

class Activity(db.Model):
    '''活动'''
    __tablename__ = 'activities'

    def generateAID():
        s=str(uuid1())
        return s

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    AID = db.Column('AID', db.String(36),default=generateAID)
    teamId = db.Column('teamId', db.Integer, db.ForeignKey('teams.id',ondelete='cascade'))
    thumb = db.Column('thumb', db.String(128))
    starttime = db.Column('starttime', db.DateTime, nullable=False)
    endtime = db.Column('endtime',db.DateTime,nullable=False)
    location = db.Column('location', db.String(50), nullable=False)
    title = db.Column('title', db.String(70), nullable=False)
    content = db.Column('content', db.String(400), nullable=False)
    totalRecruits = db.Column('totalRecruits', db.Integer)
    appliedRecruits = db.Column('appliedRecruits', db.Integer,default=0)
    managePerson = db.Column('manageperson', db.String(70), nullable=False) # 增加
    managePhone = db.Column('managephone', db.String(70), nullable=False) # 增加
    manageEmail = db.Column('manageemail', db.String(70), nullable=False) # 增加
    qrcode = db.Column('qrcode',db.String(128))
    userActivities = db.relationship('UserActivity', backref='activity',lazy='dynamic',cascade='all, delete-orphan')
    messages = db.relationship('Message',backref='activity',cascade='all, delete-orphan')
    type = db.Column('type', db.Enum('creating', 'created','refused'),default='creating')
    isRead=db.Column('isRead',db.Boolean)
    time=db.Column('time',db.DateTime,default=datetime.now)
    isMessage=db.Column('isMessage',db.Boolean,default=False)

    @staticmethod
    def on_changed_type(target,value,oldvalue,initiator):
        target.isMessage=True
        target.time=datetime.now()
        target.isRead=False
        db.session.commit()
        print("type")

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py as fp
        seed()
        team_count=Team.query.count()
        for i in range(count):
            a = Activity(
                AID=i,
                team=Team.query.offset(randint(0,team_count-1)).first(),
                thumb=fp.internet.domain_name(),
                starttime=fp.date.datetime(),
                endtime=fp.date.datetime(),
                location=fp.address.city(),
                title=fp.lorem_ipsum.title(),
                content=fp.lorem_ipsum.sentence(),
                managePerson=fp.lorem_ipsum.title(),
                manageEmail=fp.internet.email_address(),
                managePhone=fp.address.phone(),
                totalRecruits=fp.basic.number(at_least=20, at_most=100),
                appliedRecruits=fp.basic.number(at_least=0, at_most=20),
            )
            db.session.add(a)
            db.session.commit()
    @staticmethod
    def search_bytitle(title):
        l = Activity.query.all()
        ans=[]
        for x in l:
            if (len(title) < len(x.title)):
                if re.search(title, x.title) != None:
                    ans.append(x)
            else:
                title_length = len(x.title)
                if re.search(title[0:int(title_length / 2)], x.title) != None:
                    ans.append(x)
        return ans
    @staticmethod
    def search_bytime(time):
        l = Activity.query.all()
        # input example : '2017-04-09 15:25'
        time=datetime.datetime.strptime(time,'%Y-%m-%d %H:%M')
        time_date=time.date()
        return [x for x in l if time_date.__eq__(x.datetime.date())]
    @staticmethod
    def search_bylocation(location):
        l = Activity.query.all()
        ans=[]
        for x in l:
            if (len(location) < len(x.location)):
                if re.search(location, x.location) != None:
                    ans.append(x)
            else:
                location_length = len(x.location)
                if re.search(location[0:int(location_length / 2)], x.location) != None:
                    ans.append(x)
        return ans
    @staticmethod
    def search_byteam(teamname):
        l = Activity.query.all()
        ans=[]
        for x in l:
            Name=x.team.first().teamName
            if (len(teamname) < len(Name)):
                if re.search(teamname, Name) != None:
                    ans.append(x)
            else:
                Name_length = len(Name)
                if re.search(teamname[0:int(Name_length / 2)], Name) != None:
                    ans.append(x)
        return ans

    @staticmethod
    def search_byAID(aid):
        return Activity.query.filter_by(Activity.AID.startswith(aid)).all()

    @staticmethod
    def search(param,type):
        if(type=='activity'):
            return Activity.search_bytitle(param)
        if(type=='coordinates'):
            return Activity.search_bylocation(param)
        if(type=='time'):
            return Activity.search_bytime(param)
        if(type=='group'):
            return Activity.search_byteam(param)
        if(type=='barrage'):
            return Activity.search_byAID(param)

    def to_json(self):
        json_activity={
            'id':self.id,
            'teamId':self.teamId,
            'teamName':self.team.teamName,
            'AID':self.AID,
            'starttime':self.starttime,
            'endtime':self.endtime,
            'location':self.location,
            'title':self.title,
            'content':self.content,
            'totalRecruits':self.totalRecruits,
            'appliedRecruits':self.appliedRecruits,
            'thumb':self.thumb,
            'endtime':self.endtime
        }
        return json_activity

    def members(self):
        l=self.userActivities.filter_by(type='applied').all()
        res=[x.user for x in l]
        return res

db.event.listen(Activity.type,'set',Activity.on_changed_type)

class Message(db.Model):
    '''消息'''
    __tablename__ = 'messages'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('users.id',ondelete='cascade'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('activities.id',ondelete='cascade'))
    content = db.Column('content', db.Text)
    time = db.Column('time', db.DateTime)
    isRead = db.Column('isRead', db.Boolean,default=False)

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py as fp

        seed()
        user_count=User.query.count()
        activity_count=Activity.query.count()
        for i in range(count):
            u=User.query.offset(randint(0,user_count-1)).first()
            count=UserActivity.query.filter_by(user=u,type='applying').count()
            if(count==0):
                continue
            userA=UserActivity.query.filter_by(user=u,type='applying').offset(randint(0,count-1)).first()
            a=userA.activity
            t=a.team
            m=Message(user=u,team=t,activity=a,content = fp.lorem_ipsum.sentence(),
                      time = fp.date.date(),isRead = fp.basic.boolean())
            db.session.add(m)
            db.session.commit()

    def to_json(self):
        json_message={
            'id':self.id,
            'userId':self.userId,
            'team':self.activity.team.to_json(),
            'activityId':self.activityId,
            'content':self.content,
            'qrcode':self.activity.qrcode,
            'time':self.time,
            'isRead':self.isRead,
        }
        return json_message

class UserActivity(db.Model):
    '''个人活动'''
    __tablename__ = 'useractivities'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('users.id',ondelete='cascade'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('activities.id',ondelete='cascade'))
    # workDate = db.Column('workdate', db.DateTime, nullable=False) # 增加
    content = db.Column('content', db.String(400), nullable=False) # 增加
    applyTime = db.Column('applytime', db.DateTime,default=datetime.now) # 增加
    type = db.Column('type', db.Enum('applying', 'applied','finished'),default='applying') # 志愿团体是否已阅申请消息？
    isRead=db.Column('isRead', db.Boolean,default=False)

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
            u_activity=UserActivity(user=u,applyTime=fp.date.datetime(),content = fp.lorem_ipsum.sentence(),activity=a,type='applying'if t==0 else 'applied' if t==1 else 'finished')
            db.session.add(u_activity)
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