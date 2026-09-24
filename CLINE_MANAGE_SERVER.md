# 🎮 PROMPT: Manage Railway Server via Cline

**Full prompt untuk control & maintain Railway 9Router**

---

## 📌 Server Info

```
Name: 9router-deploy
Platform: Railway (production)
Status: Always running 24/7
URL: https://9router-deploy-production-3a0f.up.railway.app
API: https://9router-deploy-production-3a0f.up.railway.app/v1
Key: sk-05b0d0b73a8aee96-25ki8w-e142ea50

CLI Commands:
- railway status
- railway logs -f (live logs)
- railway logs --tail 50
- railway restart
- railway variables
- railway variables set KEY=value
- railway open (dashboard)

Backup: Auto-sync HF every 5 min
```

---

## 🟢 MASTER PROMPT: Full Management

Copy-paste ke Cline:

```
I have a 9Router server on Railway (9router-deploy).

SERVER:
- URL: https://9router-deploy-production-3a0f.up.railway.app
- API: https://9router-deploy-production-3a0f.up.railway.app/v1
- Key: sk-05b0d0b73a8aee96-25ki8w-e142ea50
- Runs 24/7 on Railway

YOUR ROLE:
1. Health checks - verify running properly
2. Monitor logs - watch for errors
3. Troubleshoot - fix issues immediately
4. Performance - check CPU/RAM
5. Configuration - manage variables
6. Maintenance - restart if needed

AVAILABLE COMMANDS:
- railway status
- railway logs -f
- railway restart
- railway variables
- railway variables set
- railway open

START: Check server status and health. Report findings.
```

---

## 🔍 Daily Health Check

```
"Run health check on the server"
"Is railway running properly?"
"Show status and recent logs"
"Any errors in logs?"
```

---

## 🚨 Troubleshooting

When something wrong:
```
"Server is down"
"API returns 500 error"
"Logs show exceptions"
"Dashboard not accessible"
"Server is lagging"

→ Cline will:
1. Check logs
2. Find error
3. Suggest fix
4. Execute if approved
5. Verify recovery
```

---

## 📊 Performance Check

```
"Check server performance"
"CPU and RAM usage?"
"How many requests processed?"
"Any memory leaks?"
"Optimize if needed"
```

---

## 🔧 Configuration

```
"List environment variables"
"Set HF_TOKEN to..."
"Update LOG_LEVEL"
"Show configuration"
"Validate variables"
```

---

## 🔄 Maintenance

### Restart:
```
"Restart the server"
"Reboot 9Router"
```

### Logs:
```
"Show server logs"
"Watch live logs"
"Filter for errors"
"Last 100 lines"
```

### Dashboard:
```
"Open dashboard"
"Login and check"
"Verify accessible"
```

---

## 🧪 Testing

```
"Test /v1/models endpoint"
"Send test API request"
"Test chat completion"
"Check auth working"
"Verify all endpoints"
```

---

## 📈 Schedules

### Morning:
```
"Good morning - health check"
```

### Afternoon:
```
"Everything still running?"
```

### Night:
```
"Night check - stable?"
"What happened today?"
```

### Weekly:
```
"Weekly review"
"Check performance"
"Review logs"
"Verify backup"
"Optimize if needed"
```

---

## 🚨 Emergency

```
"SERVER DOWN - EMERGENCY!"
"Check logs immediately"
"What's the error?"
"Restart now"
"Verify back online"
```

---

## 📋 Quick Commands

```
Status:       "Check server status"
Health:       "Server health?"
Logs:         "Show logs"
Restart:      "Restart server"
Performance:  "Check performance"
Config:       "List variables"
Test:         "Test API"
Dashboard:    "Open dashboard"
Emergency:    "Server down - fix!"
```

---

## ✅ Daily Workflow

1. **Morning (5 min):**
   ```
   "Morning check - is server healthy?"
   ```

2. **During Day:**
   ```
   "Any issues?"
   "Test if changes made"
   "Monitor performance"
   ```

3. **Night (5 min):**
   ```
   "Final check - stable for night?"
   "Activity summary"
   ```

4. **Weekly (10 min):**
   ```
   "Weekly maintenance"
   "Full health report"
   "Optimizations needed?"
   ```

---

## 🔐 Remember

✅ Server always running 24/7
✅ Data auto-backup (HF)
✅ Keep API key secret
✅ Check health daily
✅ Restart takes ~30s
✅ Update password from 123456
✅ Verify backup regularly

---

## 🎯 Simple Rule

Tell Cline what you need.
Cline manages the server.
Life is easy! 🚀

---

**Start managing via Cline!** 🎮
