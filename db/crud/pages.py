from typing import Mapping, Sequence

from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.categories import CategoryCRUD
from db.models.categories import Category
from db.models.pages import Page
from schemas.categories import Categories
from schemas.pages import Pages, PageCreate


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
    async def create_or_update(session: AsyncSession, page_data: PageCreate):
        # Попробуем найти по name (или другому уникальному полю)
        result = await session.execute(
            select(Page).where(Page.name == page_data.name)
        )
        page = result.scalar_one_or_none()
        status = None
        if page:
            for key, value in page_data.dict().items():
                setattr(page, key, value)
            status = True
        else:
            page = Page(**page_data.dict())
            session.add(page)
            status = False

        await session.commit()
        await session.refresh(page)

        return page, status

    from sqlalchemy import select, desc

    @staticmethod
    async def get_all_pages(session: AsyncSession) -> Pages:
        try:
            result = await session.execute(
                select(Page).order_by(desc(Page.id))  # новые первыми
            )
            return result.scalars().all()
        except NoResultFound:
            print("Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ...")
            return None

    @staticmethod
    async def get_cat_pages(session: AsyncSession, category_id: int) -> Sequence[Page] | None:
        try:
            stmt = select(Page).where(Page.category_id == category_id)
            result = await session.execute(stmt)
            return result.scalars().all()  # Возвращаем список Page
        except NoResultFound:
            print('Нет результатов по категории.')
            return None
        except Exception as e:
            print('Ошибка при получении страниц по категории:', e)
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