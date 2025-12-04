"""Simple tests for status endpoint."""
from fastapi.testclient import TestClient

from backend.app.main import app



client = TestClient(app)


def test_status_endpoint_returns_ok():
    """Проверяем, что /api/status отвечает статусом ok."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
