# ============================================================
#  Hapus Auto-Start 9Router (Startup folder)
#  - Menghapus shortcut autostart, 9router tidak lagi
#    otomatis nyala saat login.
# ============================================================
$ErrorActionPreference = "SilentlyContinue"

$startupDir = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupDir "9router-Workspace.lnk"

if (Test-Path $shortcutPath) {
    Remove-Item $shortcutPath -Force
    Write-Host "✅ Auto-start 9Router dihapus."
    Write-Host "Shortcut : $shortcutPath"
    Write-Host "9Router tidak lagi otomatis nyala saat login."
} else {
    Write-Host "ℹ️ Tidak ditemukan shortcut autostart 9Router."
    Write-Host "   (Mungkin sudah dihapus sebelumnya.)"
}