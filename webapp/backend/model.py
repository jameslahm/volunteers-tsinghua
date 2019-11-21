# -*- coding: utf-8 -*-
'''模型'''

from .database import db


class User(db.Model):
    '''用户'''
    __tablename__ = 'User'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # TODO: how to get openId?
    # openId = db.Column("openId", db.String(64), unique=True, nullable=False)
    userName = db.Column("userName", db.String(16), unique=False, nullable=False)
    wx = db.Column("wx", db.String(64), unique=True, nullable=False)
    email = db.Column("email", db.String(64))
    avatar = db.Column("avatar", db.String(128))
    schoolId = db.Column("schoolId", db.Integer, unique=True, nullable=False)
    phone = db.Column("phone", db.Integer, unique=True, nullable=False)
    department = db.Column("department", db.String(16), unique=False, nullable=False)
    profile = db.Column("profile", db.String(16), unique=False, nullable=True)


class Team(db.Model):
    '''志愿团体'''
    __tablename__ = 'Team'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column("userName", db.String(64), unique=False, nullable=False)
    email = db.Column("email", db.String(64))
    avatar = db.Column("avatar", db.String(128))


class Activity(db.Model):
    '''活动'''
    __tablename__ = 'Activity'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    # TODO: how to set AId?
    # AID = db.Column('AID', db.Integer, primary_key=True)
    thumb = db.Column('thumb', db.String(128), nullable=False)
    time = db.Column('time', db.DateTime, nullable=False)
    location = db.Column('location', db.String(20), nullable=False)
    title = db.Column('title', db.String(16), nullable=False)
    description = db.Column('description', db.String(50), nullable=False)
    content = db.Column('content', db.String(128), nullable=False)
    totalRecruits = db.Column('totalRecruits', db.Integer, nullable=False)
    applyedRecruits = db.Column('applyedRecruits', db.Integer, nullable=False)
    # qrCode = db.Column('qrCode')


class Message(db.Model):
    '''消息'''
    __tablename__ = 'Message'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('User.id'))
    notifier = db.Column('notifier', db.Integer, db.ForeignKey('Team.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('Activity.id'))
    content = db.Column('content', db.String(128), nullable=False)

    user = db.relationship('User', backref='message_receiver', foreign_keys=[userId])
    team = db.relationship('Team', backref='message_sender', foreign_keys=[notifier])
    activity = db.relationship('Activity', backref='message_activity', foreign_keys=[activityId])

class UserActivity(db.Model):
    '''个人活动'''
    __tablename__ = 'UserActivity'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('User.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('Activity.id'))
    type = db.Column('type', db.Enum('applying', 'applyed', 'creating', 'created'))

    user = db.relationship('User', backref='user', foreign_keys=[userId])
    activity = db.relationship('Activity', backref='participator', foreign_keys=[activityId])


class TeamActivity(db.Model):
    '''团队活动'''
    __tablename__ = 'TeamActivity'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    teamId = db.Column('teamId', db.Integer, db.ForeignKey('Team.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('Activity.id'))
    type = db.Column('type', db.Enum('applying', 'applyed', 'creating', 'created'))

    team = db.relationship('Team', backref='team', foreign_keys=[teamId])
    activity = db.relationship('Activity', backref='activity', foreign_keys=[activityId])