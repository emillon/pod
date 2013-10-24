from app import db

ROLE_USER=0
ROLE_ADMIN=1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
