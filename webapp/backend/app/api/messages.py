from flask import Blueprint, render_template, redirect, jsonify,request,abort
from ..model import User,UserActivity,Message
from . import api
from .. import db
from .authentication import verify_token

@api.route('messages/<int:id>/changeIsRead',methods=['POST'])
def change_message_isread(id):
    data=request.json
    token=data.get('token')
    u=verify_token(token)
    if not u:
        return jsonify({'error':'invalid token'})
    message=Message.query.filter_by(id=id).first()
    if message.user!=u:
        abort(403)
    message.isRead=True
    db.session.commit()
    return jsonify({})

@api.route('messages/<int:id>/delete',methods=['POST'])
def delete_message(id):
    data=request.json
    token=data.get('token')
    u=verify_token(token)
    if not u:
        return jsonify({'error':'invalid token'})
    message=Message.query.filter_by(id=id).first()
    if message and message.user!=u:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return jsonify({})