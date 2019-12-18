from flask import current_app, json
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode, Suggestion)

import unittest, random


class ModelTestCase(unittest.TestCase):

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
        new_message = Message(user=new_user, activity=new_activity, content='hao',
                    time='2017-04-09 15:30', isRead=False)
        db.session.add_all([new_user, new_team, new_activity,new_message])
        db.session.commit()

    def tearDown(self):
        
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_generate_fake(self):
        for i in [User, Team, Activity, Message, UserActivity]:
            if i.query.first() is None:
                i.generate_fake()

    def test_add_data(self):
        self.assertIsNotNone(User.query.filter_by(userName='testUser').first())
        self.assertIsNotNone(Team.query.filter_by(teamName='testTeam').first())

        new_suggestion = Suggestion(content="test suggestion")
        new_intro_code = IntroCode(code="12345678")
        db.session.add_all([new_suggestion, new_intro_code])
        db.session.commit()

        self.assertIsNotNone(Suggestion.query.first())
        self.assertIsNotNone(IntroCode.query.filter_by(code="12345678"))

        Suggestion.query.filter_by(content="test suggestion").delete()
        IntroCode.query.filter_by(code="12345678").delete()
        db.session.commit()

    def test_to_json(self):
        self.assertEqual('testUser',
                         User.query.filter_by(userName='testUser').first().to_json()['userName'])
        self.assertEqual('testTeam',
                         Team.query.filter_by(teamName='testTeam').first().to_json()['teamName'])
        self.assertEqual('hao',Message.query.filter_by(content='hao').first().to_json()['content'])
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
    def test_introcode(self):
        new_intro_code = IntroCode(code="12345678")
        db.session.add_all([new_intro_code])
        db.session.commit()
        self.assertTrue(IntroCode.verify_code('12345678'))
        IntroCode.query.filter_by(code="12345678").delete()
    def test_search_activity(self):
        self.assertIsNotNone(Activity.search('2017-04-09 15:25', 'time'))
        self.assertIsNotNone(Activity.search('testActivity', 'activity'))
        self.assertIsNotNone(Activity.search('testLocation', 'coordinates'))
        self.assertIsNotNone(Activity.search('testTeam', 'group'))
        self.assertIsNotNone(Activity.search('998', 'barrage'))

    def test_members(self):
        self.assertIsNotNone(Activity.search_bytitle('testActivity'))
