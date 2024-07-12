from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project_crud
from app.models import CharityProject
from app.schemas.project import ProjectUpdate


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта."""
    project = await project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_is_closed(
        project: CharityProject
) -> None:
    """ Проверка закрытого проекта."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_update_amount_lower_invested(
        project_in_request: ProjectUpdate,
        project: CharityProject
) -> None:
    """Проверка, что сумма проекта больше, чем уже внесена."""
    if (
            project_in_request.full_amount and
            project_in_request.full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя изменить сумму проекта,'
                    'если она меньше уже внесенной суммы!')
        )


async def check_invested_before_delete_project(
        project: CharityProject
) -> None:
    """ Проверка, что в проект были внесены инвестиции."""
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект, в который внесли инвестиции нельзя удалить!'
        )


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка на уникальность названия проекта."""
    project_id = await project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким названием уже существует!'
        )
