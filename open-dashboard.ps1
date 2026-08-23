# ============================================================
#  Buka Dashboard 9Router di browser
#  Alamat: http://localhost:20128 (login bawaan 9Router)
# ============================================================
$ErrorActionPreference = "Stop"

# Buka dashboard 9Router (proteksi login BAWAAN 9router)
$url = "http://localhost:20128"

Write-Host "Membuka dashboard 9Router di browser..."
Write-Host "URL: $url"
Write-Host "Akan diminta password login (bawaan 9Router)."

# Buka di browser default
Start-Process $url
