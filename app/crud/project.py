from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDProject(CRUDBase):
    """Класс для CRUD операций с проектами."""

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Функция получения id проекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, str]]:
        """Получение и сортировка закрытых проектов"""
        closed_projects = await session.execute(
            select([
                self.model.name,
                (
                    func.EXTRACT('epoch', self.model.close_date) -
                    func.EXTRACT('epoch', self.model.create_date)
                ).label('collection_time'),
                self.model.description
            ]).where(self.model.fully_invested).order_by('collection_time')
        )
        projects = closed_projects.all()
        return projects


project_crud = CRUDProject(CharityProject)
