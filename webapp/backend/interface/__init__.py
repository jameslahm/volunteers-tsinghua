# -*- coding: utf-8 -*-
'''数据接口定义'''

from flask import Blueprint

interface = Blueprint('interface', __name__)

from . import users, activities
