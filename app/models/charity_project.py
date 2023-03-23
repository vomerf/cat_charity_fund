from sqlalchemy import Column, String, Text

from .abstact_model import ProjectDonation


class CharityProject(ProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
