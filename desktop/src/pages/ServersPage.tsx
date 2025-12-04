import ServerCard from '../components/common/ServerCard';
import { useConnection } from '../hooks/useConnection';
import { useServers } from '../hooks/useServers';

export default function ServersPage() {
  const { servers, search, setSearch, statusFilter, setStatusFilter, toggleFavorite } = useServers();
  const { connect, connection } = useConnection();

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 rounded-2xl bg-white p-4 shadow-sm dark:bg-slate-900">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-xl font-semibold">Servers</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">Выберите сервер для подключения</p>
          </div>
          <div className="flex flex-col gap-3 md:flex-row">
            <input
              className="input md:min-w-[240px]"
              placeholder="Поиск по имени, стране или городу"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <select
              className="input md:w-48"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
            >
              <option value="all">Все</option>
              <option value="online">Online</option>
              <option value="offline">Offline</option>
            </select>
          </div>
        </div>
      </div>
      <div className="space-y-3">
        {servers.map((srv) => (
          <ServerCard
            key={srv.id}
            server={srv}
            onFavorite={toggleFavorite}
            onConnect={connect}
          />
        ))}
        {servers.length === 0 && (
          <div className="rounded-xl border border-slate-200 p-6 text-center text-sm text-slate-500 dark:border-slate-800 dark:text-slate-400">
            Ничего не найдено по текущим фильтрам
          </div>
        )}
      </div>
      {connection.connected && connection.server && (
        <div className="card border border-green-200 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-900/40 dark:text-green-100">
          Подключены к {connection.server.name}
        </div>
      )}
    </div>
  );
}
