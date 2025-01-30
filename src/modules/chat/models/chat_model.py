import uuid
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, INTEGER, TEXT, VARCHAR

from db_config.database import  Base

class CHAT_model(Base):
    __tablename__ = 'chat'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level = Column(VARCHAR, nullable=False)
    username = Column(VARCHAR, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now)


class MESSAGES_model(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    message = Column(TEXT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now)

