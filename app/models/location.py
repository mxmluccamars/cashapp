"""
Módulo de Modelo de Dados para Local (Location).

Define o mapeamento relacional (ORM) da tabela 'locations' no banco de dados.
Esta entidade atua como o contexto permanente de locais.
"""

import uuid
from sqlalchemy import (
    Column, 
    String, 
    DateTime
)
from sqlalchemy.sql import func
from app.database.base import Base


class Location(Base):
    """
    Representa o molde de um local.

    Relacionamentos:
        - Nenhum
    """

    __tablename__ = "locations"

    # id
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), doc="ID único do local.")

    # dados
    name = Column(String(50), nullable=False, unique=True, index=True, doc="Nome do local.")
    city = Column(String(50), nullable=False, doc="Cidade do local.")
    state = Column(String(2), nullable=False, doc="Estado do local.")
    # maybe someday...
    # country = Column(String(50), nullable=False, default="BR")

    # foreing keys

    # mapeamento de relacionamentos

    # auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, doc="Data de criação do local.")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, doc="Data de atualização do local.")

    def __repr__(self) -> str:
        """Representação em texto para depuração e logs do terminal."""
        return f"<Location(name='{self.name}', city='{self.city}', state='{self.state}')>"