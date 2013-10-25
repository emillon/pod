import os
from random import choice
from string import ascii_uppercase, digits
from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from flask.ext.rq import RQ
from flask.ext.sqlalchemy import SQLAlchemy


def generate_key(n):
    return ''.join(choice(ascii_uppercase + digits) for x in range(n))


def get_secret_key(app):
    filename = os.path.join(app.instance_path, 'secret.key')
    try:
        with open(filename) as f:
            secret = f.read()
    except IOError as e:
        secret = generate_key(64)
        with open(filename, 'w+') as f:
            f.write(secret)
    return secret


app = Flask(__name__)
app.config.from_object('config')

# CSRF & stuff
app.config['SECRET_KEY'] = get_secret_key(app)

# RQ
RQ(app)

# SQLAlchemy
uri = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

# login
lm = LoginManager()
lm.init_app(app)


@app.before_request
def set_g_user():
    g.user = current_user

from app import views, models
