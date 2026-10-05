from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class LocationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Nome do local")
    city: str = Field(..., min_length=2, max_length=50, description="Cidade do local")
    state: str = Field(..., min_length=2, max_length=2, description="Estado do local")

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    city: Optional[str] = Field(None, min_length=2, max_length=50)
    state: Optional[str] = Field(None, min_length=2, max_length=2)

class LocationResponse(LocationBase):
    id: str
    name: str
    city: str
    state: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)