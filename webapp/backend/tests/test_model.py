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

    def test_generate_fake(self):
        for i in [User, Team, Activity, Message, UserActivity]:
            if i.query.first() is None:
                i.generate_fake()

    def test_add_data(self):
        self.assertIsNotNone(User.query.filter_by(userName='testUser').first())
        self.assertIsNotNone(Team.query.filter_by(teamName='testTeam').first())

    def test_to_json(self):
        self.assertEqual('testUser',
                         User.query.filter_by(userName='testUser').first().to_json()['userName'])
        self.assertEqual('testTeam',
                         Team.query.filter_by(teamName='testTeam').first().to_json()['teamName'])

    def test_is_admin(self):
        new_team = Team.query.filter_by(teamName='testTeam').first()
        self.assertFalse(new_team.is_administrator())

    def test_password(self):
        new_team = Team.query.filter_by(teamName='testTeam').first()
        with self.assertRaises(AttributeError):
            new_team.password
        self.assertTrue(new_team.verify_password('123456'))
        self.assertFalse(new_team.verify_password('12345678'))

    def test_user_token(self):
        new_user = User.query.filter_by(userName='testUser').first()
        token = new_user.generate_auth_token(expiration=3600*24*30)
        self.assertIsNotNone(token)
        self.assertTrue(new_user.verify_auth_token(token))

    def test_team_token(self):
        new_team = Team.query.filter_by(teamName='testTeam').first()
        token = new_team.generate_reset_token(expiration=3600 * 24 * 30)
        self.assertIsNotNone(token)
        self.assertTrue(new_team.verify_reset_token(token))