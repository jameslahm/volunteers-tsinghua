from flask import Blueprint, render_template, redirect, jsonify
from ..model import User,UserActivity
from . import api


@api.route('/users/<int:id>', methods=['GET'])
def query_by_id(id):
    user_info = User.query.filter(User.id == id).first()
    if user_info is None:
        return jsonify({})
    return jsonify(user_info.to_json())


@api.route('/users/<int:id>/activities', methods=['GET'])
def get_activities(user_id):
    pass
