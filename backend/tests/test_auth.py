import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import AsyncSessionLocal, Base, engine
from backend.app.main import app
from backend.app.services.auth import ensure_admin_user


async def setup_db():
    """Create tables and seed admin user."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        await ensure_admin_user(session)


def test_login_and_me_endpoint():
    # Setup: create tables and seed admin
    asyncio.run(setup_db())

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
