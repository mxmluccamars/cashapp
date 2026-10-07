from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
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
    response_model=List[TransactionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Criar transação (à vista ou parcelada)"
)
def create_transaction(
    schema: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Cadastra uma transação financeira.
    - Se `installments == 1` (ou não informado): cria um lançamento à vista.
    - Se `installments > 1`: divide o valor nas faturas mensais subsequentes e retorna todas as parcelas geradas.
    """
    return transaction_service.create(db, schema=schema)


@router.get(
    "/",
    response_model=List[TransactionResponse],
    summary="Listar transações"
)
def list_transactions(
    skip: int = Query(0, ge=0, description="Registros para pular (paginação)"),
    limit: int = Query(100, ge=1, le=500, description="Limite máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Lista o extrato de transações cadastradas no sistema.
    """
    return transaction_service.list_all(db, skip=skip, limit=limit)


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Buscar transação por ID"
)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Obtém os detalhes completos de uma transação específica, incluindo as entidades aninhadas.
    """
    return transaction_service.get_by_id(db, transaction_id=transaction_id)


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Atualizar transação parcialmente"
)
def update_transaction(
    transaction_id: str,
    schema: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza apenas os campos enviados no corpo da requisição (ex.: alterar categoria ou valor).
    """
    return transaction_service.update(db, transaction_id=transaction_id, schema=schema)


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover transação"
)
def delete_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Exclui um lançamento do banco de dados pelo seu ID.
    """
    transaction_service.delete(db, transaction_id=transaction_id)
    return None