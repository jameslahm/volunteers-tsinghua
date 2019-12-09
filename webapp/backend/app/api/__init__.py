# -*- coding: utf-8 -*-
'''数据接口定义'''

from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, activities,messages,userActivities,authentication
