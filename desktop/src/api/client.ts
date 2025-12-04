import axios from 'axios';
import { getAuthToken } from '../store/auth';
import { getBaseUrl } from '../store/settings';

const client = axios.create({
  baseURL: getBaseUrl(),
  timeout: 10000,
});

client.interceptors.request.use((config) => {
  // Динамически подставляем baseURL, чтобы учитывать изменения настроек
  config.baseURL = getBaseUrl();
  const token = getAuthToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Будущий хук для глобального логаута можно повесить здесь
      console.warn('Unauthorized, token may be invalid.');
    }
    return Promise.reject(error);
  }
);

export default client;
