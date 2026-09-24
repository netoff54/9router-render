> ## ⚠️ DEPRECATED — JANGAN DIKUTI
> File ini menyuruh mengedit `%APPDATA%\Claude\globalState.json`, `providers.json`,
> dan `models.json` (file aplikasi Claude Desktop, bukan Cline). Pola ini adalah
> vektor serangan peretasan API key — **jangan dilakukan**.
>
> ✅ **Ganti dengan:** `REMOTE_MODE_TOGGLE.md` — toggle aman berbasis prompt,
> tanpa menyentuh file konfigurasi aplikasi lain.

# ⚙️ Konfigurasi Cline untuk Railway 9Router

Deploy 9Router ke Railway, sekarang ubah Cline setting untuk terhubung.

---

## 🔗 CONNECTION FLOW

```
Cline (VS Code)
  ↓ HTTPS
  → https://9router-deploy-production-3a0f.up.railway.app/v1/chat/completions
  ↓
  → 9Router di Railway (routing)
  ↓
  → Model (mimo, claude, dll)
  ↓ Response
  ← Back to Cline
```

---

## 📝 File Konfigurasi Cline

### **1. globalState.json**

**Path:** `%APPDATA%\Claude\globalState.json`

**Change from:**
```json
{"openAiBaseUrl": "http://localhost:20128/v1"}
```

**Change to:**
```json
{"openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1"}
```

### **2. providers.json**

```json
{
  "name": "9Router Railway",
  "baseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1",
  "headers": {
    "Authorization": "Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"
  }
}
```

### **3. models.json**

```json
{
  "id": "mimo-v2.5-free",
  "baseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1",
  "provider": "9router-railway"
}
```

---

## 🔐 API Key

**Token:** `sk-05b0d0b73a8aee96-25ki8w-e142ea50`

**Header:**
```
Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50
```

---

## 🧪 Test Connection

```powershell
# Test 1: Ping
curl -I https://9router-deploy-production-3a0f.up.railway.app

# Test 2: Auth
curl https://9router-deploy-production-3a0f.up.railway.app/api/settings `
  -H "Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"

# Test 3: Models
curl https://9router-deploy-production-3a0f.up.railway.app/v1/models `
  -H "Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"
```

---

## 📱 Setup Cline

1. Edit `%APPDATA%\Claude\globalState.json`
2. Change base URL to Railway endpoint
3. Set API key in providers.json
4. Restart Cline
5. Test first message

---

## ✅ Checklist

- [ ] Railway deployment OK
- [ ] Dashboard accessible
- [ ] Changed password
- [ ] Updated globalState.json
- [ ] Updated providers.json
- [ ] Test curl requests pass
- [ ] Cline connects to Railway
- [ ] Chat works end-to-end

---

**Next:** Start using Cline with Railway! 🚀
