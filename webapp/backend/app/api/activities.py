from flask import Blueprint, render_template, redirect, jsonify
from ..model import Activity,UserActivity
from . import api


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
