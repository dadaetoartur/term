from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from service.monitoring.logger import logger
from service.settings import Settings

BaseTable = declarative_base()


class SqlSessionFactory:
    def __init__(self, settings: Settings) -> None:
        self._engine = create_async_engine(
            settings.POSTGRES_SERVERS.unicode_string(),
            future=True,
            pool_size=50,
            max_overflow=30,
        )
        self._session_cls = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self._engine,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_cls() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def on_startup(self) -> None:
        async with self.get_session():
            logger.info(f"All database connections successfully established. URL['{self._engine.url}']")

    async def on_shutdown(self) -> None:
        await self._engine.dispose()
        logger.info("All database connections are disposed of")
