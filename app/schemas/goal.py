"""
Módulo de Schemas (DTOs) para Objetivos.

Define os contratos de validação de dados de entrada e serialização de saída (Pydantic).
Separa claramente o que é exigido no cadastro (POST), na atualização parcial (PATCH)
e o que é formatado e devolvido para a internet (GET).
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# 1. Base (Campos fundamentais comuns)
class GoalBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do objetivo")
    description: str = Field(..., min_length=2, max_length=100, description="Descrição do objetivo")
    target_amount: Decimal = Field(..., gt=0, description="Valor alvo do objetivo")
    target_date: Optional[datetime] = Field(None, description="Data alvo do objetivo")
    icon: Optional[str] = Field("tag", max_length=30, description="Nome da imagem do icone")
    color: Optional[str] = Field("#FFEE00", pattern="^#([A-Fa-f0-9]{6})$", description="Cor do icone")

# 2. Create (Contrato do POST)
class GoalCreate(GoalBase):
    pass

# 3. Update (Contrato do PATCH - tudo opcional)
class GoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=2, max_length=100)
    target_amount: Optional[Decimal] = Field(None, gt=0)
    target_date: Optional[datetime] = Field(None)
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")

# 4. Response (O que a API devolve ao cliente)
class GoalResponse(GoalBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

