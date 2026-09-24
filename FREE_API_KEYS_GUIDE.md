# Free API Keys Guide for 9Router Providers

This guide shows you how to get free API keys for the providers that are currently disabled in your 9Router setup.

## 🔧 Currently Disabled Providers

The following providers are temporarily disabled due to invalid API keys:
- **MISTRAL** - Invalid API Key
- **GROQ** - Invalid API Key  
- **CLOUDFLARE-AI** - Invalid access token
- **COHERE** - Incorrect API Key

## 🚀 How to Get Free API Keys

### 1. MISTRAL AI (Free, No Credit Card Required)

**Steps:**
1. Go to [console.mistral.ai](https://console.mistral.ai)
2. Create an account (email + phone verification required)
3. Navigate to **API Keys** in the left sidebar
4. Click **Create new key**
5. Give it a name (e.g., "9Router-Mistral")
6. Click **Create** and copy the key immediately

**Free Tier Limits:**
- 500,000 tokens per minute
- 1,000,000,000 tokens per month
- No credit card required
- Phone verification required

**Important:** You must activate a billing plan (even the free Experiment plan) for the API key to work.

### 2. GROQ AI (Free, No Credit Card Required)

**Steps:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google, GitHub, or email
3. Verify your email
4. Click **API Keys** in the left sidebar
5. Click **Create API Key**
6. Give it a name (e.g., "9Router-Groq")
7. Click **Create** and copy the key immediately

**Free Tier Limits:**
- 14,400 requests per day
- 30-100 requests per minute (varies by model)
- 6,000-15,000 tokens per minute
- 500,000 tokens per day total
- No credit card required
- No expiration (standing free tier)

### 3. CLOUDFLARE WORKERS AI (Free, No Credit Card Required)

**Steps:**
1. Go to [cloudflare.com](https://cloudflare.com) and create an account
2. Go to **Workers AI** in the dashboard
3. Select **Use REST API**
4. Click **Create a Workers AI API Token**
5. Review the prefilled information
6. Click **Create API Token**
7. Copy the API Token
8. Copy your **Account ID** from the dashboard sidebar

**Free Tier Limits:**
- 10,000 neurons per day (free)
- $0.011 per 1,000 neurons above free tier
- No credit card required for free tier
- 50+ open-source models available

### 4. COHERE AI (Free Trial, No Credit Card Required)

**Steps:**
1. Go to [dashboard.cohere.com](https://dashboard.cohere.com)
2. Create an account
3. A trial key is automatically generated on signup
4. Click **API Keys** in the left sidebar
5. Copy the trial key

**Free Trial Limits:**
- 1,000 total API calls per month
- Per-minute rate limits vary by endpoint
- No credit card required
- Trial keys are for non-commercial use only
- Production keys require paid plan

## 📝 After Getting Your API Keys

Once you have your new API keys, run the following command to update the database:

```bash
python update_provider_keys.py
```

Then provide the new keys in the format:
```
provider_name:new_api_key
```

Example:
```
mistral:your_new_mistral_key_here
groq:your_new_groq_key_here
cloudflare-ai:your_new_cloudflare_token
cohere:your_new_cohere_key
```

## 🎯 Current Working Providers

These providers are currently working and don't need updates:

✅ **GEMINI** - 2 working keys
✅ **OPENROUTER** - 446 models available  
✅ **NVIDIA** - 4 connections (key, cline, onet, milihsesuai) - 81 models
✅ **CEREBRAS** - 3 models available
✅ **KIRO** - 10 OAuth accounts (no test endpoint)
✅ **LLM7** - 2 connections (onet, cline1)
✅ **BAZAARLINK** - 2 connections (onet, cline 1)
✅ **OLLAMA** - 2 connections (onet, cline 1)

## 🔄 Re-enabling Disabled Providers

After updating the API keys, run:

```bash
python enable_failing_providers.py
```

This will re-enable the disabled providers with the new keys.

## 📊 Status Summary

- **Total Provider Connections:** 28
- **Active Providers:** 24
- **Working Providers:** 8/24 testable providers
- **Disabled Providers:** 4 (Mistral, Groq, Cloudflare-AI, Cohere)
- **Custom Providers:** 8 (Kiro, LLM7, Bazaarlink, Ollama - no test endpoints)

## ⚠️ Important Notes

1. **Security:** Never share your API keys publicly
2. **Rotation:** Consider rotating keys regularly for security
3. **Limits:** Monitor your usage to stay within free tier limits
4. **Backup:** Keep your keys in a secure password manager
5. **Testing:** Always test new keys before using in production

## 🆘 Troubleshooting

If you still get 401 errors after updating keys:
- Verify the key was copied correctly
- Check that billing is activated (especially for Mistral)
- Ensure the key has the correct permissions
- Try regenerating the key if it's corrupted

---

**Generated:** 2026-09-15
**9Router Status:** Most providers working, 4 providers need new API keys
