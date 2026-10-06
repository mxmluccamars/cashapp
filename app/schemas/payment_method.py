from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PaymentMethodBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do método de pagamento")
    icon: Optional[str] = Field("tag", max_length=30)
    color: Optional[str] = Field("#10B981", pattern="^#([A-Fa-f0-9]{6})$")

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")

class PaymentMethodResponse(PaymentMethodBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)