import { useQuery } from '@tanstack/react-query';
import client from '../api/client';
import { StatusResponse } from '../types';

export const useStatus = () => {
  return useQuery({
    queryKey: ['status'],
    queryFn: async () => {
      const res = await client.get<StatusResponse>('/api/status');
      return res.data;
    },
    refetchInterval: 30_000,
  });
};
