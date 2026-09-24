# ✅ 9Router Railway Deployment Checklist

Final checklist untuk deploy ke Railway.

---

## 🔍 PRE-DEPLOYMENT

### Infrastructure
- [ ] Railway CLI: `railway --version` ✅
- [ ] Docker: `docker --version` ✅
- [ ] Git: `git --version` ✅
- [ ] HF_TOKEN environment set

### Files
- [ ] Dockerfile exists
- [ ] sync.py exists
- [ ] requirements.txt exists
- [ ] .env.railway exists
- [ ] railway-deploy.ps1 exists

### Local Check
- [ ] 9Router running: localhost:20128 ✅
- [ ] Providers configured ✅
- [ ] API key set ✅

### Credentials
- [ ] HF Token: `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`
- [ ] 9Router Key: `sk-05b0d0b73a8aee96-25ki8w-e142ea50`

---

## 🚀 DEPLOYMENT

### Step 1: Env
- [ ] `$env:HF_TOKEN = "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"`
- [ ] `echo $env:HF_TOKEN` verified

### Step 2: Login
- [ ] `railway login` succeeded
- [ ] Browser authentication OK

### Step 3: Deploy
- [ ] `.\railway-deploy.ps1` ran
- [ ] No errors
- [ ] Completed successfully

### Step 4: Verify
- [ ] Wait 2-5 minutes
- [ ] `railway status` → deployed
- [ ] `railway logs -f` → 9Router running

---

## ✨ POST-DEPLOYMENT

### Service
- [ ] Status: deployed ✅
- [ ] Dashboard accessible
- [ ] Login works (password: 123456)
- [ ] No errors in logs

### API Tests
- [ ] Health endpoint: 200 OK
- [ ] Models list: returns array
- [ ] Bearer auth: works
- [ ] Chat completion: response OK

### Storage
- [ ] Volume mounted: /app/data
- [ ] Database exists
- [ ] Sync started
- [ ] HF backup initiated

---

## 🔧 SETUP

### Security
- [ ] Changed default password
- [ ] New password set in Settings
- [ ] No secrets in logs

### Cline (Optional)
- [ ] Updated globalState.json
- [ ] Updated providers.json
- [ ] Restarted Cline
- [ ] Tested connection
- [ ] Chat works

---

## 📊 TESTS

```powershell
# Test 1: Health
curl https://9router-deploy-production-3a0f.up.railway.app/api/health

# Test 2: Models
curl https://9router-deploy-production-3a0f.up.railway.app/v1/models \
  -H "Authorization: Bearer sk-..."

# Test 3: Chat
curl -X POST https://9router-deploy-production-3a0f.up.railway.app/v1/chat/completions \
  -H "Authorization: Bearer sk-..." \
  -d '{"model":"mimo-v2.5-free","messages":[...]}'
```

All tests passing? ✅

---

## 🎯 FINAL

✅ **9Router on Railway - LIVE!**

- 24/7 online
- HTTPS ready
- Auto-backup active
- Remote access enabled
- Cline connected
- Monitoring set up

---

## 📋 OPERATIONS

### Daily
- [ ] Check: `.\railway-monitor.ps1 -Command status`

### If Error
- [ ] View logs: `railway logs -f`
- [ ] Restart: `railway restart`

### Weekly
- [ ] Check HF backup dataset
- [ ] Verify file counts

---

## 🆘 QUICK FIX

| Issue | Fix |
|-------|-----|
| Not accessible | `railway status`, check deploy |
| 401 error | Verify token in `railway variables` |
| Backup not sync | Check HF token, restart |
| Slow response | Check `railway logs`, restart |

---

## 📞 COMMANDS

```powershell
railway status              # Check
railway logs -f             # Logs
railway restart             # Restart
railway variables           # Vars
railway open                # Dashboard
.\railway-monitor.ps1       # Monitor tool
```

---

**When all checked: Deployment Complete!** ✅🎉
