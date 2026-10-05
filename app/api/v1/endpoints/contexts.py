from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.context import ContextCreate, ContextUpdate, ContextResponse
from app.services.context import context_service

router = APIRouter()

@router.post("/", response_model=ContextResponse, status_code=status.HTTP_201_CREATED)
def create_context(context_in: ContextCreate, db: Session = Depends(get_db)):
    """Cria um novo contexto (Ex: Trabalho, Lazer, Família)."""
    return context_service.create(db, context_in)

@router.get("/", response_model=List[ContextResponse])
def list_contexts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os contextos (Ex: Trabalho, Lazer, Família)."""
    return context_service.list_all(db, skip=skip, limit=limit)

@router.get("/{context_id}", response_model=ContextResponse)
def get_context(context_id: str, db: Session = Depends(get_db)):
    """Retorna os detalhes de um contexto por ID."""
    return context_service.get_by_id(db, context_id)

@router.patch("/{context_id}", response_model=ContextResponse)
def update_context(context_id: str, context_in: ContextUpdate, db: Session = Depends(get_db)):
    """Atualiza dados parciais de um contexto."""
    return context_service.update(db, context_id, context_in)

@router.delete("/{context_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_context(context_id: str, db: Session = Depends(get_db)):
    """Remove um contexto."""
    context_service.delete(db, context_id)
    return None

