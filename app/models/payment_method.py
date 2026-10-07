"""
Módulo de Modelo de Dados para Formas de Pagamento (Payment Methods).

Define o mapeamento relacional (ORM) da tabela 'payment_methods' no banco de dados.
Esta entidade atua como o catálogo permanente de formas de pagamento.
"""

import uuid
from sqlalchemy import (
    Column, 
    String, 
    DateTime,
    Boolean
)
from sqlalchemy.sql import func
from app.database.base import Base


class PaymentMethod(Base):
    """
    Representa o molde de uma forma de pagamento.

    Relacionamentos:
        - Nenhum
    """

    __tablename__ = "payment_methods"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único da forma de pagamento.")

    # dados
    name = Column(String(50), nullable=False, unique=True, index=True, doc="Nome da forma de pagamento.")
    icon = Column(String(30), nullable=True, default="tag", doc="Ícone da forma de pagamento.")
    color = Column(String(7), nullable=False, default="#10B981", doc="Cor da forma de pagamento.")
    allow_installments = Column(Boolean, nullable=False, default=False, doc="Permite parcelamento?")

    # foreing keys

    # mapeamento de relacionamentos

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação da forma de pagamento.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização da forma de pagamento.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<PaymentMethod(name='{self.name}', icon='{self.icon}', color='{self.color}', allow_installments='{self.allow_installments}')>"