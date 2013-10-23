from flask import render_template
from app import app
from forms import NewFeedForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new')
def new_feed():
    form = NewFeedForm()
    return render_template('new_feed.html', title='New feed', form=form)
