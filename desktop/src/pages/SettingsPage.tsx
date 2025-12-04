import { FormEvent, useState } from 'react';
import { useSettings } from '../store/settings';
import { useStatus } from '../hooks/useStatus';

export default function SettingsPage() {
  const { settings, updateSettings, checkConnection } = useSettings();
  const { refetch } = useStatus();
  const [baseUrl, setBaseUrl] = useState(settings.baseUrl);
  const [message, setMessage] = useState<string | null>(null);

  const handleSave = (e: FormEvent) => {
    e.preventDefault();
    updateSettings({ baseUrl });
    setMessage('Настройки сохранены');
  };

  const handleCheck = async () => {
    try {
      const res = await checkConnection();
      setMessage(`Статус: ${res.status}, версия ${res.version}`);
      refetch();
    } catch (err: any) {
      setMessage(err?.message || 'Не удалось связаться с сервером');
    }
  };

  return (
    <div className="space-y-6">
      <div className="card space-y-4">
        <h1 className="text-xl font-semibold">General</h1>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200">Language</label>
            <select
              className="input mt-1"
              value={settings.language}
              onChange={(e) => updateSettings({ language: e.target.value as any })}
            >
              <option value="en">English</option>
              <option value="ru">Русский</option>
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200">Theme</label>
            <select
              className="input mt-1"
              value={settings.theme}
              onChange={(e) => updateSettings({ theme: e.target.value as any })}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System</option>
            </select>
          </div>
        </div>
      </div>

      <div className="card space-y-4">
        <h2 className="text-xl font-semibold">Connection</h2>
        <div className="flex flex-col gap-3 md:flex-row">
          <label className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
            <input
              type="checkbox"
              checked={settings.autoConnect}
              onChange={(e) => updateSettings({ autoConnect: e.target.checked })}
            />
            Авто-подключение при старте
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
            <input
              type="checkbox"
              checked={settings.killSwitch}
              onChange={(e) => updateSettings({ killSwitch: e.target.checked })}
            />
            Kill-switch (UI only)
          </label>
        </div>
      </div>

      <div className="card space-y-4">
        <h2 className="text-xl font-semibold">Advanced</h2>
        <form className="space-y-4" onSubmit={handleSave}>
          <div>
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200">Backend BASE_URL</label>
            <input
              className="input mt-1"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              placeholder="http://127.0.0.1:8000"
            />
          </div>
          <div className="flex gap-3">
            <button className="btn-primary" type="submit">
              Сохранить
            </button>
            <button className="btn-ghost" type="button" onClick={handleCheck}>
              Проверить соединение
            </button>
          </div>
          {message && <div className="rounded-xl bg-slate-100 p-3 text-sm dark:bg-slate-800">{message}</div>}
        </form>
      </div>
    </div>
  );
}
