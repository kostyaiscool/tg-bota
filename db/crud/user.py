from typing import Mapping

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User
from schemas.user import TelegramUser


class TelegramUserCRUD:
    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> TelegramUser:
        try:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, user_data: TelegramUser):
        user = await TelegramUserCRUD.get_user(session, user_data.id)

        if user:
            for key, value in user_data.dict().items():
                setattr(user, key, value)
        else:
            user = User(**user_data.dict())
            session.add(user)

        await session.commit()
        await session.refresh(user)

        return user