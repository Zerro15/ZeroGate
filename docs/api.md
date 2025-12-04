# API ZerroGate (черновик)

## `/api/status` GET
- Ответ: `{ "status": "ok", "version": "0.1.0", "timestamp": "..." }`

## `/api/auth/login` POST (form)
- Параметры: `username`, `password`
- Ответ: `{ "access_token": "<jwt>", "token_type": "bearer" }`

## `/api/auth/demo-login` POST (json)
- Тело: `{ "email": "admin@zerrogate.local", "password": "admin" }`
- Ответ: токен как выше

## `/api/auth/me` GET
- Заголовок: `Authorization: Bearer <token>`
- Ответ: данные пользователя

## `/api/devices`
- `GET /api/devices/` — список устройств текущего пользователя
- `POST /api/devices/` — создать устройство
- `PATCH /api/devices/{id}` — обновить имя/статус
- `DELETE /api/devices/{id}` — удалить

## `/api/profiles`
- Аналогичные CRUD-эндпоинты для профилей подключений

## `/api/logs`
- `GET /api/logs/recent` — последние события
- `GET /api/logs/device/{id}` — логи конкретного устройства
- `POST /api/logs/` — создать запись (например, при подключении или ошибке)

> Примечание: Эндпоинты защищены JWT, кроме `/api/status` и `/api/auth/*`.
