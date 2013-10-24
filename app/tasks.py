from flask.ext.rq import job
import feedparser

@job
def get_feed(url):
    f = feedparser.parse(url)
    print f['feed']['title']
