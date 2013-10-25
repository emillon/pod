from app import db
from sqlalchemy.orm.exc import NoResultFound
from models import User
import bcrypt


def auth_user(login, password):
    try:
        user = db.session.query(User).filter(User.name == login).one()
    except NoResultFound:
        return None
    db_hash = user.password
    hashed = bcrypt.hashpw(password.encode('utf-8'), db_hash.encode('ascii'))
    if db_hash != hashed:
        return None
    return user
