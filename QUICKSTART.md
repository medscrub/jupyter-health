# MedScrub Jupyter Notebooks - Quick Start

## ✅ Auth Issues Fixed!

Both JWT tokens and API keys now work correctly with all Jupyter notebooks.

---

## 🚀 Getting Started (2 Options)

### Option 1: Demo API Key (Fastest - Already Configured)

**Status:** ✅ Ready to use

The `.env` file is already configured with the demo API key. Just run the notebooks!

```bash
# Start Jupyter
jupyter notebook notebooks/

# Run any notebook - authentication is automatic
```

**What's configured:**
```bash
MEDSCRUB_API_KEY=msk_test_demo0000000000000000000000000000
MEDSCRUB_API_URL=https://stage.api.medscrub.dev
```

**Good for:**
- Quick testing
- Learning the API
- Running examples
- No login required

---

### Option 2: JWT Token (Recommended for Production)

**Status:** ✅ JWT_SECRET now configured - tokens work!

#### Step 1: Get Your JWT Token

1. Visit https://medscrub.dev/playground
2. Login with your account (GitHub or Google)
3. Copy the JWT token displayed on the page

#### Step 2: Update .env File

Open `jupyter-health/.env` and uncomment these lines:

```bash
# Before:
# MEDSCRUB_JWT_TOKEN=your-jwt-token-from-medscrub.dev-playground
# MEDSCRUB_API_URL=https://api.medscrub.dev

# After:
MEDSCRUB_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Your actual token
MEDSCRUB_API_URL=https://api.medscrub.dev
```

Also comment out the API key:

```bash
# Before:
MEDSCRUB_API_KEY=msk_test_demo0000000000000000000000000000

# After:
# MEDSCRUB_API_KEY=msk_test_demo0000000000000000000000000000
```

#### Step 3: Restart Jupyter Kernel

In Jupyter: **Kernel → Restart & Clear Output**

#### Step 4: Run Notebooks

```python
# Cell 1 will now show:
✅ Authenticated with JWT token
📡 Connected to: https://api.medscrub.dev
```

**Good for:**
- Production usage
- Higher rate limits (with paid plans)
- User-specific analytics
- Team collaboration

---

## 📊 What Was Fixed

### Problem
JWT tokens from `medscrub.dev/playground` failed with:
```
❌ Authentication failed: Invalid or missing authentication
Cloudflare Worker logs: "Invalid JWT signature"
```

### Root Cause
`JWT_SECRET` was not configured in Cloudflare Worker environments.

### Solution Applied
✅ Set `JWT_SECRET` in Cloudflare Worker (dev, staging, production)
✅ Now matches the secret in Next.js app
✅ JWT signature validation works correctly

### Results
- ✅ JWT tokens from playground now work
- ✅ Demo API key continues to work
- ✅ All notebooks compatible with both methods

---

## 📚 Available Notebooks

1. **01_quickstart_api.ipynb** - 5-minute intro to MedScrub API
2. **02_mcp_powered_workflow.ipynb** - Claude Desktop integration
3. **03_fhir_resources.ipynb** - All supported FHIR resource types
4. **04_data_science_workflow.ipynb** - Complete diabetes research study
5. **05_mcp_demo_script.ipynb** - Hackathon demo with Synthea FHIR

---

## 🔍 Verify Your Setup

Run this test script:

```bash
cd jupyter-health

python3 -c "
from medscrub_client import MedScrubClient
import os
from dotenv import load_dotenv

load_dotenv()

# This will use whichever auth method is in .env
jwt_token = os.getenv('MEDSCRUB_JWT_TOKEN')
api_key = os.getenv('MEDSCRUB_API_KEY')
api_url = os.getenv('MEDSCRUB_API_URL', 'https://api.medscrub.dev')

if jwt_token:
    client = MedScrubClient(jwt_token=jwt_token, api_url=api_url)
    print('✅ Using JWT token authentication')
elif api_key:
    client = MedScrubClient(api_key=api_key, api_url=api_url)
    print('✅ Using API key authentication')

patient = {'resourceType': 'Patient', 'name': [{'family': 'Test'}]}
result = client.deidentify_fhir(patient)
print(f'✅ Authentication successful!')
print(f'   Session ID: {result[\"sessionId\"]}')
"
```

Expected output:
```
✅ Using API key authentication  # or "JWT token authentication"
✅ Authentication successful!
   Session ID: 1762018377918-y1bj3xdnl
```

---

## 🆘 Troubleshooting

### "Invalid or missing authentication"

**Check `.env` file:**
```bash
cat .env | grep -E "JWT_TOKEN|API_KEY|API_URL"
```

Should show one of:
```bash
# Option 1: API Key
MEDSCRUB_API_KEY=msk_test_demo0000000000000000000000000000
MEDSCRUB_API_URL=https://stage.api.medscrub.dev

# Option 2: JWT Token
MEDSCRUB_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
MEDSCRUB_API_URL=https://api.medscrub.dev
```

**Restart Jupyter kernel:**
- Kernel → Restart & Clear Output
- Re-run cells from the top

### "JWT token expired"

JWT tokens expire after 24 hours. Get a fresh token:
1. Visit https://medscrub.dev/playground
2. Copy new token
3. Update `.env`
4. Restart kernel

### "Rate limit exceeded"

Free tier: 100 requests/hour

**Solutions:**
- Wait for rate limit to reset (shown in error message)
- Upgrade to paid plan: https://medscrub.dev/pricing
- Use demo API key for testing (no rate limits on staging)

---

## 📖 Learn More

- **Full Documentation:** https://medscrub.dev/docs
- **API Reference:** https://medscrub.dev/docs/api
- **FHIR Resources:** https://medscrub.dev/docs/fhir
- **Troubleshooting:** [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- **JWT Fix Details:** [JWT_FIX_SUMMARY.md](./JWT_FIX_SUMMARY.md)

---

**Ready to de-identify healthcare data!** 🏥 🤖
