# Oracle Cloud Deployment Guide untuk 9Router

## ⚠️ Realitas Check

Ini adalah **satu-satunya opsi cloud hosting yang benar-benar gratis** dengan resources cukup untuk 9Router, TAPI:

- ❌ **WAJIB punya credit card** (untuk verification saja, tidak di-charge)
- ❌ Setup rumit (butuh technical knowledge)
- ❌ ARM architecture (perlu adjustment untuk 9Router)

## 📋 Oracle Cloud Always Free Specs

- **Compute**: 2 Arm Ampere cores + 12GB RAM (always-on)
- **Storage**: 200GB block storage
- **Bandwidth**: 10TB/month outbound
- **Network**: IPv4 address included
- **Duration**: Selamanya gratis (selama dalam limit)

## 🚀 Deployment Steps

### Step 1: Sign Up Oracle Cloud (Manual - Wajib CC)

1. **Buka**: https://www.oracle.com/cloud/free/
2. **Click**: "Try Free Tier"
3. **Fill Information**:
   - Email address
   - Real name & address (harus match dengan CC billing address)
   - Phone number (untuk OTP)
   - **Credit/Debit Card** (Visa/MasterCard - untuk verification)
4. **Select Home Region**: Pilih region dengan capacity (Singapore, Tokyo, Mumbai)
5. **Verify**: Email OTP + SMS OTP
6. **Wait Approval**: Biasanya instant, kadang butuh 1-2 jam

**⚠️ Penting**:
- Gunakan credit card yang valid (bukan virtual/prepaid kalau bisa)
- Billing address harus match persis dengan bank records
- Jangan gunakan VPN saat signup
- Oracle akan temporary hold $1-5 untuk verification (akan di-release)

### Step 2: Create Instance

1. **Login ke**: https://cloud.oracle.com
2. **Navigate**: Compute → Instances → Create Instance
3. **Configure**:
   - **Name**: 9router-server
   - **Shape**: VM.Standard.E4.Flex (Always Free Eligible)
   - **OCPU**: 2 (Always Free limit)
   - **Memory**: 12GB (Always Free limit)
   - **Operating System**: Oracle Linux 8 atau Ubuntu 22.04
   - **SSH Key**: Upload atau create new SSH key pair
4. **Networking**: Use default VCN (Virtual Cloud Network)
5. **Create**: Instance akan terdeploy dalam 2-5 menit

### Step 3: Setup Server Environment

**SSH ke instance:**
```bash
ssh -i ~/.ssh/your-key.pem ubuntu@your-public-ip
```

**Update system:**
```bash
sudo apt update && sudo apt upgrade -y
```

**Install Node.js 20+ (9Router requirement):**
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**Install build tools (untuk native modules):**
```bash
sudo apt install -y build-essential python3
```

**Install PM2 (process manager):**
```bash
sudo npm install -g pm2
```

### Step 4: Deploy 9Router

**Clone atau upload 9Router workspace:**
```bash
# Option 1: Upload dari lokal
scp -i ~/.ssh/your-key.pem -r "D:\Milih Sesuai\9router claudeflare" ubuntu@your-public-ip:/home/ubuntu/

# Option 2: Git clone jika di GitHub
git clone your-9router-repo
```

**Setup di server:**
```bash
cd /home/ubuntu/9router-claudeflare
npm install
```

**Start 9Router dengan PM2:**
```bash
pm2 start npm --name "9router" -- start
pm2 save
pm2 startup
```

### Step 5: Configure Firewall

**Di Oracle Cloud Console:**
1. Navigate ke instance → Virtual Cloud Network
2. Security Lists → Ingress Rules
3. Add rule:
   - Source: 0.0.0.0/0
   - IP Protocol: TCP
   - Destination Port: 20128
   - Description: 9Router Dashboard

**Di server (jika perlu):**
```bash
sudo firewall-cmd --permanent --add-port=20128/tcp
sudo firewall-cmd --reload
```

### Step 6: Setup Domain (Opsional)

**Gunakan nxtdev.xyz (gratis):**
1. Claim domain di https://nxtdev.xyz
2. Di Oracle Cloud, create DNS zone atau CNAME record
3. Point domain ke instance public IP

**Atau gunakan IP langsung:**
- Access via: `http://your-public-ip:20128`

### Step 7: Setup Auto-Start & Monitoring

**PM2 sudah auto-start**, tapi tambahkan:

**Systemd service (optional):**
```bash
sudo nano /etc/systemd/system/9router.service
```

```
[Unit]
Description=9Router AI Router
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/9router-claudeflare
ExecStart=/usr/bin/pm2 start npm -- start
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable 9router
sudo systemctl start 9router
```

**Monitoring:**
```bash
pm2 monit
pm2 logs 9router
```

## 🔧 Troubleshooting Oracle Cloud

### Instance tidak bisa create
- **Error**: "Out of capacity"
- **Solution**: Coba region lain (Singapore, Tokyo, Mumbai) atau coba di off-peak hours

### Credit card declined
- **Error**: "Payment method declined"
- **Solution**: Gunakan Visa/MasterCard internasional, atau virtual card dari Payoneer/Privacy.com

### SSH permission denied
- **Error**: "Permission denied (publickey)"
- **Solution**: Check permission SSH key: `chmod 400 ~/.ssh/your-key.pem`

### Port tidak accessible
- **Error**: Connection timeout
- **Solution**: Check Security List Ingress Rules di Oracle Console

### 9Router memory issue
- **Error**: Out of memory
- **Solution**: Setup swap file:
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 💰 Cost Management

**Untuk menghindari charge:**
1. Setup budget alert di Oracle Console
2. Pastikan instance bertanda "Always Free Eligible"
3. Jangan create shape di luar Always Free limit
4. Monitor usage dashboard secara regular

**Always Free Limits:**
- 2 OCPUs + 12GB RAM compute
- 200GB block storage
- 10TB/month bandwidth

## 📊 Performance Expectations

- **CPU**: 2 Arm Ampere cores (baik untuk multi-threading)
- **RAM**: 12GB (cukup untuk 9Router + buffer untuk memory leak)
- **Storage**: NVMe SSD (fast I/O untuk SQLite)
- **Network**: Bervariasi tergantung region

## ⚠️ Limitations

1. **ARM Architecture**: 9Router perlu test untuk compatibility
2. **Setup Complexity**: Butuh Linux knowledge
3. **Verification**: Butuh credit card (walau tidak di-charge)
4. **Region Lock**: Home region tidak bisa diubah setelah signup

## 🎯 Summary

**Pros:**
- ✅ Benar-benar gratis selamanya
- ✅ Resources besar (12GB RAM)
- ✅ 24/7 uptime
- ✅ Full control

**Cons:**
- ❌ Butuh credit card verification
- ❌ Setup rumit (1-2 jam)
- ❌ ARM architecture
- ❌ Butuh technical knowledge

**Total Setup Time:** 1-2 jam (termasuk approval)
**Total Cost:** $0 (selama dalam Always Free limits)
**Maintenance:** Minimal (PM2 auto-restart)

---

**Alternative:** Jika tidak mau ribet dengan Oracle Cloud, pertimbangkan Railway ($5/bulan) - deploy dari GitHub dalam 15 menit.