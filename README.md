# ZeroGate

> Учебный безопасный сетевой сервис и кроссплатформенный клиент

## Описание
ZeroGate — учебный проект, который показывает, как связать backend на FastAPI и кроссплатформенный клиент на Flutter. Мы фокусируемся на прозрачной архитектуре, ясных комментариях и легальных сценариях использования: защита данных в публичных сетях, обучение и демонстрации. В проекте нет и не будет функциональности обхода цензуры или блокировок.

Backend предоставляет REST API для управления пользователями, устройствами, профилями подключений и базовой телеметрией. Клиент показывает статус сервера, даёт простой экран авторизации и заготовки экранов для устройств, профилей и логов.

## Архитектура
Проект разделён на два основных блока: backend (FastAPI) и клиенты (Flutter + Electron). Общение идёт через REST API. В качестве хранилища используется SQLite (по умолчанию), а переход на PostgreSQL возможен благодаря SQLAlchemy.

```mermaid
graph TD
    A[Flutter Client] -- JSON/HTTPS --> B[FastAPI Backend]
    B --> C[Service Layer]
    C --> D[(Database)]
    C --> E[External Tunnel Provider]
    B --> F[Telemetry & Logs]
```

## Стек технологий
- Backend: Python 3.11, FastAPI, SQLAlchemy 2.x, Pydantic 2.x, JWT (python-jose), SQLite (по умолчанию)
- Клиент: Flutter, Riverpod, Dio, SharedPreferences
- CI: GitHub Actions (простая основа под pytest)

## Структура репозитория
- `backend/` — исходники FastAPI
- `app/` — Flutter-приложение (Android + Windows)
- `desktop/` — Electron + React + TypeScript клиент для Windows
- `docs/` — дополнительная документация
- `.github/workflows/` — CI
- Корень: README, LICENSE, CONTRIBUTING и т.д.

## Как запустить backend
1. Установите Python 3.11+
2. Создайте виртуальное окружение и активируйте его
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Запустите dev-сервер
   ```bash
   uvicorn app.main:app --reload
   ```
4. Откройте браузер на `http://localhost:8000/docs`

## Как запустить Flutter-клиент
1. Установите Flutter (stable)
2. Установите зависимости
   ```bash
   cd app
   flutter pub get
   ```
3. Запустите
   ```bash
   flutter run -d windows # или -d linux / -d android
   ```
4. В форме логина укажите адрес backend (по умолчанию `http://localhost:8000`) и креды демо-админа `admin@zerogate.local` / `admin`.

## Как запустить десктоп-клиент (Electron + React)
1. Установите Node.js 18+ и npm.
2. Поставьте зависимости:
   ```bash
   cd desktop
   npm install
   ```
3. Запуск в dev-режиме (Vite + Electron):
   ```bash
   npm run electron:dev
   ```
   По умолчанию клиент ходит на `http://127.0.0.1:8000`. Базовый URL можно сменить в настройках UI.
4. Сборка production и .exe:
   ```bash
   npm run build
   npm run electron:build
   ```

## Для кого проект
Проект ориентирован на разработчиков, которые начинают изучать сетевую безопасность и хотят увидеть, как связать backend и мобильный клиент. Код снабжён русскими комментариями и лаконичной архитектурой.

## План развития / Roadmap
- Добавить роли и разграничение доступа в API
- Реализовать историю подключений и статистику трафика
- Поддержка push-уведомлений о статусе устройств
- UI-экран управления профилями и устройствами
- Локализация клиента (ru/en) и темы оформления

## Скриншоты
Плейсхолдеры: добавьте сюда снимки экранов из Flutter-клиента, когда соберёте приложение.
