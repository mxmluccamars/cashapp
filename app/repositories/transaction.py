from typing import List
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        # Passa a classe Transaction para o BaseRepository saber qual tabela manipular
        super().__init__(Transaction)

    def get_by_category(self, db: Session, category_id: str) -> List[Transaction]:
        """
        Exemplo de consulta personalizada:
        Retorna todas as movimentações associadas a uma categoria específica.
        SQL gerado por baixo dos panos:
        SELECT * FROM transactions WHERE category_id = :category_id;
        """
        return db.query(self.model).filter(self.model.category_id == category_id).all()

    def get_by_installment_group(self, db: Session, group_id: str) -> List[Transaction]:
        """Busca todas as parcelas pertencentes a um mesmo grupo de parcelamento."""
        return (
            db.query(self.model)
            .filter(self.model.installment_group_id == group_id)
            .order_by(self.model.installment_current.asc())
            .all()
        )

    def create_many(self, db: Session, objs_in_data: List[dict]) -> List[Transaction]:
        """Cria múltiplas transações de uma só vez (usado na geração de parcelas)."""
        db_objs = [self.model(**data) for data in objs_in_data]
        db.add_all(db_objs)
        db.commit()
        for obj in db_objs:
            db.refresh(obj)
        return db_objs


# Instância única para ser importada e utilizada pelo Service
transaction_repository = TransactionRepository()