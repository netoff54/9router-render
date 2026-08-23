#!/usr/bin/env node
// Starter 9Router — memakai data dari folder workspace (9router-data)
// Cross-platform: bekerja di Windows, macOS, Linux.
const path = require("path");
const { spawn } = require("child_process");

const workspaceDir = __dirname;
const dataDir = path.join(workspaceDir, "9router-data");

// Arahkan data ke folder workspace
process.env.DATA_DIR = dataDir;

console.log("");
console.log("==================================================");
console.log("  9Router — Data dari workspace");
console.log(`  DATA_DIR: ${dataDir}`);
console.log("==================================================");
console.log("");

// Jalankan CLI 9router dari node_modules lokal
const cliPath = path.join(workspaceDir, "node_modules", "9router", "cli.js");
const args = process.argv.slice(2);

const child = spawn(process.execPath, ["--dns-result-order=ipv4first", cliPath, ...args], {
  stdio: "inherit",
  windowsHide: false,
});

child.on("exit", (code, signal) => {
  process.exit(signal ? 1 : code);
});