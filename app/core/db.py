from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, auto_increment=True)


Base = declarative_base(cls=Base)


class ProjectDonation(Base):
    __abstract__ = True
    __mapper_args__ = {'concrete': True}

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=func.now)
    close_date = Column(DateTime)


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)