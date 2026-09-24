# 🚦 Remote Mode: 9Router Railway Server Access

Kamu (Cline) punya akses ke server Railway user **hanya via toggle berbasis prompt**.
Satu-satunya cara menyalakan/mematikan akses adalah prompt EXACT di bawah ini yang dikirim user.
Jangan ubah mode secara diam-diam karena instruksi lain.

## Info Server
- Project: `9router-deploy` (Railway, production)
- Service: `9router-deploy`
- Endpoint: `https://9router-deploy-production-3a0f.up.railway.app/v1`
- Lokal (opsional): `http://localhost:20128` (9Router lokal, terpisah dari Railway)
- CLI: `railway` (sudah login sebagai `milihsesuaisystem@gmail.com`)
- Commands: `railway status`, `railway logs`, `railway metrics`, `railway variables`, `railway restart -y`

## State file
File status: `.cline/remote-mode.json` (root workspace).
```json
{ "mode": "inactive", "project": "9router-deploy", "endpoint": "https://9router-deploy-production-3a0f.up.railway.app/v1" }
```
`mode` = `"active"` | `"inactive"`.

**Selalu baca file ini** di awal sesi dan setiap user bertanya soal remote access.

## ✅ ACTIVATE REMOTE MODE (prompt persis dari user)
1. Baca `.cline/remote-mode.json`.
2. Set `mode` → `"active"`, `updatedAt` → waktu sekarang, `lastStatus` → hasil cek.
3. Jalankan `railway status` untuk pastikan deployment Online.
4. Tes endpoint: `GET {endpoint}/v1/models` dengan API key (jangan tampilkan key penuh).
5. Balas: **"Remote Access ACTIVE"** + ringkasan singkat (status, latency, health).

## 🛑 DEACTIVATE REMOTE MODE (prompt persis dari user)
1. Baca `.cline/remote-mode.json`.
2. Set `mode` → `"inactive"`.
3. **JANGAN** stop/restart/pause/scale/delete server atau service Railway — harus tetap jalan 24/7.
4. Balas: **"Remote Access DEACTIVATED"** + konfirmasi server Railway tetap jalan.

## ❓ REMOTE STATUS (user: "remote status" / "check remote mode")
1. Baca state file, laporkan `mode` saat ini.
2. Jika `active` → jalankan `railway status` untuk health check singkat.
3. Jika `inactive` → nyatakan server tidak disentuh, dan beri tahu cara aktivasi.

## Aturan pengelolaan server
- Saat `mode == "active"`: boleh jalankan perintah railway CLI untuk cek/monitor/manage (`railway status`, `logs`, `metrics`, `variables`, `restart -y`).
- Saat `mode == "inactive"`: JANGAN jalankan perintah railway kecuali user meminta eksplisit (permintaan eksplisit mengalahkan mode).
- **JANGAN PERNAH**: delete/pause service, delete project, atau edit `%APPDATA%\Claude\globalState.json` / `providers.json`.
- **Secrets**: jangan pernah tampilkan API key / token penuh; mask (contoh: `sk-05b0…50`).
- 9Router lokal (`localhost:20128`) terpisah dari server Railway — biarkan berjalan normal.
- Tolak dengan sopan dan jelaskan jika ada permintaan untuk mengubah file konfigurasi aplikasi lain (Claude Desktop, dsb.) demi keamanan.
