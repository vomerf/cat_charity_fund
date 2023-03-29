from datetime import datetime
from typing import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def update_account(
    db_project: CharityProject,
    db_donation: Donation,
    data_project: dict,
    data_donation: dict,
    status: str,
):
    if status == 'close_project':
        setattr(db_donation, 'invested_amount', data_donation['invested_amount'])
        setattr(db_project, 'invested_amount', data_project['invested_amount'])
        setattr(db_project, 'fully_invested', True)
        setattr(db_project, 'close_date', datetime.utcnow())
    if status == 'close_donate':
        setattr(db_project, 'invested_amount', data_project['invested_amount'])
        setattr(db_donation, 'invested_amount', data_donation['invested_amount'])
        setattr(db_donation, 'fully_invested', True)
        setattr(db_donation, 'close_date', datetime.utcnow())


async def invest(
    session: AsyncSession,
    db_obj: Union[CharityProject, Donation]
):
    '''Поисходит процесс инвестирования,
    распределение средств из пожертвований в открытые проекты'''
    lst = []
    db_obj_data = jsonable_encoder(db_obj)
    if isinstance(db_obj, CharityProject):
        all_act = await donation_crud.get_all_not_closed_donations(session)
    else:
        all_act = await project_crud.get_all_not_closed_projects(session)
    if not all_act:
        return db_obj
    balance_of_created_object = db_obj_data['full_amount'] - db_obj_data['invested_amount']
    for act in all_act:
        data_act = jsonable_encoder(act)
        balance_existing_object = data_act['full_amount'] - data_act['invested_amount']
        if balance_of_created_object < balance_existing_object:
            db_obj_data['invested_amount'] += balance_of_created_object
            data_act['invested_amount'] += balance_of_created_object
            if isinstance(db_obj, CharityProject):
                status = 'close_project'
                await update_account(db_obj, act, db_obj_data, data_act, status)
            else:
                status = 'close_donate'
                await update_account(act, db_obj, data_act, db_obj_data, status)
            lst.append(act)
            break
        elif balance_of_created_object > balance_existing_object:
            db_obj_data['invested_amount'] += balance_existing_object
            data_act['invested_amount'] += balance_existing_object
            if isinstance(db_obj, CharityProject):
                status = 'close_donate'
                await update_account(db_obj, act, db_obj_data, data_act, status)
            else:
                status = 'close_project'
                await update_account(act, db_obj, data_act, db_obj_data, status)
            balance_of_created_object -= balance_existing_object
            lst.append(act)
        elif balance_of_created_object == balance_existing_object:
            db_obj_data['invested_amount'] += balance_existing_object
            data_act['invested_amount'] += balance_of_created_object
            if isinstance(db_obj, CharityProject):
                await update_account(
                    db_obj, act, db_obj_data, data_act, status='close_donate'
                )
                await update_account(
                    db_obj, act, db_obj_data, data_act, status='close_project'
                )
            else:
                await update_account(
                    act, db_obj, data_act, db_obj_data, status='close_donate'
                )
                await update_account(
                    act, db_obj, data_act, db_obj_data, status='close_project'
                )
            lst.append(act)
            break

    lst.append(db_obj)
    session.add_all(lst)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj
