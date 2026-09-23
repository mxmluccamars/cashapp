from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category import category_service

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria (Despesa ou Receita)."""
    return category_service.create(db, category_in)


@router.get("/", response_model=List[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista as categorias cadastradas com suporte a paginação."""
    return category_service.list_all(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, db: Session = Depends(get_db)):
    """Busca os detalhes de uma categoria por ID."""
    return category_service.get_by_id(db, category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    """Atualiza dados parciais de uma categoria."""
    return category_service.update(db, category_id, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """Remove uma categoria."""
    category_service.delete(db, category_id)
    return None