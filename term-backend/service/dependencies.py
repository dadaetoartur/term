from contextlib import asynccontextmanager
from functools import cache
from typing import AsyncIterator
from uuid import UUID

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
    Strategy,
    Transport,
)

from service.constants import COOKIE_NAME
from service.database.common import SqlSessionFactory
from service.database.models.building_project import BuildingInfo, ConstructionPart, ConstructionSection
from service.database.models.users import Group as DbGroup, User
from service.services.group_service import GroupService
from service.services.user_group_db_context import UserGroupDbContext
from service.services.user_manager import DbUserContext
from service.services.user_service import UserService
from service.settings import Settings
from service.utils.building_project_xml_processor import XMLSchemaProcessor
from service.utils.db_context import DbContext
from service.utils.s3_client import S3BucketContext, S3Client
from service.utils.sensor_reader import SensorReader


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def _get_factory() -> SqlSessionFactory:
    settings = get_settings()
    return SqlSessionFactory(settings)


@cache
def get_auth_transport() -> Transport:
    settings = get_settings()
    return CookieTransport(
        cookie_name=COOKIE_NAME,
        cookie_max_age=settings.USER_SESSION_LIFETIME_SECONDS,
        cookie_httponly=False,
        cookie_secure=False,
    )


@cache
def get_auth_strategy() -> Strategy:
    settings = get_settings()
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.USER_SESSION_LIFETIME_SECONDS,
    )


@cache
def get_group_db_context() -> DbContext[DbGroup]:
    return DbContext[DbGroup](_get_factory(), DbGroup)


@cache
def get_building_info_db_context() -> DbContext[BuildingInfo]:
    return DbContext[BuildingInfo](_get_factory(), BuildingInfo)


@cache
def get_construction_part_db_context() -> DbContext[ConstructionPart]:
    return DbContext[ConstructionPart](_get_factory(), ConstructionPart)


@cache
def get_construction_section_db_context() -> DbContext[ConstructionSection]:
    return DbContext[ConstructionSection](_get_factory(), ConstructionSection)


@cache
def get_user_group_db_context() -> UserGroupDbContext:
    return UserGroupDbContext(_get_factory())


@cache
def get_db_user_context() -> DbUserContext:
    return DbUserContext(_get_factory(), get_settings())


@cache
def get_xml_schema_processor() -> XMLSchemaProcessor:
    settings = get_settings()
    return XMLSchemaProcessor(
        xsd_path=settings.XML_SCHEMA_PATH,
        units_map_path=settings.UNITS_MAP_PATH,
    )


@cache
def get_auth_backend() -> AuthenticationBackend:
    return AuthenticationBackend(
        name="jwt",
        transport=get_auth_transport(),
        get_strategy=get_auth_strategy,
    )


@cache
def get_fastapi_users() -> FastAPIUsers:
    user_context = get_db_user_context()
    return FastAPIUsers[User, UUID](user_context.get_user_manager, [get_auth_backend()])


@cache
def get_allow_origins() -> list[str]:
    return ["*"]


@cache
def get_s3_client() -> S3Client:
    settings = get_settings()
    return S3Client(url=settings.S3_URI, access_key=settings.S3_USER, secret_key=settings.S3_PASSWORD)


@cache
def get_group_service() -> GroupService:
    return GroupService(
        db_group_context=get_group_db_context(),
        db_user_group_context=get_user_group_db_context(),
        get_user_manager=get_fastapi_users().get_user_manager,  # type: ignore[arg-type]
    )


@cache
def get_user_service() -> UserService:
    return UserService(
        get_user_manager=get_fastapi_users().get_user_manager,  # type: ignore[arg-type]
        group_service=get_group_service(),
    )


@cache
def get_bim_s3_context() -> S3BucketContext:
    settings = get_settings()
    s3_client = get_s3_client()
    return s3_client.get_bucket_context(settings.BIM_BUCKET)


@cache
def get_sensor_reader() -> SensorReader:
    settings = get_settings()
    return SensorReader(settings)


@cache
def get_documents_s3_context() -> S3BucketContext:
    settings = get_settings()
    s3_client = get_s3_client()
    return s3_client.get_bucket_context(settings.DOCUMENTS_BUCKET)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    s3_client = get_s3_client()
    get_bim_s3_context()
    get_documents_s3_context()
    sensor_reader = get_sensor_reader()
    session_factory = _get_factory()
    try:
        await s3_client.on_startup()
        await sensor_reader.initialize()
        await session_factory.on_startup()
        yield
    finally:
        await s3_client.on_shutdown()
        await session_factory.on_shutdown()
