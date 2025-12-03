from fastapi import FastAPI

# Создаём объект приложения FastAPI.
# Комментарии пишем по-русски, чтобы новичку было понятно.
app = FastAPI(title="ZerroGate Backend")


@app.get("/api/status")
def get_status() -> dict:
    """Простой эндпоинт для проверки, что сервер работает.

    Возвращаем просто словарь с текстом.
    Это удобно, чтобы мобильное приложение могло проверить соединение.
    """
    return {
        "project": "ZerroGate",
        "status": "ok",
    }
