from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.role import Role, Permission
from schemas.permissions import PermissionRead, PermissionCreate


class PermCRUD:
    @staticmethod
    async def get_role(session: AsyncSession, perm_id: int) -> PermissionRead:
        try:
            result = await session.execute(select(Permission).where(Permission.id == perm_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, perm_data: PermissionCreate):
        # Попробуем найти по name (или другому уникальному полю)
        result = await session.execute(
            select(Permission).where(Permission.name == perm_data.name)
        )
        perm = result.scalar_one_or_none()
        status = None
        if perm:
            for key, value in perm_data.dict().items():
                setattr(perm, key, value)
            status = True
        else:
            perm = Role(**perm_data.dict())
            session.add(perm)
            status = False

        await session.commit()
        await session.refresh(perm)

        return perm, status

    from sqlalchemy import select, desc

    @staticmethod
    async def get_all_perms(session: AsyncSession) -> PermissionRead:
        try:
            result = await session.execute(
                select(Permission).order_by(desc(Permission.id))  # новые первыми
            )
            return result.scalars().all()
        except NoResultFound:
            print("Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ...")
            return None