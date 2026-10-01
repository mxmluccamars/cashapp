from fastapi import APIRouter
from app.api.v1.endpoints import categories, transactions

api_router = APIRouter()
api_router.include_router(categories.router, prefix="/categories", tags=["Categorias"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transações"])