import { Server } from '../../types';

interface Props {
  server: Server;
  onConnect: (server: Server) => void;
  onFavorite: (id: string) => void;
}

export default function ServerCard({ server, onConnect, onFavorite }: Props) {
  return (
    <div className="card flex items-center justify-between gap-4">
      <div>
        <div className="flex items-center gap-2 text-lg font-semibold">
          <span>{server.name}</span>
          {server.status === 'online' ? (
            <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-700 dark:bg-green-900/50 dark:text-green-100">
              Online
            </span>
          ) : (
            <span className="rounded-full bg-rose-100 px-2 py-1 text-xs font-semibold text-rose-700 dark:bg-rose-900/50 dark:text-rose-100">
              Offline
            </span>
          )}
        </div>
        <div className="text-sm text-slate-500 dark:text-slate-400">
          {server.country} · {server.city}
        </div>
        <div className="mt-2 flex gap-3 text-xs text-slate-600 dark:text-slate-300">
          <span>Ping: {server.ping} ms</span>
          <span>Load: {server.load}%</span>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={() => onFavorite(server.id)}
          className={`rounded-full px-3 py-2 text-sm font-medium shadow-sm transition ${
            server.favorite
              ? 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-50'
              : 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200'
          }`}
        >
          {server.favorite ? '★ Favorite' : '☆ Favorite'}
        </button>
        <button
          className="btn-primary"
          onClick={() => onConnect(server)}
          disabled={server.status !== 'online'}
        >
          Connect
        </button>
      </div>
    </div>
  );
}
