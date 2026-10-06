from typing import Optional
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self):
        super().__init__(Goal)

    def get_by_name(self, db: Session, name: str) -> Optional[Goal]:
        return db.query(self.model).filter(self.model.name == name).first()

goal_repository = GoalRepository()