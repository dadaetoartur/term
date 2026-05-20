from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi_users.exceptions import (
    InvalidID,
    InvalidPasswordException,
    InvalidResetPasswordToken,
    InvalidVerifyToken,
    UserAlreadyExists,
    UserAlreadyVerified,
    UserInactive,
    UserNotExists,
)
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from service.monitoring.logger import logger
from service.utils.building_project_xml_processor import XMLSchemaProcessorError
from service.utils.errors import GroupNotExistsError
from service.utils.s3_client import S3ClientError


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exception:
            logger.exception(f"{exception.__class__.__name__} error processed")
            return handle_exception(request, exception)


def handle_exception(request: Request, exception: Exception) -> JSONResponse:  # noqa: PLR0911, PLR0912
    if isinstance(exception, RequestValidationError):
        logger.error(f"Validation error for {request.url.path}: {exception.errors()}")
        return JSONResponse(
            {"detail": jsonable_encoder(exception.errors(), exclude={"ctx"})},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exception, HTTPException):
        logger.warning(f"HTTP exception for {request.url.path}: {exception.detail}")
        return JSONResponse({"detail": exception.detail}, status_code=exception.status_code)

    if isinstance(exception, S3ClientError):
        logger.warning(f"S3Client exception for {request.url.path}: {exception}")
        return JSONResponse({"detail": str(exception)}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    if isinstance(exception, XMLSchemaProcessorError):
        logger.error(f"XMLSchemaProcessorError exception: {exception}")
        return JSONResponse({"detail": str(exception)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exception, InvalidID):
        logger.error(f"Invalid ID error: {exception}")
        return JSONResponse({"detail": "Invalid ID provided."}, status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, UserAlreadyExists):
        logger.error(f"User already exists error: {exception}")
        return JSONResponse({"detail": "User already exists."}, status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, UserNotExists):
        logger.error(f"User not exists error: {exception}")
        return JSONResponse({"detail": "User not exists."}, status_code=status.HTTP_404_NOT_FOUND)

    if isinstance(exception, GroupNotExistsError):
        logger.error(f"Group not exists error: {exception}")
        return JSONResponse({"detail": "Group not exists."}, status_code=status.HTTP_404_NOT_FOUND)

    if isinstance(exception, UserInactive):
        logger.error(f"User inactive error: {exception}")
        return JSONResponse({"detail": "User is inactive."}, status_code=status.HTTP_403_FORBIDDEN)

    if isinstance(exception, UserAlreadyVerified):
        logger.error(f"User already verified error: {exception}")
        return JSONResponse({"detail": "User already verified."}, status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, InvalidVerifyToken):
        logger.error(f"Invalid verify token error: {exception}")
        return JSONResponse({"detail": "Invalid verification token."}, status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, InvalidResetPasswordToken):
        logger.error(f"Invalid reset password token error: {exception}")
        return JSONResponse({"detail": "Invalid reset password token."}, status_code=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, InvalidPasswordException):
        logger.error(f"Invalid password error: {exception}")
        return JSONResponse(
            {"detail": f"Invalid password: {exception.reason}"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    logger.exception(f"Unhandled exception for {request.url.path}: {exception}")
    return JSONResponse({"detail": str(exception)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
