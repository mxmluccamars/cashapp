"""
Módulo de Modelo de Dados para Assinaturas (Recurring Bills).

Define o mapeamento relacional (ORM) da tabela 'recurring_bills' no banco de dados.
Esta entidade atua como o catálogo permanente de assinaturas.
"""

import uuid
from sqlalchemy import (
    Column, 
    Numeric, 
    String, 
    DateTime,
    Boolean,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base


class RecurringBill(Base):
    """
    Representa o molde de uma assinatura.

    Relacionamentos:
        - Category: Categoria principal da conta (N:1, Opcional)
        - PaymentMethod: Forma de pagamento da conta (N:1, Opcional)
        - Transaction: Transações associadas a esta conta (1:N backref)
    """

    __tablename__ = "recurring_bills"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único da conta.")

    # dados
    name = Column(String(100), nullable=False, unique=True, index=True, doc="Nome da conta.")
    amount = Column(Numeric(12, 2), nullable=False, doc="Valor da conta.")
    due_day = Column(Integer, nullable=False, doc="Dia de vencimento da conta.")
    is_active = Column(Boolean, default=True, nullable=False, doc="Ativo ou inativo da conta.")

    # foreing keys
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

    # mapeamento de relacionamentos
    category = relationship("Category", backref="recurring_bills", lazy="joined")
    payment_method = relationship("PaymentMethod", backref="recurring_bills", lazy="joined")

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação da conta.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização da conta.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<RecurringBill(name='{self.name}', amount='{self.amount}', due_day='{self.due_day}', is_active='{self.is_active}')>"