from flask import render_template, flash, redirect, url_for, request
from app import app, db, lm
from forms import NewFeedForm, LoginForm, SignupForm
from tasks import get_feed
from auth import auth_user
from flask.ext.login import login_user, logout_user
from models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/new', methods=['GET', 'POST'])
def new_feed():
    form = NewFeedForm()
    if form.validate_on_submit():
        url = form.podcast_url.data
        flash('Adding podcast : ' + url)
        get_feed.delay(url)
        return redirect(url_for('home'))
    return render_template('new_feed.html', title='New feed', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.username.data
        password = form.password.data
        user = auth_user(login, password)
        if user is None:
            flash('Bad login or password')
            return redirect(url_for('login'))
        login_user(user)
        flash('Logged in')
        return redirect(request.args.get('next') or url_for('home'))
    return render_template('login.html', title='Log in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('signup.html', title='Sign up', form=form)
