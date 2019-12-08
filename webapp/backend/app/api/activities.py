from flask import Blueprint, render_template, redirect, jsonify,request,current_app
from ..model import Activity,UserActivity,Message
from . import api
from .. import db
from flask_login import login_required


@api.route('/activities', methods=['GET'])
def get_activities():
    page=request.args.get('page',1,type=int)
    type=request.args.get('type','',type=str)
    text=request.args.get('text','',type=str)
    if(type==''):
        pagination = Activity.query.order_by(Activity.starttime.desc()).paginate(
            page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False
        )
        total=int(len(Activity.query.all())/current_app.config['FLASKY_POSTS_PER_PAGE'])
        if(len(Activity.query.all())%current_app.config['FLASKY_POSTS_PER_PAGE']!=0):
            total+=1
        activities=pagination.items
        if activities is None:
            return jsonify({})
        items=[x.to_json() for x in activities]
        res={'total':total,'items':items}
    else:
        items=Activity.search(text,type)
        total=len(items)
        res={'total':total,'items':items}
    return jsonify(res)


@api.route('/activities/<int:id>', methods=['GET'])
def get_activity_info(id):
    activity_info = Activity.query.filter(id == id).first()
    if activity_info is None:
        return jsonify({})
    return jsonify(activity_info.to_json())


@api.route('/activities/<int:id>/members', methods=['GET'])
def get_activity_members(id):
    activity=Activity.query.filter_by(id == id).first()
    members=[x.to_json() for x in activity.members()]
    return jsonify(members)


@api.route('/deleteActivity',methods=['GET'])
@login_required
def deleteActivity():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    db.session.delete(activity)
    db.session.commit()
    return jsonify({})

@api.route('/deleteMember',methods=['GET'])
@login_required
def deleteMember():
    id=request.args.get('id')
    userA=UserActivity.query.filter_by(id=id).first()
    db.session.delete(userA)
    db.session.commit()
    return jsonify({})

@api.route('/replyApply',methods=['GET'])
@login_required
def replyApply():
    id=request.args.get('id')
    res=request.args.get('res')
    userA=UserActivity.query.filter_by(id=id).first()
    if res=='1':
        userA.type='applied'
        message=Message(user=userA.user,activity=userA.activity,content="同意")
    else:
        message=Message(user=userA.user,activity=userA.activity,content="拒绝")
        db.session.delete(userA)
    db.session.add(message)
    db.session.commit()
    return jsonify({})

@api.route('/changeIsRead',methods=['GET'])
@login_required
def changeIsRead():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    activity.isRead=True
    db.session.commit()
    return jsonify({})