# Railway 9Router Deployment Script (PowerShell)
# Deploy 9Router to Railway with auto-sync via Hugging Face

param(
    [string]$ProjectName = "9router-deploy",
    [string]$Environment = "production",
    [string]$Region = "us-west"
)

$ErrorActionPreference = "Stop"

# Color output
function Write-Success { Write-Host "[✅] $args" -ForegroundColor Green }
function Write-Error { Write-Host "[❌] $args" -ForegroundColor Red }
function Write-Info { Write-Host "[ℹ️] $args" -ForegroundColor Cyan }
function Write-Warning { Write-Host "[⚠️] $args" -ForegroundColor Yellow }

Write-Info "9Router Railway Deployment Script"
Write-Info "==================================`n"

# CHECK PREREQUISITES
Write-Info "Checking prerequisites..."

try {
    $railwayVersion = railway --version 2>$null
    Write-Success "Railway CLI: $railwayVersion"
} catch {
    Write-Error "Railway CLI not found!"
    exit 1
}

try {
    $dockerVersion = docker --version 2>$null
    Write-Success "Docker: $dockerVersion"
} catch {
    Write-Error "Docker not found!"
    exit 1
}

Write-Success "`nPrerequisites OK!`n"

# SETUP ENVIRONMENT
Write-Info "Setting up environment..."

$envFile = ".env.railway"
$envContent = @"
# 9Router Railway Deployment Configuration
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

DATA_DIR=/app/data
PORT=20128
NODE_ENV=production
ENABLE_MITM=false
LOG_LEVEL=info
HF_TOKEN=$env:HF_TOKEN
HF_USERNAME=otakcoding
HF_DATASET=9router-data-backup
AUTH_MODE=password
REQUIRE_LOGIN=true
SECURE_COOKIES=false
ENABLE_API=true
API_RATE_LIMIT=100
CORS_ORIGIN=*
"@

Set-Content -Path $envFile -Value $envContent
Write-Success "Environment file created: $envFile"

# LOGIN RAILWAY
Write-Info "`nLogging in to Railway..."
Write-Warning "Browser will open for authentication"

railway login
Write-Success "Logged in to Railway"

# LINK PROJECT
Write-Info "`nLinking to project: $ProjectName"
railway link --project $ProjectName 2>$null || Write-Info "Project will be created on deploy"

# DEPLOY
Write-Info "`nDeploying to Railway (2-5 minutes)..."
railway up --detach

Write-Success "`nDeployment initiated!`n"

Start-Sleep -Seconds 5
railway status

Write-Success "`n╔════════════════════════════════════════════╗"
Write-Success "║  Deployment Complete!                      ║"
Write-Success "╚════════════════════════════════════════════╝`n"

Write-Info "📋 Next Steps:"
Write-Info "• Check status: railway status"
Write-Info "• View logs: railway logs -f"
Write-Info "• Restart: railway restart"
Write-Info "• Dashboard: https://railway.app"

Write-Success "✅ 9Router is now on Railway (24/7 online)"
