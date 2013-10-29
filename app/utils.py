from app import app
from flask.ext.rq import job as _job


class job(object):
    def __init__(self, fn):
        self.fn = fn

    def delay(self, *args, **kwargs):
        if app.config['TESTING']:
            return self.fn(*args, **kwargs)
        else:
            return _job(fn).delay(*args, **kwargs)
