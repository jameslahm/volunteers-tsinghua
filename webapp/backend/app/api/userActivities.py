from flask import Blueprint, render_template, redirect, jsonify,request,current_app
from ..model import Activity,UserActivity,Message
from . import api
from .. import db
from flask_login import login_required


@api.route('/userActivities/changeIsRead',methods=['GET'])
@login_required
def UA_changeIsRead():
    id=request.args.get('id')
    userA=UserActivity.query.filter_by(id=id).first()
    userA.isRead=True
    db.session.commit()
    return jsonify({})