from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse
from app.services.payment_method import payment_method_service

router = APIRouter()

@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(payment_method_in: PaymentMethodCreate, db: Session = Depends(get_db)):
    """Cria um novo método de pagamento (Ex: Cartão de Crédito, Boleto, etc)."""
    return payment_method_service.create(db, payment_method_in)

@router.get("/", response_model=List[PaymentMethodResponse])
def list_payment_methods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os métodos de pagamento (Ex: Cartão de Crédito, Boleto, etc)."""
    return payment_method_service.list_all(db, skip=skip, limit=limit)

@router.get("/{payment_method_id}", response_model=PaymentMethodResponse)
def get_payment_method(payment_method_id: str, db: Session = Depends(get_db)):
    """Retorna os detalhes de um método de pagamento por ID."""
    return payment_method_service.get_by_id(db, payment_method_id)

@router.patch("/{payment_method_id}", response_model=PaymentMethodResponse)
def update_payment_method(payment_method_id: str, payment_method_in: PaymentMethodUpdate, db: Session = Depends(get_db)):
    """Atualiza dados parciais de um método de pagamento."""
    return payment_method_service.update(db, payment_method_id, payment_method_in)

@router.delete("/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_method(payment_method_id: str, db: Session = Depends(get_db)):
    """Remove um método de pagamento."""
    payment_method_service.delete(db, payment_method_id)
    return None