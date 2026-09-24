#!/usr/bin/env node
// Production startup script for 9Router
const { spawn } = require('child_process');
const path = require('path');

const PORT = process.env.PORT || 20128;
const HOST = process.env.HOST || '0.0.0.0';

console.log('Starting 9Router production server...');
console.log(`PORT: ${PORT}`);
console.log(`HOST: ${HOST}`);
console.log(`DATA_DIR: ${process.env.DATA_DIR}`);

// Try to run 9router server directly without tray mode
// Use the CLI with explicit environment to prevent tray detection
const cliPath = path.join('/usr/local/lib/node_modules/9router', 'cli.js');

const child = spawn('node', [
  cliPath,
  '--port', PORT.toString(),
  '--host', HOST,
  '--skip-update',
  '--no-browser',
  '--log'
], {
  stdio: 'inherit',
  env: {
    ...process.env,
    CI: 'true',
    NODE_ENV: 'production',
    // Override display-related environment variables to prevent tray mode
    DISPLAY: undefined,
    WAYLAND_DISPLAY: undefined,
    XDG_SESSION_TYPE: undefined,
    QT_QPA_PLATFORM: undefined,
    // Force headless mode
    ELECTRON_RUN_AS_NODE: '1'
  }
});

child.on('exit', (code) => {
  console.log(`9Router exited with code ${code}`);
  process.exit(code || 1);
});

child.on('error', (err) => {
  console.error('Failed to start 9Router:', err);
  process.exit(1);
});
