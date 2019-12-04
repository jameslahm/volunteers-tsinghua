from flask import g,jsonify,request
from ..model import User
from . import api

def verify_token(email,token):
    user=User.query.filter_by(email=email).first()
    return user.verify_auth_token(token)


@api.route('/token',methods=['POST'])
def get_token():
    data=request.json
    schoolId=data.get('schoolId')
    password=data.get('password')
    #加入清华认证 
    user=User.query.filter_by(schoolId=schoolId).first()
    return jsonify({'token':user.generate_auth_token(expiration=3600*24*30),'expiration':3600*24*30})

