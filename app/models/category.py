"""
Módulo de Modelo de Dados para Categorias (Categories).

Define o mapeamento relacional (ORM) da tabela 'categories' no banco de dados.
Esta entidade atua como o catálogo permanente de categorias.
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


class Category(Base):
    """
    Representa o molde de uma categoria.

    Relacionamentos:
        - Nenhum
    """

    __tablename__ = "categories"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único da categoria.")

    # dados
    name = Column(String(50), nullable=False, unique=True, index=True, doc="Nome da categoria.")
    type = Column(String(10), nullable=False, doc="Tipo de categoria (INCOME ou EXPENSE).")
    icon = Column(String(30), nullable=True, default="tag", doc="Ícone da categoria.")
    color = Column(String(7), nullable=False, default="#10B981", doc="Cor da categoria.")
    monthly_limit = Column(Numeric(12, 2), nullable=True, doc="Limite mensal da categoria.")

    # foreing keys

    # mapeamento de relacionamentos

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação da categoria.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização da categoria.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<Category(name='{self.name}', type='{self.type}', icon='{self.icon}', color='{self.color}', monthly_limit='{self.monthly_limit}')>"