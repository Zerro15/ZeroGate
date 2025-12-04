"""Точка входа приложения FastAPI для ZeroGate."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from backend.app.api.routes import auth, devices, logs, profiles, status, users
from backend.app.core.config import settings
from backend.app.db.base import Base
from backend.app.db.session import async_session_maker, engine
from backend.app.models import device, log_entry, profile, user  # noqa: F401
from backend.app.schemas.user import UserCreate
from backend.app.services.user_service import UserService


@asynccontextmanager
def lifespan(app: FastAPI):
    """Создаём таблицы и сидим админов при старте."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        service = UserService(session)
        existing = await service.get_by_email(settings.ADMIN_EMAIL)
        if not existing:
            await service.create(
                user_in=UserCreate(email=settings.ADMIN_EMAIL, password=settings.ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
            )
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = settings.API_V1_PREFIX
app.include_router(status.router, prefix=api_prefix, tags=["status"])
app.include_router(auth.router, prefix=api_prefix, tags=["auth"])
app.include_router(users.router, prefix=api_prefix, tags=["users"])
app.include_router(devices.router, prefix=api_prefix, tags=["devices"])
app.include_router(profiles.router, prefix=api_prefix, tags=["profiles"])
app.include_router(logs.router, prefix=api_prefix, tags=["logs"])


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    """Простой дашборд: проверяем статус и показываем базовую информацию."""

    return f"""
    <!doctype html>
    <html lang='ru'>
    <head>
      <meta charset='utf-8'/>
      <title>{settings.PROJECT_NAME} status</title>
      <style>
        body {{ font-family: Arial, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; padding:2rem; }}
        .card {{ background:#1e293b; border-radius:12px; padding:1.5rem; box-shadow:0 10px 25px rgba(0,0,0,0.35); max-width:640px; }}
        h1 {{ margin-top:0; margin-bottom:0.5rem; }}
        .status-ok {{ color:#22c55e; font-weight:700; }}
        .muted {{ color:#94a3b8; font-size:0.95rem; }}
      </style>
    </head>
    <body>
      <div class="card">
        <h1>{settings.PROJECT_NAME}</h1>
        <p id="version" class="muted">Загрузка версии...</p>
        <p>Статус: <span id="status" class="status-ok">—</span></p>
        <p class="muted" id="time">—</p>
      </div>
      <script>
        async function loadStatus() {{
          try {{
            const response = await fetch('{settings.API_V1_PREFIX}/status');
            const data = await response.json();
            document.getElementById('version').textContent = `Версия: ${'{'}data.version{'}'}`;
            document.getElementById('status').textContent = data.status;
            document.getElementById('time').textContent = `UTC: ${'{'}data.time{'}'}`;
          }} catch (e) {{
            document.getElementById('status').textContent = 'offline';
            document.getElementById('time').textContent = 'Не удалось получить статус';
          }}
        }}
        loadStatus();
        setInterval(loadStatus, 5000);
      </script>
    </body>
    </html>
    """
