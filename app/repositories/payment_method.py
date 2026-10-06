from typing import Optional
from sqlalchemy.orm import Session
from app.models.payment_method import PaymentMethod
from app.repositories.base import BaseRepository


class PaymentMethodRepository(BaseRepository[PaymentMethod]):
    def __init__(self):
        super().__init__(PaymentMethod)

    def get_by_name(self, db: Session, name: str) -> Optional[PaymentMethod]:
        return db.query(self.model).filter(self.model.name == name).first()


payment_method_repository = PaymentMethodRepository()