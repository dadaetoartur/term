from typing import Any

from sqlalchemy import delete, select

from service.database.common import SqlSessionFactory
from service.database.models.users import UserGroup


class UserGroupDbContext:
    def __init__(self, session_factory: SqlSessionFactory) -> None:
        self._session_factory = session_factory

    async def get_by_user_id_and_group_id(self, group_id: Any, user_id: Any) -> UserGroup | None:
        async with self._session_factory.get_session() as session:
            query = select(UserGroup).where(UserGroup.group_id == group_id, UserGroup.user_id == user_id)
            return (await session.execute(query)).scalar()

    async def create(self, group_id: Any, user_id: Any) -> UserGroup:
        item = UserGroup(group_id=group_id, user_id=user_id)  # type:ignore[call-arg]
        async with self._session_factory.get_session() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return item

    async def delete(self, group_id: Any, user_id: Any) -> None:
        async with self._session_factory.get_session() as session, session.begin():
            query = delete(UserGroup).where(UserGroup.group_id == group_id, UserGroup.user_id == user_id)
            await session.execute(query)
            await session.commit()
