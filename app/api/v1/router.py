from fastapi import APIRouter
from app.api.v1.endpoints import categories, transactions, contexts, locations

api_router = APIRouter()
api_router.include_router(categories.router, prefix="/categories", tags=["Categorias"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transações"])
api_router.include_router(contexts.router, prefix="/contexts", tags=["Contextos"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locais"])