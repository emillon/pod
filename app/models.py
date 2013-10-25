from app import db
import bcrypt


ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(self, login, password, workfactor=12):
        self.name = login
        salt = bcrypt.gensalt(workfactor)
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def by_name(name):
        return db.session.query(User).filter_by(name=name).first()

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    title = db.Column(db.String)

    def __init__(self, url, fp):
        """
        Parameters

        fp: a feedparser object
        """
        self.url = url
        self.title = fp['feed']['title']


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feed = db.Column(db.Integer, db.ForeignKey('feed.id'))
    title = db.Column(db.String)

    def __init__(self, feed, title):
        self.feed = feed
        self.title = title
