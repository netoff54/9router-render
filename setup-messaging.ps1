# Setup Script for 9Router Messaging Service
# This script helps configure Twilio and Telegram integration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  9Router Messaging Service Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.messaging exists
if (-not (Test-Path ".env.messaging")) {
    Write-Host "Error: .env.messaging file not found!" -ForegroundColor Red
    Write-Host "Please ensure you're in the correct directory." -ForegroundColor Red
    exit 1
}

# Copy template to .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.messaging" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
} else {
    Write-Host ".env file already exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Please provide your messaging service credentials:" -ForegroundColor Cyan
Write-Host ""

# Twilio Configuration
Write-Host "--- Twilio Configuration ---" -ForegroundColor Cyan
$twilioAccountSid = Read-Host "Enter your Twilio Account SID (or press Enter to skip)"
$twilioAuthToken = Read-Host "Enter your Twilio Auth Token (or press Enter to skip)"
$twilioPhoneNumber = Read-Host "Enter your Twilio Phone Number (or press Enter to skip)"

# Telegram Configuration
Write-Host ""
Write-Host "--- Telegram Configuration ---" -ForegroundColor Cyan
$telegramBotToken = Read-Host "Enter your Telegram Bot Token (or press Enter to skip)"

# Hugging Face Token
Write-Host ""
Write-Host "--- Hugging Face Configuration ---" -ForegroundColor Cyan
$hfToken = Read-Host "Enter your Hugging Face Token (or press Enter to skip)"

# Update .env file
if ($twilioAccountSid -or $twilioAuthToken -or $twilioPhoneNumber -or $telegramBotToken -or $hfToken) {
    Write-Host ""
    Write-Host "Updating .env file..." -ForegroundColor Yellow
    
    $envContent = Get-Content ".env"
    
    if ($twilioAccountSid) {
        $envContent = $envContent -replace "^TWILIO_ACCOUNT_SID=.*", "TWILIO_ACCOUNT_SID=$twilioAccountSid"
    }
    if ($twilioAuthToken) {
        $envContent = $envContent -replace "^TWILIO_AUTH_TOKEN=.*", "TWILIO_AUTH_TOKEN=$twilioAuthToken"
    }
    if ($twilioPhoneNumber) {
        $envContent = $envContent -replace "^TWILIO_PHONE_NUMBER=.*", "TWILIO_PHONE_NUMBER=$twilioPhoneNumber"
    }
    if ($telegramBotToken) {
        $envContent = $envContent -replace "^TELEGRAM_BOT_TOKEN=.*", "TELEGRAM_BOT_TOKEN=$telegramBotToken"
    }
    if ($hfToken) {
        $envContent = $envContent -replace "^HF_TOKEN=.*", "HF_TOKEN=$hfToken"
    }
    
    Set-Content ".env" -Value $envContent
    Write-Host "✅ .env file updated" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "No credentials provided. You can update .env file manually later." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review and update .env file if needed" -ForegroundColor White
Write-Host "2. Test the messaging service locally:" -ForegroundColor White
Write-Host "   python messaging_api.py" -ForegroundColor Yellow
Write-Host "3. Deploy to Railway:" -ForegroundColor White
Write-Host "   .\deploy-messaging.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "For more information, see MESSAGING_SETUP.md" -ForegroundColor Cyan
Write-Host ""