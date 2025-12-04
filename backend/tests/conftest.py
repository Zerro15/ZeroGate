# backend/tests/conftest.py
"""
Настройка пути для pytest, чтобы он видел пакеты проекта.

pytest запускается так, что иногда корень проекта не оказывается в sys.path,
из-за этого импорт `from backend.app.main import app` падает с ModuleNotFoundError.

Этот файл добавляет корень репозитория в sys.path перед запуском тестов.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
