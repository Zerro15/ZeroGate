import React, { createContext, useContext, useEffect, useState } from 'react';
import { AppSettings } from '../types';
import client from '../api/client';
import { StatusResponse } from '../types';

const DEFAULT_BASE_URL = 'http://127.0.0.1:8000';
const SETTINGS_KEY = 'zg_settings';

const defaultSettings: AppSettings = {
  theme: 'system',
  language: 'en',
  autoConnect: false,
  killSwitch: false,
  baseUrl: DEFAULT_BASE_URL,
};

let cachedSettings: AppSettings = { ...defaultSettings, ...loadSettings() };

function loadSettings(): Partial<AppSettings> {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (raw) return JSON.parse(raw) as AppSettings;
  } catch (err) {
    console.warn('Failed to read settings from storage', err);
  }
  return {};
}

function persistSettings(settings: AppSettings) {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch (err) {
    console.warn('Failed to store settings', err);
  }
}

export const getBaseUrl = () => cachedSettings.baseUrl;

interface SettingsContextValue {
  settings: AppSettings;
  setSettings: (next: AppSettings) => void;
  updateSettings: (partial: Partial<AppSettings>) => void;
  checkConnection: () => Promise<StatusResponse>;
}

const SettingsContext = createContext<SettingsContextValue | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettingsState] = useState<AppSettings>(cachedSettings);

  const setSettings = (next: AppSettings) => {
    cachedSettings = next;
    persistSettings(next);
    setSettingsState(next);
    // Переключаем класс для тёмной темы
    if (next.theme === 'dark') document.body.classList.add('dark');
    else document.body.classList.remove('dark');
  };

  const updateSettings = (partial: Partial<AppSettings>) => {
    setSettings({ ...settings, ...partial });
  };

  useEffect(() => {
    // Инициализируем тему при старте
    if (settings.theme === 'dark') document.body.classList.add('dark');
  }, []);

  const checkConnection = async () => {
    const response = await client.get<StatusResponse>('/api/status');
    return response.data;
  };

  return (
    <SettingsContext.Provider value={{ settings, setSettings, updateSettings, checkConnection }}>
      {children}
    </SettingsContext.Provider>
  );
};

export const useSettings = () => {
  const ctx = useContext(SettingsContext);
  if (!ctx) throw new Error('useSettings must be used within SettingsProvider');
  return ctx;
};
