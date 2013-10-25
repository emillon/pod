from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo


class NewFeedForm(Form):
    podcast_url = TextField(validators=[Required()])


class LoginForm(Form):
    username = TextField(validators=[Required()])
    password = PasswordField(validators=[Required()])


class SignupForm(Form):
    username = TextField(validators=[Required()])
    password = PasswordField(
        validators=[Required(),
                    EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(validators=[Required()])
