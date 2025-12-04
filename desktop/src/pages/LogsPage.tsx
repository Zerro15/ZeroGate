import LogListItem from '../components/common/LogListItem';
import { useLogs } from '../hooks/useLogs';

export default function LogsPage() {
  const { logs, level, setLevel, search, setSearch, refresh } = useLogs();

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 rounded-2xl bg-white p-4 shadow-sm dark:bg-slate-900">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-xl font-semibold">Logs</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">Последние события клиента</p>
          </div>
          <div className="flex flex-col gap-3 md:flex-row">
            <select
              className="input md:w-40"
              value={level}
              onChange={(e) => setLevel(e.target.value as any)}
            >
              <option value="ALL">Все уровни</option>
              <option value="INFO">INFO</option>
              <option value="WARN">WARN</option>
              <option value="ERROR">ERROR</option>
            </select>
            <input
              className="input md:min-w-[240px]"
              placeholder="Поиск по тексту"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <button className="btn-primary" onClick={refresh}>
              Обновить
            </button>
          </div>
        </div>
      </div>
      <div className="space-y-2">
        {logs.map((log) => (
          <LogListItem key={log.id} entry={log} />
        ))}
      </div>
    </div>
  );
}
