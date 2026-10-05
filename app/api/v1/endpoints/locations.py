from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.services.location import location_service

router = APIRouter()

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(location_in: LocationCreate, db: Session = Depends(get_db)):
    """Cria um novo local (Ex: Rio de Janeiro, São Paulo, Belo Horizonte)."""
    return location_service.create(db, location_in)

@router.get("/", response_model=List[LocationResponse])
def list_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os locais (Ex: Rio de Janeiro, São Paulo, Belo Horizonte)."""
    return location_service.list_all(db, skip=skip, limit=limit)

@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: str, db: Session = Depends(get_db)):
    """Retorna os detalhes de um local por ID."""
    return location_service.get_by_id(db, location_id)

@router.get("/city/{city}", response_model=List[LocationResponse])
def get_location_by_city(city: str, db: Session = Depends(get_db)):
    """Retorna os locais de uma cidade."""
    return location_service.get_by_city(db, city)

@router.get("/state/{state}", response_model=List[LocationResponse])
def get_location_by_state(state: str, db: Session = Depends(get_db)):
    """Retorna os locais de um estado."""
    return location_service.get_by_state(db, state)

@router.patch("/{location_id}", response_model=LocationResponse)
def update_location(location_id: str, location_in: LocationUpdate, db: Session = Depends(get_db)):
    """Atualiza dados parciais de um local."""
    return location_service.update(db, location_id, location_in)

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: str, db: Session = Depends(get_db)):
    """Remove um local."""
    location_service.delete(db, location_id)