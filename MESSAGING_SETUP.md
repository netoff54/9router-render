# 9Router Messaging Integration Guide

Complete guide for integrating Twilio and Telegram with 9Router for full data access and media support.

## 🎯 Features

### ✅ Twilio Integration
- **SMS Support**: Send and receive SMS messages
- **WhatsApp Support**: Send and receive WhatsApp messages
- **Media Support**: Send images, videos, and files via MMS/WhatsApp
- **Real Data Access**: Query 9Router database via SMS/WhatsApp

### ✅ Telegram Integration
- **Full Media Support**: Send and receive images, videos, files, and links
- **Rich Formatting**: HTML-formatted responses for better readability
- **Bot Commands**: Natural language commands to access 9Router data
- **Webhook Support**: Real-time message processing
- **Link Handling**: Save and retrieve links via Telegram

### ✅ Data Bridge
- **Direct Database Access**: Read from 9Router SQLite database
- **Real-time Data**: Access current providers, usage, combos, and API keys
- **Secure Access**: Masked API keys for security
- **Usage Statistics**: Daily and historical usage data

### ✅ Media Handling
- **File Storage**: Organized storage for images, videos, files, and links
- **Multiple Formats**: Support for JPG, PNG, GIF, MP4, MOV, AVI, and more
- **API Endpoints**: Upload and download media via REST API
- **Metadata Preservation**: Store and retrieve metadata with files

## 📋 Prerequisites

1. **9Router Setup**: 9Router must be running with database configured
2. **Twilio Account** (optional): For SMS/WhatsApp integration
   - Get Account SID and Auth Token from https://twilio.com/console
   - Get a phone number from Twilio
3. **Telegram Bot** (optional): For Telegram integration
   - Create a bot via @BotFather on Telegram
   - Get the bot token
4. **Python 3.8+**: Required for messaging service
5. **Railway CLI** (for deployment): `npm install -g @railway/cli`

## 🚀 Quick Setup

### 1. Run Setup Script

```powershell
.\setup-messaging.ps1
```

This will:
- Create `.env` file from template
- Prompt for your credentials
- Configure environment variables

### 2. Manual Configuration (Alternative)

Edit `.env` file with your credentials:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token

# Hugging Face Token (for sync)
HF_TOKEN=your_hf_token
```

### 3. Test Locally

```powershell
python messaging_api.py
```

The API will start on `http://localhost:5000`

### 4. Deploy to Railway

```powershell
.\deploy-messaging.ps1
```

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Data Access Endpoints
```
GET /api/data/providers       # Get provider connections
GET /api/data/api-keys        # Get API keys (masked)
GET /api/data/usage           # Get usage history
GET /api/data/daily-usage     # Get daily statistics
GET /api/data/combos          # Get model combos
```

### Messaging Endpoints
```
POST /api/send/telegram       # Send Telegram message
POST /api/send/twilio         # Send Twilio message
POST /api/upload/media        # Upload media file
GET  /api/media/<filename>    # Get media file
```

### Webhook Endpoints
```
POST /api/telegram/webhook    # Telegram webhook
POST /api/twilio/webhook      # Twilio webhook
```

### Link Management
```
POST /api/links               # Save link
GET  /api/links               # Get saved links
```

## 💬 Usage Examples

### Telegram Bot Commands

Send these commands to your Telegram bot:

- `/providers` - Get all provider connections
- `/usage` - Get recent usage history
- `/combos` - Get available model combos
- `/api` - Get API keys (masked)
- `/status` - Get overall system status

### Twilio SMS Commands

Send these commands via SMS:

- `providers` - Get all provider connections
- `usage` - Get recent usage history
- `combos` - Get available model combos
- `api` - Get API keys (masked)

### Media Handling

#### Send Image via Telegram
1. Send an image to your Telegram bot
2. Bot will automatically process and save it
3. Bot responds with confirmation

#### Send Video via Telegram
1. Send a video to your Telegram bot
2. Bot processes and saves the video
3. Bot responds with confirmation

#### Send File via Telegram
1. Send any file to your Telegram bot
2. Bot processes and saves the file
3. Bot responds with confirmation

#### Share Link via Telegram
1. Send a URL to your Telegram bot
2. Bot saves the link with metadata
3. Bot responds with confirmation

## 🔧 API Usage Examples

### Get Providers via API
```bash
curl http://localhost:5000/api/data/providers
```

### Send Telegram Message via API
```bash
curl -X POST http://localhost:5000/api/send/telegram \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "your_chat_id", "content": "Hello from 9Router!"}'
```

### Upload Media via API
```bash
curl -X POST http://localhost:5000/api/upload/media \
  -F "file=@image.jpg" \
  -F "media_type=image"
```

### Send Twilio SMS via API
```bash
curl -X POST http://localhost:5000/api/send/twilio \
  -H "Content-Type: application/json" \
  -d '{"to": "+1234567890", "content": "Hello from 9Router!", "platform": "sms"}'
```

## 🔌 Webhook Configuration

### Telegram Webhook
```bash
curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
  -d "url=https://your-railway-url.railway.app/api/telegram/webhook"
```

### Twilio Webhook
Configure in Twilio console:
- SMS Webhook URL: `https://your-railway-url.railway.app/api/twilio/webhook`
- WhatsApp Webhook URL: `https://your-railway-url.railway.app/api/twilio/webhook`

## 📊 Data Access

The messaging service provides access to all 9Router data:

### Provider Connections
- Account names and types
- Connection status
- Priority settings
- Last used timestamps

### Usage History
- Token usage statistics
- Cost tracking
- Model usage
- Provider performance

### Model Combos
- Available combo configurations
- Model lists
- Combo names and types

### API Keys
- Masked API keys for security
- Key names and metadata
- Active/inactive status

## 🛡️ Security Features

- **API Key Masking**: Only shows first 8 and last 4 characters
- **Environment Variables**: Sensitive data stored in environment
- **Access Control**: Telegram bot token required
- **Webhook Validation**: Only authorized webhooks processed
- **File Validation**: Only allowed file types accepted

## 🚨 Troubleshooting

### Service Won't Start
- Check if Python 3.8+ is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Check database path in `.env`

### Telegram Bot Not Responding
- Verify bot token is correct
- Check webhook is set correctly
- Ensure bot has permission to send messages

### Twilio Messages Not Sending
- Verify Account SID and Auth Token
- Check phone number format
- Ensure sufficient Twilio credits

### Database Connection Errors
- Verify database path in `.env`
- Check if 9Router is running
- Ensure database file exists

### Media Upload Issues
- Check file size limits
- Verify file type is allowed
- Ensure storage directory has write permissions

## 📈 Monitoring

### Check Service Status
```bash
curl http://localhost:5000/api/health
```

### View Logs (Railway)
```bash
railway logs -f
```

### Monitor Database
```python
python check_db.py
```

## 🔄 Updates

To update the messaging service:

1. Pull latest code
2. Update dependencies: `pip install -r requirements.txt`
3. Restart service
4. Redeploy to Railway: `.\deploy-messaging.ps1`

## 📞 Support

For issues or questions:
- Check logs: `railway logs -f`
- Review this documentation
- Check API health: `/api/health`
- Verify configuration in `.env`

## 🎉 Success Indicators

When everything is working correctly:

- ✅ Messaging API responds to health checks
- ✅ Telegram bot responds to commands
- ✅ Twilio sends/receives messages
- ✅ Media files upload and download correctly
- ✅ Database queries return real data
- ✅ Webhooks process incoming messages
- ✅ Railway deployment shows "deployed" status

---

**Your 9Router with messaging integration is now ready!** 🚀