from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.config import settings

# Ajuste específico apenas caso estejamos usando SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=True  # Se quiser ver todas as queries SQL no terminal para aprender, descomente aqui!
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Injetor de dependência do FastAPI.
    Abre uma sessão com o banco e garante que ela seja fechada ao final da requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()