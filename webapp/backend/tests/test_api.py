from flask import current_app, json
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random


class APITestCase(unittest.TestCase):

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
        User.query.filter_by(userName='testUser').delete()
        Team.query.filter_by(teamName='testTeam').delete()
        db.session.commit()

        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = current_app.test_client().post(
            'auth/login',
            data={"email": "test@team", "password": "wrongpw", "remember_me": 0})
        json_data = response.data
        self.assertIn("remember-me", str(json_data))  # 登陆页面

        response2 = current_app.test_client().post(
            'auth/login',
            data={"email": "test@team", "password": "123456", "remember_me": 0})
        json_data2 = response2.data
        self.assertNotIn("remember-me", str(json_data2))  # 团体主页

    def test_register(self):
        new_intro_code = IntroCode(code="12345678")
        db.session.add(new_intro_code)
        db.session.commit()

        response = current_app.test_client().post(
            'auth/register',
            data={"code": new_intro_code.code, "email": "test@register",
                  "username": "test_user_name", "password": "test_user_pw"}
        )
        json_data = response.data
        self.assertIn("login", str(json_data))  # 登陆页面

        IntroCode.query.filter_by(code="12345678").delete()
        db.session.commit()