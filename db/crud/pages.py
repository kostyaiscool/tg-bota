from typing import Mapping

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.categories import CategoryCRUD
from db.models.categories import Category
from db.models.pages import Page
from schemas.categories import Categories
from schemas.pages import Pages


class PageCRUD:
    @staticmethod
    async def get_page(session: AsyncSession, page_id: int) -> Pages:
        try:
            result = await session.execute(select(Page).where(Page.id == page_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, page_data: Pages):
        page = await PageCRUD.get_page(session, page_data.id)

        if page:
            for key, value in page_data.dict().items():
                setattr(page, key, value)
        else:
            page = Page(**page_data.dict())
            session.add(page)

        await session.commit()
        await session.refresh(page)

        return page

    @staticmethod
    async def get_all_pages(session: AsyncSession) -> Pages:
        try:
            result = await session.execute(select(Page))
            return result.scalars().all()
        except NoResultFound:
            print('Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def get_cat_pages(session: AsyncSession, category_id: int) -> Pages:
        try:
            category = await CategoryCRUD.get_category(session, category_id)
            result = await session.execute(select(Page).where(category == Page.categories))
            return result.scalars().all()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def get_page_name(session: AsyncSession, page_name: str) -> list[Page]:
        try:
            query = select(Page).where(
                Page.name.ilike(f"%{page_name}%")  # ищем по подстроке, нечувствительно к регистру
            )
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as e:
            print("Ошибка поиска страницы:", e)
            return []