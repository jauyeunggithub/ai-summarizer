from models.user import User
from db import Session


def get_user(email):
    session = Session()
    return session.query(User).filter(User.email == email).first()


def create_user(**args):
    session = Session()
    new_user = User(**args)
    session.add(new_user)
    session.commit()
