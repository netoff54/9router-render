# 🚀 START HERE: Deploy 9Router ke Railway (5 Menit)

Panduan singkat langsung praktik. Teori disimpan di file lain.

---

## ⚡ 5 STEPS TO LIVE

### 1️⃣ **SET TOKEN** (30 detik)

Buka PowerShell di folder ini, ketik:

```powershell
$env:HF_TOKEN = "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"
```

Verify:
```powershell
echo $env:HF_TOKEN
```

### 2️⃣ **CHECK TOOLS** (30 detik)

```powershell
railway --version
docker --version
```

Keduanya OK? Lanjut...

### 3️⃣ **DEPLOY** (30 detik)

```powershell
.\railway-deploy.ps1
```

Browser akan pop-up untuk Railway login. Approve.
Script akan handle semua otomatis.

### 4️⃣ **WAIT** (3-5 menit)

Tunggu sampai script selesai. Jangan tutup terminal.

```powershell
railway status
```

Harus show: "deployed" ✅

### 5️⃣ **ACCESS** (1 menit)

Buka browser:

```
https://9router-deploy-production-3a0f.up.railway.app
```

Login password: `123456`

**🎉 DONE! 9Router is LIVE!**

---

## 🔗 Next: Connect Cline (Optional)

Edit file: `%APPDATA%\Claude\globalState.json`

```json
{
  "openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1"
}
```

Restart Cline → Done!

---

## ⚠️ Stuck Somewhere?

Check these files:

```
❓ Don't understand?           → ACTIVATION_SUMMARY.md
❓ Script error?               → RAILWAY_SETUP.md
❓ Need API docs?              → RAILWAY_API_GUIDE.md
❓ How to check status?        → railway-monitor.ps1
❓ Full documentation?         → INDEX.md
❓ Before deploy checklist?    → DEPLOYMENT_CHECKLIST.md
```

---

## 🛠️ Common Commands

```powershell
# Check status
railway status

# View logs
railway logs -f

# Restart
railway restart

# Monitor
.\railway-monitor.ps1
```

---

**Ready? Start with: `.\railway-deploy.ps1`** 🚀
