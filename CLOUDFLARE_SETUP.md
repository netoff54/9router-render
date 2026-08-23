# Cloudflare Tunnel Setup for 9Router

## Domain Registration Process (Manual Steps Required)

Based on research, **DigitalPlat dpdns.org** is the best option for free permanent domains compatible with Cloudflare nameservers in 2026.

### Registration Steps:

1. **Create DigitalPlat Account**
   - Go to: https://dash.domain.digitalplat.org/auth/register
   - Fill in required information (name, email, phone format: +1-**********, address with commas)
   - Verify email via activation link sent to your inbox

2. **GitHub KYC Verification**
   - Login to dashboard: https://dash.domain.digitalplat.org/auth/login
   - Complete GitHub OAuth verification (Login with GitHub)
   - Star the GitHub repo for extra domain quota: https://github.com/DigitalPlatDev/FreeDomain
   - Verify star at: https://dash.domain.digitalplat.org/auth/kyc/github

3. **Register Domain**
   - Go to Domain Registration page
   - Enter desired domain name (e.g., `9router.dpdns.org`)
   - Select `.dpdns.org` suffix
   - Check availability and register
   - Note: Default 1 domain free, +1 after GitHub star verification

4. **Configure Nameservers**
   - After registration, you'll need to set nameservers to Cloudflare
   - Cloudflare nameservers will be provided after adding domain to Cloudflare account
   - Update NS records in DigitalPlat dashboard

## Cloudflare Setup (Automated Parts)

### Prerequisites:
- Cloudflare account (free tier)
- Domain registered with DigitalPlat
- cloudflared installed (✅ Already done)

### Setup Steps:

1. **Add Domain to Cloudflare**
   - Login to Cloudflare dashboard
   - Add your registered domain (e.g., `9router.dpdns.org`)
   - Select Free plan
   - Copy the assigned nameservers (usually: `xxx.ns.cloudflare.com`, `yyy.ns.cloudflare.com`)

2. **Update Nameservers at DigitalPlat**
   - Go to DigitalPlat dashboard → Domains → Your domain
   - Update NS records with Cloudflare nameservers
   - Wait for DNS propagation (2-48 hours)

3. **Create Cloudflare Tunnel**
   - Run: `cloudflared tunnel login` (requires browser authentication)
   - Create tunnel: `cloudflared tunnel create 9router-tunnel`
   - Note the tunnel ID

4. **Configure Tunnel**
   - Create config file: `~/.cloudflared/config.yml`
   - Set up routing to local 9Router (http://localhost:20128)
   - Configure public hostname

5. **Install as Service**
   - Run: `cloudflared service install`
   - Configure auto-start with Windows

## Current Status

✅ cloudflared installed (version 2026.8.2)
✅ Researched domain options - DigitalPlat dpdns.org recommended
⏳ Domain registration - requires manual steps
⏳ Cloudflare account setup - requires manual authentication
⏳ Tunnel creation - pending domain and account setup

## Next Manual Steps Required

1. Register domain at DigitalPlat (requires email verification, GitHub OAuth)
2. Create/login to Cloudflare account (requires browser authentication)
3. Add domain to Cloudflare and get nameservers
4. Update nameservers at DigitalPlat
5. Run `cloudflared tunnel login` for authentication
6. Complete tunnel configuration

## Security Configuration

Per requirements:
- Use existing 9Router login system (no custom auth)
- Ensure session-only cookies (no persistent login)
- Test password protection on public domain
- Verify auto-logout on tab close