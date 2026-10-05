import uuid
from sqlalchemy import Column, String, Boolean, DateTime    
from sqlalchemy.sql import func
from app.database.base import Base

class Context(Base):
    __tablename__ = "contexts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
