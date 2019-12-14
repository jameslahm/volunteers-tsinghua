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
        self.assertIsNotNone(json_data)

        response2 = current_app.test_client().post(
            'auth/login',
            data={"email": "test@team", "password": "123456", "remember_me": 0})
        json_data2 = response2.data
        self.assertIsNotNone(json_data2)
        self.assertNotEqual(json_data, json_data2)
