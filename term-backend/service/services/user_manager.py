import uuid

from fastapi import Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select

from service.database.common import SqlSessionFactory
from service.database.models.users import User
from service.monitoring.logger import logger
from service.settings import Settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    def __init__(self, user_db: SQLAlchemyUserDatabase, settings: Settings) -> None:
        super().__init__(user_db)
        self.reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
        self.verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def list_all(self) -> list[User]:
        query = select(self.user_db.user_table)  # type: ignore[attr-defined]
        result = await self.user_db.session.execute(query)  # type: ignore[attr-defined]
        return result.unique().scalars().all()

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,  # noqa: ARG002
        response: Response | None = None,
    ) -> None:
        logger.info(f"User {user.id} has logged in. Headers[{response.headers if response else 'No Response'}]")

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,  # noqa: ARG002
    ) -> None:
        logger.info(f"User {user.id} has registered.")
        await self._update(user, {"is_verified": True})


class DbUserContext:
    def __init__(self, session_factory: SqlSessionFactory, settings: Settings) -> None:
        self._session_factory = session_factory
        self._settings = settings

    async def get_user_manager(self) -> UserManager:
        async with self._session_factory.get_session() as session:
            user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = SQLAlchemyUserDatabase(session, User)
            return UserManager(user_db, self._settings)
