from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.api.v1.router import api_router

# Garante que as tabelas sejam criadas no SQLite local (ao adicionar novos models)
import app.models  # noqa: F401
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- CONFIGURAÇÃO DE CORS ---
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

# Inclui as rotas versionadas sob o prefixo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}