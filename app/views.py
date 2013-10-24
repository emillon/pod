from flask import render_template, flash, redirect
from app import app
from forms import NewFeedForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new', methods=['GET', 'POST'])
def new_feed():
    form = NewFeedForm()
    if form.validate_on_submit():
        flash('Adding podcast : ' + form.podcast_url.data)
        return redirect('/')
    return render_template('new_feed.html', title='New feed', form=form)
