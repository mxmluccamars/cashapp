import uuid
from typing import List, Optional
from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.repositories.transaction import TransactionRepository, transaction_repository

# Repositórios das entidades de apoio para validação de integridade referencial
from app.repositories.category import category_repository
from app.repositories.payment_method import payment_method_repository
from app.repositories.context import context_repository
from app.repositories.location import location_repository
from app.repositories.goal import goal_repository
from app.repositories.recurring_bill import recurring_bill_repository


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def _validate_relations(
        self,
        db: Session,
        category_id: Optional[str] = None,
        payment_method_id: Optional[str] = None,
        context_id: Optional[str] = None,
        location_id: Optional[str] = None,
        goal_id: Optional[str] = None,
        recurring_bill_id: Optional[str] = None,
    ) -> None:
        """Verifica a existência física de cada chave estrangeira referenciada."""
        if category_id and not category_repository.get_by_id(db, id=category_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID '{category_id}' não encontrada."
            )

        if payment_method_id and not payment_method_repository.get_by_id(db, id=payment_method_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Forma de pagamento com ID '{payment_method_id}' não encontrada."
            )

        if context_id and not context_repository.get_by_id(db, id=context_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contexto com ID '{context_id}' não encontrado."
            )

        if location_id and not location_repository.get_by_id(db, id=location_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Local com ID '{location_id}' não encontrado."
            )

        if goal_id and not goal_repository.get_by_id(db, id=goal_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Caixinha/Meta com ID '{goal_id}' não encontrada."
            )

        if recurring_bill_id and not recurring_bill_repository.get_by_id(db, id=recurring_bill_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assinatura com ID '{recurring_bill_id}' não encontrada."
            )

    def create(self, db: Session, schema: TransactionCreate) -> List[Transaction]:
        """
        Cria uma transação à vista ou divide em lote caso `installments > 1`.
        Retorna uma lista contendo a(s) transação(ões) criada(s).
        """
        # 1. Validação de integridade referencial
        self._validate_relations(
            db,
            category_id=schema.category_id,
            payment_method_id=schema.payment_method_id,
            context_id=schema.context_id,
            location_id=schema.location_id,
            goal_id=schema.goal_id,
            recurring_bill_id=schema.recurring_bill_id,
        )

        num_installments = schema.installments or 1

        # 2. Caso de compra parcelada
        if num_installments > 1:
            if not schema.payment_method_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="É obrigatório informar uma forma de pagamento para compras parceladas."
                )

            payment_method = payment_method_repository.get_by_id(db, id=schema.payment_method_id)
            if not payment_method.allow_installments:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A forma de pagamento '{payment_method.name}' não aceita parcelamento."
                )

            group_id = str(uuid.uuid4())
            installment_amount = (schema.amount / Decimal(num_installments)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            transactions_data = []
            base_data = schema.model_dump(exclude={"installments"})

            for i in range(1, num_installments + 1):
                tx_data = base_data.copy()
                tx_data.update({
                    "id": str(uuid.uuid4()),
                    "amount": installment_amount,
                    "date": schema.date + relativedelta(months=i - 1),
                    "installment_current": i,
                    "installment_total": num_installments,
                    "installment_group_id": group_id,
                })
                transactions_data.append(tx_data)

            return self.repository.create_many(db, objs_in_data=transactions_data)

        # 3. Caso de compra à vista (1x)
        single_data = schema.model_dump(exclude={"installments"})
        single_data["id"] = str(uuid.uuid4())
        created_obj = self.repository.create(db, obj_in=single_data)
        return [created_obj]

    def get_by_id(self, db: Session, transaction_id: str) -> Transaction:
        transaction = self.repository.get(db, id=transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transação com ID '{transaction_id}' não encontrada."
            )
        return transaction

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def update(self, db: Session, transaction_id: str, schema: TransactionUpdate) -> Transaction:
        transaction = self.get_by_id(db, transaction_id)
        update_data = schema.model_dump(exclude_unset=True)

        # Valida relacionamentos se enviados na atualização
        self._validate_relations(
            db,
            category_id=update_data.get("category_id"),
            payment_method_id=update_data.get("payment_method_id"),
            context_id=update_data.get("context_id"),
            location_id=update_data.get("location_id"),
            goal_id=update_data.get("goal_id"),
            recurring_bill_id=update_data.get("recurring_bill_id"),
        )

        return self.repository.update(db, db_obj=transaction, obj_in=update_data)

    def delete(self, db: Session, transaction_id: str) -> None:
        self.get_by_id(db, transaction_id)
        self.repository.remove(db, id=transaction_id)


transaction_service = TransactionService(transaction_repository)