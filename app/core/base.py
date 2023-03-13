"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base  # noqa
from app.models import CharityProject, Donation  # noqa
from app.models.abstact_model import ProjectDonation  # noqa
