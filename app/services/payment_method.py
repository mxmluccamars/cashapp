from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.payment_method import PaymentMethod
from app.repositories.payment_method import payment_method_repository
from app.schemas.payment_method import PaymentMethodCreate, PaymentMethodUpdate, PaymentMethodResponse

class PaymentMethodService:
    def __init__(self):
        self.repository = payment_method_repository

    def create(self, db: Session, payment_method_in: PaymentMethodCreate) -> PaymentMethod:
        # Regra: Não permitir locais com o mesmo nome
        existing = self.repository.get_by_name(db, name=payment_method_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um método de pagamento com o nome '{payment_method_in.name}'."
            )
        return self.repository.create(db, payment_method_in.model_dump())

    def get_by_id(self, db: Session, payment_method_id: str) -> PaymentMethod:
        payment_method = self.repository.get_by_id(db, id=payment_method_id)
        if not payment_method:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Método de pagamento não encontrado."
            )
        return payment_method

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[PaymentMethod]:
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, payment_method_id: str, payment_method_in: PaymentMethodUpdate) -> PaymentMethod:
        payment_method = self.get_by_id(db, payment_method_id)

        # Se estiver alterando o nome, checa se já existe outra com esse novo nome
        if payment_method_in.name and payment_method_in.name != payment_method.name:
            existing = self.repository.get_by_name(db, name=payment_method_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um método de pagamento com o nome '{payment_method_in.name}'."
                )

        update_data = payment_method_in.model_dump(exclude_unset=True)
        return self.repository.update(db, payment_method, update_data)

    def delete(self, db: Session, payment_method_id: str) -> PaymentMethod:
        payment_method = self.get_by_id(db, payment_method_id)
        # Futuramente: checaremos se existem transações vinculadas a esta categoria antes de deletar!
        return self.repository.remove(db, payment_method)

payment_method_service = PaymentMethodService()