import React, { createContext, useContext, useEffect, useState } from 'react';
import client from '../api/client';
import { AuthResponse, User } from '../types';

const TOKEN_KEY = 'zg_token';

let tokenCache: string | null = localStorage.getItem(TOKEN_KEY);

export const getAuthToken = () => tokenCache;

interface AuthContextValue {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(tokenCache);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const persistToken = (nextToken: string | null) => {
    tokenCache = nextToken;
    if (nextToken) localStorage.setItem(TOKEN_KEY, nextToken);
    else localStorage.removeItem(TOKEN_KEY);
    setToken(nextToken);
  };

  const refreshUser = async () => {
    if (!tokenCache) return;
    const res = await client.get<User>('/api/auth/me');
    setUser(res.data);
  };

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);
      const res = await client.post<AuthResponse>('/api/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      persistToken(res.data.access_token);
      await refreshUser();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    persistToken(null);
    setUser(null);
  };

  useEffect(() => {
    // При загрузке пытаемся подтянуть профиль, если токен есть
    if (tokenCache) {
      refreshUser().catch(() => logout());
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated: Boolean(token && user),
        isLoading,
        error,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
