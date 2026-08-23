# ============================================================
#  Stop 9Router (manual)
#  - Mematikan proses 9router + server yang berjalan di background
# ============================================================
$ErrorActionPreference = "SilentlyContinue"

Write-Host "Mencari proses 9router yang berjalan..."

# Cari proses node yang commandline-nya mengandung 9router\cli.js
$procs = Get-CimInstance Win32_Process -Filter "Name = 'node.exe'" |
    Where-Object { $_.CommandLine -match '9router[\\/]cli\.js' }

if ($procs) {
    foreach ($p in $procs) {
        Write-Host ("Mematikan PID " + $p.ProcessId + " (9router)")
        taskkill /PID $p.ProcessId /T /F 2>$null | Out-Null
    }
    Write-Host "OK: 9Router dihentikan."
} else {
    Write-Host "Info: Tidak ada proses 9router yang berjalan."
}

# Bersihkan file PID sisa bila ada (runtime & db di folder data workspace)
$dataDir = Join-Path $PSScriptRoot "9router-data"
Remove-Item (Join-Path $dataDir "runtime\*.pid") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $dataDir "*.pid") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $PSScriptRoot "*.pid") -Force -ErrorAction SilentlyContinue

Start-Sleep -Milliseconds 800
Write-Host "Selesai."