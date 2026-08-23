# ============================================================
#  Start 9Router di Background (Tray Mode)
#  - Berjalan tersembunyi, ikon muncul di system tray
#  - Server & Web UI aktif di http://localhost:20128
#  - Data dari workspace: .\9router-data
# ============================================================
$ErrorActionPreference = "Stop"

$workspaceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$dataDir = Join-Path $workspaceDir "9router-data"
$nodeExe = (Get-Command node).Source
$cliPath = Join-Path $workspaceDir "node_modules\9router\cli.js"

# Arahkan data ke folder workspace
$env:DATA_DIR = $dataDir
$env:NO_COLOR = "1"

Write-Host "Menjalankan 9Router di background (tray)..."
Write-Host "DATA_DIR : $dataDir"
Write-Host "Dashboard: http://localhost:20128"

# Quoting manual agar aman dari spasi pada path
$args = "--dns-result-order=ipv4first `"$cliPath`" --tray --no-browser --skip-update"

# Proses tersembunyi (tidak membuka jendela terminal)
Start-Process -FilePath $nodeExe -ArgumentList $args -WorkingDirectory $workspaceDir -WindowStyle Hidden

Write-Host "✅ 9Router berjalan di background. Ikon ada di system tray."
Write-Host "   Dashboard: http://localhost:20128"
