from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class GoalBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do objetivo")
    description: str = Field(..., min_length=2, max_length=100, description="Descrição do objetivo")
    target_amount: Decimal = Field(..., gt=0, description="Valor alvo do objetivo")
    target_date: datetime = Field(..., description="Data alvo do objetivo")
    icon: Optional[str] = Field("tag", max_length=30)
    color: Optional[str] = Field("#FFEE00", pattern="^#([A-Fa-f0-9]{6})$")


class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=2, max_length=100)
    target_amount: Optional[Decimal] = Field(None, gt=0)
    target_date: Optional[datetime] = Field(None, description="Data alvo do objetivo")
    icon: Optional[str] = Field(None, max_length=30)
    color: Optional[str] = Field(None, pattern="^#([A-Fa-f0-9]{6})$")


class GoalResponse(GoalBase):
    id: str
    name: str
    description: str
    target_amount: float
    target_date: datetime
    icon: str
    color: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

