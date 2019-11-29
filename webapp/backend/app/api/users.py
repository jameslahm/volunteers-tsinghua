from flask import Blueprint, render_template, redirect, jsonify
from ..model import User,UserActivity,Message
from . import api


@api.route('/users/<int:id>', methods=['GET'])
def query_by_id(id):
    user_info = User.query.filter(User.id == id).first()
    if user_info is None:
        return jsonify({})
    return jsonify(user_info.to_json())


@api.route('/users/<int:id>/activities', methods=['GET'])
def get_user_activities(id):
    activities=UserActivity.query.filter_by(userId=id).all()
    res=[x.activity.to_json() for x in activities]
    return jsonify(res)


@api.route('/users/<int:id>/messages', methods=['GET'])
def get_user_messages(id):
    messages=User.query.filter_by(id=id).first().messages
    res=[x.to_json() for x in messages]
    return jsonify(res)