from fastapi.testclient import TestClient
from backend.app.main import app


def test_login_and_me_endpoint():
    client = TestClient(app)

    # Login via form (OAuth2 password flow)
    resp = client.post(
        "/api/auth/login",
        data={"username": "admin@local", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data

    token = data["access_token"]

    # Call /me
    resp2 = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200, resp2.text
    me = resp2.json()
    assert me.get("email") == "admin@local"
