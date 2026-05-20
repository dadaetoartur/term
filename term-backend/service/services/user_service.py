from typing import Awaitable, Callable
from uuid import UUID

from fastapi_users import exceptions

from service.models.users import UserCreate, UserRead, UserUpdate
from service.services.group_service import GroupService
from service.services.user_manager import UserManager


class UserService:
    def __init__(
        self,
        get_user_manager: Callable[[], Awaitable[UserManager]],
        group_service: GroupService,
    ):
        self.get_user_manager = get_user_manager
        self.group_service = group_service

    async def create_user(self, user_create: UserCreate) -> UserRead:
        user_manager = await self.get_user_manager()
        user = await user_manager.create(user_create, safe=True)

        return UserRead.model_validate(user)

    async def get_all_users(self) -> list[UserRead]:
        user_manager = await self.get_user_manager()
        all_users = await user_manager.list_all()
        return [UserRead.model_validate(user) for user in all_users]

    async def get_user(self, user_id: UUID) -> UserRead:
        user_manager = await self.get_user_manager()
        user = await user_manager.get(user_id)
        if not user:
            raise exceptions.UserNotExists(f"User with {user_id} not found")

        return UserRead.model_validate(user)

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserRead:
        user_manager = await self.get_user_manager()
        user = await user_manager.get(user_id)
        if not user:
            raise exceptions.UserNotExists(f"User with {user_id} not found")

        updated_user = await user_manager.update(user_update, user, safe=False)
        return UserRead.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> None:
        user_manager = await self.get_user_manager()
        user = await user_manager.get(user_id)
        if not user:
            raise exceptions.UserNotExists(f"User with {user_id} not found")

        for group in user.groups:
            await self.group_service.delete_user_from_group(group_id=group.id, user_id=user_id)

        await user_manager.delete(user)
