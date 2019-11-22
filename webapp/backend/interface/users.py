from flask import Blueprint, render_template, redirect, jsonify
from ..model import User
from . import interface


@interface.route('/users/<int:id>', methods=['GET'])
def query_by_id(id):
    user_info = User.query.filter(User.id == id).first()
    if user_info is None:
        return jsonify(user_info)
    info = {
        'id': user_info.id,
        # 'openId': user_info.openId,
        'userName': user_info.userName,
        'wx': user_info.wx,
        'email': user_info.email,
        'avatar': user_info.avatar,
        'schoolId': user_info.schoolId,
        'phone': user_info.phone,
        'department': user_info.department,
        'profile': user_info.profile
    }
    return jsonify(info)


@interface.route('/users/<int:id>/activities', methods=['GET'])
def get_activities(user_id):
    pass
