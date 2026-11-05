// 电子中阮 (Electronic Zhongruan) — Electron 桌面端入口
// Copyright (c) 2026 Zhongruan
// SPDX-License-Identifier: Apache-2.0 OR GPL-3.0-or-later

const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');

let mainWindow = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 950,
    height: 820,
    minWidth: 800,
    minHeight: 700,
    title: '电子中阮',
    icon: path.join(__dirname, 'icon.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true
    }
  });

  // 加载本地 HTML 文件
  mainWindow.loadFile(path.join(__dirname, 'zhongruan.html'));

  // 隐藏菜单栏（更像原生应用）
  Menu.setApplicationMenu(null);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
