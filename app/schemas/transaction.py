from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse
from app.schemas.context import ContextResponse
from app.schemas.goal import GoalResponse
from app.schemas.location import LocationResponse
from app.schemas.payment_method import PaymentMethodResponse
from app.schemas.recurring_bill import RecurringBillResponse


class TransactionBase(BaseModel):
    description: str = Field(..., min_length=2, max_length=100)
    amount: Decimal = Field(..., gt=0)
    date: date
    type: str = Field(..., pattern="^(EXPENSE|INCOME)$")
    notes: Optional[str] = None
    category_id: str
    context_id: Optional[str] = None
    payment_method_id: str
    location_id: Optional[str] = None
    goal_id: Optional[str] = None
    recurring_bill_id: Optional[str] = None
    # installment_current: Optional[int] = None
    # installment_total: Optional[int] = None
    # installment_group_id: Optional[str] = None
    


class TransactionCreate(TransactionBase):
    installments: Optional[int] = Field(
        default=1, 
        ge=1, 
        le=72, 
        description="Quantidade de parcelas da compra. Se 1, é à vista."
    )


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    date: Optional[date] = None
    type: Optional[str] = Field(default=None, pattern="^(EXPENSE|INCOME)$")
    notes: Optional[str] = None
    category_id: Optional[str] = None
    context_id: Optional[str] = None
    payment_method_id: Optional[str] = None
    location_id: Optional[str] = None
    goal_id: Optional[str] = None
    recurring_bill_id: Optional[str] = None
    installment_current: Optional[int] = None
    installment_total: Optional[int] = None
    installment_group_id: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    context: Optional[ContextResponse] = None
    payment_method: Optional[PaymentMethodResponse] = None
    location: Optional[LocationResponse] = None
    goal: Optional[GoalResponse] = None
    recurring_bill: Optional[RecurringBillResponse] = None

    installment_current: Optional[int] = None
    installment_total: Optional[int] = None
    installment_group_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Força o Pydantic a resolver todas as referências cruzadas sem conflitos
TransactionResponse.model_rebuild()