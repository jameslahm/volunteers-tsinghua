from flask import g,jsonify,request
from ..model import User
from . import api

def verify_token(token):
    return User.verify_auth_token(token)


@api.route('/token',methods=['POST','GET'])
def get_token():
    data=request.form
    id=data.get('id') or 1
    # password=data.get('password')
    #加入清华认证 
    user=User.query.filter_by(id=id).first()
    token=user.generate_auth_token(expiration=3600*24*30)
    return jsonify({'token':token,'expiration':str(3600*24*30)})

