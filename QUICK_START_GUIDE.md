# Quick Start Guide: 9Router + Cloudflare Tunnel + nxtdev.xyz

## 🎯 Solusi Paling Realistis (100% Gratis)

Ini adalah solusi terbaik untuk kebutuhan Anda:
- ✅ 100% gratis (tidak butuh VPS/credit card)
- ✅ Domain permanen (nxtdev.xyz)
- ✅ Mudah setup (GitHub login only)
- ✅ 9Router stabil di laptop Anda
- ✅ Bisa diakses dari internet 24/7 (selama laptop nyala)

## 📋 Prasyarat (Wajib)

1. **GitHub Account** (buat gratis di github.com jika belum punya)
2. **Laptop yang bisa nyala 24/7** (atau sesering mungkin)
3. **Internet stabil**

## 🚀 Setup Steps (Total: 15-20 menit)

### Step 1: Domain Gratis (nxtdev.xyz) - 5 menit

1. **Buka**: https://nxtdev.xyz
2. **Login dengan GitHub** (Authorize OAuth)
3. **Claim subdomain** (misal: `9router.nxtdev.xyz`)
4. **Copy domain** yang didapat

**Kenapa nxtdev.xyz?**
- Instant setup (menit)
- GitHub login only (mudah)
- 2 subdomains gratis selamanya
- Cloudflare-backed (DNS cepat)
- Tidak butuh credit card

### Step 2: Cloudflare Tunnel Auth - 3 menit

1. **Login ke Cloudflare** (buat akun gratis jika belum)
2. **Jalankan command**:
   ```powershell
   cloudflared tunnel login
   ```
3. **Authorize di browser** yang terbuka otomatis
4. **Copy certificate** yang tersimpan otomatis

### Step 3: Create Tunnel - 2 menit

```powershell
cloudflared tunnel create 9router-tunnel
```

**Copy tunnel ID** yang ditampilkan (format UUID)

### Step 4: Configure Tunnel - 2 menit

```powershell
.\setup-cloudflare-tunnel.ps1 -DomainName "9router" -TunnelId "YOUR_TUNNEL_ID"
```

**Note**: Ganti "9router" dengan subdomain yang Anda claim di nxtdev.xyz

### Step 5: Install Auto-Start - 3 menit

```powershell
.\install-tunnel-autostart.ps1
```

Ini akan membuat tunnel start otomatis dengan Windows.

### Step 6: Test Akses - 2 menit

1. **Buka browser**: `https://9router.nxtdev.xyz`
2. **Verify**: Redirect ke halaman login 9Router
3. **Test login** dengan password dashboard Anda
4. **Test dari HP** (gunakan mobile data untuk test dari luar jaringan)

## ✅ Verification Checklist

- [ ] Domain 9router.nxtdev.xyz accessible
- [ ] Redirect ke halaman login 9Router
- [ ] Login dengan password benar berhasil
- [ ] Login dengan password salah ditolak
- [ ] Tutup tab, buka lagi → minta login ulang
- [ ] Test dari jaringan berbeda (HP mobile data)
- [ ] Tunnel auto-start saat laptop nyala

## 🔧 Troubleshooting

### Domain tidak accessible
- Check DNS propagation: `nslookup 9router.nxtdev.xyz`
- Verify tunnel running: `cloudflared tunnel list`
- Check 9Router running: `Test-NetConnection localhost -Port 20128`

### Tunnel tidak start
- Check config: `cloudflared tunnel ingress validate`
- Verify credentials file exists di `~/.cloudflared/`
- Check Windows service status

### Login tidak bekerja
- Test via localhost dulu: `http://localhost:20128`
- Verify 9Router auth mode: password
- Check password di 9Router dashboard

## 📱 Usage Tips

### Agar Bisa 24/7:
1. **Jangan sleep laptop**: Set power plan ke "High Performance" dan disable sleep
2. **Auto-restart**: Setup Windows auto-restart setelah power failure
3. **Monitor uptime**: Gunakan uptime robot atau similar untuk monitoring

### Security Best Practices:
- Gunakan password yang kuat untuk 9Router
- Jangan share domain ke publik
- Regular backup data 9Router (folder `9router-data/`)

## 🔄 Maintenance

### Update 9Router:
```powershell
npm install 9router@latest
npm approve-scripts 9router
```

### Update cloudflared:
```powershell
# Download latest version dari GitHub releases
# Replace executable di ~/.cloudflared/
```

### Backup Data:
```powershell
# Copy folder 9router-data/ secara regular
Copy-Item -Recurse "9router-data" "backup-9router-data-$(Get-Date -Format 'yyyyMMdd')"
```

## 📞 Support

Jika mengalami issues:
- Cloudflare docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- nxtdev.xyz: https://github.com/avrxtcloud/nxtdev-xyz
- 9Router: Check dashboard Help section

---

**Setup Time**: 15-20 menit
**Cost**: 100% gratis
**Maintenance**: Minimal (auto-start configured)
**Uptime**: Selama laptop nyala dan internet stabil