from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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


project_crud = CRUDProject(CharityProject)
