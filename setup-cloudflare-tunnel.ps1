# Cloudflare Tunnel Setup Script for 9Router
# This script helps configure Cloudflare Tunnel after manual domain registration

param(
    [Parameter(Mandatory=$true)]
    [string]$DomainName,
    
    [Parameter(Mandatory=$true)]
    [string]$TunnelId
)

Write-Host "=== Cloudflare Tunnel Setup for 9Router ===" -ForegroundColor Cyan
Write-Host ""

# Configuration paths
$ConfigDir = "$env:USERPROFILE\.cloudflared"
$ConfigFile = "$ConfigDir\config.yml"
$CredentialsFile = "$ConfigDir\$TunnelId.json"

Write-Host "Configuration Directory: $ConfigDir" -ForegroundColor Yellow
Write-Host "Domain: $DomainName.dpdns.org" -ForegroundColor Yellow
Write-Host "Tunnel ID: $TunnelId" -ForegroundColor Yellow
Write-Host ""

# Check if credentials file exists
if (-not (Test-Path $CredentialsFile)) {
    Write-Host "ERROR: Credentials file not found: $CredentialsFile" -ForegroundColor Red
    Write-Host "Please run: cloudflared tunnel create 9router-tunnel" -ForegroundColor Yellow
    exit 1
}

# Create/update config file
Write-Host "Creating tunnel configuration..." -ForegroundColor Green
$configContent = @"
tunnel: $TunnelId
credentials-file: $CredentialsFile

ingress:
  - hostname: $DomainName.dpdns.org
    service: http://localhost:20128
  - service: http_status:404
"@

Set-Content -Path $ConfigFile -Value $configContent -Encoding UTF8
Write-Host "Config file created: $ConfigFile" -ForegroundColor Green
Write-Host ""

# Test tunnel configuration
Write-Host "Testing tunnel configuration..." -ForegroundColor Green
& "$env:USERPROFILE\.cloudflared\cloudflared.exe" tunnel --config "$ConfigFile" ingress validate

if ($LASTEXITCODE -eq 0) {
    Write-Host "Tunnel configuration is valid!" -ForegroundColor Green
} else {
    Write-Host "Tunnel configuration has errors. Please check the output above." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Run: cloudflared tunnel --config `"$ConfigFile`" run" -ForegroundColor Yellow
Write-Host "2. Test access at: https://$DomainName.dpdns.org" -ForegroundColor Yellow
Write-Host "3. To install as Windows service, run: cloudflared service install" -ForegroundColor Yellow
Write-Host ""

# Offer to run tunnel now
$response = Read-Host "Do you want to start the tunnel now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "Starting tunnel..." -ForegroundColor Green
    & "$env:USERPROFILE\.cloudflared\cloudflared.exe" tunnel --config "$ConfigFile" run
}