export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  full_name?: string | null;
}

export interface StatusResponse {
  status: string;
  project: string;
  version: string;
  time: string;
  network?: {
    protocol?: string;
    server_host?: string;
    server_port?: number;
  };
}

export interface Server {
  id: string;
  name: string;
  country: string;
  city: string;
  ping: number;
  load: number;
  status: 'online' | 'offline';
  favorite?: boolean;
}

export interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR';
  message: string;
}

export interface ConnectionState {
  connected: boolean;
  server?: Server;
}

export interface AppSettings {
  theme: 'light' | 'dark' | 'system';
  language: 'en' | 'ru';
  autoConnect: boolean;
  killSwitch: boolean;
  baseUrl: string;
}
