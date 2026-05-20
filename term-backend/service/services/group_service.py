from typing import Awaitable, Callable
from uuid import UUID

from fastapi_users.exceptions import UserNotExists
from fastapi_users.manager import BaseUserManager

from service.database.models.users import Group as DbGroup
from service.models.users import GroupCreate, GroupRead, GroupUpdate
from service.services.user_group_db_context import UserGroupDbContext
from service.utils.db_context import DbContext
from service.utils.errors import GroupNotExistsError


class GroupService:
    def __init__(
        self,
        db_group_context: DbContext[DbGroup],
        db_user_group_context: UserGroupDbContext,
        get_user_manager: Callable[[], Awaitable[BaseUserManager]],
    ):
        self.db_group_context = db_group_context
        self.db_user_group_context = db_user_group_context
        self.get_user_manager = get_user_manager

    async def get_all_groups(self) -> list[GroupRead]:
        all_groups = await self.db_group_context.list_all()
        return [GroupRead.model_validate(group) for group in all_groups]

    async def create_group(self, group_data: GroupCreate) -> GroupRead:
        db_group = DbGroup(**group_data.model_dump())
        new_group = await self.db_group_context.create(db_group)
        return GroupRead.model_validate(new_group)

    async def get_group_by_id(self, group_id: UUID) -> GroupRead:
        group = await self.db_group_context.get(group_id)
        if not group:
            raise GroupNotExistsError(f"Group with id['{group_id}'] not found")

        return GroupRead.model_validate(group)

    async def update_group(self, group_id: UUID, group_update: GroupUpdate) -> GroupRead:
        db_group = DbGroup(**group_update.model_dump())
        updated_group = await self.db_group_context.update(group_id, db_group)
        if not updated_group:
            raise GroupNotExistsError(f"Group with id['{group_id}'] not found")

        return await self.get_group_by_id(group_id)

    async def delete_group(self, group_id: UUID) -> None:
        await self.db_group_context.delete(group_id)

    async def add_user_to_group(self, group_id: UUID, user_id: UUID) -> GroupRead:
        user_manager = await self.get_user_manager()
        user = await user_manager.get(user_id)
        if not user:
            raise UserNotExists(f"User with id['{user_id}'] not found")

        group = await self.db_group_context.get(group_id)
        if not group:
            raise GroupNotExistsError(f"Group with id['{group_id}'] not found")

        await self.db_user_group_context.create(group_id=group.id, user_id=user.id)
        return await self.get_group_by_id(group_id)

    async def delete_user_from_group(self, group_id: UUID, user_id: UUID) -> GroupRead:
        user_group = await self.db_user_group_context.get_by_user_id_and_group_id(group_id, user_id)
        if not user_group:
            raise GroupNotExistsError(f"Group with id['{group_id}'] not found")

        await self.db_user_group_context.delete(group_id=group_id, user_id=user_id)
        return await self.get_group_by_id(group_id)
