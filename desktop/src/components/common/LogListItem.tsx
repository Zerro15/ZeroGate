import { LogEntry } from '../../types';

interface Props {
  entry: LogEntry;
}

const levelColors: Record<LogEntry['level'], string> = {
  INFO: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-100',
  WARN: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-100',
  ERROR: 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-100',
};

export default function LogListItem({ entry }: Props) {
  return (
    <div className="flex items-start justify-between rounded-xl border border-slate-200/80 bg-white px-4 py-3 text-sm shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div>
        <div className="font-medium text-slate-800 dark:text-slate-100">{entry.message}</div>
        <div className="text-xs text-slate-500 dark:text-slate-400">{new Date(entry.timestamp).toLocaleString()}</div>
      </div>
      <span className={`rounded-full px-3 py-1 text-xs font-semibold ${levelColors[entry.level]}`}>{entry.level}</span>
    </div>
  );
}
