from flask import g,jsonify,request
from ..model import User
from . import api
import requests
from .. import db

def verify_token(token):
    return User.verify_auth_token(token)

@api.route('/verifyToken',methods=['GET'])
def verifyToken():
    u=verify_token(request.args.get('token',''))
    if not u:
        return jsonify({'error':'invaild token'})
    return jsonify({})

@api.route('/verifyTHU',methods=['POST'])
def verifyTHU():
    data=request.json
    url="https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token"
    res=requests.post(url,data).json().get('user')
    u=User.query.filter_by(schoolId=res.get('card')).first()
    if not u:
        u=User(schoolId=res.get('card'),userName=res.get('name'),department=res.get('department'))
        db.session.add(u)
        db.session.commit()
    return jsonify({'user':u.to_json(),'token':u.generate_auth_token(3600*24*30)})
    
