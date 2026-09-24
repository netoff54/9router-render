# 🚀 Aktivasi Remote 9Router ke Railway (24/7 Online)

## 📌 Overview

Deploy 9Router ke Railway agar:
- ✅ **24/7 Online** - Tidak perlu laptop nyala terus
- ✅ **Remote Access** - Akses dari mana saja via HTTPS
- ✅ **Auto-Backup** - Sync otomatis ke Hugging Face setiap 5 menit
- ✅ **Production Ready** - Docker container di cloud

---

## 🔑 API Credentials Tersedia

| Service | Status | Details |
|---------|--------|---------|
| **Railway** | ✅ Terinstall | `railway` CLI ready |
| **Hugging Face** | ✅ Ada | `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` |
| **Docker** | ✅ Terinstall | WSL 2 / Docker Desktop |
| **GitHub** | ✅ Git ready | Untuk version control |

---

## 📋 LANGKAH AKTIVASI

### **STEP 1: Setup Environment Variable**

```powershell
# Temporary (session ini saja)
$env:HF_TOKEN = "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"

# Permanent
[Environment]::SetEnvironmentVariable("HF_TOKEN", "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", "User")
```

### **STEP 2: Verifikasi Semua Tools**

```powershell
railway --version
docker --version
Test-NetConnection localhost -Port 20128  # Harus connected
```

### **STEP 3: Deploy ke Railway**

```powershell
cd 'D:\Milih Sesuai\remote server 9router railway'
.\railway-deploy.ps1
```

Script akan:
- Login ke Railway (browser popup)
- Buat project "9router-deploy"
- Deploy Dockerfile
- Set environment variables
- Start 9Router di Railway

### **STEP 4: Verifikasi Deployment**

```powershell
# Status check
railway status

# View logs
railway logs -f

# Get URL
railway open
```

---

## 🎯 Setelah Berhasil Deploy

**Dashboard URL:** `https://9router-deploy-production-xxxx.up.railway.app`
**Default Password:** `123456` (ubah di dashboard!)
**API Base:** `https://9router-deploy-production-xxxx.up.railway.app/v1`

---

## ⚠️ Important

- `/app/data` volume = data **persistent**
- Auto-backup setiap 5 menit ke HF
- HTTPS enforced oleh Railway
- **Change default password!**

---

## 🛠️ Troubleshooting

```powershell
# Logs real-time
railway logs -f

# Restart
railway restart

# Check token
railway variables
```

---

## ✅ Checklist

- [ ] `$env:HF_TOKEN` set
- [ ] `railway login` OK
- [ ] `docker` running
- [ ] 9Router lokal on (localhost:20128)
- [ ] `.env.railway` exists
- [ ] `Dockerfile` exists

**Ready? Run: `.\railway-deploy.ps1`** 🚀
