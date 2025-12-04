from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Создаём объект приложения FastAPI.
# Название проекта будет видно и в /docs, и в нашей HTML-страничке.
app = FastAPI(title="ZeroGate Backend")


@app.get("/api/status")
def get_status() -> dict:
    """Простой эндпоинт для проверки, что сервер работает.

    Здесь мы возвращаем базовую информацию о состоянии сервера:
    - название проекта;
    - статус (ok / error);
    - текущее серверное время в формате ISO.

    Этим эндпоинтом будет пользоваться и мобильное приложение, и браузерный UI.
    """
    return {
        "project": "ZeroGate",
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Простая HTML-дашборда ZeroGate.

    Здесь НЕТ никакого сложного фронтенда.
    Это обычная HTML-страница с чуть-чуть CSS и JavaScript.

    JS-код раз в несколько секунд делает запрос к /api/status
    и обновляет данные на странице.
    Такой подход удобен для учебных проектов: сразу видно,
    как backend и frontend общаются через HTTP/JSON.
    """
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>ZeroGate Dashboard</title>
        <style>
            /* Небольшой минималистичный дизайн, чтобы выглядело как приложение */

            :root {
                color-scheme: dark;
                --bg: #050816;
                --card-bg: #0f172a;
                --accent: #3b82f6;
                --accent-soft: rgba(59,130,246,0.15);
                --text-main: #e5e7eb;
                --text-muted: #9ca3af;
                --border: #1f2933;
                --danger: #f97373;
            }

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                font-family: system-ui, -apple-system, BlinkMacSystemFont,
                    "Segoe UI", sans-serif;
                background: radial-gradient(
                    circle at top,
                    #1e293b 0,
                    var(--bg) 45%,
                    #020617 100%
                );
                color: var(--text-main);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
            }

            .card {
                width: 100%;
                max-width: 720px;
                background: linear-gradient(
                    135deg,
                    rgba(15,23,42,0.96),
                    rgba(15,23,42,0.92)
                );
                border-radius: 24px;
                border: 1px solid rgba(148,163,184,0.25);
                box-shadow:
                    0 18px 40px rgba(15,23,42,0.75),
                    0 0 0 1px rgba(15,23,42,0.8);
                padding: 24px 28px 20px;
                backdrop-filter: blur(22px);
            }

            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 18px;
                gap: 12px;
            }

            .title-block h1 {
                margin: 0;
                font-size: 22px;
                letter-spacing: 0.04em;
            }

            .title-block p {
                margin: 4px 0 0;
                font-size: 13px;
                color: var(--text-muted);
            }

            .pill {
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 12px;
                border: 1px solid rgba(148,163,184,0.5);
                color: var(--text-muted);
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: radial-gradient(
                    circle at top left,
                    rgba(56,189,248,0.12),
                    transparent 45%
                );
            }

            .pill span.dot {
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: #22c55e;
                box-shadow: 0 0 12px rgba(34,197,94,0.9);
            }

            .pill.off span.dot {
                background: var(--danger);
                box-shadow: 0 0 10px rgba(239,68,68,0.8);
            }

            .grid {
                display: grid;
                grid-template-columns: minmax(0, 2fr) minmax(0, 1.3fr);
                gap: 16px;
            }

            .panel {
                border-radius: 18px;
                padding: 14px 16px;
                background: radial-gradient(
                    circle at top left,
                    var(--accent-soft),
                    rgba(15,23,42,0.9)
                );
                border: 1px solid rgba(55,65,81,0.7);
            }

            .panel h2 {
                margin: 0 0 10px;
                font-size: 15px;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: #9ca3ff;
            }

            .label {
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: var(--text-muted);
                margin-bottom: 4px;
            }

            .value-big {
                font-size: 18px;
                font-weight: 600;
            }

            .value {
                font-size: 13px;
            }

            .muted {
                color: var(--text-muted);
                font-size: 12px;
            }

            .row {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                gap: 10px;
                margin-bottom: 6px;
            }

            .row:last-child {
                margin-bottom: 0;
            }

            .footer {
                margin-top: 18px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                font-size: 11px;
                color: var(--text-muted);
            }

            .badge {
                padding: 4px 10px;
                border-radius: 999px;
                background: rgba(15,23,42,0.9);
                border: 1px solid rgba(148,163,184,0.4);
                font-size: 11px;
            }

            .error {
                color: var(--danger);
            }

            @media (max-width: 700px) {
                .card {
                    padding: 18px 16px 16px;
                }
                .grid {
                    grid-template-columns: minmax(0, 1fr);
                }
            }
        </style>
    </head>
    <body>
        <main class="card">
            <header class="header">
                <div class="title-block">
                    <h1>ZeroGate Dashboard</h1>
                    <p>Учебная панель состояния backend-сервера</p>
                </div>
                <div class="pill" id="status-pill">
                    <span class="dot"></span>
                    <span id="status-text">Online</span>
                </div>
            </header>

            <section class="grid">
                <section class="panel">
                    <h2>Server</h2>
                    <div class="row">
                        <div>
                            <div class="label">Project</div>
                            <div class="value-big" id="project-name">—</div>
                        </div>
                        <div class="muted">
                            <span id="status-label">Статус: неизвестно</span>
                        </div>
                    </div>
                    <div class="row">
                        <div>
                            <div class="label">Server time (UTC)</div>
                            <div class="value" id="server-time">—</div>
                        </div>
                        <div class="muted">
                            Обновляется каждые <strong>5&nbsp;секунд</strong>
                        </div>
                    </div>
                </section>

                <section class="panel">
                    <h2>Client</h2>
                    <div class="row">
                        <div>
                            <div class="label">Browser</div>
                            <div class="value" id="client-info">—</div>
                        </div>
                    </div>
                    <div class="row">
                        <div>
                            <div class="label">Last update</div>
                            <div class="value" id="last-update">—</div>
                        </div>
                    </div>
                    <p class="muted" id="error-message"></p>
                </section>
            </section>

            <footer class="footer">
                <div>ZeroGate · локальный учебный стенд (FastAPI + простой HTML/JS)</div>
                <div class="badge">GET /api/status</div>
            </footer>
        </main>

        <script>
            // Эта функция делает запрос к /api/status и обновляет данные на странице.
            async function fetchStatus() {
                const projectEl = document.getElementById("project-name");
                const timeEl = document.getElementById("server-time");
                const lastUpdateEl = document.getElementById("last-update");
                const statusLabelEl = document.getElementById("status-label");
                const statusTextEl = document.getElementById("status-text");
                const pillEl = document.getElementById("status-pill");
                const errorEl = document.getElementById("error-message");

                try {
                    const response = await fetch("/api/status");

                    if (!response.ok) {
                        throw new Error("HTTP " + response.status);
                    }

                    const data = await response.json();

                    projectEl.textContent = data.project ?? "ZeroGate";
                    timeEl.textContent = data.time ?? "—";

                    const status = data.status ?? "unknown";
                    statusLabelEl.textContent = "Статус: " + status;

                    if (status === "ok") {
                        statusTextEl.textContent = "Online";
                        pillEl.classList.remove("off");
                        errorEl.textContent = "";
                    } else {
                        statusTextEl.textContent = "Warning";
                        pillEl.classList.add("off");
                        errorEl.textContent = "Сервер ответил статусом: " + status;
                    }

                    const now = new Date();
                    lastUpdateEl.textContent = now.toLocaleTimeString();

                } catch (error) {
                    // Если сервер недоступен или случилась ошибка, показываем предупреждение.
                    statusTextEl.textContent = "Offline";
                    pillEl.classList.add("off");
                    statusLabelEl.textContent = "Статус: недоступен";
                    errorEl.textContent =
                        "Не удалось получить статус сервера: " + error;
                }
            }

            // Показываем информацию о клиенте (браузере).
            function fillClientInfo() {
                const clientInfoEl = document.getElementById("client-info");
                clientInfoEl.textContent = navigator.userAgent;
            }

            // При загрузке страницы сразу один раз обновляем статус,
            // а потом опрашиваем сервер каждые 5 секунд.
            window.addEventListener("DOMContentLoaded", () => {
                fillClientInfo();
                fetchStatus();
                setInterval(fetchStatus, 5000);
            });
        </script>
    </body>
    </html>
    """
