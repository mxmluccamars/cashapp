import uuid
from sqlalchemy import Column, String, Numeric, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class RecurringBill(Base):
    __tablename__ = "recurring_bills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(100), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    due_day = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    category_id = Column(
        String(36), 
        ForeignKey("categories.id", ondelete="SET NULL"), 
        nullable=True
    )
    payment_method_id = Column(
        String(36), 
        ForeignKey("payment_methods.id", ondelete="SET NULL"), 
        nullable=True
    )

    category = relationship("Category", backref="recurring_bills", lazy="joined")
    payment_method = relationship("PaymentMethod", backref="recurring_bills", lazy="joined")


    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )