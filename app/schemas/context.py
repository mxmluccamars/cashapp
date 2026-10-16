"""
Módulo de Schemas (DTOs) para Contextos.

Define os contratos de validação de dados de entrada e serialização de saída (Pydantic).
Separa claramente o que é exigido no cadastro (POST), na atualização parcial (PATCH)
e o que é formatado e devolvido para a internet (GET).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# 1. Base (Campos fundamentais comuns)
class ContextBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do contexto")

# 2. Create (Contrato do POST)
class ContextCreate(ContextBase):
    pass

# 3. Update (Contrato do PATCH - tudo opcional)
class ContextUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)

# 4. Response (O que a API devolve ao cliente)
class ContextResponse(ContextBase):
    id: str
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)