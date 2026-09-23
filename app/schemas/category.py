from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Propriedades base compartilhadas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome da categoria")
    type: str = Field(..., pattern="^(EXPENSE|INCOME)$", description="EXPENSE ou INCOME")
    icon: Optional[str] = Field("tag", max_length=30)
    color: Optional[str] = Field("#10B981", pattern="^#([A-Fa-f0-9]{6})$")


# Propriedades para criação (POST)
class CategoryCreate(CategoryBase):
    pass


# Propriedades para atualização parcial (PATCH)
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    type: Optional[str] = Field(None, pattern="^(EXPENSE|INCOME)$")
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")
    is_active: Optional[bool] = None


# O que a API devolve nas respostas (GET, POST, PATCH)
class CategoryResponse(CategoryBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Permite ler instâncias do SQLAlchemy diretamente
    model_config = ConfigDict(from_attributes=True)