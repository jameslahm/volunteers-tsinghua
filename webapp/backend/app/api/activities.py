from flask import Blueprint, render_template, redirect, jsonify,request,current_app
from ..model import Activity,UserActivity
from . import api


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
