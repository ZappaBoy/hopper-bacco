from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/api/v1/health/check")
    assert response.status_code == 200
    data = response.json()
    assert data == {"detail": "alive"}
