from fastapi import APIRouter
from app.api.v1.endpoints import categories, transactions, contexts, locations, goals, payment_methods

api_router = APIRouter()
api_router.include_router(categories.router, prefix="/categories", tags=["Categorias"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transações"])
api_router.include_router(contexts.router, prefix="/contexts", tags=["Contextos"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locais"])
api_router.include_router(goals.router, prefix="/goals", tags=["Objetivos"])
api_router.include_router(payment_methods.router, prefix="/payment_methods", tags=["Métodos de Pagamento"])