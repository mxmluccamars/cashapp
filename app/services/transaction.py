from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.transaction import Transaction
from app.repositories.transaction import transaction_repository
from app.repositories.category import category_repository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    def __init__(self):
        # O serviço precisa conversar com ambos os repositórios
        self.repository = transaction_repository
        self.category_repo = category_repository

    def create(self, db: Session, tx_in: TransactionCreate) -> Transaction:
        # Regra 1: A categoria informada precisa existir no banco de dados
        category = self.category_repo.get_by_id(db, id=tx_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A categoria informada não existe."
            )

        # Regra 2: Apenas aceita categorias ativas
        if hasattr(category, "is_active") and not category.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é permitido vincular lançamentos a uma categoria inativa."
            )

        # Transforma os dados validados do Pydantic em dicionário e grava no banco
        return self.repository.create(db, tx_in.model_dump())

    def get_by_id(self, db: Session, tx_id: str) -> Transaction:
        # Busca a transação e valida se ela realmente existe
        tx = self.repository.get_by_id(db, id=tx_id)
        if not tx:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transação não encontrada."
            )
        return tx

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Transaction]:
        # Lista as transações com paginação
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, tx_id: str, tx_in: TransactionUpdate) -> Transaction:
        # 1. Garante que a transação a ser alterada existe
        tx = self.get_by_id(db, tx_id)

        # 2. Se o usuário enviou uma nova categoria, valida se ela existe e está ativa
        if tx_in.category_id is not None:
            category = self.category_repo.get_by_id(db, id=tx_in.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="A nova categoria informada não existe."
                )
            if hasattr(category, "is_active") and not category.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Não é possível transferir a transação para uma categoria inativa."
                )

        # Atualiza apenas os campos enviados no payload (ignora os None)
        update_data = tx_in.model_dump(exclude_unset=True)
        return self.repository.update(db, tx, update_data)

    def delete(self, db: Session, tx_id: str) -> Transaction:
        # Garante que a transação existe antes de mandar remover
        tx = self.get_by_id(db, tx_id)
        return self.repository.remove(db, tx)


# Instância única para ser consumida pelos endpoints
transaction_service = TransactionService()