"""
Models

When editing this file don't forget to set up a migration in alembic.

Coding rules:
  - class names are singular
  - be explicit about nullable
"""

from app import db
import bcrypt


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    """
    Application user. Someone that can log in.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER, nullable=False)

    def __init__(self, login, password, workfactor=12):
        self.name = login
        salt = bcrypt.gensalt(workfactor)
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def is_active(self):
        """
        Needed for flask-login.
        """
        return True

    def is_anonymous(self):
        """
        Needed for flask-login.
        """
        return False

    def is_authenticated(self):
        """
        Needed for flask-login.
        """
        return True

    def get_id(self):
        """
        Needed for flask-login.
        """
        return unicode(self.id)

    def is_admin(self):
        """
        Has the user got administrative rights?
        This grants access to admin panel, so careful.
        """
        return (self.role == ROLE_ADMIN)


class Feed(db.Model):
    """
    A RSS Feed.

    When adding a Feed, subsequent Episodes must be fetched
    through the get_feed task.
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)

    def __init__(self, url, feed):
        """
        Parameters

        feed: a feedparser object
        """
        self.url = url
        self.title = feed['feed']['title']


class Episode(db.Model):
    """
    A podcast episode.

    It can has an enclosure (audio file) or not.
    """
    id = db.Column(db.Integer, primary_key=True)
    feed = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    enclosure = db.Column(db.String, nullable=True)

    def __init__(self, feed, title, enclosure):
        self.feed = feed
        self.title = title
        self.enclosure = enclosure
