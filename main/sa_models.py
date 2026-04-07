"""
Таблицы SQLAlchemy (PostgreSQL). Миграции в проде обычно ведут через Alembic;
для обучения таблицы создаются командой: python manage.py sa_init_db
"""

from datetime import datetime

from sqlalchemy import DateTime, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Item(Base):
    """Первая таблица: простая сущность с заголовком и текстом."""

    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text(), default='')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
    )
