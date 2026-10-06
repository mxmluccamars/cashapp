import os
from contextlib import asynccontextmanager  # <--- Essa linha é obrigatória
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.api.v1.router import api_router
from app.database.seed import run_seed
from app.models.category import Category

# Garante que todos os models sejam conhecidos pelo Base
import app.models  # noqa: F401

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Cria todas as tabelas físicas no SQLite
    Base.metadata.create_all(bind=engine)

    # 2. Verifica se o banco já possui registros
    db = SessionLocal()
    try:
        has_categories = db.query(Category).first() is not None
        if not has_categories:
            print("📦 Banco de dados novo/vazio detectado. Executando seed inicial...")
            run_seed()
        else:
            print("✅ Banco de dados já inicializado.")
    finally:
        db.close()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configuração de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}