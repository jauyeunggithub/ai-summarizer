from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class Summary(Base):
    __tablename__ = 'summaries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    file_path = Column(String(), nullable=True)
    text_to_summarize = Column(String(), nullable=True)
    created = Column(DateTime, nullable=False)
    summary_result = Column(String(), nullable=True)
    description = Column(String(), nullable=True)
    file_name = Column(String(), nullable=True)
    status = Column(String(), nullable=True)
    is_deleted = Column(Boolean(), nullable=True)
