from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.api.validators import check_name_duplicate, check_project_exist
from app.core.db import get_async_session
from app.crud.charityproject import project_crud
from app.core.user import current_superuser

from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.invest import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude={'close_date'}
)
async def create_new_charityproject(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    new_project = await invest(session, new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'}
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_project = await project_crud.get_multi(session=session)
    return all_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exist(
        project_id, session
    )
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if obj_in.full_amount is not None and project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=400,
            detail='Нельзя уменьшить сумму сбора ниже чем собранно денег.'
        )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_or_close_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exist(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if project.invested_amount > 0:
        project = await project_crud.close_project(project, session)
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    project = await project_crud.remove(project, session)
    return project
