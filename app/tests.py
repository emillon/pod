import httpretty
import os
import unittest
import PyRSS2Gen

from app import app, db
from key import get_secret_key
import models


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

    def login(self, username, password, signup=False):
        if signup:
            self.signup(username, password)
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def setup_podcast(self, url):
        assert httpretty.is_enabled()
        items = [PyRSS2Gen.RSSItem(
            title='Episode %d' % n,
            enclosure=PyRSS2Gen.Enclosure('http://example.com/%d.mp3' % n,
                                          42,
                                          'audio/mpeg'
                                          )
            ) for n in [1, 2, 3]]
        items.append(PyRSS2Gen.RSSItem(title='Not an episode'))
        rss = PyRSS2Gen.RSS2('title', 'link', 'description', items=items)
        httpretty.register_uri(httpretty.GET, url, body=rss.to_xml())

    def add_podcast(self, url, with_setup=False):
        if with_setup:
            self.setup_podcast(url)
        r = self.app.post('/new',
                          data={'podcast_url': url},
                          follow_redirects=True)
        return r

    def test_signup_login_logout(self):
        r = self.app.get('/')
        self.assertIn('Log in', r.data)
        self.assertNotIn('Log out', r.data)
        self.assertNotIn('Admin panel', r.data)
        r = self.signup('a', 'a')
        self.assertIn('User successfully created', r.data)
        r = self.login('a', 'a')
        self.assertIn('Signed in as a', r.data)
        self.assertNotIn('Log in', r.data)
        self.assertIn('Log out', r.data)
        self.assertNotIn('Admin panel', r.data)
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

    @httpretty.activate
    def test_add_podcast(self):
        self.login('a', 'a', signup=True)
        url = 'http://example.com/podcast.rss'
        self.setup_podcast(url)
        r = self.add_podcast(url)
        self.assertIn('Adding podcast : ' + url, r.data)
        r = self.app.get('/episodes')
        self.assertIn('Episode 1', r.data)
        self.assertIn('Episode 2', r.data)
        self.assertIn('Episode 3', r.data)
        self.assertNotIn('Not an episode', r.data)

    @httpretty.activate
    def test_add_podcast_twice(self):
        self.login('a', 'a', signup=True)
        url = 'http://example.com/podcast.rss'
        self.setup_podcast(url)
        self.add_podcast(url)
        r = self.add_podcast(url)
        self.assertIn('This podcast already exists', r.data)

    def test_admin(self):
        r = self.signup('admin', 'admin')
        db.session.execute('UPDATE user SET role=:r WHERE name=:n',
                           {'r': models.ROLE_ADMIN,
                            'n': 'admin'
                            })
        db.session.commit()
        r = self.login('admin', 'admin')
        self.assertIn('Admin panel', r.data)
        r = self.app.get('/admin', follow_redirects=True)
        self.assertIn('Episode', r.data)

    def test_admin_denied(self):
        r = self.app.get('/admin', follow_redirects=True)
        self.assertNotIn('Episode', r.data)

    @httpretty.activate
    def test_episode_other_user(self):
        self.login('a', 'a', signup=True)
        url = 'http://example.com/podcast.rss'
        self.add_podcast(url, with_setup=True)
        self.logout()
        self.login('b', 'b', signup=True)
        r = self.app.get('/episodes')
        self.assertNotIn('Episode 1', r.data)
