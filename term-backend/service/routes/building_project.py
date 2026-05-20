from uuid import UUID

from fastapi import Depends, HTTPException, UploadFile, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from pydantic import TypeAdapter

from service.database.models.building_project import BuildingInfo, ConstructionPart, ConstructionSection
from service.dependencies import (
    get_building_info_db_context,
    get_construction_part_db_context,
    get_construction_section_db_context,
    get_fastapi_users,
    get_xml_schema_processor,
)
from service.models.building_project import (
    BuildingInfoCreate,
    BuildingInfoRead,
    BuildingInfoUpdate,
    ConstructionPartCreate,
    ConstructionPartRead,
    ConstructionPartUpdate,
    ConstructionSectionCreate,
    ConstructionSectionRead,
    ConstructionSectionUpdate,
)
from service.utils.building_project_xml_processor import XMLSchemaProcessor
from service.utils.db_context import DbContext

router = InferringRouter()
fastapi_users = get_fastapi_users()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)


@cbv(router)
class BuildingProjectAPI:
    building_info_db_context: DbContext[BuildingInfo] = Depends(get_building_info_db_context)
    construction_part_db_context: DbContext[ConstructionPart] = Depends(get_construction_part_db_context)
    construction_section_db_context: DbContext[ConstructionSection] = Depends(get_construction_section_db_context)
    xml_processor: XMLSchemaProcessor = Depends(get_xml_schema_processor)

    adapter_list_building_info = TypeAdapter(list[BuildingInfoRead])

    @router.get(
        "/all_building_info",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Все записи о строительных объектах успешно получены."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о строительных объектах не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Получить все записи о строительных объектах",
    )
    async def get_all_building_info(self) -> list[BuildingInfoRead]:
        all_building_info = await self.building_info_db_context.list_all()
        return self.adapter_list_building_info.validate_python(all_building_info, from_attributes=True)

    @router.post(
        "/building_info",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Запись о строительном объекте успешно создана."},
            status.HTTP_400_BAD_REQUEST: {
                "description": "Предоставлены неверные данные для создания информации о строительном объекте."
            },
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Создать новую запись о строительном объекте",
    )
    async def create_building_info(self, building_info_data: BuildingInfoCreate) -> BuildingInfoRead:
        db_building_info = BuildingInfo(**building_info_data.model_dump())
        new_project = await self.building_info_db_context.create(db_building_info)
        return BuildingInfoRead.model_validate(new_project)

    @router.post(
        "/building_info/xml",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Новый строительный проект успешно создан."},
            status.HTTP_400_BAD_REQUEST: {"description": "Предоставлены неверные данные строительного проекта."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Не суперпользователь."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Создать новый строительный проект из XML файла",
    )
    async def create_building_project_from_xml(self, file: UploadFile) -> BuildingInfoRead:
        building_info = self.xml_processor.process_xml(file.file.read())
        new_project = await self.building_info_db_context.create(building_info)
        return BuildingInfoRead.model_validate(new_project)

    @router.get(
        "/building_info/{building_info_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Запись о строительном объекте успешно получена."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется пользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Не суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о строительном объекте не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Получить информацию о строительном объекте по ID",
    )
    async def get_building_info_by_id(self, building_info_id: UUID) -> BuildingInfoRead:
        building_info = await self.building_info_db_context.get(building_info_id)
        if not building_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building info not found")
        return BuildingInfoRead.model_validate(building_info)

    @router.patch(
        "/building_info/{building_info_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Запись о строительном объекте успешно обновлена."},
            status.HTTP_400_BAD_REQUEST: {
                "description": "Предоставлены неверные данные для обновления информации о строительном объекте."
            },
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о строительном объекте не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Обновить информацию о строительном объекте по ID",
    )
    async def update_building_info(
        self, building_info_id: UUID, building_info_data: BuildingInfoUpdate
    ) -> BuildingInfoRead:
        db_building_info = BuildingInfo(**building_info_data.model_dump(exclude_unset=True))
        updated_building_info = await self.building_info_db_context.update(building_info_id, db_building_info)
        if not updated_building_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building info not found")
        return await self.get_building_info_by_id(building_info_id)

    @router.delete(
        "/building_info/{building_info_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Запись о строительном объекте успешно удалена."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о строительном объекте не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Удалить информацию о строительном объекте по ID",
    )
    async def delete_building_info(self, building_info_id: UUID) -> None:
        await self.building_info_db_context.delete(building_info_id)

    @router.post(
        "/building_info/{building_info_id}/construction_part",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Новая часть объекта успешно создана."},
            status.HTTP_400_BAD_REQUEST: {"description": "Предоставлены неверные данные для создания части объекта."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о строительном объекте не найдена."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Добавить новую часть объекта к информации о строительном объекте",
    )
    async def add_construction_part(
        self, building_info_id: UUID, construction_part: ConstructionPartCreate
    ) -> ConstructionPartRead:
        building_info = await self.building_info_db_context.get(building_info_id)
        if not building_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building info not found")

        db_construction_part = ConstructionPart(
            **construction_part.model_dump(),
            building_info=building_info,  # type: ignore[call-arg]
            building_info_id=building_info.id,
        )
        new_construction_part = await self.construction_part_db_context.create(db_construction_part)
        return ConstructionPartRead.model_validate(new_construction_part)

    @router.get(
        "/construction_part/{construction_part_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Запись о части объекте успешно получена."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется пользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Не суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о части объекте не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Получить информацию о части объекте по ID",
    )
    async def get_construction_part(self, construction_part_id: UUID) -> ConstructionPartRead:
        construction_part = await self.construction_part_db_context.get(construction_part_id)
        if not construction_part:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coonstruction part not found")
        return ConstructionPartRead.model_validate(construction_part)

    @router.patch(
        "/construction_part/{construction_part_id}",
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {"description": "Часть объекта успешно обновлена."},
            status.HTTP_400_BAD_REQUEST: {"description": "Предоставлены неверные данные для обновления части объекта."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Часть объекта не найдена."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Обновить часть объекта по ID",
    )
    async def update_construction_part(
        self, construction_part_id: UUID, construction_part_data: ConstructionPartUpdate
    ) -> ConstructionPartRead:
        db_construction_part = ConstructionPart(**construction_part_data.model_dump(exclude_unset=True))
        construction_part = await self.construction_part_db_context.update(construction_part_id, db_construction_part)
        if not construction_part:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction part not found")
        return await self.get_construction_part(construction_part_id)

    @router.delete(
        "/construction_part/{construction_part_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Часть объекта успешно удалена."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Часть объекта не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Удалить часть объекта по ID",
    )
    async def delete_construction_part(self, construction_part_id: UUID) -> None:
        await self.construction_part_db_context.delete(construction_part_id)

    @router.post(
        "/construction_part/{construction_part_id}/construction_section",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Раздел строительства успешно добавлен."},
            status.HTTP_400_BAD_REQUEST: {
                "description": "Предоставлены неверные данные для создания раздела строительства."
            },
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Часть объекта не найдена."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Добавить новый раздел строительства к части объекта",
    )
    async def add_construction_section(
        self, construction_part_id: UUID, construction_section: ConstructionSectionCreate
    ) -> ConstructionPartRead:
        construction_part = await self.construction_part_db_context.get(construction_part_id)
        if not construction_part:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction part not found")

        db_construction_section = ConstructionSection(
            **construction_section.model_dump(),
            construction_part_id=construction_part.id,  # type: ignore[call-arg]
        )
        new_construction_section = await self.construction_section_db_context.create(db_construction_section)
        construction_part.sections.append(new_construction_section)
        return ConstructionPartRead.model_validate(construction_part)

    @router.get(
        "/construction_section/{construction_section_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Запись о разделе строительства успешно получена."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется пользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Не суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Информация о разделе строительства не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Получить информацию о разделе строительства по ID",
    )
    async def get_construction_section(self, construction_section_id: UUID) -> ConstructionSectionRead:
        construction_section = await self.construction_section_db_context.get(construction_section_id)
        if not construction_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coonstruction section not found")
        return ConstructionSectionRead.model_validate(construction_section)

    @router.patch(
        "/construction_section/{construction_section_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Раздел строительства успешно обновлен."},
            status.HTTP_400_BAD_REQUEST: {
                "description": "Предоставлены неверные данные для обновления раздела строительства."
            },
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_404_NOT_FOUND: {"description": "Раздел строительства не найден."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Обновить раздел строительства по ID",
    )
    async def update_construction_section(
        self, construction_section_id: UUID, construction_section_data: ConstructionSectionUpdate
    ) -> ConstructionSectionRead:
        db_construction_section = ConstructionSection(**construction_section_data.model_dump(exclude_unset=True))
        construction_section = await self.construction_section_db_context.update(
            construction_section_id, db_construction_section
        )
        if not construction_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction section not found")
        return await self.get_construction_section(construction_section_id)

    @router.delete(
        "/construction_section/{construction_section_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Раздел строительства успешно удален."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Неавторизованный доступ - требуется суперпользователь."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Раздел строительства не найден."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Произошла внутренняя ошибка сервера."},
        },
        description="Удалить раздел строительства по ID",
    )
    async def delete_construction_section(self, construction_section_id: UUID) -> None:
        await self.construction_section_db_context.delete(construction_section_id)
