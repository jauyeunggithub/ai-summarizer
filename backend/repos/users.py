from models.user import User
from db import session


def get_user(email):
    return session.query(User).filter(User.email == email).first()
