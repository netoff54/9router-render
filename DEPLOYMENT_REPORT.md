# 9Router Cloudflare Tunnel Deployment Report

## Executive Summary

Setup untuk deploy 9Router agar bisa diakses 24/7 dari internet via Cloudflare Tunnel dengan domain gratis permanen telah dipersiapkan. Sebagian besar langkah otomatis sudah selesai, namun ada beberapa langkah manual yang memerlukan interaksi user karena keterbatasan tools (CAPTCHA, verifikasi email, approval browser).

## Status Komponen

### ✅ Selesai (Otomatis)

1. **Workspace Analysis**
   - 9Router v0.5.55 sudah terinstall di workspace
   - Data tersimpan di `9router-data/` (bukan %APPDATA%)
   - Auto-start via Windows Startup folder sudah aktif
   - 9Router berjalan di background/tray

2. **cloudflared Installation**
   - cloudflared v2026.8.2 terinstall di `C:\Users\muham\.cloudflared\`
   - Added to system PATH
   - Siap untuk tunnel creation

3. **Domain Research**
   - DigitalPlat dpdns.org terpilih sebagai opsi terbaik untuk 2026
   - Free, permanent, compatible dengan Cloudflare nameservers
   - Require GitHub verification (anti-abuse)

4. **Security Verification**
   - 9Router menggunakan sistem login bawaan (authMode: password)
   - Session-only cookies (tidak persistent)
   - Password dashboard wajib untuk akses
   - Tidak ada "remember me" feature

5. **Setup Scripts**
   - `setup-cloudflare-tunnel.ps1` - Configure tunnel setelah domain & tunnel ID tersedia
   - `install-tunnel-autostart.ps1` - Install tunnel sebagai Windows service
   - `CLOUDFLARE_SETUP.md` - Dokumentasi lengkap proses setup

### ⏳ Menunggu Langkah Manual

Langkah berikut **HARUS** dilakukan oleh user karena memerlukan:

1. **Interaksi Browser** (CAPTCHA, OAuth, popup approval)
2. **Verifikasi Email** (OTP di inbox)
3. **Keputusan Manual** (pilihan domain, persetujuan terms)

## Langkah Manual yang Diperlukan

### 1. Register Domain Gratis (DigitalPlat)

**URL:** https://dash.domain.digitalplat.org/auth/register

**Steps:**
1. Isi form registration (name, email, phone format: +1-**********, address dengan commas)
2. Verifikasi email via link di inbox
3. Login ke dashboard
4. Complete GitHub OAuth verification (Login with GitHub)
5. Star repo GitHub untuk quota tambahan: https://github.com/DigitalPlatDev/FreeDomain
6. Verify star di: https://dash.domain.digitalplat.org/auth/kyc/github
7. Register domain (misal: `9router.dpdns.org`)
8. Note: 1 domain gratis default, +1 setelah GitHub star

**Estimated Time:** 10-15 menit

### 2. Setup Cloudflare Account

**URL:** https://dash.cloudflare.com/sign-up

**Steps:**
1. Create akun Cloudflare (free tier, no credit card required)
2. Add domain yang sudah diregister di DigitalPlat
3. Select Free plan
4. Copy dua nameserver yang diberikan (format: `xxx.ns.cloudflare.com`, `yyy.ns.cloudflare.com`)

**Estimated Time:** 5-10 menit

### 3. Update Nameservers

**URL:** https://dash.domain.digitalplat.org/

**Steps:**
1. Login ke DigitalPlat dashboard
2. Navigate ke Domains → Your domain
3. Update NS records dengan nameserver Cloudflare
4. Tunggu DNS propagation (2-48 jam, biasanya <1 jam)

**Estimated Time:** 5 menit + waiting time

### 4. Create Cloudflare Tunnel

**Commands:**
```powershell
# Login (buka browser untuk auth)
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create 9router-tunnel

# Copy tunnel ID yang ditampilkan
```

**Steps:**
1. Jalankan `cloudflared tunnel login` - akan buka browser
2. Authorize cloudflared dengan akun Cloudflare Anda
3. Jalankan `cloudflared tunnel create 9router-tunnel`
4. Copy tunnel ID yang ditampilkan (format: UUID)

**Estimated Time:** 5 menit

### 5. Configure Tunnel

**Script:** `.\setup-cloudflare-tunnel.ps1`

**Command:**
```powershell
.\setup-cloudflare-tunnel.ps1 -DomainName "9router" -TunnelId "YOUR_TUNNEL_ID"
```

**Steps:**
1. Jalankan script dengan domain name dan tunnel ID
2. Script akan membuat config file otomatis
3. Validasi configuration
4. Pilih untuk start tunnel sekarang atau nanti

**Estimated Time:** 2 menit

### 6. Install Auto-Start Service

**Script:** `.\install-tunnel-autostart.ps1`

**Command:**
```powershell
.\install-tunnel-autostart.ps1
```

**Steps:**
1. Jalankan script (mungkin butuh Administrator privileges)
2. Script akan install tunnel sebagai Windows service
3. Pilih untuk start service sekarang
4. Tunnel akan otomatis start dengan Windows

**Estimated Time:** 3 menit

### 7. Final Testing

**Steps:**
1. Buka browser dan akses: `https://9router.dpdns.org` (ganti dengan domain Anda)
2. Verify redirect ke halaman login 9Router
3. Test login dengan password yang benar
4. Test akses dengan password yang salah (harus ditolak)
5. Tutup tab dan buka lagi - harus minta login ulang
6. Test dari jaringan berbeda (mobile data) jika memungkinkan

**Estimated Time:** 5 menit

## Total Estimated Manual Time: 30-45 menit (excluding DNS propagation)

## File yang Dibuat/Diupdate

1. **CLOUDFLARE_SETUP.md** - Dokumentasi lengkap setup process
2. **setup-cloudflare-tunnel.ps1** - Script untuk configure tunnel
3. **install-tunnel-autostart.ps1** - Script untuk install auto-start service
4. **README.md** - Updated dengan Cloudflare Tunnel section
5. **DEPLOYMENT_REPORT.md** - File ini (laporan lengkap)

## Security Configuration (Per Requirements)

✅ **No Custom Login System** - Menggunakan login bawaan 9Router saja
✅ **Password Protection** - Semua akses publik wajib password dashboard
✅ **Session-Only Cookies** - Tidak ada persistent login
✅ **No Remember Me** - Session habis saat tab ditutup
✅ **Auto-Logout** - Login ulang tiap buka tab baru

## Next Actions (Immediate)

1. Register domain di DigitalPlat (Section 1)
2. Setup Cloudflare account (Section 2)
3. Update nameservers (Section 3)
4. Create tunnel (Section 4)
5. Run setup script (Section 5)
6. Install auto-start (Section 6)
7. Test deployment (Section 7)

## Troubleshooting

### Tunnel tidak start
- Check jika config file valid: `cloudflared tunnel ingress validate`
- Verify 9Router berjalan: `Test-NetConnection localhost -Port 20128`
- Check Windows service status

### Domain tidak resolve
- Check nameserver configuration di DigitalPlat
- Tunggu DNS propagation (gunakan `nslookup` untuk test)
- Verify domain active di Cloudflare dashboard

### Login tidak bekerja
- Verify 9Router menggunakan authMode: password
- Check password di 9Router dashboard (Settings → Profile)
- Test login via localhost dulu: http://localhost:20128

## Contact & Support

Jika mengalami issues setelah mengikuti langkah manual:
- Cloudflare Tunnel docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- DigitalPlat support: https://github.com/DigitalPlatDev/FreeDomain
- 9Router docs: Check 9Router dashboard Help section

---

**Generated:** 2026-08-22
**Status:** Ready for manual deployment steps
**Automation:** 70% complete (30% requires manual interaction)