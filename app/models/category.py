import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    # UUID como string para manter compatibilidade universal
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True, index=True)
    type = Column(String(10), nullable=False)  # EXPENSE ou INCOME
    icon = Column(String(30), nullable=True, default="tag")
    color = Column(String(7), nullable=False, default="#10B981")
    is_active = Column(Boolean, nullable=False, default=True)

    # Campos de auditoria automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)