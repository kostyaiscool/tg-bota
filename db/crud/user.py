from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from db.models.user import TelegramUser
from schemas.user import TelegramUser as TelegramUserSchema


class TelegramUserCRUD:

    @staticmethod
    async def get_user(session: AsyncSession, user_id: int) -> TelegramUser | None:
        try:
            result = await session.execute(select(TelegramUser).where(TelegramUser.id == user_id))
            return result.scalar_one()
        except NoResultFound:
            return None

    @staticmethod
    async def create_or_update_user(session: AsyncSession, user_data: TelegramUserSchema) -> tuple[TelegramUser, bool]:
        user = await TelegramUserCRUD.get_user(session, user_data.id)
        is_new_user = False

        if user:
            for key, value in user_data.dict().items():
                setattr(user, key, value)
        else:
            user = TelegramUser(**user_data.dict())
            session.add(user)
            is_new_user = True

        await session.commit()
        await session.refresh(user)

        return user, is_new_user