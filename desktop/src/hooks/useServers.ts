import { useMemo, useState } from 'react';
import { Server } from '../types';

const baseServers: Server[] = [
  { id: '1', name: 'Frankfurt-01', country: 'Germany', city: 'Frankfurt', ping: 22, load: 35, status: 'online' },
  { id: '2', name: 'New York-Edge', country: 'USA', city: 'New York', ping: 95, load: 65, status: 'online' },
  { id: '3', name: 'Tokyo-Core', country: 'Japan', city: 'Tokyo', ping: 180, load: 40, status: 'online' },
  { id: '4', name: 'Sydney-POP', country: 'Australia', city: 'Sydney', ping: 240, load: 55, status: 'offline' },
  { id: '5', name: 'London-Cloud', country: 'UK', city: 'London', ping: 40, load: 20, status: 'online' },
];

export const useServers = () => {
  const [servers, setServers] = useState<Server[]>(baseServers);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'online' | 'offline'>('all');

  const filtered = useMemo(() => {
    return servers.filter((srv) => {
      const matchesSearch = `${srv.name} ${srv.country} ${srv.city}`
        .toLowerCase()
        .includes(search.toLowerCase());
      const matchesStatus = statusFilter === 'all' ? true : srv.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  }, [servers, search, statusFilter]);

  const toggleFavorite = (id: string) => {
    setServers((prev) =>
      prev.map((s) => (s.id === id ? { ...s, favorite: !s.favorite } : s))
    );
  };

  return {
    servers: filtered,
    search,
    setSearch,
    statusFilter,
    setStatusFilter,
    toggleFavorite,
    setServers,
  };
};
