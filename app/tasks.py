from flask.ext.rq import job
import feedparser
from models import Feed
from app import db


@job
def get_feed(url):
    fp = feedparser.parse(url)
    f = Feed(url, fp)
    db.session.add(f)
    db.session.commit()
