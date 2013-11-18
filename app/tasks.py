"""
Tasks ran asynchronously through RQ
"""

import feedparser
from app.models import Feed, Episode, Subscription
from app import app, db
from flask.ext.rq import get_queue


def job(func):
    """
    Redefinition of job decorator from flask-rq, to
    work around some limitations.
    If we're testing, we don't want to hit redis.
    """

    def wrapper(fn):
        def delay(*args, **kwargs):
            if app.config['TESTING']:
                return fn(*args, **kwargs)
            else:
                q = get_queue()
                return q.enqueue(fn, *args, **kwargs)

        fn.delay = delay
        return fn

    return wrapper(func)


def find_enclosure(entry):
    """
    Find first enclosure in a feedparser entry
    (one element of fp['entries'])
    """
    if 'links' in entry:
        for link in entry['links']:
            if link['rel'] == 'enclosure':
                return link['href']
    return None


@job
def get_feed(url, and_subscribe=None):
    """
      - download a RSS url
      - make a Feed entry for it
      - populate corresponding Episodes

    kwargs

    and_subscribe: if not None, the specified userid gets subscribed to it.
    """
    feedp = feedparser.parse(url)
    feed = Feed(url, feedp)
    db.session.add(feed)
    db.session.flush()
    for entry in feedp['entries']:
        title = entry['title']
        enclosure = find_enclosure(entry)
        episode = Episode(feed.id, title, enclosure)
        db.session.add(episode)
    if and_subscribe is not None:
        userid = and_subscribe
        sub = Subscription(feed.id, userid)
        db.session.add(sub)
    db.session.commit()
