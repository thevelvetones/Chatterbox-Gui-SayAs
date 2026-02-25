/**
 * SayAs Electron App - Preload Script
 * 
 * Exposes secure IPC APIs to the renderer process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('sayasAPI', {
  // App paths
  getAppPath: () => ipcRenderer.invoke('get-app-path'),
  getUserDataPath: () => ipcRenderer.invoke('get-user-data-path'),
  getVoicesPath: () => ipcRenderer.invoke('get-voices-path'),
  getPresetsPath: () => ipcRenderer.invoke('get-presets-path'),
  getOutputPath: () => ipcRenderer.invoke('get-output-path'),
  
  // File dialogs
  selectFile: (options) => ipcRenderer.invoke('select-file', options),
  saveFile: (options) => ipcRenderer.invoke('save-file', options),
  
  // Notifications
  showNotification: (message, type) => ipcRenderer.invoke('show-notification', message, type),
  
  // App info
  getVersion: () => ipcRenderer.invoke('get-version'),
  isDev: () => ipcRenderer.invoke('is-dev'),
  
  // Event listeners
  onPythonError: (callback) => {
    ipcRenderer.on('python-error', (event, error) => callback(error));
  },
  onPythonExit: (callback) => {
    ipcRenderer.on('python-exit', (event, code) => callback(code));
  },
  
  // Remove event listeners
  removeAllListeners: () => {
    ipcRenderer.removeAllListeners('python-error');
    ipcRenderer.removeAllListeners('python-exit');
  }
});

// Log preload script loaded
console.log('💕 SayAs Preload Script Loaded');
