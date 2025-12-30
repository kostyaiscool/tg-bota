from typing import Mapping, Sequence

from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.categories import CategoryCRUD
from db.models.categories import Category
from db.models.commentaries import Commentary
from db.models.pages import Page
from schemas.categories import Categories
from schemas.commentaries import CommentaryCreate
from schemas.pages import Pages, PageCreate


class PageCRUD:
    @staticmethod
    async def get_comment(session: AsyncSession, comment_id: int) -> Pages:
        try:
            result = await session.execute(select(Commentary).where(Commentary.id == comment_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, comm_data: PageCreate):
        # Попробуем найти по name (или другому уникальному полю)
        result = await session.execute(
            select(Commentary).where(Commentary.id == comm_data.id)
        )
        comm = result.scalar_one_or_none()
        status = None
        if comm:
            for key, value in comm_data.dict().items():
                setattr(comm, key, value)
            status = True
        else:
            page = Page(**comm_data.dict())
            session.add(comm)
            status = False

        await session.commit()
        await session.refresh(comm)

        return comm, status


    @staticmethod
    async def get_page_comments(session: AsyncSession, page_id: int) -> Pages:
        try:
            # result = await session.execute(select(Commentary).where(Commentary.id == page_id))
            # return result.scalar_one()
            stmt = select(Page).where(Commentary.page_id == page_id)
            result = await session.execute(stmt)
            return result.scalars().all()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

