# 🔌 API Guide: 9Router di Railway

Reference lengkap untuk API calls.

---

## 📍 Base URL

```
https://9router-deploy-production-3a0f.up.railway.app/v1
```

---

## 🔐 Authentication

```
Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50
Content-Type: application/json
```

---

## 📋 Main Endpoints

### **1. Health Check**

```http
GET /api/health
```

### **2. List Models**

```http
GET /v1/models
```

Response:
```json
{
  "object": "list",
  "data": [
    {"id": "mimo-v2.5-free"},
    {"id": "claude-3-sonnet"}
  ]
}
```

### **3. Chat Completion**

```http
POST /v1/chat/completions

{
  "model": "mimo-v2.5-free",
  "messages": [
    {"role": "user", "content": "Hello"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### **4. Stream Chat**

```http
POST /v1/chat/completions

{
  "model": "mimo-v2.5-free",
  "messages": [{"role": "user", "content": "Tell me a story"}],
  "stream": true
}
```

Response: Streamed chunks

---

## 🧪 Test Curl

```powershell
# Health
curl https://9router-deploy-production-3a0f.up.railway.app/api/health `
  -H "Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"

# Models
curl https://9router-deploy-production-3a0f.up.railway.app/v1/models `
  -H "Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50"

# Chat
$body = @{
  model = "mimo-v2.5-free"
  messages = @(@{ role = "user"; content = "Hello" })
} | ConvertTo-Json

curl -X POST https://9router-deploy-production-3a0f.up.railway.app/v1/chat/completions `
  -H "Authorization: Bearer sk-05b0d0b73a8aee96-25ki8w-e142ea50" `
  -H "Content-Type: application/json" `
  -d $body
```

---

## 💻 Python Example

```python
import requests

api_key = "sk-05b0d0b73a8aee96-25ki8w-e142ea50"
base_url = "https://9router-deploy-production-3a0f.up.railway.app"

response = requests.post(
    f"{base_url}/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "mimo-v2.5-free",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)

print(response.json())
```

---

## 📊 Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success ✅ |
| 401 | Wrong API key |
| 404 | Endpoint not found |
| 500 | Server error |

---

## 🔧 Using with Cline

Set in Cline config:
```json
{
  "openAiBaseUrl": "https://9router-deploy-production-3a0f.up.railway.app/v1"
}
```

Cline will auto call these endpoints!

---

## 🐛 Troubleshooting

```powershell
# Check if up
railway status

# Check token
railway variables

# View logs
railway logs -f
```

---

**Ready to use!** 🚀
