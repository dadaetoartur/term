from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient

from service.main import app
from service.settings import Settings
from service.utils.s3_client import S3Client

EXISTING_ARTIFACTS_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
ARTIFACTS_JSON_FILENAME = "small.json"
ARTIFACTS_FRAG_FILENAME = "small.frag"
ARTIFACTS_JSON_KEY = f"{EXISTING_ARTIFACTS_ID}/{ARTIFACTS_JSON_FILENAME}"
ARTIFACTS_FRAG_KEY = f"{EXISTING_ARTIFACTS_ID}/{ARTIFACTS_FRAG_FILENAME}"
ARTIFACTS_JSON_BODY = b"1"
ARTIFACTS_FRAG_BODY = b"2"
LAST_MODIFIED = datetime(1970, 1, 1, tzinfo=UTC)


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app, base_url="http://testserver")


@pytest.fixture
def test_settings() -> Settings:
    return Settings()


class Paginator:
    def __init__(self, data_map: dict) -> None:
        self._data_map = data_map

    async def paginate(self, Bucket: str, Prefix: str) -> AsyncIterator[dict]:
        artifacts = [
            {
                "Contents": [
                    {"LastModified": entry.LastModified, "Key": entry.Key}
                    for entry in self._data_map[Bucket].values()
                    if entry.Key.startswith(Prefix)
                ]
            }
        ]
        for artifact in artifacts:
            yield artifact


class BotocoreClientMock:
    @dataclass
    class Entry:
        Key: str
        LastModified: datetime
        data: bytes
        ContentType: str | None = None
        Metadata: dict | None = None

    class DataReader:
        def __init__(self, data: bytes) -> None:
            self._data = data

        async def read(self) -> bytes:
            return self._data

    def __init__(self, bucket: str) -> None:
        self._data_map: dict[str, dict[str, BotocoreClientMock.Entry]] = {}
        self._data_map[bucket] = {}

        self._exception: Exception | None = None

    def set_content(
        self,
        bucket: str,
        key: str,
        data: bytes,
        last_modified: datetime | None = None,
        content_type: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        self._data_map[bucket][key] = BotocoreClientMock.Entry(
            key,
            last_modified or datetime.now(tz=UTC),
            data,
            ContentType=content_type,
            Metadata=metadata,
        )

    def get_content(self, bucket: str, key: str) -> bytes:
        return self._data_map[bucket][key].data

    def throw_at_next_calls(self, exception: Exception) -> None:
        self._exception = exception

    async def list_buckets(self) -> dict:
        if self._exception:
            raise self._exception
        return {"Buckets": [{"Name": bucket} for bucket in self._data_map]}

    async def close(self) -> None:
        if self._exception:
            raise self._exception

    async def create_bucket(self, Bucket: str) -> None:
        if self._exception:
            raise self._exception
        self._data_map[Bucket] = {}

    async def put_object(self, Body: bytes, Bucket: str, Key: str, Metadata: dict | None = None) -> dict:
        if self._exception:
            raise self._exception

        self.set_content(Bucket, Key, Body)
        return {}

    async def delete_object(self, Bucket: str, Key: str) -> None:
        if self._exception:
            raise self._exception

        self._data_map.get(Bucket, {}).pop(Key)

    async def get_object(self, Bucket: str, Key: str) -> dict:
        if self._exception:
            raise self._exception

        entry = self._data_map.get(Bucket, {}).get(Key)
        if entry is None:
            raise ClientError(error_response={"Error": {"Code": "NoSuchKey"}}, operation_name="get_object")

        return {
            "Body": self._get_data_reader(entry.data),
            "LastModified": entry.LastModified,
            "Key": entry.Key,
            "ContentType": entry.ContentType,
            "Metadata": entry.Metadata,
        }

    async def list_objects(self, Bucket: str) -> dict:
        if self._exception:
            raise self._exception

        return {
            "Contents": [
                {
                    "Body": self._get_data_reader(entry.data),
                    "LastModified": entry.LastModified,
                    "Key": entry.Key,
                    "ContentType": entry.ContentType,
                    "Metadata": entry.Metadata,
                }
                for entry in self._data_map.get(Bucket, {}).values()
            ]
        }

    def get_paginator(self, operation_name: Any) -> Paginator:
        if self._exception:
            raise self._exception

        return Paginator(self._data_map)

    @asynccontextmanager
    async def _get_data_reader(self, data: bytes) -> AsyncIterator[BotocoreClientMock.DataReader]:
        yield BotocoreClientMock.DataReader(data)


@pytest.fixture(name="botocore_client_mock")
def fixture_botocore_client_mock(test_settings: Settings) -> BotocoreClientMock:
    s3_mock = BotocoreClientMock(test_settings.BIM_BUCKET)

    s3_mock.set_content(test_settings.BIM_BUCKET, ARTIFACTS_FRAG_KEY, ARTIFACTS_FRAG_BODY, LAST_MODIFIED)
    s3_mock.set_content(test_settings.BIM_BUCKET, ARTIFACTS_JSON_KEY, ARTIFACTS_JSON_BODY, LAST_MODIFIED)

    return s3_mock


@pytest.fixture
async def s3_client(test_settings: Settings, botocore_client_mock: BotocoreClientMock) -> AsyncIterator[S3Client]:
    client = S3Client(url=test_settings.S3_URI, access_key=test_settings.S3_USER, secret_key=test_settings.S3_PASSWORD)

    with patch("contextlib.AsyncExitStack.enter_async_context", AsyncMock()) as mock_enter_async_context:
        mock_enter_async_context.return_value = botocore_client_mock
        yield client
