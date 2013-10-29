"""
All views.
"""

from app import app, db, lm
from app.auth import auth_user
from app.tasks import get_feed
from app.models import User, Episode
from flask import render_template, flash, redirect, url_for, request
from flask.ext.wtf import Form
from flask.ext.login import login_user, logout_user, login_required
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo


@lm.user_loader
def load_user(userid):
    """
    Needed for flask-login.
    """
    return User.query.get(int(userid))


@app.route('/')
def home():
    """
    Home page
    """
    return render_template('home.html')


class NewFeedForm(Form):
    """
    Form used in new_feed
    """
    podcast_url = TextField(validators=[Required()])


@app.route('/new', methods=['GET', 'POST'])
def new_feed():
    """
    Add a new feed
    """
    form = NewFeedForm()
    if form.validate_on_submit():
        url = form.podcast_url.data
        flash('Adding podcast : ' + url)
        get_feed.delay(url)
        return redirect(url_for('home'))
    return render_template('new_feed.html', title='New feed', form=form)


class LoginForm(Form):
    """
    Form used in login
    """
    username = TextField(validators=[Required()])
    password = PasswordField(validators=[Required()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log a user in
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = auth_user(username, password)
        if user is None:
            flash('Bad login or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in')
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    """
    Log a user out
    """
    logout_user()
    return redirect(url_for('home'))


class SignupForm(Form):
    """
    Form used in signup
    """
    username = TextField(validators=[Required()])
    password = PasswordField(
        validators=[Required(),
                    EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(validators=[Required()])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign up a new user
    """
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('User successfully created')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign up', form=form)


@app.route('/episodes')
@login_required
def episodes():
    """
    Display all episodes
    """
    eps = db.session.query(Episode).filter(Episode.enclosure != None)
    return render_template('episodes.html', episodes=eps)
