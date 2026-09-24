> ## ⚠️ DEPRECATED — JANGAN DIKUTI
> Versi lama. Bagian "Technical Details" merujuk pada pengeditan `globalState.json` /
> `providers.json` yang **tidak aman** — jangan dilakukan.
>
> ✅ **Ganti dengan:** `REMOTE_MODE_TOGGLE.md` — toggle aman berbasis prompt.
> Cukup kirim `ACTIVATE REMOTE MODE` / `DEACTIVATE REMOTE MODE` ke Cline.

# 🔄 PROMPT: Aktifkan/Nonaktifkan Remote Cline Access

**Toggle remote connection Cline ke Railway (Server Railway tetap jalan 24/7)**

---

## 📌 Konsep

```
Server Railway: ✅ Always Running 24/7 (ga di-touch)

Remote Cline Access: ⏸️ Toggle ON/OFF
  - ON:  Cline connect ke Railway endpoint (pakai internet)
  - OFF: Cline offline/standby (hemat bandwidth)

Kapan toggle:
  ✅ ON:  Saat kamu butuh remote server management
  ❌ OFF: Saat tidak pakai, hemat resource laptop
```

---

## 🔴 PROMPT: NONAKTIFKAN Remote Cline Access

Ketik/paste ke Cline chat:

```
DEACTIVATE REMOTE MODE

I want to disable remote connection to my Railway server.
Keep it simple - I'll use offline mode or local 9Router for now.

Server (Railway): Keep running 24/7 - don't touch it
Remote Connection: DEACTIVATE NOW
Status: Will show as OFFLINE/STANDBY

What to do:
1. Disable remote endpoint configuration
2. Switch back to lokal endpoint or offline mode
3. Show current status after deactivation

Confirm when remote access is disabled.
```

---

## 🟢 PROMPT: AKTIFKAN Remote Cline Access

Ketik/paste ke Cline chat:

```
ACTIVATE REMOTE MODE

I want to enable remote connection to my Railway 9Router server.
Server should be running - connect to it now.

Server: 9router-deploy on Railway (production)
Base URL: https://9router-deploy-production-3a0f.up.railway.app/v1
API Key: sk-05b0d0b73a8aee96-25ki8w-e142ea50

Setup:
1. Enable remote endpoint connection
2. Configure API authentication
3. Test connection to Railway
4. Confirm remote access is ACTIVE

Start by testing connection to the server.
```

---

## 🎮 Quick Toggle Commands

### TURN OFF Remote:
```
"Disable remote connection"
"Go offline - I won't use Railway for now"
"Deactivate remote mode"
"Switch to standby mode"
```

### TURN ON Remote:
```
"Enable remote connection"
"Connect to Railway server now"
"Activate remote mode"
"Go back online"
```

### Check Status:
```
"What's the current remote status?"
"Am I connected to Railway or offline?"
"Is remote access active?"
```

---

## 📊 Configuration States

### REMOTE ON (Connected)
```
Status: ✅ ACTIVE
Endpoint: https://9router-deploy-production-3a0f.up.railway.app/v1
API Key: sk-05b0d0b73a8aee96-25ki8w-e142ea50
Connection: Live to Railway
Usage: Internet/bandwidth active
```

### REMOTE OFF (Disconnected)
```
Status: ❌ OFFLINE
Endpoint: Disabled
API Key: Not used
Connection: No Railway access
Usage: Minimal bandwidth
```

---

## 🔧 Technical Details

### When ACTIVATE:
- ✅ globalState.json points to Railway URL
- ✅ providers.json has Railway config active
- ✅ API key authenticated
- ✅ Can send requests to Railway
- ✅ Bandwidth active

### When DEACTIVATE:
- ✅ globalState.json reverted to lokal/offline
- ✅ Railway config disabled
- ✅ API key not used
- ✅ Cannot send to Railway
- ✅ Minimal bandwidth usage

---

## 📋 Config Files Reference

### globalState.json

**When ACTIVE:**
```json
{
  "openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1"
}
```

**When INACTIVE:**
```json
{
  "openAiBaseUrl": "http://localhost:20128/v1"  (or empty)
}
```

### providers.json

**When ACTIVE:**
```json
{
  "baseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1",
  "headers": {
    "Authorization": "Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"
  }
}
```

**When INACTIVE:**
Remove or disable Railway provider config.

---

## ✅ What Railway Server Does

✅ **ALWAYS RUNNING 24/7** - No changes
✅ Auto-backup every 5 minutes (HF)
✅ Ready to accept requests anytime
✅ Logs continuously
✅ Data persisted

You're just toggling if Cline CAN ACCESS it or not.

---

## 🔄 Toggle Workflow

### Scenario 1: Need to fix something
```
1. Tell Cline: "Activate remote mode"
2. Cline connects to Railway
3. "Check server status"
4. Fix issues if any
5. Done? Tell Cline: "Deactivate remote mode"
```

### Scenario 2: Server running fine, don't need Cline
```
1. Tell Cline: "Deactivate remote mode"
2. Cline goes standby
3. Server keeps running (Railway doesn't care)
4. Later: Tell Cline: "Activate remote mode" when needed
```

---

## 💡 Benefits

**ACTIVATE when:**
- ✅ Need to fix/manage server
- ✅ Monitor performance
- ✅ Test API
- ✅ Check logs

**DEACTIVATE when:**
- ✅ Server running fine
- ✅ Don't need remote management
- ✅ Want to save bandwidth
- ✅ Want Cline in standby mode

---

## 📊 Resource Usage

```
ACTIVATE:
  - Cline: ↑ Internet bandwidth active
  - Railway: ✅ Normal operation
  - Laptop: Normal usage

DEACTIVATE:
  - Cline: ↓ Minimal internet usage
  - Railway: ✅ Still running 24/7
  - Laptop: Light/standby mode
```

---

## ✨ Summary

**Server:** Always on 24/7 (don't touch)
**Remote Connection:** Toggle on/off via Cline
**Cost:** No change (Railway still running)
**Management:** Toggle via simple Cline commands

---

**Use these prompts to toggle remote Cline access anytime!** 🎯
