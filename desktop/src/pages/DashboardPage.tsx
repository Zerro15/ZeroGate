import StatCard from '../components/common/StatCard';
import Sparkline from '../components/common/Sparkline';
import { useStatus } from '../hooks/useStatus';
import { useConnection } from '../hooks/useConnection';
import { useServers } from '../hooks/useServers';

export default function DashboardPage() {
  const { data: status } = useStatus();
  const { connection, connect, disconnect, isLoading } = useConnection();
  const { servers } = useServers();

  const nextServer = servers[0];
  const latencyHistory = [32, 45, 28, 40, 51, 38, 36, 48, 29, 34];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <StatCard
          title="Connection"
          value={connection.connected ? 'Connected' : 'Disconnected'}
          description={connection.server ? connection.server.name : 'Not selected'}
          accent={connection.connected ? 'green' : 'red'}
        />
        <StatCard
          title="Backend"
          value={status?.status === 'ok' ? 'Online' : 'Offline'}
          description={`Version ${status?.version ?? '—'}`}
          accent={status?.status === 'ok' ? 'green' : 'red'}
        />
        <StatCard
          title="Protocol"
          value={status?.network?.protocol ?? 'none'}
          description={`${status?.network?.server_host ?? 'N/A'}:${status?.network?.server_port ?? '—'}`}
          accent="amber"
        />
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="card col-span-2">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-lg font-semibold">Connection status</h2>
            <div className="text-sm text-slate-500 dark:text-slate-400">
              {connection.server ? connection.server.name : 'No server selected'}
            </div>
          </div>
          <div className="flex flex-col gap-4 md:flex-row md:items-center">
            <div className="flex-1 space-y-3">
              <div className="text-3xl font-semibold">
                {connection.connected ? 'Connected' : 'Disconnected'}
              </div>
              <div className="text-sm text-slate-500 dark:text-slate-400">
                Управляйте подключением — здесь позже будет вызов реального API.
              </div>
              <div className="flex gap-3">
                <button
                  className="btn-primary"
                  onClick={() => (connection.connected && connection.server ? disconnect() : connect(nextServer))}
                  disabled={isLoading}
                >
                  {connection.connected ? 'Disconnect' : 'Quick Connect'}
                </button>
                <button
                  className="btn-ghost"
                  onClick={() => connect(nextServer)}
                  disabled={isLoading}
                >
                  Выбрать {nextServer?.name}
                </button>
              </div>
            </div>
            <div className="flex-1 rounded-2xl bg-slate-100 p-4 dark:bg-slate-800">
              <h3 className="text-sm font-medium text-slate-600 dark:text-slate-300">Latency history</h3>
              <Sparkline values={latencyHistory} />
            </div>
          </div>
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold">My IP / Location</h2>
          <div className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
            <div>IP address: 10.0.0.1</div>
            <div>Location: Unknown</div>
            <div className="rounded-lg bg-slate-100 px-3 py-2 text-xs dark:bg-slate-800">
              Здесь можно подключить реальный API, который вернёт геоданные.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
