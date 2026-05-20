from datetime import UTC, datetime, timedelta
from uuid import UUID

from fastapi import Depends, Query, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from service.database.models.building_project import ConstructionSection
from service.dependencies import get_construction_section_db_context, get_fastapi_users, get_sensor_reader
from service.models.sensors import SensorConfig, SensorData
from service.utils.db_context import DbContext
from service.utils.sensor_reader import SensorReader

router = InferringRouter()
fastapi_users = get_fastapi_users()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)


@cbv(router)
class SensorsAPI:
    sensor_reader: SensorReader = Depends(get_sensor_reader)
    construction_section_db_context: DbContext[ConstructionSection] = Depends(get_construction_section_db_context)

    @router.get(
        "/{construction_section_id}/all-sensors",
        status_code=status.HTTP_200_OK,
        response_model=list[SensorConfig],
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Список сенсоров успешно получен."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена."},
            status.HTTP_404_NOT_FOUND: {"description": "Секция строительства не найдена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "  # noqa: RUF001
                "которое помешало ему выполнить запрос."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Получить список всех сенсоров.",
    )
    async def get_all_sensors(self, construction_section_id: UUID) -> list[SensorConfig]:
        return await self.sensor_reader.get_sensors(construction_section_id)

    @router.get(
        "/{construction_section_id}/get-data/{sensor_id}",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Данные сенсора успешно получены."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Доступ запрещен."},
            status.HTTP_404_NOT_FOUND: {"description": "Секция строительства или сенсор не найдены."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "  # noqa: RUF001
                "которое помешало ему выполнить запрос."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Получить данные сенсора за указанный промежуток времени.",
    )
    async def get_sensor_data(
        self,
        construction_section_id: UUID,
        sensor_id: str,
        start: datetime = Query(default_factory=lambda: datetime.now(UTC) - timedelta(days=1)),
        end: datetime = Query(default_factory=lambda: datetime.now(UTC)),
    ) -> list[SensorData]:
        return await self.sensor_reader.get_sensor_data(construction_section_id, sensor_id, start, end)
