from typing import Mapping

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.categories import Category
from schemas.categories import Categories


class CategoryCRUD:
    @staticmethod
    async def get_category(session: AsyncSession, category_id: int) -> Categories:
        try:
            result = await session.execute(select(Category).where(Category.id == category_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, category_data: Categories):
        category = await CategoryCRUD.get_category(session, category_data.id)

        if category:
            for key, value in category_data.dict().items():
                setattr(category, key, value)
        else:
            category = Category(**category_data.dict())
            session.add(category)

        await session.commit()
        await session.refresh(category)

        return category

    @staticmethod
    async def get_all_categories(session: AsyncSession) -> Categories:
        try:
            result = await session.execute(select(Category))
            return result.scalars().all()
        except NoResultFound:
            print('Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None