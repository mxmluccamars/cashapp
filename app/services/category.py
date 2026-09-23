from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.category import Category
from app.repositories.category import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self):
        self.repository = category_repository

    def create(self, db: Session, category_in: CategoryCreate) -> Category:
        # Regra: Não permitir categorias com o mesmo nome
        existing = self.repository.get_by_name(db, name=category_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe uma categoria com o nome '{category_in.name}'."
            )
        return self.repository.create(db, category_in.model_dump())

    def get_by_id(self, db: Session, category_id: str) -> Category:
        category = self.repository.get_by_id(db, id=category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada."
            )
        return category

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, category_id: str, category_in: CategoryUpdate) -> Category:
        category = self.get_by_id(db, category_id)

        # Se estiver alterando o nome, checa se já existe outra com esse novo nome
        if category_in.name and category_in.name != category.name:
            existing = self.repository.get_by_name(db, name=category_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe uma categoria com o nome '{category_in.name}'."
                )

        update_data = category_in.model_dump(exclude_unset=True)
        return self.repository.update(db, category, update_data)

    def delete(self, db: Session, category_id: str) -> Category:
        category = self.get_by_id(db, category_id)
        # Futuramente: checaremos se existem transações vinculadas a esta categoria antes de deletar!
        return self.repository.remove(db, category)


category_service = CategoryService()