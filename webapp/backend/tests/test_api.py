from flask import current_app, json
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random


class APITestCase(unittest.TestCase):

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

    def test_login(self):
        response = current_app.test_client().post(
            'auth/login',
            data={"email": "wrong@email", "password": "wrongpw", "remember_me": 1})
        json_data = response.data
        print("json_data:\n", json_data[:100])
