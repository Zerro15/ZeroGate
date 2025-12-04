import { contextBridge } from 'electron';

// Простая заглушка для будущих безопасных мостов между main и renderer
contextBridge.exposeInMainWorld('zerogate', {
  // В будущем можно добавить методы для работы с нативными API
});
