import { useStatus } from '../../hooks/useStatus';
import { useAuth } from '../../store/auth';
import { useSettings } from '../../store/settings';

export default function Header() {
  const { data } = useStatus();
  const { logout } = useAuth();
  const { settings, updateSettings } = useSettings();
  const online = data?.status === 'ok';

  const toggleTheme = () => {
    const next = settings.theme === 'dark' ? 'light' : 'dark';
    updateSettings({ theme: next });
  };

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white/80 px-6 py-4 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-semibold">ZeroGate</h1>
        <div
          className={`flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${
            online ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-100' : 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-100'
          }`}
        >
          <span className="h-2 w-2 rounded-full bg-current" />
          {online ? 'Online' : 'Offline'}
        </div>
        {data?.version && (
          <span className="text-xs text-slate-500 dark:text-slate-400">v{data.version}</span>
        )}
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={toggleTheme}
          className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-medium shadow-sm transition hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
        >
          {settings.theme === 'dark' ? 'Light mode' : 'Dark mode'}
        </button>
        <button
          onClick={logout}
          className="rounded-xl border border-red-200 px-3 py-2 text-sm font-medium text-red-700 shadow-sm transition hover:bg-red-50 dark:border-red-700 dark:text-red-200 dark:hover:bg-red-900/40"
        >
          Logout
        </button>
      </div>
    </header>
  );
}
