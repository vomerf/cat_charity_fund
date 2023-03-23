from datetime import datetime
from typing import Optional
from sqlalchemy import false, select
from app.models.charity_project import CharityProject
from app.schemas.charityproject import CharityProjectCreate, CharityProjectUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase


class CRUDProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):

    async def get_project_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        db_project_id = (
            await session.execute(
                select(CharityProject).
                where(CharityProject.name == project_name)
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def close_project(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        setattr(project, 'fully_invested', True)
        setattr(project, 'close_date', datetime.now())
        session.add(project)
        await session.commit()

    async def get_all_not_closed_projects(
        self,
        session: AsyncSession,
    ):
        donation = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == false()
            ).order_by(CharityProject.create_date)
        )
        donation = donation.scalars().all()
        return donation


project_crud = CRUDProject(CharityProject)