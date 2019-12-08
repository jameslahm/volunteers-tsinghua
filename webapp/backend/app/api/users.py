from flask import Blueprint, render_template, redirect, jsonify,request
from ..model import User,UserActivity,Message,Activity
from . import api
from .authentication import verify_token
from .. import db


@api.route('/users/<int:id>', methods=['GET'])
def query_by_id(id):
    user_info = User.query.filter(User.id == id).first()
    if user_info is None:
        return jsonify({})
    return jsonify(user_info.to_json())


@api.route('/users/<int:id>/activities', methods=['GET'])
def get_user_activities(id):
    activities=UserActivity.query.filter_by(userId=id).all()
    res=[]
    for x in activities:
        temp=x.activity.to_json()
        temp['type']=x.type
        res.append(temp)
    return jsonify(res)


@api.route('/users/<int:id>/messages', methods=['GET'])
def get_user_messages(id):
    messages=User.query.filter_by(id=id).first().messages
    res=[x.to_json() for x in messages]
    return jsonify(res)

@api.route('/users/<int:id>/apply',methods=['GET'])
def user_apply(id):
    user=User.query.filter_by(id=id).first()
    content=request.args.get('content')
    itemId=request.args.get('id')
    activity=Activity.query.filter_by(id=itemId).first()
    userA=UserActivity(user=user,activity=activity,content=content,type='applying')
    db.session.add(userA)
    db.session.commit()
    return jsonify({})