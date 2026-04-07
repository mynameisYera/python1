from django.core.management.base import BaseCommand

from main import sa_models  # noqa: F401 — регистрация моделей в metadata
from main.db import Base, engine


class Command(BaseCommand):
    help = 'Создать таблицы SQLAlchemy в PostgreSQL (CREATE TABLE IF NOT EXISTS).'

    def handle(self, *args, **options):
        Base.metadata.create_all(bind=engine)
        self.stdout.write(self.style.SUCCESS('SQLAlchemy: таблицы созданы (или уже существуют).'))
