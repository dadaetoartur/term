import logging
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, AsyncContextManager, AsyncIterator, Callable
from urllib.parse import quote, unquote
from uuid import UUID

from aiobotocore.session import AioBaseClient, AioSession, get_session
from fastapi import Response, UploadFile
from pydantic import TypeAdapter

from service.models.s3_artifacts import FileInfo

logger = logging.getLogger(__name__)


class S3ClientError(Exception):
    pass


class S3BucketContext:
    def __init__(self, get_s3_client: Callable[[], AsyncContextManager[AioBaseClient]], bucket_name: str) -> None:
        self._get_s3_client = get_s3_client
        self._bucket_name = bucket_name
        self._adapter_list_file_info = TypeAdapter(list[FileInfo])

    async def list_objects(self) -> list[FileInfo]:
        try:
            async with self._get_s3_client() as client:
                result = await client.list_objects(Bucket=self._bucket_name)
                return self._adapter_list_file_info.validate_python(result.get("Contents", []))
        except Exception as exception:
            logger.error(f"Error listing objects in bucket '{self._bucket_name}': {exception}")
            raise S3ClientError(f"Failed to list objects in bucket '{self._bucket_name}'") from exception

    async def delete_object(self, key: str) -> None:
        try:
            async with self._get_s3_client() as client:
                await client.delete_object(Bucket=self._bucket_name, Key=key)
        except Exception as exception:
            logger.error(f"Error deleting object '{key}': {exception}")
            raise S3ClientError(f"Failed to delete object '{key}'") from exception

    async def upload_artifact(self, artifacts_id: UUID, file: UploadFile) -> FileInfo:
        if not file.filename:
            raise S3ClientError("Uploaded file must have a filename")

        file_path = f"{artifacts_id}/{file.filename}"
        metadata = {"filename": quote(file.filename)}
        await self._put_object(file_path, await file.read(), metadata)
        return FileInfo(artifacts_id=artifacts_id, filename=file.filename, file_path=file_path)

    async def download_artifact(self, file_path: str) -> Response:
        file_obj = await self._get_object(file_path)
        headers = self._make_header(file_obj)
        async with file_obj["Body"] as stream:
            serialized = await stream.read()
        return Response(content=serialized, media_type=file_obj["ContentType"], headers=headers)

    async def _get_object(self, key: str) -> dict[Any, Any]:
        try:
            async with self._get_s3_client() as client:
                return await client.get_object(Bucket=self._bucket_name, Key=key)
        except Exception as exception:
            logger.error(f"Error retrieving object '{key}': {exception}")
            raise S3ClientError(f"Object '{key}' not found") from exception

    async def _get_paginator(self, prefix: str) -> list[FileInfo]:
        objects = []
        try:
            async with self._get_s3_client() as client:
                paginator = client.get_paginator("list_objects")
                async for result in paginator.paginate(Bucket=self._bucket_name, Prefix=prefix):
                    objects.extend(self._adapter_list_file_info.validate_python(result.get("Contents", [])))
        except Exception as exception:
            logger.error(f"Error retrieving object with prefix '{prefix}': {exception}")
            raise S3ClientError(f"Object with prefix '{prefix}' not found") from exception
        return objects

    async def _put_object(self, key: str, file_body: bytes, metadata: dict[str, str] | None = None) -> None:
        try:
            async with self._get_s3_client() as client:
                await client.put_object(Bucket=self._bucket_name, Key=key, Body=file_body, Metadata=metadata)
        except Exception as exception:
            logger.error(f"Error uploading object '{key}': {exception}")
            raise S3ClientError(f"Failed to upload object '{key}'") from exception

    @staticmethod
    def _make_header(file_obj: dict[str, Any]) -> dict[str, str]:
        headers = file_obj.get("ResponseMetadata", {}).get("HTTPHeaders", {})
        filename = unquote(file_obj.get("Metadata", {}).get("filename"))
        if filename:
            content_disposition_filename = quote(filename)
            if content_disposition_filename != filename:
                content_disposition = f"attachment; filename*=utf-8''{content_disposition_filename}"
            else:
                content_disposition = f'attachment; filename="{filename}"'
            headers.setdefault("content-disposition", content_disposition)
        return headers


class S3Client:
    def __init__(self, url: str, access_key: str, secret_key: str) -> None:
        self._url = url
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket_names: list[str] = []
        self._client: AioBaseClient | None = None

        self._exit_stack = AsyncExitStack()
        self._botocore_session: AioSession = get_session()

    def get_bucket_context(self, bucket_name: str) -> S3BucketContext:
        self._bucket_names.append(bucket_name)
        return S3BucketContext(get_s3_client=self._get_client, bucket_name=bucket_name)

    async def on_startup(self) -> None:
        buckets = await self._list_buckets()
        for bucket_name in self._bucket_names:
            if bucket_name not in buckets:
                logger.warning(f"Bucket '{bucket_name}' was not found on the list of available buckets")
                await self._create_bucket(bucket_name)
            else:
                logger.info(f"Bucket '{bucket_name}' is available")

    async def on_shutdown(self) -> None:
        if self._client:
            await self._client.close()
            logger.info("S3Client connection closed")

    @asynccontextmanager
    async def _get_client(self) -> AsyncIterator[AioBaseClient]:
        if not self._client:
            self._client = await self._exit_stack.enter_async_context(
                self._botocore_session.create_client(
                    "s3",
                    endpoint_url=self._url,
                    aws_access_key_id=self._access_key,
                    aws_secret_access_key=self._secret_key,
                )
            )
        yield self._client

    async def _list_buckets(self) -> list[str]:
        try:
            async with self._get_client() as client:
                buckets = await client.list_buckets()
                return [bucket["Name"] for bucket in buckets["Buckets"]]
        except Exception as exception:
            logger.error(f"Error retrieving the list of buckets: {exception}")
            raise S3ClientError("Failed to retrieve bucket list") from exception

    async def _create_bucket(self, bucket_name: str) -> None:
        try:
            async with self._get_client() as client:
                await client.create_bucket(Bucket=bucket_name)
                logger.info(f"Bucket '{bucket_name}' has been successfully created")
        except Exception as exception:
            logger.error(f"Error creating bucket '{bucket_name}': {exception}")
            raise S3ClientError(f"Failed to create bucket '{bucket_name}'") from exception
