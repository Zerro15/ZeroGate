import { app, BrowserWindow, nativeTheme } from 'electron';
import path from 'path';

const isDev = process.env.VITE_DEV_SERVER_URL !== undefined;

function createWindow(): void {
  // Создаём окно Electron и подсовываем в него либо dev server, либо собранный index.html
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    title: 'ZeroGate',
    autoHideMenuBar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (isDev && process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL);
    win.webContents.openDevTools({ mode: 'detach' });
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });

  // Переключаем тему приложения под системную
  nativeTheme.themeSource = 'system';
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
