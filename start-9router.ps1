# ============================================
#  Starter 9Router — pakai data dari workspace
#  Folder data: .\9router-data
# ============================================
$ErrorActionPreference = "Stop"

$workspaceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$dataDir = Join-Path $workspaceDir "9router-data"

# Arahkan data ke folder workspace
$env:DATA_DIR = $dataDir

Write-Host ""
Write-Host "=================================================="
Write-Host "  9Router — Data dari workspace"
Write-Host "  DATA_DIR: $dataDir"
Write-Host "=================================================="
Write-Host ""

# Jalankan 9router (dari node_modules lokal workspace)
& node (Join-Path $workspaceDir "node_modules\9router\cli.js") @args