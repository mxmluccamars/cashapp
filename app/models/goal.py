"""
Módulo de Modelo de Dados para Metas (Goals).

Define o mapeamento relacional (ORM) da tabela 'goals' no banco de dados.
Esta entidade atua como o catálogo permanente de metas.
"""

import uuid
from sqlalchemy import (
    Column, 
    Numeric, 
    String, 
    DateTime
)
from sqlalchemy.sql import func
from app.database.base import Base


class Goal(Base):
    """
    Representa o molde de uma meta.

    Relacionamentos:
        - Nenhum
    """

    __tablename__ = "goals"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único da meta.")

    # dados
    name = Column(String(50), nullable=False, unique=True, index=True, doc="Nome da meta.")
    description = Column(String(100), nullable=False, doc="Descrição da meta.")
    target_amount = Column(Numeric(12, 2), nullable=False, doc="Valor alvo da meta.")
    target_date = Column(DateTime, nullable=True, doc="Data alvo da meta.")
    icon = Column(String(30), nullable=True, default="tag", doc="Ícone da meta.")
    color = Column(String(7), nullable=False, default="#FFEE00", doc="Cor da meta.")

    # foreing keys

    # mapeamento de relacionamentos

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação da meta.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização da meta.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<Goal(name='{self.name}', description='{self.description}', target_amount='{self.target_amount}', target_date='{self.target_date}', icon='{self.icon}', color='{self.color}')>"