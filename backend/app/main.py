from fastapi import FastAPI

from backend.app.api.routes import auth as auth_routes

app = FastAPI(title="ZerroGate Backend")

# Include auth router
app.include_router(auth_routes.router)


@app.get("/api/status")
def get_status() -> dict:
    """Простой эндпоинт для проверки, что сервер работает."""
    return {
        "project": "ZeroGate",
        "status": "ok",
        "version": "0.1.0",
    }
