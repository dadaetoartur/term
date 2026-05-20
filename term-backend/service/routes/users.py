from uuid import UUID

from fastapi import Depends, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from fastapi_users import models

from service.dependencies import get_fastapi_users, get_user_service
from service.models.users import UserCreate, UserRead, UserUpdate
from service.services.user_service import UserService
from service.utils.responses import response_400, response_401, response_403, response_404, response_500

router = InferringRouter()

fastapi_users = get_fastapi_users()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True)


@cbv(router)
class UserAPI:
    user_service: UserService = Depends(get_user_service)

    @router.get(
        "/all-users",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Список всех пользователей успешно получен."},
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Получение списка всех пользователей",
    )
    async def get_all_users(self) -> list[UserRead]:
        return await self.user_service.get_all_users()

    @router.post(
        "/create-user",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Новый пользователь успешно создан."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Создать нового пользователя.",
    )
    async def create_user(self, user_create: UserCreate) -> UserRead:
        return await self.user_service.create_user(user_create)

    @router.get(
        "/me",
        dependencies=[Depends(current_user)],
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": "Информация о текущем пользователе успешно получена."},
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Получить информацию о текущем пользователе.",
    )
    async def get_info_current_user(self, user: models.UP = Depends(current_user)) -> UserRead:
        return UserRead.model_validate(user)

    @router.get(
        "/{id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Информация о пользователе успешно получена."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Получить информацию о пользователе по ID.",
    )
    async def get_info_user_by_id(self, id: UUID) -> UserRead:
        return await self.user_service.get_user(id)

    @router.patch(
        "/{id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Пользователь успешно обновлен."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Обновить данные пользователя по ID.",
    )
    async def update_user_by_id(self, user_update: UserUpdate, id: UUID) -> UserRead:
        return await self.user_service.update_user(id, user_update)

    @router.delete(
        "/{id}",
        dependencies=[Depends(current_user)],
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Пользователь успешно удален."},
            status.HTTP_400_BAD_REQUEST: response_400,
            status.HTTP_401_UNAUTHORIZED: response_401,
            status.HTTP_403_FORBIDDEN: response_403,
            status.HTTP_404_NOT_FOUND: response_404,
            status.HTTP_500_INTERNAL_SERVER_ERROR: response_500,
        },
        description="Удалить пользователя по ID.",
    )
    async def delete_user_by_id(self, id: UUID) -> None:
        await self.user_service.delete_user(id)
