from flask.ext.rq import job
import feedparser
from models import Feed, Episode
from app import db


@job
def get_feed(url):
    fp = feedparser.parse(url)
    f = Feed(url, fp)
    db.session.add(f)
    db.session.expunge(f)
    for e in fp['entries']:
        title = e['title']
        ep = Episode(f.id, title)
        db.session.add(ep)
    db.session.commit()
