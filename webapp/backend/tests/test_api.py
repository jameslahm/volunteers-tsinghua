from flask import current_app, jsonify, url_for
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode, Suggestion)

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
        
        db.session.remove()
        db.drop_all()
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
        response2 = current_app.test_client().get(
            url_for('api.deleteActivity', id=Activity.query.filter_by(AID='998').first().id))
        # self.assertEqual(200, response.status_code)
        # self.assertIsNone(Activity.query.filter_by(AID='998').first())
        response3 = current_app.test_client().get(
            url_for('api.deleteMember',id=Activity.query.filter_by(AID='998').first().id))
        #self.assertEqual(200, response3.status_code)
        response4 = current_app.test_client().get(
            url_for('api.get_activity_info',id=Activity.query.filter_by(AID='998').first().id))
        #self.assertEqual(200, response4.status_code)
        response5 = current_app.test_client().get(
            url_for('api.get_activities'))
        current_app.test_client().get(url_for('auth.logout'))

    def test_user(self):
        test_user = User.query.filter_by(userName='testUser').first()
        user_info = test_user.to_json()
        for i in list(user_info.keys()):
            user_info[i] = str(user_info[i])
        user_info['token'] = test_user.generate_auth_token(3600 * 24 * 30)
        response = current_app.test_client().post(
            url_for('api.query_by_id', id=test_user.id),\
                headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, \
                data=json.dumps(user_info) )
        # response code 400
        self.assertEqual(200, response.status_code)
        response2 = current_app.test_client().get(
            url_for('api.get_user_activities',id=test_user.id),
        )
        self.assertEqual(200,response2.status_code)
        apply_info = {
            "id":1,
            "content": "",
            "token": user_info['token']
        }
        response3 = current_app.test_client().post(
            url_for('api.user_apply',id=test_user.id),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data=json.dumps(apply_info)
        )
        self.assertEqual(200,response3.status_code)
        response4 = current_app.test_client().get(
            url_for('api.get_user_messages',id=test_user.id),
        )
        self.assertEqual(200,response4.status_code)

    def test_mess(self):
        test_user = User.query.filter_by(userName='testUser').first()
        test_activity = Activity.query.filter_by(AID='998').first()

        test_ua = UserActivity(user=test_user, applyTime='2017-04-09', content="test ua", activity=test_activity,
                                  type='applied')
        test_mess = Message(user=test_user, activity=test_activity,
                            content="test message", time='2017-04-09', isRead=False)

        db.session.add_all([test_mess, test_ua])
        db.session.commit()

        mess_info = {"token": test_user.generate_auth_token(expiration=3600 * 24 * 30)}
        response = current_app.test_client().post(
            url_for('api.change_message_isread', id=test_mess.id),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data=json.dumps(mess_info))
        self.assertEqual(200, response.status_code)

        response = current_app.test_client().post(
            url_for('api.delete_message', id=test_mess.id),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data=json.dumps(mess_info))
        self.assertIsNone(Message.query.filter_by(content="test message").first())
        self.assertEqual(200, response.status_code)

        Message.query.filter_by(content="test message").delete()
        UserActivity.query.filter_by(content="test ua").delete()
        db.session.commit()

    def test_auth(self):
        test_user = User.query.filter_by(userName='testUser').first()
        user_token = {"token": test_user.generate_auth_token(expiration=3600 * 24 * 30)}
        response = current_app.test_client().get(
            url_for('api.verifyToken'),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data=json.dumps(user_token))
        # self.assertNotIn('error', str(response.data))
        self.assertEqual(200, response.status_code)
        print(str(response.data))

    def test_suggestion(self):
        info = {"content": "test suggestion"}
        response = current_app.test_client().post(
            url_for('api.suggestions'),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
            data=json.dumps(info)
        )
        t = Suggestion.query.filter_by(content="test suggestion").first()
        self.assertIsNotNone(t)
        Suggestion.query.filter_by(content="test suggestion").delete()
