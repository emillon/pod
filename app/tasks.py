import feedparser
from models import Feed, Episode
from app import db
from utils import job


def find_enclosure(entry):
    """
    entry is a feedparser entry (one element of fp['entries'])
    """
    if 'links' in entry:
        for l in entry['links']:
            if l['rel'] == 'enclosure':
                return l['href']
    return None


@job
def get_feed(url):
    fp = feedparser.parse(url)
    f = Feed(url, fp)
    db.session.add(f)
    db.session.expunge(f)
    for e in fp['entries']:
        title = e['title']
        enclosure = find_enclosure(e)
        ep = Episode(f.id, title, enclosure)
        db.session.add(ep)
    db.session.commit()
