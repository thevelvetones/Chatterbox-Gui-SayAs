/**
 * SayAs Electron App - Main Process
 * 
 * Handles:
 * - Window creation
 * - Python backend management
 * - IPC communication
 */

const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const log = require('electron-log');

// Configure logging
log.transports.file.level = 'info';
log.info('SayAs Electron App starting...');

// Global references
let mainWindow = null;
let pythonWebuiProcess = null;
let pythonApiProcess = null;
let apiPort = 8765;
let webuiPort = 7860;

// Get paths
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
// In dev mode, use the known project root path
const appPath = isDev 
  ? 'C:\\Users\\User\\.qwen\\projects\\SayAs'  // Project root
  : path.dirname(app.getPath('exe'));

const pythonPath = isDev
  ? path.join(appPath, 'venv', 'Scripts', 'python.exe')
  : path.join(process.resourcesPath, 'python', 'venv', 'Scripts', 'python.exe');

const webuiScript = path.join(appPath, 'src', 'webui.py');

// Log for debugging
console.log('DEBUG: __dirname =', __dirname);
console.log('DEBUG: appPath =', appPath);
console.log('DEBUG: pythonPath =', pythonPath);
console.log('DEBUG: webuiScript =', webuiScript);

// User data paths
const userDataPath = app.getPath('userData');
const voicesDir = path.join(userDataPath, 'voices');
const presetsDir = path.join(userDataPath, 'presets');
const outputDir = path.join(userDataPath, 'output');

// Ensure directories exist
[voicesDir, presetsDir, outputDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    log.info(`Created directory: ${dir}`);
  }
});

function createWindow() {
  log.info('Creating main window...');
  
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    title: 'SayAs TTS - LUDICUS OVERKILL Edition',
    icon: path.join(__dirname, '../../assets/icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, '../preload/preload.js')
    },
    backgroundColor: '#fce4ec',
    show: false,
    frame: true,
    titleBarStyle: 'default'
  });

  // Load the WebUI URL
  const webuiUrl = `http://localhost:${webuiPort}`;
  log.info(`Loading WebUI: ${webuiUrl}`);
  
  mainWindow.loadURL(webuiUrl);

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
    log.info('Window ready and shown');
  });

  // Handle window close
  mainWindow.on('closed', () => {
    log.info('Main window closed');
    mainWindow = null;
  });

  // Open DevTools in development
  if (isDev && mainWindow && mainWindow.webContents) {
    mainWindow.webContents.devTools = true;
    // mainWindow.webContents.openDevTools();
  }
}

function startPythonBackend() {
  return new Promise((resolve, reject) => {
    log.info('Starting Python backends (API + WebUI)...');
    log.info(`App path: ${appPath}`);
    log.info(`Python path: ${pythonPath}`);
    log.info(`WebUI script: ${webuiScript}`);
    
    // Check if python exists
    const fs = require('fs');
    if (!fs.existsSync(pythonPath)) {
      const errorMsg = `Python not found at: ${pythonPath}`;
      log.error(errorMsg);
      reject(new Error(errorMsg));
      return;
    }
    
    if (!fs.existsSync(webuiScript)) {
      const errorMsg = `WebUI script not found at: ${webuiScript}`;
      log.error(errorMsg);
      reject(new Error(errorMsg));
      return;
    }

    // Set environment variables
    const env = {
      ...process.env,
      PYTHONUNBUFFERED: '1',
      PYTHONUTF8: '1',
      PYTHONIOENCODING: 'utf-8',
      PATH: `${process.env.PATH};C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin`
    };

    // Start API server first
    const apiScript = path.join(appPath, 'src', 'api.py');
    if (fs.existsSync(apiScript)) {
      log.info('Spawning API server...');
      pythonApiProcess = spawn(pythonPath, [apiScript], {
        env,
        cwd: appPath,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      pythonApiProcess.stdout.on('data', (data) => {
        const output = data.toString();
        log.info(`API: ${output}`);
      });

      pythonApiProcess.stderr.on('data', (data) => {
        const error = data.toString();
        log.info(`API: ${error}`);  // Log warnings as info
      });

      pythonApiProcess.on('error', (error) => {
        log.error(`API server error: ${error.message}`);
      });

      pythonApiProcess.on('exit', (code, signal) => {
        log.info(`API server exited with code: ${code}, signal: ${signal}`);
      });
    }

    // Spawn WebUI process
    log.info('Spawning WebUI process...');
    pythonWebuiProcess = spawn(pythonPath, [webuiScript], {
      env,
      cwd: appPath,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let started = false;

    pythonWebuiProcess.stdout.on('data', (data) => {
      const output = data.toString();
      log.info(`WebUI: ${output}`);
      
      // Check if WebUI is ready
      if (output.includes('http://localhost:7860') && !started) {
        started = true;
        log.info('Python WebUI started successfully!');
        resolve(true);
      }
    });

    pythonWebuiProcess.stderr.on('data', (data) => {
      const error = data.toString();
      log.info(`WebUI: ${error}`);  // Log warnings as info
      
      // Send error to renderer
      if (mainWindow) {
        mainWindow.webContents.send('python-error', error);
      }
    });

    pythonWebuiProcess.on('error', (error) => {
      log.error(`Failed to start WebUI: ${error.message}`);
      log.error(`Error code: ${error.code}`);
      log.error(`Error syscall: ${error.syscall}`);
      reject(error);
    });

    pythonWebuiProcess.on('exit', (code, signal) => {
      log.info(`WebUI exited with code: ${code}, signal: ${signal}`);
      if (mainWindow) {
        mainWindow.webContents.send('python-exit', code);
      }
      if (!started) {
        reject(new Error(`WebUI exited with code ${code} before starting`));
      }
    });

    // Timeout after 90 seconds (API + WebUI need time to load models)
    setTimeout(() => {
      if (!started) {
        const errorMsg = 'Python backend failed to start within 90 seconds';
        log.error(errorMsg);
        reject(new Error(errorMsg));
      }
    }, 90000);
  });
}

function stopPythonBackend() {
  if (pythonApiProcess) {
    log.info('Stopping API server...');
    pythonApiProcess.kill('SIGTERM');
    pythonApiProcess = null;
  }
  if (pythonWebuiProcess) {
    log.info('Stopping WebUI...');
    pythonWebuiProcess.kill('SIGTERM');
    pythonWebuiProcess = null;
  }
}

// App lifecycle
app.whenReady().then(async () => {
  log.info('App ready, starting backend...');
  
  try {
    await startPythonBackend();
    createWindow();
  } catch (error) {
    log.error(`Failed to start app: ${error.message}`);
    dialog.showErrorBox(
      'Startup Error',
      `Failed to start SayAs TTS:\n${error.message}\n\nPlease ensure Python and dependencies are installed correctly.`
    );
    app.quit();
  }
});

app.on('window-all-closed', () => {
  log.info('All windows closed, cleaning up...');
  stopPythonBackend();
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

app.on('before-quit', () => {
  log.info('App quitting, stopping Python backend...');
  stopPythonBackend();
});

// IPC Handlers
ipcMain.handle('get-app-path', () => {
  return appPath;
});

ipcMain.handle('get-user-data-path', () => {
  return userDataPath;
});

ipcMain.handle('get-voices-path', () => {
  return voicesDir;
});

ipcMain.handle('get-presets-path', () => {
  return presetsDir;
});

ipcMain.handle('get-output-path', () => {
  return outputDir;
});

ipcMain.handle('select-file', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options);
  return result;
});

ipcMain.handle('save-file', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options);
  return result;
});

ipcMain.handle('show-notification', (event, message, type = 'info') => {
  log.info(`Notification: ${message}`);
  // Could use native notifications here
  return true;
});

ipcMain.handle('get-version', () => {
  return app.getVersion();
});

ipcMain.handle('is-dev', () => {
  return isDev;
});

log.info('SayAs Electron App initialized');
