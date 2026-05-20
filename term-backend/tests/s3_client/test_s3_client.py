import re

import pytest
from pydantic import TypeAdapter

from service.models.s3_artifacts import FileInfo
from service.settings import Settings
from service.utils.s3_client import S3Client, S3ClientError
from tests.s3_client.conftest import (
    ARTIFACTS_FRAG_FILENAME,
    ARTIFACTS_FRAG_KEY,
    ARTIFACTS_JSON_FILENAME,
    ARTIFACTS_JSON_KEY,
    EXISTING_ARTIFACTS_ID,
    LAST_MODIFIED,
    BotocoreClientMock,
)


async def test_on_startup_success(s3_client: S3Client) -> None:
    await s3_client.on_startup()
    buckets = await s3_client._list_buckets()
    assert "bim-forge" in buckets


async def test_on_shutdown_success(s3_client: S3Client) -> None:
    await s3_client.on_shutdown()
    buckets = await s3_client._list_buckets()
    assert "bim-forge" in buckets


async def test_list_buckets_success(s3_client: S3Client) -> None:
    buckets = await s3_client._list_buckets()
    assert "bim-forge" in buckets


async def test_list_buckets_error(s3_client: S3Client, botocore_client_mock: BotocoreClientMock) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("S3 Service Down"))
    with pytest.raises(S3ClientError, match=re.escape(r"Failed to retrieve bucket list")):
        await s3_client._list_buckets()


async def test_create_bucket_success(s3_client: S3Client) -> None:
    await s3_client._create_bucket("mybucket")
    buckets = await s3_client._list_buckets()
    assert "mybucket" in buckets


async def test_create_bucket_error_handling(s3_client: S3Client, botocore_client_mock: BotocoreClientMock) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("AWS Service Error"))
    with pytest.raises(S3ClientError, match=re.escape(r"Failed to create bucket 'mybucket'")):
        await s3_client._create_bucket("mybucket")


async def test_list_objects_success(s3_client: S3Client, test_settings: Settings) -> None:
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    objects = await bucket_context.list_objects()
    assert TypeAdapter(list[FileInfo]).dump_python(objects) == [
        {
            "artifacts_id": EXISTING_ARTIFACTS_ID,
            "file_path": ARTIFACTS_FRAG_KEY,
            "filename": ARTIFACTS_FRAG_FILENAME,
            "last_modified": LAST_MODIFIED,
        },
        {
            "artifacts_id": EXISTING_ARTIFACTS_ID,
            "file_path": ARTIFACTS_JSON_KEY,
            "filename": ARTIFACTS_JSON_FILENAME,
            "last_modified": LAST_MODIFIED,
        },
    ]


@pytest.mark.asyncio
async def test_list_objects_error_handling(
    s3_client: S3Client, botocore_client_mock: BotocoreClientMock, test_settings: Settings
) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("AWS Service Error"))
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    with pytest.raises(S3ClientError, match=re.escape(r"Failed to list objects in bucket 'bim-forge'")):
        await bucket_context.list_objects()


@pytest.mark.asyncio
async def test_get_object_success(s3_client: S3Client, test_settings: Settings) -> None:
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    result = await bucket_context._get_object(ARTIFACTS_JSON_KEY)
    assert result["Key"] == ARTIFACTS_JSON_KEY


@pytest.mark.asyncio
async def test_get_object_error_handling(
    s3_client: S3Client, botocore_client_mock: BotocoreClientMock, test_settings: Settings
) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("Object not found"))
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    with pytest.raises(S3ClientError, match=re.escape(r"Object 'test_key' not found")):
        await bucket_context._get_object("test_key")


@pytest.mark.asyncio
async def test_get_paginator_success(s3_client: S3Client, test_settings: Settings) -> None:
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    objects = await bucket_context._get_paginator(str(EXISTING_ARTIFACTS_ID))
    assert TypeAdapter(list[FileInfo]).dump_python(objects) == [
        {
            "artifacts_id": EXISTING_ARTIFACTS_ID,
            "file_path": ARTIFACTS_FRAG_KEY,
            "filename": ARTIFACTS_FRAG_FILENAME,
            "last_modified": LAST_MODIFIED,
        },
        {
            "artifacts_id": EXISTING_ARTIFACTS_ID,
            "file_path": ARTIFACTS_JSON_KEY,
            "filename": ARTIFACTS_JSON_FILENAME,
            "last_modified": LAST_MODIFIED,
        },
    ]


async def test_get_paginator_error_handling(
    s3_client: S3Client, botocore_client_mock: BotocoreClientMock, test_settings: Settings
) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("Pagination Error"))
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    with pytest.raises(S3ClientError, match=re.escape(r"Object with prefix 'prefix' not found")):
        await bucket_context._get_paginator("prefix")


async def test_put_object_success(s3_client: S3Client, test_settings: Settings) -> None:
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    await bucket_context._put_object("test_key", b"Hello, world!")
    result = await bucket_context._get_object("test_key")
    assert result["Key"] == "test_key"


async def test_put_object_error_handling(
    s3_client: S3Client, botocore_client_mock: BotocoreClientMock, test_settings: Settings
) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("Upload Failed"))
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    with pytest.raises(S3ClientError, match=re.escape(r"Failed to upload object 'test_key'")):
        await bucket_context._put_object("test_key", b"Hello, world!")


async def test_delete_object_success(s3_client: S3Client, test_settings: Settings) -> None:
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    await bucket_context.delete_object(ARTIFACTS_JSON_KEY)
    objects = await bucket_context.list_objects()
    assert len(objects) == 1


async def test_delete_object_error_handling(
    s3_client: S3Client, botocore_client_mock: BotocoreClientMock, test_settings: Settings
) -> None:
    botocore_client_mock.throw_at_next_calls(Exception("Deletion Failed"))
    bucket_context = s3_client.get_bucket_context(test_settings.BIM_BUCKET)
    with pytest.raises(S3ClientError, match=re.escape(rf"Failed to delete object '{ARTIFACTS_JSON_KEY}'")):
        await bucket_context.delete_object(ARTIFACTS_JSON_KEY)
