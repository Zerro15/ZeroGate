import { FormEvent, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/auth';

export default function LoginPage() {
  const { login, isAuthenticated, isLoading, error } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@local');
  const [password, setPassword] = useState('admin123');
  const [toast, setToast] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated) navigate('/app/dashboard');
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/app/dashboard');
    } catch {
      setToast('Неверный логин или пароль');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="w-full max-w-md rounded-2xl bg-white/95 p-8 shadow-2xl backdrop-blur dark:bg-slate-900/90">
        <div className="mb-6 text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-600 text-xl font-bold text-white">
            ZG
          </div>
          <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-white">ZeroGate Desktop</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Войдите, чтобы управлять безопасным соединением</p>
        </div>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Email</label>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@local"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••"
              required
            />
          </div>
          {toast && <div className="rounded-xl bg-rose-100 p-3 text-sm text-rose-700">{toast}</div>}
          {error && <div className="rounded-xl bg-amber-100 p-3 text-sm text-amber-800">{error}</div>}
          <button type="submit" className="btn-primary w-full" disabled={isLoading}>
            {isLoading ? 'Входим...' : 'Войти'}
          </button>
          <button
            type="button"
            className="btn-ghost w-full justify-center"
            onClick={() => {
              setEmail('demo@zerogate.local');
              setPassword('demo123');
            }}
          >
            Заполнить демо-данные
          </button>
        </form>
      </div>
    </div>
  );
}
