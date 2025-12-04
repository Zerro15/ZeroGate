import { useAuth } from '../store/auth';

export default function ProfilePage() {
  const { user, refreshUser, logout } = useAuth();

  return (
    <div className="space-y-4">
      <div className="card space-y-3">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold">Profile</h1>
          <button className="btn-ghost" onClick={refreshUser}>
            Refresh
          </button>
        </div>
        <div className="space-y-2 text-sm text-slate-700 dark:text-slate-200">
          <div>Email: {user?.email}</div>
          <div>Active: {user?.is_active ? 'Yes' : 'No'}</div>
          <div>Role: {user?.is_admin ? 'Admin' : 'User'}</div>
        </div>
        <div className="rounded-xl bg-slate-100 p-3 text-xs text-slate-500 dark:bg-slate-800 dark:text-slate-300">
          Здесь можно будет добавить смену пароля и включение 2FA.
        </div>
        <button className="btn-primary" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}
