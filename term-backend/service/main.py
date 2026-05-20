from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from service.constants import SERVICE_DESCRIPTION, SERVICE_TITLE, TAGS_METADATA
from service.dependencies import get_allow_origins, get_settings, lifespan
from service.routes import (
    auth,
    bim_artifacts,
    building_project,
    document_artifacts,
    group,
    health,
    sensors,
    users,
)
from service.utils.middleware import ErrorHandlingMiddleware, handle_exception

settings = get_settings()


app = FastAPI(
    title=SERVICE_TITLE,
    description=SERVICE_DESCRIPTION,
    openapi_tags=TAGS_METADATA,
    version=settings.SERVICE_VERSION,
    lifespan=lifespan,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(group.router, prefix="/group", tags=["group"])
app.include_router(bim_artifacts.router, prefix="/bim_artifacts", tags=["bim_artifacts"])
app.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
app.include_router(building_project.router, prefix="/building_project", tags=["building_project"])
app.include_router(document_artifacts.router, prefix="/document_artifacts", tags=["document_artifacts"])

app.add_middleware(ErrorHandlingMiddleware)

if not settings.is_production:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_allow_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_exception_handler(RequestValidationError, handle_exception)
app.add_exception_handler(HTTPException, handle_exception)
