import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class ProjectDonation(Base):
    __abstract__ = True
    __mapper_args__ = {"concrete": True}

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    close_date = Column(DateTime)
    __table_args__ = (CheckConstraint("full_amount > 0", name="check_full_amount"),)
