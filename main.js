const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let djangoProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        icon: path.join(__dirname, 'icon.ico')
    });

    // Esperar a que Django inicie
    setTimeout(() => {
        mainWindow.loadURL('http://127.0.0.1:8000');
    }, 3000);

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function startDjango() {
    // Iniciar servidor Django
    djangoProcess = spawn('python', ['manage.py', 'runserver', '--noreload'], {
        cwd: __dirname
    });

    djangoProcess.stdout.on('data', (data) => {
        console.log(`Django: ${data}`);
    });

    djangoProcess.stderr.on('data', (data) => {
        console.error(`Django Error: ${data}`);
    });
}

app.on('ready', () => {
    startDjango();
    createWindow();
});

app.on('window-all-closed', function () {
    if (djangoProcess) {
        djangoProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});
