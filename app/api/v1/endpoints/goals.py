from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse        
from app.services.goal import goal_service

router = APIRouter()

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal_in: GoalCreate, db: Session = Depends(get_db)):
    """Cria um novo objetivo (Despesa ou Receita)."""
    return goal_service.create(db, goal_in)

@router.get("/", response_model=List[GoalResponse])
def list_goals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os objetivos (Despesa ou Receita)."""
    return goal_service.list_all(db, skip=skip, limit=limit)

@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: str, db: Session = Depends(get_db)):
    """Retorna os detalhes de um objetivo por ID."""
    return goal_service.get_by_id(db, goal_id)

@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: str, goal_in: GoalUpdate, db: Session = Depends(get_db)):
    """Atualiza dados parciais de um objetivo."""
    return goal_service.update(db, goal_id, goal_in)

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: str, db: Session = Depends(get_db)):
    """Remove um objetivo."""
    goal_service.delete(db, goal_id)
    return None