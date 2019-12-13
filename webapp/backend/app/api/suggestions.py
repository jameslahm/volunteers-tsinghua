from flask import Blueprint, render_template, redirect, jsonify,request,current_app
from ..model import Suggestion
from . import api
from .. import db
from flask_login import login_required

@api.route('/suggestions',methods=['POST'])
def suggestions():
    data=request.json
    content=data.get('content')
    suggestion=Suggestion(content=content)
    try:
        db.session.add(suggestion)
        db.session.commit()
        return jsonify({})
    except Exception as e:
        return jsonify({'error':e.message})

