# Deployment Script for 9Router Messaging Service to Railway
# This script deploys the updated 9Router with messaging integration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deploy 9Router with Messaging to Railway" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
Write-Host "Checking Railway CLI..." -ForegroundColor Yellow
try {
    $railwayVersion = railway --version
    Write-Host "✅ Railway CLI found: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "npm install -g @railway/cli" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is installed
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found. Please run setup-messaging.ps1 first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Checking Railway login status..." -ForegroundColor Yellow
try {
    $railwayStatus = railway status
    Write-Host "✅ Logged in to Railway" -ForegroundColor Green
} catch {
    Write-Host "❌ Not logged in to Railway. Please login:" -ForegroundColor Red
    railway login
    Write-Host "Please approve the login in your browser and press Enter when done..."
    Read-Host
}

Write-Host ""
Write-Host "Updating Railway environment variables..." -ForegroundColor Yellow

# Read .env file and set variables
$envVars = Get-Content ".env" | Where-Object { $_ -match "^[A-Z_]+=" }
foreach ($var in $envVars) {
    $parts = $var -split "=", 2
    $varName = $parts[0]
    $varValue = $parts[1]
    
    if ($varValue -and $varValue -ne "your_*_here") {
        Write-Host "Setting $varName..." -ForegroundColor White
        railway variables set $varName="$varValue"
    }
}

Write-Host ""
Write-Host "Deploying to Railway..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Cyan

try {
    railway up
    Write-Host ""
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host ""
    
    # Get deployment URL
    Write-Host "Getting deployment information..." -ForegroundColor Yellow
    railway status
    railway domain
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  Deployment Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your 9Router with messaging is now live!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access points:" -ForegroundColor Cyan
    Write-Host "• 9Router Dashboard: Check railway domain" -ForegroundColor White
    Write-Host "• Messaging API: Check railway domain + :5000" -ForegroundColor White
    Write-Host ""
    Write-Host "To monitor your deployment:" -ForegroundColor Cyan
    Write-Host "railway logs -f" -ForegroundColor Yellow
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host "Check the error message above and try again." -ForegroundColor Yellow
    Write-Host "For troubleshooting, run: railway logs" -ForegroundColor Yellow
    exit 1
}