from fastapi import APIRouter, HTTPException
from app.crud.charityproject import create_charity_project
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB
from app.crud.charityproject import get_project_by_name

router = APIRouter()


@router.post(
    "/charity_project/",
    response_model=CharityProjectDB
    )
async def create_new_charityproject(
    project: CharityProjectCreate,
):
    project_id = get_project_by_name(project.name)
    if project_id:
        raise HTTPException(
            status_code=422,
            detail='Project already exists'
        )
    new_project = await create_charity_project(project)
    return new_project
