# ⚡ QUICK START: Deploy 9Router ke Railway

Panduan singkat langsung praktek tanpa teori panjang.

---

## 🚀 5 MENIT DEPLOY

### **1. Set Token (Terminal PowerShell)**

```powershell
$env:HF_TOKEN = "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"
cd 'D:\Milih Sesuai\remote server 9router railway'
```

### **2. Check Tools**

```powershell
railway --version
docker --version
```

Both OK? Continue...

### **3. Deploy**

```powershell
.\railway-deploy.ps1
```

Script akan:
- Ask you to login Railway (browser akan pop-up)
- Build & deploy Dockerfile
- Setup environment variables
- Start 9Router

**Wait 2-5 minutes...**

### **4. Verify**

```powershell
railway status
railway logs -f
```

See logs flowing? **SUCCESS!** ✅

### **5. Access**

Browser: `https://9router-deploy-production-3a0f.up.railway.app`

**Login:**
- Password: `123456`

---

## 🔄 Next: Connect Cline

Edit: `%APPDATA%\Claude\globalState.json`

```json
{
  "openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1"
}
```

Restart Cline → Done! 🎉

---

## 🛠️ Common Commands

```powershell
# Status
railway status

# Live logs
railway logs -f

# Restart
railway restart

# View vars
railway variables

# Set variable
railway variables set MY_VAR=value

# Open dashboard
railway open
```

---

## ⚠️ If Something Goes Wrong

### Error: "Railway not found"
```powershell
npm install -g @railway/cli
```

### Error: "Docker not running"
- Start Docker Desktop

### Error: "Deployment failed"
```powershell
railway logs
# Check error, fix, then:
railway restart
```

### Error: "Can't access Railway URL"
- Wait 1-2 minutes more
- Check: `railway status`
- See "crashed"? Check: `railway logs -f`

---

## 📊 What You Get

```
✅ 24/7 Online Server
✅ HTTPS URL ready to use
✅ Auto-backup to Hugging Face every 5 minutes
✅ Dashboard access via browser
✅ API endpoint for Cline
✅ Auto-restarts on crash
✅ Persistent storage
```

---

## 🎯 URLs & Access

| What | URL/Command |
|------|-------------|
| Dashboard | https://9router-deploy-production-3a0f.up.railway.app |
| API Base | https://9router-deploy-production-3a0f.up.railway.app/v1 |
| Check Status | `railway status` |
| Live Logs | `railway logs -f` |
| HF Backup | https://huggingface.co/datasets/otakcoding/9router-data-backup |

---

## ✅ Success Checklist

- [ ] `.\railway-deploy.ps1` ran without errors
- [ ] Browser login works (password: 123456)
- [ ] `railway status` shows "deployed"
- [ ] Logs show "9Router listening on 20128"
- [ ] Can access URL in browser
- [ ] Dashboard visible (empty or with your providers)

---

**That's it! You now have 9Router on Railway.** 🚀

Next: Update Cline config and start using it!
