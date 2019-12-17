import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.model import User, Team


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        try:
            cls.client = webdriver.Chrome('F:/Programs/chromedriver_win32/chromedriver.exe',chrome_options=options)
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()
            email = cls.app.config['FLASK_ADMIN']
            name = 'admin'
            password = cls.app.config['FLASK_ADMIN_PASSWORD']

            if Team.query.filter_by(email=email).count() < 1:
                admin = Team(teamName=name, email=email, password=password)
                db.session.add(admin)
                db.session.commit()

            new_team = Team(teamName='testTeam', email='test@team', password='123456')
            db.session.add(new_team)
            db.session.commit()

            # start the Flask server in a thread
            cls.server_thread = threading.Thread(target=cls.app.run,
                                                 kwargs={'debug': False})
            cls.server_thread.start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.close()

            # destroy database
            db.session.remove()
            db.drop_all()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_home_page(self):
        self.client.get('http://127.0.0.1:5000')  
        self.assertTrue(re.search('志在清华',self.client.page_source) is not None)
        self.client.find_element_by_name('email').send_keys('test@team')
        self.client.find_element_by_name('password').send_keys('123456')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('上传头像',self.client.page_source) is not None)