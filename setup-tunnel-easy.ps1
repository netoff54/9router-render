# ============================================================
#  Setup Cloudflare Tunnel 9Router - EASY MODE
#  Syarat: pernah login sekali: cloudflared tunnel login
#  (browser terbuka, pilih domain apa saja yang mau dipakai)
#  Lalu jalankan script ini.
# ============================================================
param(
    [string]$DomainName = "",
    [string]$TunnelName = "9router-tunnel"
)
$ErrorActionPreference = "Stop"
$configDir = "$env:USERPROFILE\.cloudflared"
$certPem   = Join-Path $configDir "cert.pem"
$cloudflared = Join-Path $configDir "cloudflared.exe"
if (-not (Test-Path $cloudflared)) { $cloudflared = "cloudflared" }

Write-Host "=== Cloudflare Tunnel Setup (9Router) ===" -ForegroundColor Cyan

# [1/5] Cek login
if (-not (Test-Path $certPem)) {
    Write-Host "[1/5] BELUM LOGIN. Jalankan ini SEKALI (browser akan terbuka):" -ForegroundColor Yellow
    Write-Host "  & `"$cloudflared`" tunnel login" -ForegroundColor White
    Write-Host "Pilih domain yang mau dipakai (bebas), lalu jalankan ulang script ini." -ForegroundColor Yellow
    exit 1
}
Write-Host "[1/5] Login OK (cert.pem ditemukan)" -ForegroundColor Green

# [2/5] Buat tunnel kalau belum ada
Write-Host "[2/5] Cek tunnel '$TunnelName'..." -ForegroundColor Cyan
$tunnelId = $null
try {
    $listOutput = & $cloudflared tunnel list 2>&1 | Out-String
    $line = ($listOutput -split "`n" | Where-Object { $_ -match $TunnelName } | Select-Object -First 1)
    if ($line -match '([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})') {
        $tunnelId = $Matches[1]
    }
} catch { }
if (-not $tunnelId) {
    Write-Host "  Membuat tunnel baru..." -ForegroundColor Cyan
    $createOutput = & $cloudflared tunnel create $TunnelName 2>&1 | Out-String
    if ($createOutput -match '([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})') {
        $tunnelId = $Matches[1]
    }
}
if (-not $tunnelId) { Write-Host "[2/5] GAGAL buat tunnel. Cek output di atas." -ForegroundColor Red; exit 1 }
Write-Host "[2/5] Tunnel ID: $tunnelId" -ForegroundColor Green

# [3/5] Domain
if (-not $DomainName) {
    $DomainName = Read-Host "[3/5] Subdomain untuk akses (contoh: 9router) -> jadi 9router.dpdns.org"
}
$hostname = "$DomainName.dpdns.org"

# [4/5] Tulis config.yml
$credentialsFile = Join-Path $configDir "$tunnelId.json"
$configContent = @"
tunnel: $tunnelId
credentials-file: $credentialsFile

ingress:
  - hostname: $hostname
    service: http://localhost:20128
  - service: http_status:404
"@
Set-Content -Path (Join-Path $configDir "config.yml") -Value $configContent -Encoding UTF8
Write-Host "[4/5] config.yml ditulis -> $hostname -> http://localhost:20128" -ForegroundColor Green

# [5/5] Route DNS & validasi
Write-Host "[5/5] Route DNS..." -ForegroundColor Cyan
& $cloudflared tunnel route dns $tunnelId $hostname 2>&1 | Out-Host
& $cloudflared tunnel --config (Join-Path $configDir "config.yml") ingress validate
if ($LASTEXITCODE -eq 0) {
    Write-Host "Konfigurasi VALID." -ForegroundColor Green
    Write-Host "Jalankan tunnel sekarang:" -ForegroundColor White
    Write-Host "  & `"$cloudflared`" tunnel --config `"$(Join-Path $configDir 'config.yml')`" run" -ForegroundColor White
    Write-Host "Akses dari luar: https://$hostname" -ForegroundColor White
} else {
    Write-Host "Konfigurasi TIDAK valid. Cek output di atas." -ForegroundColor Red
}
