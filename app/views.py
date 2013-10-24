from flask import render_template, flash, redirect
from app import app
from forms import NewFeedForm
from tasks import get_feed


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
        return redirect('/')
    return render_template('new_feed.html', title='New feed', form=form)
