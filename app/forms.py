from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class NewFeedForm(Form):
    podcast_url=TextField('openid', validators = [Required()])
