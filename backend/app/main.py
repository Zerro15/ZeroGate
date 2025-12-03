"""FastAPI entrypoint for ZerroGate backend."""
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, devices, logs, profiles, status as status_route
from app.core.config import settings
from app.db.session import Base, engine, get_session
from app.services.auth import ensure_admin_user

app = FastAPI(title=settings.app_name, version=settings.version)

# Настраиваем CORS так, чтобы мобильное приложение могло обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status_route.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(devices.router, prefix="/api")
app.include_router(profiles.router, prefix="/api")
app.include_router(logs.router, prefix="/api")


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database and demo admin user."""
    # Комментарий: для простоты создаем таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Создаем демо-админа, чтобы можно было сразу логиниться
    async for session in get_session():
        await ensure_admin_user(session)
        break


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Friendly root endpoint."""
    return {"message": "ZerroGate backend is running", "docs": "/docs"}
