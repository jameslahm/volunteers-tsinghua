# -*- coding: utf-8 -*-
'''测试阶段-启动文件'''
import os
import sys

from werkzeug.routing import EndpointPrefix

from backend.startup import create_app
from backend.utils import touch, md5


def start_server(run_cfg=None, is_deploy=False):
    '''启动web服务器'''
    if not bool(run_cfg):
        run_cfg = {}
    proj_root = os.path.abspath(os.path.dirname(__file__))
    os.environ['PROJ_ROOT'] = proj_root
    config = {
        'use_cdn': False,
        'debug': run_cfg.get('debug', False),
        'secret': md5('!secret!'),
        'url_prefix': None,
        'debugtoolbar': True
    }
    app = create_app(config)
    app.proj_root = proj_root

    if 'host' in run_cfg and 'port' in run_cfg:
        print_host = run_cfg['host']
        if print_host == '0.0.0.0':
            if sys.platform == 'win32' or os.name == 'nt':
                print_host = '127.0.0.1'
        print('=' * 28, 'visit by', '=' * 28)
        print('    http://{0}:{1}/'.format(print_host, run_cfg['port']))
        print('=' * 66)

    if is_deploy:
        return app
    app.run(**run_cfg)

if __name__ == '__main__':
    run_cfg = {
        'host': '0.0.0.0',
        'port': 5556,
        'debug': True,
        'threaded': True
    }
    start_server(run_cfg)