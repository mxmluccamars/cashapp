from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
)
from app.services.transaction import transaction_service

router = APIRouter()


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar transação",
    description="Registra uma nova receita ou despesa associada a uma categoria existente."
)
def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db)
):
    # Repassa diretamente os dados validados para o Service
    return transaction_service.create(db, tx_in)


@router.get(
    "/",
    response_model=List[TransactionResponse],
    summary="Listar transações",
    description="Retorna todas as transações cadastradas com paginação."
)
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return transaction_service.list_all(db, skip=skip, limit=limit)


@router.get(
    "/{tx_id}",
    response_model=TransactionResponse,
    summary="Buscar transação por ID",
    description="Obtém os detalhes completos de uma transação específica pelo seu identificador."
)
def get_transaction(
    tx_id: str,
    db: Session = Depends(get_db)
):
    return transaction_service.get_by_id(db, tx_id)


@router.patch(
    "/{tx_id}",
    response_model=TransactionResponse,
    summary="Atualizar transação",
    description="Atualiza parcialmente os dados de uma transação existente."
)
def update_transaction(
    tx_id: str,
    tx_in: TransactionUpdate,
    db: Session = Depends(get_db)
):
    return transaction_service.update(db, tx_id, tx_in)


@router.delete(
    "/{tx_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir transação",
    description="Remove definitivamente uma transação do banco de dados."
)
def delete_transaction(
    tx_id: str,
    db: Session = Depends(get_db)
):
    transaction_service.delete(db, tx_id)
    # No status 204 (No Content), não se retorna corpo na resposta
    return None