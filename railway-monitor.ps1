# Railway 9Router Monitoring & Maintenance Script
# Check status, logs, and health of deployment

param(
    [string]$Command = "status",
    [int]$TailLines = 50
)

function Write-Section { Write-Host "`n>>> $args <<<`n" -ForegroundColor Cyan -BackgroundColor Black }
function Write-Success { Write-Host "[✅] $args" -ForegroundColor Green }
function Write-Error { Write-Host "[❌] $args" -ForegroundColor Red }
function Write-Info { Write-Host "[ℹ️] $args" -ForegroundColor White }
function Write-Warn { Write-Host "[⚠️] $args" -ForegroundColor Yellow }

Write-Host "`n═══════════════════════════════════════════════════"
Write-Host "    9Router Railway Monitoring & Maintenance"
Write-Host "═══════════════════════════════════════════════════`n"

Write-Info "Available commands: status | logs | health | vars | restart | logs-sync | help"
Write-Info "Usage: .\railway-monitor.ps1 -Command 'status'`n"

# Handle different commands
switch ($Command.ToLower()) {
    "status" {
        Write-Section "Deployment Status"
        railway status
        Write-Info "`nFor more details: railway logs -f"
    }
    
    "logs" {
        Write-Section "Recent Logs ($TailLines lines)"
        railway logs --tail $TailLines
    }
    
    "logs-sync" {
        Write-Section "Sync Logs (HF Backup Activity)"
        railway logs --tail $TailLines | findstr "sync"
        Write-Info "`nIf no output, auto-sync may not be running."
    }
    
    "logs-api" {
        Write-Section "API Logs (9Router Activity)"
        railway logs --tail $TailLines | findstr "POST|GET|chat"
    }
    
    "health" {
        Write-Section "Health Check"
        Write-Info "Testing 9Router health endpoint..."
        try {
            $response = Invoke-WebRequest -Uri "https://9router-deploy-production-3a0f.up.railway.app/api/health" `
                -Headers @{"Authorization" = "Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"} `
                -ErrorAction Stop
            Write-Success "Health check passed (Status: $($response.StatusCode))"
            Write-Info "Response: $($response.Content)"
        } catch {
            Write-Error "Health check failed: $_"
        }
    }
    
    "vars" {
        Write-Section "Environment Variables"
        railway variables
        Write-Info "`nTo set a variable: railway variables set KEY=value"
    }
    
    "restart" {
        Write-Section "Restarting 9Router..."
        Write-Warn "Service will be offline for ~30 seconds"
        railway restart
        Write-Success "Restart initiated"
        Write-Info "Checking status in 5 seconds..."
        Start-Sleep -Seconds 5
        railway status
    }
    
    "live" {
        Write-Section "Live Logs (Press Ctrl+C to stop)"
        railway logs -f
    }
    
    "help" {
        Write-Host @"
📖 Railway Monitoring Commands
═════════════════════════════════

STATUS & LOGS:
  .\railway-monitor.ps1 -Command "status"      → Full deployment status
  .\railway-monitor.ps1 -Command "logs"        → Last 50 log lines
  .\railway-monitor.ps1 -Command "logs" -TailLines 100
  .\railway-monitor.ps1 -Command "live"        → Real-time logs (Ctrl+C stop)
  
DIAGNOSTICS:
  .\railway-monitor.ps1 -Command "health"      → Test API health
  .\railway-monitor.ps1 -Command "logs-sync"   → Filter sync logs
  .\railway-monitor.ps1 -Command "logs-api"    → Filter API logs
  .\railway-monitor.ps1 -Command "vars"        → Environment variables
  
MANAGEMENT:
  .\railway-monitor.ps1 -Command "restart"     → Restart service
  
Other:
  railway open                                  → Open Railway dashboard
  railway logs -f                               → Manual live logs
  railway variables set KEY=value               → Set environment variable

═════════════════════════════════════════════════════════════════════════════
"@
    }
    
    default {
        Write-Error "Unknown command: $Command"
        Write-Info "Run with -Command 'help' for available commands"
    }
}

Write-Host ""
