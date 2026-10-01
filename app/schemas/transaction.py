from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryResponse


class TransactionBase(BaseModel):
    description: str = Field(..., min_length=2, max_length=100)
    amount: Decimal = Field(..., gt=0)
    date: date
    type: str = Field(..., pattern="^(EXPENSE|INCOME)$")
    notes: Optional[str] = None
    category_id: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    date: Optional[date] = None
    type: Optional[str] = Field(default=None, pattern="^(EXPENSE|INCOME)$")
    notes: Optional[str] = None
    category_id: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)


# Força o Pydantic a resolver todas as referências cruzadas sem conflitos
TransactionResponse.model_rebuild()