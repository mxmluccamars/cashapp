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


# Instância única para ser importada e utilizada pelo Service
transaction_repository = TransactionRepository()