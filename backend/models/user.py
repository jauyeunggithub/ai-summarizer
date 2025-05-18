from sqlalchemy import Column, Integer, String
from models import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
