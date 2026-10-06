import sys
from decimal import Decimal
from datetime import date
from sqlalchemy.orm import Session

from app.database.session import SessionLocal, engine
from app.database.base import Base

# Importa os models para garantir que o SQLAlchemy conheça todos
import app.models  # noqa: F401

# Importa repositórios e schemas
from app.repositories import (
    category_repository,
    payment_method_repository,
    context_repository,
    location_repository,
    goal_repository,
    recurring_bill_repository,
)
from app.schemas.category import CategoryCreate
from app.schemas.payment_method import PaymentMethodCreate
from app.schemas.context import ContextCreate
from app.schemas.location import LocationCreate
from app.schemas.goal import GoalCreate
from app.schemas.recurring_bill import RecurringBillCreate


def seed_payment_methods(db: Session):
    methods = [
        {"name": "Pix", "icon": "zap", "color": "#10B981", "allow_installments": False},
        {"name": "Dinheiro", "icon": "banknote", "color": "#F59E0B", "allow_installments": False},
        {"name": "Cartão de Crédito", "icon": "credit-card", "color": "#8A05BE", "allow_installments": True},
    ]
    created = {}
    for data in methods:
        existing = payment_method_repository.get_by_name(db, name=data["name"])
        if not existing:
            existing = payment_method_repository.create(db, obj_in_data=PaymentMethodCreate(**data))
        created[data["name"]] = existing
    return created


def seed_contexts(db: Session):
    contexts = ["Dia a dia", "Trabalho", "Igreja", "Férias", "Faculdade"]
    created = {}
    for name in contexts:
        existing = context_repository.get_by_name(db, name=name)
        if not existing:
            existing = context_repository.create(db, obj_in_data=ContextCreate(name=name))
        created[name] = existing
    return created


def seed_categories(db: Session):
    categories = [
        {"name": "Alimentação", "type": "EXPENSE", "icon": "utensils", "color": "#EF4444", "monthly_limit": Decimal("800.00")},
        {"name": "Transporte", "type": "EXPENSE", "icon": "car", "color": "#F59E0B", "monthly_limit": Decimal("400.00")},
        {"name": "Moradia", "type": "EXPENSE", "icon": "home", "color": "#3B82F6", "monthly_limit": Decimal("1200.00")},
        {"name": "Lazer", "type": "EXPENSE", "icon": "film", "color": "#EC4899", "monthly_limit": Decimal("300.00")},
        {"name": "Saúde", "type": "EXPENSE", "icon": "heart-pulse", "color": "#10B981", "monthly_limit": None},
        {"name": "Salário", "type": "INCOME", "icon": "wallet", "color": "#10B981", "monthly_limit": None},
        {"name": "Rendimentos / Freelance", "type": "INCOME", "icon": "trending-up", "color": "#6366F1", "monthly_limit": None},
    ]
    created = {}
    for data in categories:
        existing = category_repository.get_by_name(db, name=data["name"])
        if not existing:
            existing = category_repository.create(db, obj_in_data=CategoryCreate(**data))
        created[data["name"]] = existing
    return created


def seed_locations(db: Session):
    locations = [
        {"name": "Padaria Central", "city": "Jacareí", "state": "SP"},
        {"name": "Supermercado Shibata", "city": "Jacareí", "state": "SP"},
        {"name": "Posto Shell", "city": "Jacareí", "state": "SP"},
    ]
    created = {}
    for data in locations:
        existing = location_repository.get_by_name(db, name=data["name"]) if hasattr(location_repository, "get_by_name") else None
        if not existing:
            existing = location_repository.create(db, obj_in_data=LocationCreate(**data))
        created[data["name"]] = existing
    return created


def seed_goals(db: Session):
    goals = [
        {
            "name": "Viagem Copa 2030",
            "description": "Economizar para ingressos e passagens da Copa",
            "target_amount": Decimal("10000.00"),
            "target_date": date(2030, 6, 1),
            "icon": "plane",
            "color": "#6366F1",
        },
        {
            "name": "Reserva de Emergência",
            "description": "6 meses de custo fixo",
            "target_amount": Decimal("15000.00"),
            "target_date": None,
            "icon": "shield-check",
            "color": "#10B981",
        },
    ]
    for data in goals:
        existing = db.query(goal_repository.model).filter_by(name=data["name"]).first()
        if not existing:
            goal_repository.create(db, obj_in_data=GoalCreate(**data))


def seed_recurring_bills(db: Session, categories: dict, payment_methods: dict):
    lazer = categories.get("Lazer")
    moradia = categories.get("Moradia")
    credito = payment_methods.get("Cartão de Crédito")

    bills = [
        {
            "name": "Netflix",
            "amount": Decimal("55.90"),
            "due_day": 10,
            "category_id": lazer.id if lazer else None,
            "payment_method_id": credito.id if credito else None,
            "is_active": True,
        },
        {
            "name": "Spotify",
            "amount": Decimal("21.90"),
            "due_day": 15,
            "category_id": lazer.id if lazer else None,
            "payment_method_id": credito.id if credito else None,
            "is_active": True,
        },
        {
            "name": "Internet Fibra",
            "amount": Decimal("120.00"),
            "due_day": 5,
            "category_id": moradia.id if moradia else None,
            "payment_method_id": credito.id if credito else None,
            "is_active": True,
        },
    ]
    for data in bills:
        existing = recurring_bill_repository.get_by_name(db, name=data["name"])
        if not existing:
            recurring_bill_repository.create(db, obj_in_data=RecurringBillCreate(**data))


def run_seed():
    print("🌱 Iniciando o Seeder do CashApp...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        methods = seed_payment_methods(db)
        print("  ✓ Payment Methods inseridos com sucesso!")

        contexts = seed_contexts(db)
        print("  ✓ Contexts inseridos com sucesso!")

        categories = seed_categories(db)
        print("  ✓ Categories inseridas com sucesso!")

        seed_locations(db)
        print("  ✓ Locations inseridas com sucesso!")

        seed_goals(db)
        print("  ✓ Goals inseridos com sucesso!")

        seed_recurring_bills(db, categories, methods)
        print("  ✓ Recurring Bills inseridas com sucesso!")

        print("✨ Banco de dados populado com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante o seed: {e}", file=sys.stderr)
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()