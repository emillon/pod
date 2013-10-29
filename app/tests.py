import os
import unittest

from app import app, db
from key import get_secret_key


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        uri = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        self.key_file = os.path.join(app.instance_path, 'secret-test.key')
        app.config['SECRET_KEY'] = get_secret_key(self.key_file)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove(self.key_file)

    def test_home(self):
        r = self.app.get('/')
        self.assertIn('Hello', r.data)

    def signup(self, username, password):
        return self.app.post('/signup', data=dict(
            username=username,
            password=password,
            confirm=password
            ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_signup_login_logout(self):
        r = self.app.get('/')
        self.assertIn('Log in', r.data)
        self.assertNotIn('Log out', r.data)
        r = self.signup('a', 'a')
        self.assertIn('User successfully created', r.data)
        r = self.login('a', 'a')
        self.assertIn('Signed in as a', r.data)
        self.assertNotIn('Log in', r.data)
        self.assertIn('Log out', r.data)
        r = self.logout()
        self.assertIn('Log in', r.data)
        self.assertNotIn('Log out', r.data)

    def test_login_nonexistent(self):
        r = self.login('doesnt', 'exist')
        self.assertIn('Bad login or password', r.data)

    def test_login_bad_pass(self):
        self.signup('a', 'a')
        r = self.login('a', 'b')
        self.assertIn('Bad login or password', r.data)
