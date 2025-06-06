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


def update_user(**args):
    session = Session()
    id = args['id']
    user = session.query(User).filter(User.id == id).first()
    if 'is_active' in args:
        user.is_active = args['is_active']
    if 'subscription_id' in args:
        user.subscription_id = args['subscription_id']
    if 'password_reset_token' in args:
        user.password_reset_token = args['password_reset_token']
    session.commit()


def reset_user_password(password_reset_token, new_hashed_password):
    session = Session()
    user = session.query(User).filter(
        User.password_reset_token == password_reset_token).first()
    user.hashed_password = new_hashed_password
    user.password_reset_token = None
    session.commit()
