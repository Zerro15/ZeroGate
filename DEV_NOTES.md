В VS Code:

В проводнике слева: New File → DEV_NOTES.md

Вставь туда это (можешь прям копипаст + чуть под себя подправить):

# ZeroGate — шпаргалка разработчика

## Как открыть проект и запустить backend

1. Открыть WSL (Ubuntu).
2. Перейти в папку проекта:
   ```bash
   cd /mnt/c/Users/Mashenin_Bogdan/Workshop/Project/GitHub/ZeroGate/ZeroGate


Активировать виртуальное окружение:

source .venv/bin/activate


Запустить сервер:

python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000


Открыть в браузере:

http://localhost:8000/

— ZeroGate Dashboard

http://localhost:8000/api/status

— JSON-статус

http://localhost:8000/docs

— Swagger UI

Как остановить сервер

В терминале, где запущен uvicorn:

Ctrl + C