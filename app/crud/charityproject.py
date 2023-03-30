from datetime import datetime
from typing import Optional

from sqlalchemy import false, func, select, true, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectUpdate)


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

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        print(CharityProject.close_date - CharityProject.create_date)

        projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.create_date,
                CharityProject.close_date,
                (
                    func.strftime('%s', CharityProject.close_date) -
                    func.strftime('%s', CharityProject.create_date)
                ).label('duration'),
                CharityProject.description
            ).where(CharityProject.fully_invested == true()).order_by(
                'duration', CharityProject.name)
        )
        projects = projects.all()
        print(projects)
        return projects


project_crud = CRUDProject(CharityProject)