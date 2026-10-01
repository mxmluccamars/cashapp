from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.category import CategoryResponse

# campos comrtilhados
class TransactionBase(BaseModel):
    description: str = Field(..., min_length=2, max_length=100, description="Descrição da transação")
    amount: Decimal = Field(..., gt=0, description="Valor da transação")
    date: date = Field(..., description="Data da transação")
    type: str = Field(..., pattern="^(EXPENSE|INCOME)$", description="EXPENSE ou INCOME")
    notes: Optional[str] = Field(None, description="Observações adicionais opcionais")
    category_id: str = Field(..., description="ID da categoria vinculada")

# post herda tudo da base com os campos obrigatórios
class TransactionCreate(TransactionBase):
    pass

# patch herda direto da base model com tudo opcional
class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=2, max_length=100)
    amount: Optional[Decimal] = Field(None, gt=0)
    date: Optional[date] = None
    type: Optional[str] = Field(None, pattern="^(EXPENSE|INCOME)$")
    notes: Optional[str] = None
    category_id: Optional[str] = None

# formato de resposta (GET, POST, PATCH)
class TransactionResponse(TransactionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None

    # permite ler instâncias do SQLAlchemy diretamente
    model_config = ConfigDict(from_attributes=True)
