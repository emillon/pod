"""
Tasks ran asynchronously through RQ
"""

import feedparser
from app.models import Feed, Episode
from app import db
from app.utils import job


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
def get_feed(url):
    """
      - download a RSS url
      - make a Feed entry for it
      - populate corresponding Episodes
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
    db.session.commit()
