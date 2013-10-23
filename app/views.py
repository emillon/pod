from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new')
def new_feed():
    return render_template('new_feed.html')
