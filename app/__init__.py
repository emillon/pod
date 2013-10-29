import os
from flask import Flask, g
from flask.ext.login import LoginManager, current_user
from flask.ext.rq import RQ
from flask.ext.sqlalchemy import SQLAlchemy
from key import get_secret_key


app = Flask(__name__)
app.config.from_object('config')

# CSRF & stuff
key_file = os.path.join(app.instance_path, 'secret.key')
app.config['SECRET_KEY'] = get_secret_key(key_file)

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
