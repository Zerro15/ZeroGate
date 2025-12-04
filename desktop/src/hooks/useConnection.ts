import { useState } from 'react';
import { ConnectionState, Server } from '../types';

export const useConnection = () => {
  const [connection, setConnection] = useState<ConnectionState>({ connected: false });
  const [isLoading, setLoading] = useState(false);

  const connect = async (server: Server) => {
    setLoading(true);
    // Здесь можно будет вызвать реальный API /api/vpn/connect
    await new Promise((resolve) => setTimeout(resolve, 600));
    setConnection({ connected: true, server });
    setLoading(false);
  };

  const disconnect = async () => {
    setLoading(true);
    // Здесь можно будет вызвать реальный API /api/vpn/disconnect
    await new Promise((resolve) => setTimeout(resolve, 400));
    setConnection({ connected: false });
    setLoading(false);
  };

  return { connection, connect, disconnect, isLoading };
};
