import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    date = Column(Date, nullable=False)
    type = Column(String(10), nullable=False)  # EXPENSE ou INCOME
    description = Column(String(100), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    notes = Column(Text, nullable=True)

    # chaves estrangeiras
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    category = relationship("Category", lazy="joined")

    context_id = Column(String(36), ForeignKey("contexts.id", ondelete="SET NULL"), nullable=True)
    context = relationship("Context", lazy="joined")

    payment_method_id = Column(String(36), ForeignKey("payment_methods.id", ondelete="RESTRICT"), nullable=False)
    payment_method = relationship("PaymentMethod", lazy="joined")

    location_id = Column(String(36), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    location = relationship("Location", lazy="joined")

    goal_id = Column(String(36), ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    goal = relationship("Goal", lazy="joined")

    recurring_bill_id = Column(String(36), ForeignKey("recurring_bills.id", ondelete="SET NULL"), nullable=True)
    recurring_bill = relationship("RecurringBill", lazy="joined")

    # INSTALLMENTS
    installment_current = Column(Integer, nullable=True)
    installment_total = Column(Integer, nullable=True)
    installment_group_id = Column(String(36), nullable=True)

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)