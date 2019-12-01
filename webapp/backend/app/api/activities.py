from flask import Blueprint, render_template, redirect, jsonify,request,current_app
from ..model import Activity,UserActivity,Message
from . import api
from .. import db


@api.route('/activities', methods=['GET'])
def get_activities():
    page=request.args.get('page',1,type=int)
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
def deleteActivity():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    db.session.delete(activity)
    db.session.commit()
    return jsonify({})

@api.route('/deleteMember',methods=['GET'])
def deleteMember():
    id=request.args.get('id')
    userA=UserActivity.query.filter_by(id=id).first()
    db.session.delete(userA)
    db.session.commit()
    return jsonify({})

@api.route('/replyApply',methods=['GET'])
def replyApply():
    id=request.args.get('id')
    res=request.args.get('res')
    userA=UserActivity.query.filter_by(id=id).first()
    userA.type='applied' if res=='1' else 'applying'
    message=Message(user=userA.user,activity=userA.activity,content="拒绝")
    db.session.add(message)
    db.session.commit()
    return jsonify({})