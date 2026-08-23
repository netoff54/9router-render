# ============================================================
#  Install Auto-Start 9Router saat Login (Startup folder)
#  - Menjalankan 9router di background (tray) otomatis saat
#    laptop nyala & user login.
#  - Tidak membuka jendela terminal (tersembunyi).
#  - Untuk menghapus: jalankan uninstall-autostart.ps1
# ============================================================
$ErrorActionPreference = "Stop"

$workspaceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$startupDir = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupDir "9router-Workspace.lnk"

# Target: powershell.exe menjalankan start-9router-background.ps1 secara tersembunyi
$powershellExe = (Get-Command powershell.exe).Source
$scriptPath = Join-Path $workspaceDir "start-9router-background.ps1"
$arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

# Buat shortcut
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $powershellExe
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $workspaceDir
$shortcut.Description = "Auto-start 9Router (data dari workspace)"
$shortcut.Save()

Write-Host "✅ Auto-start terpasang."
Write-Host "Startup  : $startupDir"
Write-Host "Shortcut : $shortcutPath"
Write-Host ""
Write-Host "9Router akan otomatis berjalan di background saat laptop nyala & login."