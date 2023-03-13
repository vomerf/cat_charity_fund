from app.core.db import ProjectDonation

from sqlalchemy import String, Column, Text


class CharityProject(ProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
