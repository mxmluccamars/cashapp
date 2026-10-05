from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.location import Location
from app.repositories.location import location_repository
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse

class LocationService:
    def __init__(self):
        self.repository = location_repository

    def create(self, db: Session, location_in: LocationCreate) -> Location:
        # Regra: Não permitir locais com o mesmo nome
        existing = self.repository.get_by_name(db, name=location_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um local com o nome '{location_in.name}'."
            )
        return self.repository.create(db, location_in.model_dump())

    def get_by_id(self, db: Session, location_id: str) -> Location:
        location = self.repository.get_by_id(db, id=location_id)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Local não encontrado."
            )
        return location

    def get_by_city(self, db: Session, city: str) -> List[Location]:
        return self.repository.get_by_city(db, city=city)

    def get_by_state(self, db: Session, state: str) -> List[Location]:
        return self.repository.get_by_state(db, state=state)

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Location]:
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, location_id: str, location_in: LocationUpdate) -> Location:
        location = self.get_by_id(db, location_id)

        # Se estiver alterando o nome, checa se já existe outra com esse novo nome
        if location_in.name and location_in.name != location.name:
            existing = self.repository.get_by_name(db, name=location_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um local com o nome '{location_in.name}'."
                )

        update_data = location_in.model_dump(exclude_unset=True)
        return self.repository.update(db, location, update_data)

    def delete(self, db: Session, location_id: str) -> Location:
        location = self.get_by_id(db, location_id)
        # Futuramente: checaremos se existem transações vinculadas a esta categoria antes de deletar!
        return self.repository.remove(db, location)

location_service = LocationService()