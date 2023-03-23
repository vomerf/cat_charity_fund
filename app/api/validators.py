# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import project_crud


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
):
    project_id = await project_crud.get_project_by_name(project_name, session)
    if project_id:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exist(
    project_id: int,
    session: AsyncSession
):
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта не существует'
        )
    return project