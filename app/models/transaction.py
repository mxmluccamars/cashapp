"""
Módulo de Modelo de Dados para Transações (Transactions).

Define o mapeamento relacional (ORM) da tabela 'transactions' no banco de dados.
Esta entidade atua como o catálogo permanente de transações.
"""

import uuid
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Numeric, 
    Date, 
    ForeignKey, 
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Transaction(Base):
    """
    Representa o molde de uma transação.

    Relacionamentos:
        - Category: Categoria principal da transação (N:1)
        - Context: Contexto da transação (N:1, Opcional)
        - PaymentMethod: Forma de pagamento da transação (N:1)
        - Location: Local da transação (N:1, Opcional)
        - Goal: Meta da transação (N:1, Opcional)
        - RecurringBill: Conta de pagamento (N:1, Opcional)
    """
    __tablename__ = "transactions"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único da transação.")

    # dados
    date = Column(Date, nullable=False, doc="Data da transação.")
    type = Column(String(10), nullable=False, doc="Tipo de transação (EXPENSE ou INCOME).")
    description = Column(String(100), nullable=False, doc="Descrição da transação.")
    amount = Column(Numeric(12, 2), nullable=False, doc="Valor da transação.")
    notes = Column(Text, nullable=True, doc="Notas da transação.")

    # chaves estrangeiras
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, doc="Categoria da transação.")
    category = relationship("Category", lazy="joined")

    context_id = Column(String(36), ForeignKey("contexts.id", ondelete="SET NULL"), nullable=True, doc="Contexto da transação.")
    context = relationship("Context", lazy="joined")

    payment_method_id = Column(String(36), ForeignKey("payment_methods.id", ondelete="RESTRICT"), nullable=False, doc="Forma de pagamento da transação.")
    payment_method = relationship("PaymentMethod", lazy="joined")

    location_id = Column(String(36), ForeignKey("locations.id", ondelete="SET NULL"), nullable=True, doc="Local da transação.")
    location = relationship("Location", lazy="joined")

    goal_id = Column(String(36), ForeignKey("goals.id", ondelete="SET NULL"), nullable=True, doc="Meta da transação.")
    goal = relationship("Goal", lazy="joined")

    recurring_bill_id = Column(String(36), ForeignKey("recurring_bills.id", ondelete="SET NULL"), nullable=True, doc="Conta de pagamento da transação.")
    recurring_bill = relationship("RecurringBill", lazy="joined")

    # INSTALLMENTS
    installment_current = Column(Integer, nullable=True, doc="Número atual da parcela.")
    installment_total = Column(Integer, nullable=True, doc="Número total de parcelas.")
    installment_group_id = Column(String(36), nullable=True, doc="ID do grupo de parcelas.")

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação da transação.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização da transação.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<Transaction(date='{self.date}', type='{self.type}', description='{self.description}', amount='{self.amount}', notes='{self.notes}')>"