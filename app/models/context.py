"""
Módulo de Modelo de Dados para Contexto (Context).

Define o mapeamento relacional (ORM) da tabela 'contexts' no banco de dados.
Esta entidade atua como o contexto permanente de contextos.
"""

import uuid
from sqlalchemy import (
    Column, 
    String,
    DateTime
)   
from sqlalchemy.sql import func
from app.database.base import Base

class Context(Base):
    """
    Representa o molde de um contexto.

    Relacionamentos:
        - Nenhum
    """

    __tablename__ = "contexts"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único do contexto.")

    # dados
    name = Column(String(50), nullable=False, unique=True, index=True)

    # foreing keys

    # mapeamento de relacionamentos

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação do contexto.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização do contexto.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<Context(name='{self.name}')>"