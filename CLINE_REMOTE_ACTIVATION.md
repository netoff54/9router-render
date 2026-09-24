> ## ⚠️ DEPRECATED — JANGAN DIKUTI
> File ini berisi instruksi yang **TIDAK AMAN** (mengedit `%APPDATA%\Claude\globalState.json`
> dan `providers.json` — file konfigurasi aplikasi lain, bukan Cline, dan berisiko membajak
> traffic/API key aplikasi tersebut).
>
> ✅ **Ganti dengan:** `REMOTE_MODE_TOGGLE.md` — toggle aman berbasis prompt,
> tanpa menyentuh file konfigurasi aplikasi apa pun. Cline memuat aturannya otomatis
> dari `.clinerules/remote-mode.md`.

# 🚀 PROMPT #1: Aktifkan Cline untuk Remote Railway Access

**Jalankan ini untuk setup Cline agar bisa akses 9Router di Railway**

---

## ⚙️ Setup Cline untuk Railway 9Router

### Step 1: Update globalState.json

**Lokasi:** `%APPDATA%\Claude\globalState.json`

**Tambah/ubah ke:**
```json
{
  "openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1",
  "defaultModelId": "mimo-v2.5-free"
}
```

### Step 2: Update providers.json

**Lokasi:** `%APPDATA%\Claude\providers.json`

**Tambah section:**
```json
{
  "providers": [
    {
      "name": "9Router Railway (Remote)",
      "id": "railway-9router",
      "type": "openai",
      "baseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1",
      "apiKey": "sk-05b0d0b73a8aee96-25ki8w-e142ea50",
      "headers": {
        "Authorization": "Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50",
        "Content-Type": "application/json"
      }
    }
  ]
}
```

### Step 3: Verify Connection

Buka Cline dan coba message pertama:
```
Test connection to Railway 9Router
```

Jika berhasil → Cline akan connect ke endpoint Railway (bukan lokal).

### Step 4: Restart Cline (if needed)

Jika masih connect ke lokal, restart VS Code.

---

## ✅ Success Indicators

✅ Cline model dropdown menampilkan Railway models
✅ Response datang dari Railway endpoint (cek latency ~200ms+)
✅ Chat messages terproses di Railway
✅ Dashboard Railway menunjukkan activity

---

**DONE! Cline sekarang connect ke Railway 9Router.** 🎉
