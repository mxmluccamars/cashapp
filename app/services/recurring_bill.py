from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.recurring_bill import RecurringBill
from app.schemas.recurring_bill import RecurringBillCreate, RecurringBillUpdate
from app.repositories.recurring_bill import RecurringBillRepository, recurring_bill_repository
from app.repositories.category import category_repository
from app.repositories.payment_method import payment_method_repository


class RecurringBillService:
    def __init__(self, repository: RecurringBillRepository):
        self.repository = repository

    def _validate_foreign_keys(
        self, 
        db: Session, 
        category_id: Optional[str] = None, 
        payment_method_id: Optional[str] = None
    ) -> None:
        """Garante que categoria e forma de pagamento existam no banco caso informadas."""
        if category_id:
            category = category_repository.get_by_id(db, id=category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoria com ID '{category_id}' não encontrada."
                )

        if payment_method_id:
            payment_method = payment_method_repository.get_by_id(db, id=payment_method_id)
            if not payment_method:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Forma de pagamento com ID '{payment_method_id}' não encontrada."
                )

    def create(self, db: Session, schema: RecurringBillCreate) -> RecurringBill:
        # 1. Verifica duplicidade de nome
        existing = self.repository.get_by_name(db, name=schema.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe uma conta recorrente cadastrada com o nome '{schema.name}'."
            )

        # 2. Valida se as FKs passadas existem
        self._validate_foreign_keys(
            db, 
            category_id=schema.category_id, 
            payment_method_id=schema.payment_method_id
        )

        # 3. Criação pelo repositório
        return self.repository.create(db, obj_in_data=schema.model_dump())

    def get_by_id(self, db: Session, bill_id: str) -> RecurringBill:
        bill = self.repository.get_by_id(db, id=bill_id)
        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conta recorrente com ID '{bill_id}' não encontrada."
            )
        return bill

    def list_all(
        self, 
        db: Session, 
        active_only: bool = False, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[RecurringBill]:
        if active_only:
            return self.repository.get_active_bills(db, skip=skip, limit=limit)
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, bill_id: str, schema: RecurringBillUpdate) -> RecurringBill:
        bill = self.get_by_id(db, bill_id)

        # Se enviou alteração de nome, checa se não colide com outra conta existente
        if schema.name and schema.name != bill.name:
            existing = self.repository.get_by_name(db, name=schema.name)
            if existing and existing.id != bill.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe outra conta cadastrada com o nome '{schema.name}'."
                )

        # Valida chaves estrangeiras se foram enviadas no payload
        update_data = schema.model_dump(exclude_unset=True)
        self._validate_foreign_keys(
            db,
            category_id=update_data.get("category_id"),
            payment_method_id=update_data.get("payment_method_id")
        )

        update_data = schema.model_dump(exclude_unset=True)
        return self.repository.update(db, bill, update_data)

    def delete(self, db: Session, bill_id: str) -> None:
        recurring_bill = self.get_by_id(db, bill_id)
        self.repository.remove(db, recurring_bill)


# Instância única exportada
recurring_bill_service = RecurringBillService(recurring_bill_repository)