import { useMemo, useState } from 'react';
import { LogEntry } from '../types';

const mockLogs: LogEntry[] = Array.from({ length: 18 }).map((_, idx) => ({
  id: `${idx}`,
  timestamp: new Date(Date.now() - idx * 10 * 60 * 1000).toISOString(),
  level: idx % 3 === 0 ? 'ERROR' : idx % 2 === 0 ? 'WARN' : 'INFO',
  message: `Sample log message #${idx}`,
}));

export const useLogs = () => {
  const [logs, setLogs] = useState<LogEntry[]>(mockLogs);
  const [search, setSearch] = useState('');
  const [level, setLevel] = useState<'ALL' | 'INFO' | 'WARN' | 'ERROR'>('ALL');

  const filtered = useMemo(() => {
    return logs.filter((log) => {
      const matchesLevel = level === 'ALL' ? true : log.level === level;
      const matchesSearch = log.message.toLowerCase().includes(search.toLowerCase());
      return matchesLevel && matchesSearch;
    });
  }, [logs, search, level]);

  const refresh = () => {
    // Позже здесь будет вызов реального API /api/logs
    setLogs([...mockLogs]);
  };

  return { logs: filtered, setLogs, search, setSearch, level, setLevel, refresh };
};
