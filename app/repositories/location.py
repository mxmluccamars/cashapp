from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.location import Location
from app.repositories.base import BaseRepository


class LocationRepository(BaseRepository[Location]):
    def __init__(self):
        super().__init__(Location)

    def get_by_name(self, db: Session, name: str) -> Optional[Location]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_city(self, db: Session, city: str) -> List[Location]:
        return db.query(self.model).filter(self.model.city == city).all()

    def get_by_state(self, db: Session, state: str) -> List[Location]:
        return db.query(self.model).filter(self.model.state == state).all()

location_repository = LocationRepository()