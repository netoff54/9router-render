# Cara Mengaktifkan Kembali Saat Ingin Setting Server

## 🖥️ Opsi A: Aktifkan 9Router Lokal (Untuk Setting di Localhost)

Buka **PowerShell** di folder workspace ini (`D:\Milih Sesuai\9router claudeflare`), lalu:

### 1. Nyalakan 9Router di background (tray)
```powershell
.\start-9router-background.ps1
```

### 2. Buka dashboard
```powershell
.\open-dashboard.ps1
```
→ Browser terbuka ke **http://localhost:20128** → login dengan password 9Router (default: `123456`)

### 3. Setelah selesai setting, matikan lagi (opsional)
```powershell
.\stop-9router.ps1
```

---

## ☁️ Opsi B: Manage Server Railway (Cloud — 24/7 Online)

Server di Railway **tidak perlu diaktifkan** — sudah selalu online. Yang perlu diaktifkan hanya **alat kelolanya** (Railway CLI):

### 1. Login Railway (sekali saja, buka browser untuk auth)
```powershell
railway login
```

### 2. Link ke project (jika belum ter-link)
```powershell
railway link
```
→ Pilih project **9router-deploy** → environment **production**

### 3. Perintah yang sering dipakai
```powershell
railway status        # Lihat status & URL server
railway logs          # Lihat log 9Router di server
railway variables     # Atur environment variables
railway restart       # Restart service di cloud
```

### 4. Akses langsung dari browser (tanpa CLI)
Tinggal buka: **https://9router-deploy-production-3a0f.up.railway.app** → login dengan password dashboard.

---

## 🔁 Ringkasan Pilihan

| Tujuan | Perintah |
|--------|----------|
| Setting di **localhost** (laptop) | `.\start-9router-background.ps1` → `.\open-dashboard.ps1` |
| Setting di **server cloud** Railway | `railway login` → `railway link` → `railway status/logs/variables` |
| Akses server langsung di browser | https://9router-deploy-production-3a0f.up.railway.app |
| Matikan 9Router lokal setelah selesai | `.\stop-9router.ps1` |

> 💡 **Catatan:** Data & API keys tidak hilang saat dimatikan — semuanya tersimpan di `9router-data/` (lokal) dan volume server (cloud). Jadi aman untuk nyala-mati kapan saja.
