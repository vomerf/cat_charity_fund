from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


async def create_charity_project(new_project: CharityProjectCreate):
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    async with AsyncSessionLocal() as session:
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
    return db_project


async def get_project_by_name(project_name: str):
    async with AsyncSessionLocal() as session:
        db_project_id = (
            await session.execute(
                select(CharityProject).
                where(CharityProject.name == project_name)
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id