# -*- coding: utf-8 -*-
'''读取应用环境变量配置'''
import os
import json


def get_config():
    '''读取配置'''
    root = os.environ.get('PROJ_ROOT', os.getcwd())


    # 数据库配置
    db_config = {}
    with open(os.path.join(root, 'config', 'database.json'), 'r') as db_f:
        db_config = json.loads(db_f.read())


    # 管理员账户
    admin_config = {}
    with open(os.path.join(root, 'config',  'admin.json'), 'r') as admin_f:
        admin_config = json.loads(admin_f.read())

    return {
        #'cdn_list': cdn_list,
        'db_config': db_config,
        'admin_config': admin_config, 
    }