from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, false
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:
    """Базовый класс для CRUD операций."""

    def __init__(self, model):
        self.model = model

    async def save(
            self,
            session: AsyncSession,
            obj
    ):
        """Функция сохранения объекта в базу данных."""
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Функция получения объекта по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Функция получения всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        """Функция создания объекта."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        return await self.save(session, db_obj)

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        """Функция обновления объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return await self.save(session, db_obj)

    async def delete(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Функция удаления объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_all_active(
            self,
            session: AsyncSession
    ):
        """Функция получения всех активных объектов."""
        all_active = await session.execute(
            select(self.model).where(
                self.model.fully_invested == false()
            ).order_by(
                self.model.create_date
            )
        )
        return all_active.scalars().all()
