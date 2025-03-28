from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from core.settings import settings
from db.base import Base


class DbHelp:
    def __init__(self, url) -> None:
        self.engine: AsyncEngine = create_async_engine(url=url, echo=False, future=True)
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=self.engine, class_=AsyncSession)

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_get(self):
        async with self.session() as session:
            yield session
    async def init_db(self):
        async with self.engine.begin() as con:
            await con.run_sync(Base.metadata.create_all)

db_help: DbHelp = DbHelp(settings.db.url)
