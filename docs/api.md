# API ZeroGate (черновик)

## `/api/status` GET
- Ответ: `{ "project": "ZeroGate", "status": "ok", "timestamp": "..." }`

## `/api/auth/login` POST (form)
- Параметры: `username`, `password`
- Ответ: `{ "access_token": "<jwt>", "token_type": "bearer" }`

## `/api/auth/logout` POST
- Заглушка, клиент забывает токен.

## `/api/users/me` GET
- Заголовок: `Authorization: Bearer <token>`
- Ответ: данные пользователя

## `/api/devices`
- `GET /api/devices` — список устройств текущего пользователя
- `POST /api/devices` — создать устройство
- `PATCH /api/devices/{id}` — обновить имя/статус
- `DELETE /api/devices/{id}` — удалить

## `/api/profiles`
- Аналогичные CRUD-эндпоинты для профилей подключений

## `/api/logs`
- `GET /api/logs/recent` — последние события
- `GET /api/logs/device/{id}` — логи конкретного устройства

> Примечание: Эндпоинты защищены JWT, кроме `/api/status` и `/api/auth/*`.
