import os
import unittest

from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        uri = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        r = self.app.get('/')
        self.assertIn('Hello', r.data)
