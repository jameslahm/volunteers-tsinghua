from flask import Blueprint, render_template, redirect, jsonify,request,abort
from ..model import User,UserActivity,Message,Activity
from . import api
from .authentication import verify_token
from .. import db


@api.route('/users/<int:id>', methods=['GET','POST'])
def query_by_id(id):
    if request.method=='POST':
        data=request.json
        user=verify_token(data.get('token'))
        if not user:
            abort(403)
        user.userName=data.get('userName')
        user.department=data.get('department')
        user.wx=data.get('wx')
        user.email=data.get('email')
        user.phone=data.get('phone')
        user.description=data.get('description')
        user.avatar=data.get('avatar')
        db.session.commit()
        return jsonify(user.to_json())
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
        temp['hours']=x.hours
        res.append(temp)
    return jsonify(res)


@api.route('/users/<int:id>/messages', methods=['GET'])
def get_user_messages(id):
    messages=User.query.filter_by(id=id).first().messages
    res=[x.to_json() for x in messages]
    return jsonify(res)

@api.route('/users/<int:id>/apply',methods=['POST'])
def user_apply(id):
    data=request.json
    token=data.get('token')
    u=verify_token(token)
    if not u:
        abort(403)
    content=data.get('content')
    itemId=data.get('id')
    activity=Activity.query.filter_by(id=itemId).first()
    userA=UserActivity(user=u,activity=activity,content=content,type='applying')
    db.session.add(userA)
    db.session.commit()
    return jsonify({})