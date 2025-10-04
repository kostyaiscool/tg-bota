from sqlalchemy import select, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.role import Role
from schemas.roles import RoleRead, RoleCreate


class RoleCRUD:
    @staticmethod
    async def get_role(session: AsyncSession, role_id: int) -> RoleRead:
        try:
            result = await session.execute(select(Role).where(Role.id == role_id))
            return result.scalar_one()
        except NoResultFound:
            print('Я ЗАПЕР 456 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ, И ПОСЛЕДНИЙ, КТО СБЕЖИТ ИЗ НЕГО, ПОЛУЧИТ 456,000,000 ДОЛЛАРОВ!')
            return None

    @staticmethod
    async def create_or_update(session: AsyncSession, role_data: RoleCreate):
        # Попробуем найти по name (или другому уникальному полю)
        result = await session.execute(
            select(Role).where(Role.name == role_data.name)
        )
        role = result.scalar_one_or_none()
        status = None
        if role:
            for key, value in role_data.dict().items():
                setattr(role, key, value)
            status = True
        else:
            role = Role(**role_data.dict())
            session.add(role)
            status = False

        await session.commit()
        await session.refresh(role)

        return role, status

    from sqlalchemy import select, desc

    @staticmethod
    async def get_all_roles(session: AsyncSession) -> RoleRead:
        try:
            result = await session.execute(
                select(Role).order_by(desc(Role.id))  # новые первыми
            )
            return result.scalars().all()
        except NoResultFound:
            print("Я ЗАПЕР 500 ДЕТЕЙ В СВОЕМ ПОДВАЛЕ...")
            return None