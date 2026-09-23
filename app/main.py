from fastapi import FastAPI
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

# Inclui as rotas versionadas sob o prefixo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}