from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND


def test_health(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"status": "Ok"}


def test_nonexistent_endpoint(test_client: TestClient) -> None:
    response = test_client.get("/nonexistent_endpoint")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}
