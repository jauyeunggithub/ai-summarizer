from sqlalchemy import Column, Integer, String, Date
from ..models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(300), unique=True, nullable=False)
    first_name = Column(String(300), nullable=False)
    last_name = Column(String(300), nullable=False)
    subscription_id = Column(String(300), unique=True, nullable=False)
    created = Column(Date, nullable=False)
    hashed_password = Column(String(500), unique=True, nullable=False)
