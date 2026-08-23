# Install Cloudflare Tunnel as Windows Service with Auto-Start
# This script installs the tunnel as a Windows service that starts automatically

Write-Host "=== Installing Cloudflare Tunnel as Windows Service ===" -ForegroundColor Cyan
Write-Host ""

$ConfigDir = "$env:USERPROFILE\.cloudflared"
$ConfigFile = "$ConfigDir\config.yml"

# Check if config file exists
if (-not (Test-Path $ConfigFile)) {
    Write-Host "ERROR: Config file not found: $ConfigFile" -ForegroundColor Red
    Write-Host "Please run setup-cloudflare-tunnel.ps1 first." -ForegroundColor Yellow
    exit 1
}

Write-Host "Config file found: $ConfigFile" -ForegroundColor Green
Write-Host ""

# Install as Windows service
Write-Host "Installing Cloudflare Tunnel as Windows service..." -ForegroundColor Green
& "$env:USERPROFILE\.cloudflared\cloudflared.exe" service install

if ($LASTEXITCODE -eq 0) {
    Write-Host "Service installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Service management commands:" -ForegroundColor Cyan
    Write-Host "  Start service:   cloudflared service start" -ForegroundColor Yellow
    Write-Host "  Stop service:    cloudflared service stop" -ForegroundColor Yellow
    Write-Host "  Remove service: cloudflared service uninstall" -ForegroundColor Yellow
    Write-Host ""
    
    # Start the service
    $response = Read-Host "Do you want to start the service now? (y/n)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "Starting Cloudflare Tunnel service..." -ForegroundColor Green
        & "$env:USERPROFILE\.cloudflared\cloudflared.exe" service start
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Service started successfully!" -ForegroundColor Green
            Write-Host "The tunnel will now start automatically with Windows." -ForegroundColor Green
        } else {
            Write-Host "Failed to start service. Check the error above." -ForegroundColor Red
        }
    }
} else {
    Write-Host "Failed to install service. Check the error above." -ForegroundColor Red
    Write-Host "You may need to run PowerShell as Administrator." -ForegroundColor Yellow
}