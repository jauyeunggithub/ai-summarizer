from sqlalchemy import Column, Boolean, String, Date
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String(300), unique=True, nullable=False)
    first_name = Column(String(300), nullable=False)
    last_name = Column(String(300), nullable=False)
    subscription_id = Column(String(300), unique=True, nullable=False)
    created = Column(Date, nullable=False)
    hashed_password = Column(String(500), unique=True, nullable=False)
    customer_id = Column(String(), unique=True, nullable=False)
    subscription_id = Column(String(), unique=True, nullable=False)
    status = Column(String(), unique=True, nullable=False)
    password_reset_token = Column(String(), unique=True, nullable=False)
    is_active = Column(Boolean(), nullable=True)
