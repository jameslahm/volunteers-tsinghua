from flask import Blueprint, render_template, redirect, jsonify,request,abort
from ..model import User,UserActivity,Message
from . import api
from .. import db
from .authentication import verify_token

@api.route('messages/<int:id>/changeIsRead',methods=['GET','POST'])
def change_message_isread(id):
    data=request.json
    email=data.get('schoolId')
    token=data.get('token')
    if not verify_token(email,token):
        abort(402)
    message=Message.query.filter_by(id=id).first()
    message.isRead=True
    db.session.commit()
    return jsonify({})

@api.route('messages/<int:id>/delete',methods=['GET','POST'])
def delete_message(id):
    data=request.json
    email=data.get('schoolId')
    token=data.get('token')
    if not verify_token(email,token):
        abort(402)
    message=Message.query.filter_by(id=id).first()
    db.session.delete(message)
    db.session.commit()
    return jsonify({})