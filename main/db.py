"""
SQLAlchemy: движок и фабрика сессий.

Сессия = единица работы с БД (запросы, commit/rollback). Во view открываете сессию,
делаете операции, commit, закрываете.
"""

from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy (не путать с Django models.Model)."""


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
