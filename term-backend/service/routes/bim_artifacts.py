from uuid import UUID

from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, Response
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from pydantic import TypeAdapter

from service.database.models.building_project import ConstructionSection
from service.dependencies import get_bim_s3_context, get_construction_section_db_context, get_fastapi_users
from service.models.building_project import ConstructionSectionRead
from service.models.s3_artifacts import FileInfo
from service.utils.db_context import DbContext
from service.utils.s3_client import S3BucketContext

router = InferringRouter()
fastapi_users = get_fastapi_users()
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)


@cbv(router)
class BimArtifactsAPI:
    s3_context: S3BucketContext = Depends(get_bim_s3_context)
    construction_section_db_context: DbContext[ConstructionSection] = Depends(get_construction_section_db_context)

    adapter_list_file_info = TypeAdapter(list[FileInfo])

    @router.get(
        "/all-artifacts",
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Список артефактов успешно получен."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "
                "которое помешало ему выполнить запрос."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Получить список всех артефактов.",
    )
    async def get_all_info_artifacts(self) -> list[FileInfo]:
        return await self.s3_context.list_objects()

    @router.post(
        "/{construction_section_id}/upload_artifact",
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_201_CREATED: {"description": "Артефакт успешно загружен и связан с разделом строительства."},
            status.HTTP_400_BAD_REQUEST: {
                "description": "Ошибка загрузки артефакта из-за неверного формата или размера файла."
            },
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Неавторизованный доступ - требуются учетные данные суперпользователя."
            },
            status.HTTP_403_FORBIDDEN: {"description": "Операция запрещена - требуется статус суперпользователя."},
            status.HTTP_404_NOT_FOUND: {"description": "Раздел строительства не найден."},
            status.HTTP_409_CONFLICT: {"description": "Файл уже существует."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - произошла ошибка при обработке запроса."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Загрузить файл артефакта в указанный раздел строительства и сохранить его в S3.",
        summary="Загрузить артефакт в S3",
    )
    async def upload_artifact_to_repository(
        self, construction_section_id: UUID, file: UploadFile
    ) -> ConstructionSectionRead:
        construction_section = await self.construction_section_db_context.get(construction_section_id)
        if not construction_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction section not found")

        if self._has_file_info(construction_section.bim_artifacts, filename=file.filename):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="File already exists")

        file_info = await self.s3_context.upload_artifact(construction_section_id, file)
        construction_section.bim_artifacts.append(file_info.model_dump(mode="json"))

        model_construction_section = ConstructionSectionRead.model_validate(construction_section)

        updated_construction_section = ConstructionSection(bim_artifacts=construction_section.bim_artifacts)  # type: ignore[call-arg]
        await self.construction_section_db_context.update(construction_section_id, updated_construction_section)
        return model_construction_section

    @router.get(
        "/{construction_section_id}/download/{file_path:path}",
        response_class=FileResponse,
        status_code=status.HTTP_200_OK,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_200_OK: {"description": "Артефакт успешно загружен."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Доступ запрещен."},
            status.HTTP_404_NOT_FOUND: {"description": "Артефакт не найден."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "
                "которое помешало ему выполнить запрос."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Скачать артефакт по пути.",
    )
    async def download_artifact(self, construction_section_id: UUID, file_path: str) -> Response:
        construction_section = await self.construction_section_db_context.get(construction_section_id)
        if not construction_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction section not found")

        if not self._has_file_info(construction_section.bim_artifacts, file_path=file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")

        return await self.s3_context.download_artifact(file_path)

    @router.delete(
        "/{construction_section_id}/delete/{file_path:path}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(current_user)],
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Артефакты успешно удалены."},
            status.HTTP_400_BAD_REQUEST: {"description": "Ошибка удаления артефактов."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Токен отсутствует или пользователь не активен."},
            status.HTTP_403_FORBIDDEN: {"description": "Доступ запрещен."},
            status.HTTP_404_NOT_FOUND: {"description": "Артефакты для удаления не найдены."},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Внутренняя ошибка сервера - сервер столкнулся с неожиданным состоянием, "
                "которое помешало ему выполнить запрос."
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Сервис недоступен - сервер временно не может обработать запрос "
                "из-за перегрузки или планового обслуживания."
            },
        },
        description="Удалить артефакты по ID.",
    )
    async def delete_artifacts(self, construction_section_id: UUID, file_path: str) -> None:
        construction_section = await self.construction_section_db_context.get(construction_section_id)
        if not construction_section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Construction section not found")

        if not self._has_file_info(construction_section.bim_artifacts, file_path=file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artifact not found")

        await self.s3_context.delete_object(file_path)

        construction_section.bim_artifacts = [
            artifact for artifact in construction_section.bim_artifacts if file_path != artifact.get("file_path")
        ]
        await self.construction_section_db_context.update(construction_section_id, construction_section)

    def _has_file_info(
        self,
        document_artifacts: list[dict],
        *,
        filename: str | None = None,
        file_path: str | None = None,
    ) -> bool:
        if not filename and not file_path:
            raise ValueError("Filename or file_path must be provided")

        validated_artifacts = self.adapter_list_file_info.validate_python(document_artifacts)

        if filename:
            return any(filename == artifact.filename for artifact in validated_artifacts)

        if file_path:
            return any(file_path == artifact.file_path for artifact in validated_artifacts)

        return False
