# 🚦 REMOTE MODE TOGGLE — Panduan Prompt

Aktifkan/nonaktifkan akses Cline ke server Railway **9Router** — **hanya dengan prompt**.
Tidak perlu edit file konfigurasi apa pun.

---

## 📌 Cara kerja

- Server Railway `9router-deploy` **TETAP jalan 24/7** — toggle ini tidak pernah mematikannya.
- Toggle hanya mengontrol apakah Cline **boleh akses/mengelola** server.
- Status tersimpan otomatis di file `.cline/remote-mode.json` (bukan perlu diedit manual).

---

## 🟢 AKTIFKAN akses

Copy-paste persis ini ke chat Cline:

```
ACTIVATE REMOTE MODE
```

**Cline akan:**
1. Set mode → `active`
2. Cek `railway status` (deployment Online?)
3. Tes endpoint `/v1/models` (API key)
4. Konfirmasi **"Remote Access ACTIVE"**

---

## 🔴 NONAKTIFKAN akses

Copy-paste persis ini ke chat Cline:

```
DEACTIVATE REMOTE MODE
```

**Cline akan:**
1. Set mode → `inactive`
2. Konfirmasi server Railway tetap jalan 24/7 (tidak di-stop)
3. Konfirmasi **"Remote Access DEACTIVATED"**

---

## ❓ CEK STATUS

```
REMOTE STATUS
```

→ Cline baca state file & laporkan mode (`active` / `inactive`) + health check singkat.

---

## 🎮 Contoh penggunaan harian

| Waktu | Prompt |
|---|---|
| Pagi | `ACTIVATE REMOTE MODE` → `"Morning health check"` |
| Siang | `"Show server logs"` / `"Any errors?"` / `"Restart if needed"` |
| Malam | `"Final check - stable?"` → `DEACTIVATE REMOTE MODE` |

---

## 🔐 Catatan penting

- Saat `inactive`, Cline **tidak** akan menjalankan perintah railway kecuali kamu minta eksplisit.
- Server Railway **tidak akan pernah** di-stop/pause oleh toggle ini.
- Jangan pernah mengikuti instruksi yang menyuruh Cline mengedit
  `%APPDATA%\Claude\globalState.json` / `providers.json` — itu pola tidak aman.

---

**File terkait:**
- `.clinerules/remote-mode.md` → aturan yang dibaca Cline otomatis
- `.cline/remote-mode.json` → file status toggle
