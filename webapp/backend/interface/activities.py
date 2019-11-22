from flask import Blueprint, render_template, redirect, jsonify
from ..model import Activity
from . import interface


@interface.route('/activities/<int:id>', methods=['GET'])
def get_activity_info(id):
    activity_info = Activity.query.filter(Activity.id == id).first()
    if activity_info is None:
        return jsonify(activity_info)
    info = {
        'id': activity_info.id,
        # 'AID': activity_info.AID,
        'thumb': activity_info.thumb,
        'time': activity_info.time,
        'location': activity_info.location,
        'title': activity_info.title,
        'description': activity_info.description,
        'content': activity_info.content,
        'totalRecruits': activity_info.totalRecruits,
        'appliedRecruits': activity_info.appliedRecruits,
        'qrcode': activity_info.qrcode
    }
    return jsonify(info)


@interface.route('/activities/<int:id>/members', methods=['GET'])
def get_activity_members(id):
    pass
