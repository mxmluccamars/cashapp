from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.context import Context
from app.repositories.context import context_repository
from app.schemas.context import ContextCreate, ContextUpdate, ContextResponse

class ContextService:
    def __init__(self):
        self.repository = context_repository

    def create(self, db: Session, context_in: ContextCreate) -> Context:
        # ver se existe um objeto com o mesmo nome
        existing = self.repository.get_by_name(db, name=context_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Contexto já existente"
            )
        return self.repository.create(db, context_in.model_dump())

    def get_by_id(self, db: Session, context_id: str) -> Context:
        context = self.repository.get_by_id(db, context_id)
        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Contexto não encontrado"
            )
        return context

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Context]:
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, context_id: str, context_in: ContextUpdate) -> Context:
        context = self.get_by_id(db, context_id)
        if context_in.name and context_in.name != context.name:
            existing = self.repository.get_by_name(db, name=context_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Contexto já existente"
                )
        update_data = context_in.model_dump(exclude_unset=True)
        return self.repository.update(db, context, update_data)

    def delete(self, db: Session, context_id: str) -> Context:
        context = self.get_by_id(db, context_id)
        return self.repository.remove(db, context)

context_service = ContextService()
