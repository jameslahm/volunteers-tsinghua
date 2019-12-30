from flask import Blueprint, render_template, redirect, jsonify,request,current_app,abort
from ..model import Activity,UserActivity,Message
from . import api
from .. import db
from flask_login import login_required,current_user
from .authentication import verify_token


@api.route('/activities', methods=['GET'])
def get_activities():
    page=request.args.get('page',1,type=int)
    type=request.args.get('type','',type=str)
    text=request.args.get('text','',type=str)
    if(type==''):
        pagination = Activity.query.filter_by(type='created').order_by(Activity.starttime.desc()).paginate(
            page,per_page=current_app.config['FLASK_WX_PER_PAGE'],error_out=False
        )
        total=int(len(Activity.query.filter_by(type='created').all())/current_app.config['FLASK_WX_PER_PAGE'])
        if(len(Activity.query.filter_by(type='created').all())%current_app.config['FLASK_WX_PER_PAGE']!=0):
            total+=1
        activities=pagination.items
        if activities is None:
            return jsonify({})
        items=[x.to_json() for x in activities]
        res={'total':total,'items':items}
    else:
        if(type=='general'):
            type='activity'
        items=Activity.search(text,type)
        if items is not None:
            total=len(items)
            items=[x.to_json() for x in items]
        else:
            total=0
            items=[]
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
    activity=Activity.query.filter_by(id=id).first()
    members=[x.to_json() for x in activity.members()]
    return jsonify(members)


@api.route('/activities/deleteActivity',methods=['GET'])
@login_required
def deleteActivity():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    if not activity:
        return jsonify({'error':'no activity'})
    if(activity.team==current_user):
        db.session.delete(activity)
        db.session.commit()
    return jsonify({})

@api.route('/activities/deleteMember',methods=['GET'])
@login_required
def deleteMember():
    id=request.args.get('id')
    userA=UserActivity.query.filter_by(id=id).first()
    if(userA):
        activity=Activity.query.filter_by(id=userA.activity.id).first()
        if(activity.team==current_user):
            db.session.delete(userA)
            activity.appliedRecruits=activity.appliedRecruits-1
            db.session.commit()
    return jsonify({})

@api.route('/activities/replyApply',methods=['GET'])
@login_required
def replyApply():
    id=request.args.get('id')
    res=request.args.get('res')
    userA=UserActivity.query.filter_by(id=id).first()
    if not userA:
        return jsonify({})
    if res=='1':
        if(userA.activity.team==current_user):
            userA.type='applied'
            userA.activity.appliedRecruits+=1
            message=Message(user=userA.user,activity=userA.activity,content='恭喜您，您申请参加的活动:{}，已被活动负责人批准，请及时扫描下方二维码加入活动群'.format(userA.activity.title))
            db.session.add(message)
            db.session.commit()
    else:
        if(userA.activity.team==current_user):
            userA.type='refused'
            message=Message(user=userA.user,activity=userA.activity,content="抱歉，很遗憾的通知您，您申请参加的活动:{}，已被活动负责人拒绝".format(userA.activity.title))
            db.session.delete(userA)
            db.session.add(message)
            db.session.commit()
    return jsonify({})

@api.route('/activities/changeIsRead',methods=['GET'])
@login_required
def changeIsRead():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    if activity:
        if activity.team==current_user:
            activity.isRead=True
            db.session.commit()
    return jsonify({})

@api.route('/activities/updateVolunteerHours',methods=['POST'])
@login_required
def updateVolunteerHours():
    data=request.json
    id=int(data.get('id'))
    activity=Activity.query.filter_by(id=id).first()
    if(not activity):
        return jsonify({'error':'no activity'})
    if not activity.team==current_user:
        return jsonify({})
    hours=data.get('hours')
    hours=[int(x) for x in hours]
    for i,userA in enumerate(activity.userActivities):
        userA.hours=hours[i]
    db.session.commit()
    return jsonify({})

@api.route('/activities/applyFinish',methods=['GET'])
@login_required
def applyFinish():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    if(not activity):
        return jsonify({})
    if not activity.team==current_user:
        return jsonify({})
    activity.isApplyFinish=True
    db.session.commit()
    return jsonify({})

@api.route('/activities/<int:id>/signin',methods=['GET','POST'])
def signin(id):
    data=request.json
    token=data.get('token')
    u=verify_token(token)
    if not u:
        return jsonify({'error':'invalid token'})
    userA=UserActivity.query.filter_by(activityId=id,user=u).first()
    userA.isSignIn=True
    db.session.commit()
    return jsonify({})


@api.route('/activities/<int:id>/createQrCode',methods=['GET'])
def createQrCode(id):
    return render_template('qrcode.html',id=id)

@api.route('/activities/deleteMessage',methods=['GET'])
@login_required
def deleteMessage():
    id=request.args.get('id')
    activity=Activity.query.filter_by(id=id).first()
    if activity.team==current_user:
        activity.isMessage=False
        db.session.commit()
    return jsonify({})
