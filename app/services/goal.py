from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.goal import Goal
from app.repositories.goal import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

class GoalService:
    def __init__(self):
        self.repository = GoalRepository()

    def create(self, db: Session, goal_in: GoalCreate) -> Goal:
        # Regra: Não permitir locais com o mesmo nome
        existing = self.repository.get_by_name(db, name=goal_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um objetivo com o nome '{goal_in.name}'."
            )
        return self.repository.create(db, goal_in.model_dump())

    def get_by_id(self, db: Session, goal_id: str) -> Goal:
        goal = self.repository.get_by_id(db, id=goal_id)
        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objetivo não encontrado."
            )
        return goal

    def list_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Goal]:
        return self.repository.get_all(db, skip=skip, limit=limit)

    def update(self, db: Session, goal_id: str, goal_in: GoalUpdate) -> Goal:
        goal = self.get_by_id(db, goal_id)

        # Se estiver alterando o nome, checa se já existe outra com esse novo nome
        if goal_in.name and goal_in.name != goal.name:
            existing = self.repository.get_by_name(db, name=goal_in.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um objetivo com o nome '{goal_in.name}'."
                )

        update_data = goal_in.model_dump(exclude_unset=True)
        return self.repository.update(db, goal, update_data)

    def delete(self, db: Session, goal_id: str) -> Goal:
        goal = self.get_by_id(db, goal_id)
        # Futuramente: checaremos se existem transações vinculadas a esta categoria antes de deletar!
        return self.repository.remove(db, goal)

goal_service = GoalService()