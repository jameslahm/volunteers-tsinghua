from flask import current_app
from app import create_app, db
from app.model import (User, Team, Activity, Message, UserActivity, IntroCode)

import unittest, random


class TestModel(unittest.TestCase):

    def setup(self):
        self.app = create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exits(self):
        self.assertFalse(current_app is None)

    # def test_app_is_testing(self):
    #     self.assertFalse(current_app.config['testing'])


if __name__ == "test_app_exits":
    suite = unittest.TestSuite()
    tests = [
        TestModel('test_User'),
    ]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)