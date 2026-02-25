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
let pythonProcess = null;
let apiPort = 8765;
let webuiPort = 7860;

// Get paths
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;
const appPath = isDev 
  ? path.join(__dirname, '../../..') 
  : path.dirname(app.getPath('exe'));

const pythonPath = isDev
  ? path.join(appPath, 'venv', 'Scripts', 'python.exe')
  : path.join(process.resourcesPath, 'python', 'venv', 'Scripts', 'python.exe');

const webuiScript = path.join(appPath, 'src', 'webui.py');

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
  if (isDev) {
    mainWindow.webPreferences.devTools = true;
    // mainWindow.webContents.openDevTools();
  }
}

function startPythonBackend() {
  return new Promise((resolve, reject) => {
    log.info('Starting Python WebUI backend...');
    log.info(`Python path: ${pythonPath}`);
    log.info(`WebUI script: ${webuiScript}`);

    // Set environment variables
    const env = {
      ...process.env,
      PYTHONUNBUFFERED: '1',
      PATH: `${process.env.PATH};C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\bin`
    };

    // Spawn Python process
    pythonProcess = spawn(pythonPath, [webuiScript], {
      env,
      cwd: appPath,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let started = false;

    pythonProcess.stdout.on('data', (data) => {
      const output = data.toString();
      log.info(`Python: ${output}`);
      
      // Check if WebUI is ready
      if (output.includes('http://localhost:7860') && !started) {
        started = true;
        log.info('Python WebUI started successfully!');
        resolve(true);
      }
    });

    pythonProcess.stderr.on('data', (data) => {
      const error = data.toString();
      log.error(`Python Error: ${error}`);
      
      // Send error to renderer
      if (mainWindow) {
        mainWindow.webContents.send('python-error', error);
      }
    });

    pythonProcess.on('error', (error) => {
      log.error(`Failed to start Python: ${error.message}`);
      reject(error);
    });

    pythonProcess.on('exit', (code) => {
      log.info(`Python process exited with code: ${code}`);
      if (mainWindow) {
        mainWindow.webContents.send('python-exit', code);
      }
    });

    // Timeout after 60 seconds
    setTimeout(() => {
      if (!started) {
        reject(new Error('Python backend failed to start within 60 seconds'));
      }
    }, 60000);
  });
}

function stopPythonBackend() {
  if (pythonProcess) {
    log.info('Stopping Python backend...');
    pythonProcess.kill('SIGTERM');
    pythonProcess = null;
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
