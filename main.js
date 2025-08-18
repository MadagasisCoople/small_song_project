const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pythonServer; // Will hold the backend process

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
    }
  });

  // Load your HTML frontend
  win.loadFile('song_project.html');

  win.on('closed', () => {
    // Stop Python backend when window is closed
    if (pythonServer) {
      pythonServer.kill();
    }
  });
}

app.whenReady().then(() => {
  // 🐍 Start the FastAPI backend (make sure fpt.py is correct path)
const fptPath = path.join(__dirname, 'song_project.py');
console.log("Launching backend:", fptPath);

pythonServer = spawn('python', [fptPath], {
  shell: true,
});

pythonServer.stdout.on('data', (data) => {
  console.log(`[PYTHON OUTPUT]: ${data.toString()}`);
});

pythonServer.stderr.on('data', (data) => {
  console.error(`[PYTHON ERROR]: ${data.toString()}`);
});

pythonServer.on('exit', (code) => {
  console.log(`[PYTHON EXITED] Code: ${code}`);
});

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonServer) {
      pythonServer.kill();
    }
    app.quit();
  }
});
