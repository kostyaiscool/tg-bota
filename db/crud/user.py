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
        is_new = None

        if user:
            is_new = False
            for key, value in user_data.dict().items():
                setattr(user, key, value)
        else:
            is_new = True
            user = User(**user_data.dict())
            session.add(user)

        await session.commit()
        await session.refresh(user)

        return user, is_new

    @staticmethod
    async def has_role(session: AsyncSession, role_name: str, user_id: int) -> bool:
        user = await TelegramUserCRUD.get_user(session, user_id)
        return any(role.name == role_name for role in user.roles)

    @staticmethod
    async def has_permission(session: AsyncSession, perm_name: str, user_id: int) -> bool:
        user = await TelegramUserCRUD.get_user(session, user_id)
        for role in user.roles:
            if any(permission.name == perm_name for permission in role.permission):
                return True
        return False