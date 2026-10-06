from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.recurring_bill import (
    RecurringBillCreate,
    RecurringBillUpdate,
    RecurringBillResponse,
)
from app.services.recurring_bill import recurring_bill_service

router = APIRouter()


@router.post(
    "/",
    response_model=RecurringBillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma conta recorrente ou assinatura"
)
def create_recurring_bill(
    schema: RecurringBillCreate,
    db: Session = Depends(get_db)
):
    return recurring_bill_service.create(db, schema=schema)


@router.get(
    "/",
    response_model=List[RecurringBillResponse],
    summary="Listar contas recorrentes"
)
def list_recurring_bills(
    active_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista as contas recorrentes cadastradas.
    - Se `active_only=true`, devolve apenas as assinaturas em vigor (não canceladas).
    """
    return recurring_bill_service.list_all(
        db, 
        active_only=active_only, 
        skip=skip, 
        limit=limit
    )


@router.get(
    "/{bill_id}",
    response_model=RecurringBillResponse,
    summary="Buscar conta recorrente por ID"
)
def get_recurring_bill(
    bill_id: str,
    db: Session = Depends(get_db)
):
    return recurring_bill_service.get_by_id(db, bill_id=bill_id)


@router.patch(
    "/{bill_id}",
    response_model=RecurringBillResponse,
    summary="Atualizar conta recorrente parcialmente"
)
def update_recurring_bill(
    bill_id: str,
    schema: RecurringBillUpdate,
    db: Session = Depends(get_db)
):
    return recurring_bill_service.update(db, bill_id=bill_id, schema=schema)


@router.delete(
    "/{bill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover conta recorrente"
)
def delete_recurring_bill(
    bill_id: str,
    db: Session = Depends(get_db)
):
    recurring_bill_service.delete(db, bill_id=bill_id)
    return None