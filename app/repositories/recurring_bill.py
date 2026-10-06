from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.recurring_bill import RecurringBill


class RecurringBillRepository(BaseRepository[RecurringBill]):
    def get_by_name(self, db: Session, name: str) -> Optional[RecurringBill]:
        """Busca uma conta recorrente pelo nome exato."""
        return db.query(self.model).filter(self.model.name == name).first()

    def get_active_bills(self, db: Session, skip: int = 0, limit: int = 100) -> List[RecurringBill]:
        """Retorna apenas as assinaturas que estão ativas no momento."""
        return (
            db.query(self.model)
            .filter(self.model.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )


# Instância única exportada para uso no Service
recurring_bill_repository = RecurringBillRepository(RecurringBill)