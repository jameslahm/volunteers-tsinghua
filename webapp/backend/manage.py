# -*- coding: utf-8 -*-
'''测试阶段-启动文件'''
import os
import sys

from flask_script import Manager, Shell
from flask_migrate import Migrate,MigrateCommand
from werkzeug.routing import EndpointPrefix

from app import create_app,db


def make_shell_context():
    return dict(app=app, db=db, User=User)

def init_admin(app):
    '''初始化管理员用户'''

    with app.test_request_context():
        db = app.db
        email = app.config['FLASK_ADMIN']
        name = 'admin'
        password = app.config['FLASK_ADMIN_PASSWORD']

        from app.model import Team

        if Team.query.filter_by(email=email).count() < 1:
            admin=Team(userName=name,email=email,password=password)
            db.session.add(admin)
            db.session.commit()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
init_admin(app)
migrate=Migrate(app,db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
    return


if __name__ == '__main__':
    manager.run()