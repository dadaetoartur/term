from abc import ABCMeta, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import delete, select, update

from service.database.common import SqlSessionFactory

TItem = TypeVar("TItem")


class DbContextBase(Generic[TItem], metaclass=ABCMeta):
    @abstractmethod
    async def list_all(self) -> Sequence[TItem]:
        pass

    @abstractmethod
    async def create(self, item: TItem) -> TItem:
        pass

    @abstractmethod
    async def get(self, item_id: Any) -> TItem | None:
        pass

    @abstractmethod
    async def update(self, item_id: Any, item: TItem) -> TItem | None:
        pass

    @abstractmethod
    async def delete(self, item_id: Any) -> None:
        pass


class DbContext(DbContextBase[TItem]):
    def __init__(self, session_factory: SqlSessionFactory, entity_type: type[TItem]) -> None:
        self._item_type = entity_type
        self._session_factory = session_factory

    async def list_all(self) -> Sequence[TItem]:
        async with self._session_factory.get_session() as session:
            query = select(self._item_type)
            result = await session.execute(query)
            return result.unique().scalars().all()

    async def create(self, item: TItem) -> TItem:
        async with self._session_factory.get_session() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return item

    async def get(self, item_id: Any) -> TItem | None:
        async with self._session_factory.get_session() as session:
            query = select(self._item_type).where(self._item_type.id == item_id)  # type: ignore[attr-defined]
            return (await session.execute(query)).scalar()

    async def update(self, item_id: Any, item: TItem) -> TItem | None:
        async with self._session_factory.get_session() as session:
            values = self._to_delta_dict(item)
            if not values:
                raise ValueError("No values to update")
            query = (
                update(self._item_type)
                .where(self._item_type.id == item_id)  # type: ignore[attr-defined]
                .values(**values)
                .returning(self._item_type)
            )
            result = (await session.execute(query)).scalar()
            await session.commit()

            return result

    async def delete(self, item_id: Any) -> None:
        async with self._session_factory.get_session() as session:
            query = delete(self._item_type).where(self._item_type.id == item_id)  # type: ignore[attr-defined]
            await session.execute(query)
            await session.commit()

    @staticmethod
    def _to_delta_dict(item: TItem) -> dict:
        return {
            column.name: getattr(item, column.name)
            for column in item.__table__.columns  # type: ignore[attr-defined]
            if getattr(item, column.name) is not None
        }
