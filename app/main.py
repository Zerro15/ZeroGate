"""Proxy to reuse backend FastAPI application for pytest imports."""
from backend.app.main import app  # noqa: F401
