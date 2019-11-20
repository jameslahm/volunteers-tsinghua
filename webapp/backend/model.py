# -*- coding: utf-8 -*-
'''模型'''

from .core.database import db


# class AdminUser(db.Model):
#     '''后台操作人员'''
#     __tablename__ = 'Administrator'
#
#     id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column("email", db.String(64), index=True, nullable=False)
#     name = db.Column("name", db.String(64))
#     password = db.Column("password", db.String(32))


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
    # AID = db.Column('AID', db.Integer, primary_key=True)
    thumb = db.Column('thumb', db.String(128), nullable=False)
    time = db.Column('time', db.DateTime, nullable=False)
    location = db.Column('location', db.String(20), nullable=False)
    title = db.Column('title', db.String(16), nullable=False)
    description = db.Column('description', db.String(50), nullable=False)
    content = db.Column('content', db.String(128), nullable=False)

class UserActivity(db.Model):
    '''个人活动'''
    __tablename__ = 'UserActivity'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column('userId', db.Integer, db.ForeignKey('User.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('Activity.id'))
    type = db.Column('type', db.Enum('applying', 'applyed', 'creating', 'created'))

    User = db.relationship('User', backref='UserActivity')
    Activity = db.relationship('Activity', backref='UserActivity')


class TeamActivity(db.Model):
    '''团队活动'''
    __tablename__ = 'TeamActivity'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    teamId = db.Column('teamId', db.Integer, db.ForeignKey('Team.id'))
    activityId = db.Column('activityId', db.Integer, db.ForeignKey('Activity.id'))
    type = db.Column('type', db.Enum('applying', 'applyed', 'creating', 'created'))

    Team = db.relationship('Team', backref='TeamActivity')
    Activity = db.relationship('Activity', backref='TeamActivity')