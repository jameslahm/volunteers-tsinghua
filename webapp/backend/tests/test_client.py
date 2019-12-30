from flask import current_app, jsonify, url_for
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random, json
import time

class ClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        new_user = User(userName='testUser', email='test@user', phone='123456')
        new_team = Team(teamName='testTeam', email='test@team', password='123456')
        db.session.add_all([new_user, new_team])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
        
        self.app_context.pop()

    def test_login(self):
        response = current_app.test_client().post(
            'auth/login',
            data={"email": "test@team", "password": "wrongpw", "remember_me": 0})
        json_data = response.data
        self.assertIsNotNone(json_data)

        response2 = current_app.test_client().post(
            'auth/login',
            data={"email": "test@team", "password": "123456", "remember_me": 0})
        json_data2 = response2.data
        self.assertIsNotNone(json_data2)
        current_app.test_client().get(url_for('auth.logout'))

        self.assertNotEqual(json_data, json_data2)

        response3 = current_app.test_client().post(
            'auth/login',
            data={"email": current_app.config['FLASK_ADMIN'], "password": current_app.config['FLASK_ADMIN_PASSWORD'], "remember_me": 0}
        )
        current_app.test_client().get(url_for('auth.logout'))
        self.assertIsNotNone(response3.data)

    def test_register(self):
        if IntroCode.query.filter_by(code="12345678").first() is None:
            new_intro_code = IntroCode(code="12345678")
            db.session.add(new_intro_code)
            db.session.commit()
        self.assertIsNotNone(IntroCode.query.filter_by(code="12345678").first())

        data = {"introcode": "12345678", "email": "test@register",
                "username": "test_user_name", "password": "test_user_pw","password2":"test_user_pw"}

        response = current_app.test_client().post(
            url_for('auth.register'),
            data=data
        )
        json_data = response.data

        time.sleep(2)

        new_team = Team.query.filter_by(email="test@register").first()
        self.assertIsNotNone(new_team)

        response = current_app.test_client().get(url_for('auth.logout'))
        self.assertIsNotNone(response)

        Team.query.filter_by(email="test@register").delete()
        IntroCode.query.filter_by(code="12345678").delete()
        db.session.commit()


    def test_webprofile(self):
        response = current_app.test_client().post(
            'auth/login',
            data={"email": "1436472425@qq.com", "password": "123456", "remember_me": 0})
        self.assertIsNotNone(response.data)
        response2 = current_app.test_client().get(url_for('main.index'))
        self.assertIsNotNone(response2.data)
        self.assertNotEqual(response.data, response2.data)
        response3 = current_app.test_client().post(
            'main/index',
            data={
                "teamName": "996",
                "email": "1436472425@qq.com",
                "phone": None,
                "password": None ,
                "description": None
            }
        )
        self.assertIsNotNone(response3.data)

