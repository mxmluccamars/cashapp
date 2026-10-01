import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String(100), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)  # EXPENSE ou INCOME
    notes = Column(Text, nullable=True)

    # chaves estrangeiras
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    category = relationship("Category", lazy="joined")

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)