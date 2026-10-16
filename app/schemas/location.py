"""
Módulo de Schemas (DTOs) para Locais.

Define os contratos de validação de dados de entrada e serialização de saída (Pydantic).
Separa claramente o que é exigido no cadastro (POST), na atualização parcial (PATCH)
e o que é formatado e devolvido para a internet (GET).
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# 1. Base (Campos fundamentais comuns)
class LocationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do local")
    city: str = Field(..., min_length=2, max_length=50, description="Cidade do local")
    state: str = Field(..., min_length=2, max_length=2, description="Estado do local")

# 2. Create (Contrato do POST)
class LocationCreate(LocationBase):
    pass

# 3. Update (Contrato do PATCH - tudo opcional)
class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    state: Optional[str] = Field(None, min_length=2, max_length=2)

# 4. Response (O que a API devolve ao cliente)
class LocationResponse(LocationBase):
    id: str
    name: str
    city: str
    state: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)