import { useMemo } from 'react';
import { useAuth } from '../../store/auth';

interface NavItem {
  label: string;
  path: string;
  icon: string;
}

interface Props {
  activePath: string;
  onNavigate: (path: string) => void;
}

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/app/dashboard', icon: '📊' },
  { label: 'Servers', path: '/app/servers', icon: '🛰️' },
  { label: 'Logs', path: '/app/logs', icon: '📜' },
  { label: 'Settings', path: '/app/settings', icon: '⚙️' },
  { label: 'Profile', path: '/app/profile', icon: '👤' },
];

export default function Sidebar({ activePath, onNavigate }: Props) {
  const { user } = useAuth();
  const items = useMemo(() => {
    return navItems;
  }, []);

  return (
    <aside className="flex w-64 flex-col border-r border-slate-200 bg-white/90 p-4 backdrop-blur dark:border-slate-800 dark:bg-slate-900/80">
      <div className="mb-8 flex items-center gap-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary-600 text-lg font-bold text-white shadow">
          ZG
        </div>
        <div>
          <div className="text-lg font-semibold">ZeroGate</div>
          <div className="text-xs text-slate-500 dark:text-slate-400">Desktop Client</div>
        </div>
      </div>
      <nav className="space-y-2">
        {items.map((item) => {
          const active = activePath.startsWith(item.path);
          return (
            <button
              key={item.path}
              onClick={() => onNavigate(item.path)}
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition ${
                active
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
      <div className="mt-auto pt-6 text-xs text-slate-500 dark:text-slate-400">
        {user?.email || 'Guest'}
      </div>
    </aside>
  );
}
