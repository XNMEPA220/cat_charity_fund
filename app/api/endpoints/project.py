from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import project_crud, donation_crud
from app.schemas.project import ProjectCreate, ProjectDB, ProjectUpdate
from app.services.invest import investment_process
from app.api.validators import (
    check_project_exists,
    check_project_is_closed,
    check_update_amount_lower_invested,
    check_name_duplicate,
    check_invested_before_delete_project
)

router = APIRouter()


@router.post(
    '/',
    response_model=ProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        project: ProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя. Создание нового проекта."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    invest_process = investment_process(
        await donation_crud.get_all_active(session),
        new_project
    )
    session.add_all(invest_process)
    return await project_crud.save(session, new_project)


@router.get(
    '/',
    response_model=list[ProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка всех проектов."""
    return await project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        obj_in: ProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя. Изменение проекта."""
    project = await check_project_exists(project_id, session)
    await check_project_is_closed(project)
    await check_update_amount_lower_invested(obj_in, project)
    await check_name_duplicate(obj_in.name, session)
    return await project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперпользователя. Удаление проекта."""
    project = await check_project_exists(project_id, session)
    await check_invested_before_delete_project(project)
    return await project_crud.delete(project, session)
