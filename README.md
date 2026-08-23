# 9Router di Workspace (Claude/Cline)

9Router dikonfigurasi agar **semua data tersimpan di folder workspace** ini, bukan di `%APPDATA%/9router/` (Windows), dan berjalan **otomatis di background** saat laptop nyala.

## 📂 Struktur

```
9router claudeflare/
├── 9router-data/                  ← Semua data (DB, auth, logs, runtime)
│   ├── db/data.sqlite             ← Database utama (termasuk login dashboard)
│   ├── auth/                      ← CLI secret
│   ├── logs/mitm/                 ← Log MITM
│   └── runtime/                   ← Runtime dependencies
├── node_modules/9router/          ← 9Router lokal
│
│   ── SKRIP UTAMA ──
├── start-9router.js               ← Start foreground (cross-platform)
├── start-9router.ps1              ← Start foreground (PowerShell)
├── start-9router-background.ps1   ← ★ Start background (tray, tersembunyi)
├── stop-9router.ps1               ← ★ Stop 9router (manual)
├── open-dashboard.ps1             ← ★ Buka dashboard web
├── install-autostart.ps1          ← Pasang auto-start saat login
├── uninstall-autostart.ps1        ← Hapus auto-start
│
├── package.json, README.md
```

## 🔐 Proteksi Login (Bawaan 9Router)

Dashboard 9Router memakai **proteksi login bawaan** 9Router (`authMode = "password"`, `requireLogin = true`) — tanpa auth-proxy custom.

**Cara kerja:**
- Dashboard di **http://localhost:20128** meminta login (halaman `/login` bawaan).
- `/api/*` atau `/dashboard` tanpa login → **401 / redirect ke `/login`**.
- Password & session dikelola oleh 9Router dan tersimpan di database (`data.sqlite`).
- Password default 9Router: `123456`.
- Untuk mengubah/ganti password: masuk dashboard → **Settings / Profile** → ubah password, atau via **CLI menu Settings → Reset Password**.

**Akses dashboard:**
```powershell
.\open-dashboard.ps1        # Buka http://localhost:20128 (login bawaan 9Router)
```

## 🚀 Cara Penggunaan

### ▶️ Menjalankan (background / tray) — DIREKOMENDASIKAN
```powershell
.\start-9router-background.ps1
```
- Berjalan **tersembunyi di belakang layar** (ikon di system tray).
- Dashboard aktif di **http://localhost:20128** (login bawaan 9Router).

### ⏹️ Menghentikan (manual)
```powershell
.\stop-9router.ps1
```
- Mematikan semua proses 9router + server.

### 🌐 Buka dashboard web
```powershell
.\open-dashboard.ps1
```
- Membuka **http://localhost:20128** di browser default (login bawaan 9Router).

### 🖥️ Menjalankan di depan (foreground, dengan menu interaktif)
```bash
npm start        # atau
node start-9router.js
```

## 🔄 Auto-Start saat Laptop Nyala

9Router sudah dipasang agar **otomatis berjalan di background (tray)** setiap kali laptop nyala & user login — lalu otomatis berhenti saat laptop mati.

- Pasang auto-start:
  ```powershell
  .\install-autostart.ps1
  ```
- Hapus auto-start (9router tidak lagi otomatis nyala):
  ```powershell
  .\uninstall-autostart.ps1
  ```

Mekanisme: shortcut dibuat di **Startup folder** Windows
(`C:\Users\[User]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\9router-Workspace.lnk`) yang menjalankan `start-9router-background.ps1` secara tersembunyi.

## 🗄️ Lokasi Data

| Data | Lokasi di workspace |
|---|---|
| Database utama | `9router-data/db/data.sqlite` |
| Auth CLI | `9router-data/auth/` |
| Log MITM | `9router-data/logs/mitm/` |
| Runtime dependencies | `9router-data/runtime/` |
| JWT/machine secret | `9router-data/jwt-secret`, `9router-data/machine-id` |

> Data asli sebelumnya tersimpan di `%APPDATA%/9router/` dan telah **disalin** ke `9router-data/`. Folder `%APPDATA%/9router/` dipertahankan sebagai backup.

## ⚠️ Catatan Penting

- **Path workspace mengandung spasi** (`D:\Milih Sesuai\...`). Semua script sudah menangani ini dengan aman.
- 9Router berjalan memakai `DATA_DIR` → `.\9router-data` di workspace (bukan `%APPDATA%`).
- Jangan edit `data.sqlite` saat server berjalan (WAL lock).
- Untuk backup: cukup salin folder `9router-data/`.

## 🛠️ Update 9router

```bash
npm install 9router@latest
npm approve-scripts 9router   # izinkan postinstall (diperlukan sekali)
```

## ✅ Status Saat Ini

- ✅ 9Router v0.5.55 terinstall lokal di workspace.
- ✅ Data (25 provider, 1 API key, 1 combo) tersimpan di `9router-data/db/data.sqlite`.
- ✅ 9Router **sedang berjalan di background** (dashboard: http://localhost:20128).
- ✅ Proteksi login **bawaan 9Router** aktif (`authMode=password`) — `/api/settings` → 401, `/dashboard` → redirect `/login`.
- ✅ Auto-start terpasang di Startup folder — otomatis nyala saat laptop nyala & login.
- ✅ cloudflared terinstall (v2026.8.2) untuk Cloudflare Tunnel.
- ✅ Setup scripts siap untuk deployment publik via Cloudflare Tunnel.

## 🌐 Cloudflare Tunnel Setup (24/7 Public Access)

### Prasyarat (Manual Steps Required)

Sebelum menjalankan script setup, Anda perlu:

1. **Register Domain Gratis** (DigitalPlat dpdns.org - Recommended)
   - Daftar: https://dash.domain.digitalplat.org/auth/register
   - Verifikasi email & GitHub OAuth
   - Register domain (misal: `9router.dpdns.org`)
   - Star repo GitHub untuk quota tambahan: https://github.com/DigitalPlatDev/FreeDomain

2. **Setup Cloudflare Account**
   - Buat akun Cloudflare gratis: https://dash.cloudflare.com/sign-up
   - Add domain Anda ke Cloudflare
   - Copy nameserver dari Cloudflare (format: `xxx.ns.cloudflare.com`)

3. **Update Nameservers**
   - Di DigitalPlat dashboard, update NS records dengan nameserver Cloudflare
   - Tunggu DNS propagation (2-48 jam)

4. **Create Cloudflare Tunnel**
   - Jalankan: `cloudflared tunnel login` (buka browser untuk auth)
   - Create tunnel: `cloudflared tunnel create 9router-tunnel`
   - Copy tunnel ID yang ditampilkan

### Setup Automated Scripts

Setelah langkah manual di atas selesai:

1. **Configure Tunnel**
   ```powershell
   .\setup-cloudflare-tunnel.ps1 -DomainName "9router" -TunnelId "YOUR_TUNNEL_ID"
   ```

2. **Install as Windows Service (Auto-Start)**
   ```powershell
   .\install-tunnel-autostart.ps1
   ```

### Keamanan

- ✅ Menggunakan sistem login bawaan 9Router (tidak ada custom auth)
- ✅ Session cookie hanya berlaku selama browser terbuka (session-only)
- ✅ Password dashboard wajib untuk akses publik
- ✅ Tidak ada "remember me" atau persistent login
- ✅ Auto-logout saat tab ditutup

### Status Deployment

⏳ **Menunggu langkah manual:**
- Domain registration di DigitalPlat
- Cloudflare account setup
- Nameserver configuration
- Tunnel creation & authentication

✅ **Siap otomatis:**
- cloudflared installation
- Setup scripts
- Auto-start configuration