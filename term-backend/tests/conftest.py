from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from service.main import app
from service.settings import Settings


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app, base_url="http://testserver")


@pytest.fixture
def test_settings() -> Settings:
    return Settings()
