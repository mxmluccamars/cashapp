"""
Módulo de Schemas (DTOs) para Formas de Pagamento.

Define os contratos de validação de dados de entrada e serialização de saída (Pydantic).
Separa claramente o que é exigido no cadastro (POST), na atualização parcial (PATCH)
e o que é formatado e devolvido para a internet (GET).
"""


from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# 1. Base (Campos fundamentais comuns)
class PaymentMethodBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do método de pagamento")
    icon: Optional[str] = Field("tag", max_length=30, description="Nome da imagem do icone")
    color: Optional[str] = Field("#10B981", pattern="^#([A-Fa-f0-9]{6})$", description="Cor do icone")
    allow_installments: bool = Field(False, description="Permite parcelamento")

# 2. Create (Contrato do POST)
class PaymentMethodCreate(PaymentMethodBase):
    pass

# 3. Update (Contrato do PATCH - tudo opcional)
class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")
    allow_installments: Optional[bool] = Field(None)

# 4. Response (O que a API devolve ao cliente)
class PaymentMethodResponse(PaymentMethodBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)