import uuid
from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.sql import func
from app.database.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(100), nullable=False)
    target_amount = Column(Numeric(12, 2), nullable=False)
    target_date = Column(DateTime, nullable=False)
    icon = Column(String(30), nullable=True, default="tag")
    color = Column(String(7), nullable=False, default="#FFEE00")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)