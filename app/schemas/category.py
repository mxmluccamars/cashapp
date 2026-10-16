"""
Módulo de Schemas (DTOs) para Categorias.

Define os contratos de validação de dados de entrada e serialização de saída (Pydantic).
Separa claramente o que é exigido no cadastro (POST), na atualização parcial (PATCH)
e o que é formatado e devolvido para a internet (GET).
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Propriedades base compartilhadas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    type: str = Field(..., pattern="^(EXPENSE|INCOME)$", description="EXPENSE ou INCOME")
    icon: Optional[str] = Field("tag", max_length=30, description="Nome da imagem do icone")
    color: Optional[str] = Field("#10B981", pattern="^#([A-Fa-f0-9]{6})$", description="Cor do icone")
    monthly_limit: Optional[Decimal] = Field(None, gt=0, description="Limite mensal da categoria")



# Propriedades para criação (POST)
class CategoryCreate(CategoryBase):
    pass


# Propriedades para atualização parcial (PATCH)
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    type: Optional[str] = Field(None, pattern="^(EXPENSE|INCOME)$")
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")
    monthly_limit: Optional[Decimal] = Field(None, gt=0)


# O que a API devolve nas respostas (GET, POST, PATCH)
class CategoryResponse(CategoryBase):
    id: str
    created_at: datetime
    updated_at: datetime

    # Permite ler instâncias do SQLAlchemy diretamente
    model_config = ConfigDict(from_attributes=True)