from typing import Optional
from sqlalchemy.orm import Session
from app.models.context import Context
from app.repositories.base import BaseRepository


class ContextRepository(BaseRepository[Context]):
    def __init__(self):
        super().__init__(Context)

    def get_by_name(self, db: Session, name: str) -> Optional[Context]:
        return db.query(self.model).filter(self.model.name == name).first()


context_repository = ContextRepository()