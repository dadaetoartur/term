from uuid import UUID

from fastapi import Depends, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from service.dependencies import get_fastapi_users, get_group_service
from service.models.users import GroupCreate, GroupRead, GroupUpdate
from service.services.group_service import GroupService
from service.utils.responses import response_400, response_401, response_403, response_404, response_500

router = InferringRouter()

fastapi_users = get_fastapi_users()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True)


@cbv(router)
class GroupAPI:
    group_service: GroupService = Depends(get_group_service)

    @router.get(
        "/all-groups",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Список всех групп успешно получен."},
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Получение списка всех групп",
    )
    async def get_all_groups(self) -> list[GroupRead]:
        return await self.group_service.get_all_groups()

    @router.post(
        "/create",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Новая группа успешно создана."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Создайте новую группу",
    )
    async def create_group(self, group_data: GroupCreate) -> GroupRead:
        return await self.group_service.create_group(group_data)

    @router.get(
        "/{group_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Информация о группе успешно получена."},
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Получить информацию о группе по ID.",
    )
    async def get_group_by_id(self, group_id: UUID) -> GroupRead:
        return await self.group_service.get_group_by_id(group_id)

    @router.patch(
        "/{group_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Информация о группе успешно обновлена."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Обновить информацию о группе.",
    )
    async def update_group_by_id(self, group_id: UUID, group_update: GroupUpdate) -> GroupRead:
        return await self.group_service.update_group(group_id, group_update)

    @router.delete(
        "/{group_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Группа успешно удалена."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Удалить группу по ID.",
    )
    async def delete_group_by_id(self, group_id: UUID) -> None:
        await self.group_service.delete_group(group_id)

    @router.post(
        "/{group_id}/add-user/{user_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Пользователь успешно добавлен в группу."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Добавить пользователя в группу.",
    )
    async def add_user_to_group_by_ids(self, group_id: UUID, user_id: UUID) -> GroupRead:
        return await self.group_service.add_user_to_group(group_id, user_id)

    @router.delete(
        "/{group_id}/delete-user/{user_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Пользователь успешно удален из группы."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Удалить пользователя из группы.",
    )
    async def delete_user_from_group_by_ids(self, group_id: UUID, user_id: UUID) -> GroupRead:
        return await self.group_service.delete_user_from_group(group_id, user_id)
