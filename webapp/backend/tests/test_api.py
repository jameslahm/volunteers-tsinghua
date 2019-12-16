from flask import current_app, jsonify, url_for
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random, json


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app.testing = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        new_user = User(userName='testUser', email='test@user', phone='123456')
        new_team = Team(teamName='testTeam', email='test@team', password='123456')
        new_activity = Activity(AID='998', team=new_team, starttime='2017-04-09 15:25',
                                endtime='2017-04-09 15:30', location="testLocation",
                                title="testActivity", content="testContent", managePerson="testManager",
                                managePhone=110, manageEmail='test@activity')
        db.session.add_all([new_user, new_team, new_activity])
        db.session.commit()

    def tearDown(self):
        User.query.filter_by(userName='testUser').delete()
        Team.query.filter_by(teamName='testTeam').delete()
        db.session.commit()

        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_activities(self):
        response = current_app.test_client().get(
            url_for('api.get_activity_members', id=Activity.query.filter_by(AID='998').first().id))
        self.assertEqual(200, response.status_code)
        self.assertEqual([], json.loads(response.data))

        current_app.test_client().post(
            url_for('auth.login'),
            data={"email": "test@team", "password": "123456", "remember_me": 0}
        )
        response = current_app.test_client().get(
            url_for('api.deleteActivity', id=Activity.query.filter_by(AID='998').first().id))
        # self.assertEqual(200, response.status_code)
        # self.assertIsNone(Activity.query.filter_by(AID='998').first())
        current_app.test_client().get(url_for('auth.logout'))

