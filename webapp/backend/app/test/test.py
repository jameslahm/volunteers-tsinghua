from flask import current_app, json
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random


class TestModel(unittest.TestCase):

    def setup(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exits(self):
        self.assertFalse(current_app is None)
        self.assertTrue(current_app.config['TESTING'])

    def test_add_data(self):
        for i in [User, Team, Activity, Message, UserActivity]:
            if i.query.first() is None:
                i.generate_fake()

    def test_model(self):
        User.query.filter_by(userName='testUser').delete()
        Team.query.filter_by(teamName='testTeam').delete()
        db.session.commit()

        self.assertIsNone(User.query.filter_by(userName='testUser').first())
        self.assertIsNone(Team.query.filter_by(teamName='testTeam').first())

        new_user = User(userName='testUser', email='test@user', phone='123456')
        new_team = Team(teamName='testTeam', email='test@team', password_hash='123456')
        db.session.add_all([new_user, new_team])
        db.session.commit()

        self.assertIsNotNone(User.query.filter_by(userName='testUser').first())
        self.assertIsNotNone(Team.query.filter_by(teamName='testTeam').first())

    def test_login(self):
        response = current_app.test_client().post(
            'auth/login',
            data={"email": "wrong@email", "password": "wrongpw", "remember_me": 1})
        json_data = response.data
        print("json_data:\n", json_data[:100])
