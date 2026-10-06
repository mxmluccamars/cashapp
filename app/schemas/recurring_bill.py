from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.category import CategoryResponse
from app.schemas.payment_method import PaymentMethodResponse


# 1. Base (Campos fundamentais comuns)
class RecurringBillBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome da assinatura ou conta fixa")
    amount: Decimal = Field(..., gt=0, description="Valor mensal previsto (sempre maior que zero)")
    due_day: int = Field(..., ge=1, le=31, description="Dia do vencimento no mês (1 a 31)")
    category_id: Optional[str] = Field(default=None, description="ID da categoria associada")
    payment_method_id: Optional[str] = Field(default=None, description="ID da forma de pagamento associada")
    is_active: bool = Field(default=True, description="Indica se a assinatura está ativa")


# 2. Create (Contrato do POST)
class RecurringBillCreate(RecurringBillBase):
    pass


# 3. Update (Contrato do PATCH - tudo opcional)
class RecurringBillUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    amount: Optional[Decimal] = Field(default=None, gt=0)
    due_day: Optional[int] = Field(default=None, ge=1, le=31)
    category_id: Optional[str] = None
    payment_method_id: Optional[str] = None
    is_active: Optional[bool] = None


# 4. Response (O que a API devolve ao cliente)
class RecurringBillResponse(RecurringBillBase):
    id: str
    created_at: datetime
    updated_at: datetime

    # Objetos aninhados populados automaticamente pelo lazy="joined" do SQLAlchemy!
    category: Optional[CategoryResponse] = None
    payment_method: Optional[PaymentMethodResponse] = None

    model_config = ConfigDict(from_attributes=True)