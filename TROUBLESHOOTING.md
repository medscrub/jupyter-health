# Troubleshooting Guide

Common issues and solutions for MedScrub Jupyter notebooks.

---

## 🔧 Installation Issues

### "Cannot import medscrub_client"

**Problem:** Dependencies not installed or wrong directory

**Solution:**
```bash
# Make sure you're in the jupyter-health directory
cd jupyter-health/  # Or wherever you cloned this repo

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import requests; print('OK')"
```

### "pip install fails with permissions error"

**Problem:** No write access to global Python packages

**Solution:**
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# OR install in user directory
pip install --user -r requirements.txt
```

---

## 🔑 Authentication Issues

### "Authentication failed (401)"

**Problem:** JWT token is expired or invalid

**Solution:**
1. Get a fresh token from [medscrub.dev/playground](https://medscrub.dev/playground)
2. Update `.env` file:
   ```bash
   MEDSCRUB_JWT_TOKEN=your-new-token-here
   ```
3. Restart Jupyter kernel (Kernel → Restart)

### ".env file not loading"

**Problem:** python-dotenv not finding .env file

**Solution:**
```python
# Verify .env exists in correct location
import os
print(os.path.exists('.env'))  # Should print True

# Check current directory
print(os.getcwd())  # Should be jupyter-health/ (repo root)

# Force reload .env
from dotenv import load_dotenv
load_dotenv(override=True)
```

---

## 🚦 Rate Limiting Issues

### "Rate limit exceeded (429)"

**Problem:** You've hit the 100 requests/hour limit (free tier)

**Solution:**

**Option 1: Wait for reset**
```python
# Check when rate limit resets
import requests
response = client._session.get(f"{client.api_url}/api/stats")
reset_time = response.headers.get('X-RateLimit-Reset')
print(f"Rate limit resets at: {reset_time}")
```

**Option 2: Upgrade plan**
- Starter: 1,000 req/hr - $29/month
- Pro: 10,000 req/hr - $99/month
- Visit [medscrub.dev/pricing](https://medscrub.dev/pricing)

**Option 3: Deploy locally (unlimited)**
- Contact support@medscrub.dev for self-hosted deployment options
- Docker and Kubernetes configurations available
- No rate limits on self-hosted deployments

### "Requests failing intermittently"

**Problem:** Network issues or API downtime

**Solution:**
```python
# Add retry logic
from medscrub_client import MedScrubClient
import time

def deidentify_with_retry(client, resource, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.deidentify_fhir(resource)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries}")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e
```

---

## 📊 Data Issues

### "JSON decode error when loading sample data"

**Problem:** Corrupted JSON file or incorrect path

**Solution:**
```python
import json

# Check if file exists
import os
file_path = 'sample_data/patient_john_doe.json'
print(f"File exists: {os.path.exists(file_path)}")

# Try to load and catch detailed error
try:
    with open(file_path, 'r') as f:
        patient = json.load(f)
except json.JSONDecodeError as e:
    print(f"JSON error at line {e.lineno}, column {e.colno}")
    print(f"Error: {e.msg}")
```

### "De-identification returns empty tokenCount"

**Problem:** Resource doesn't contain PHI or wrong resource type

**Solution:**
```python
# Check resource type
print(f"Resource type: {resource.get('resourceType')}")

# Verify it's a supported type
supported = ['Patient', 'Practitioner', 'Observation', 'Condition',
             'MedicationRequest', 'Encounter', 'AllergyIntolerance',
             'DiagnosticReport', 'Procedure', 'Immunization']
print(f"Supported: {resource.get('resourceType') in supported}")

# Check for PHI fields
if resource.get('resourceType') == 'Patient':
    has_phi = any([
        resource.get('name'),
        resource.get('birthDate'),
        resource.get('address'),
        resource.get('telecom')
    ])
    print(f"Contains PHI fields: {has_phi}")
```

---

## 🤖 MCP Integration Issues

### "MCP server not loading in Claude Desktop"

**Problem:** Claude Desktop can't find MedScrub MCP server

**Solution:** See [SETUP.md](./SETUP.md) for detailed setup, or:

1. **Verify installation:**
   ```bash
   npm list -g @medscrub/mcp
   # Should show: @medscrub/mcp@x.x.x
   ```

2. **Check Node.js path:**
   ```bash
   which node  # macOS/Linux
   where.exe node  # Windows
   ```

3. **Verify config file location:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

4. **Validate JSON syntax:**
   - Copy config content to [jsonlint.com](https://jsonlint.com)
   - Fix any syntax errors

5. **Restart Claude Desktop completely:**
   - Quit app (not just close window)
   - Relaunch from Applications/Start Menu

### "Claude says 'Tool not found'"

**Problem:** MedScrub MCP server loaded but tools not registered

**Solution:**
```
# In Claude Desktop, ask:
What tools are available from the medscrub server?

# Should see:
- medscrub__deidentify_fhir
- medscrub__reidentify_fhir
- medscrub__deidentify_text
- medscrub__reidentify_text
- medscrub__get_session_info
- medscrub__list_phi_types
```

If tools are missing, check MCP server logs:
- macOS: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\Logs\mcp*.log`

---

## 🐍 Jupyter Notebook Issues

### "Kernel keeps dying"

**Problem:** Out of memory or package conflicts

**Solution:**
```bash
# Create fresh virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=medscrub

# In Jupyter, select Kernel → Change kernel → medscrub
```

### "Plots not showing inline"

**Problem:** matplotlib backend not configured

**Solution:**
```python
# Add to first cell of notebook
%matplotlib inline
import matplotlib.pyplot as plt

# Verify backend
import matplotlib
print(matplotlib.get_backend())  # Should be 'module://ipykernel.pylab.backend_inline'
```

### "Changes to .env not taking effect"

**Problem:** Kernel hasn't reloaded environment variables

**Solution:**
```python
# Force reload
from dotenv import load_dotenv
import importlib

load_dotenv(override=True)

# Restart kernel
# Kernel → Restart & Clear Output
```

---

## 🌐 Network Issues

### "Connection timeout"

**Problem:** Network blocking or API endpoint unreachable

**Solution:**
```python
# Test connectivity
import requests

# Check if API is reachable
try:
    response = requests.get('https://api.medscrub.dev/health', timeout=5)
    print(f"API Status: {response.status_code}")
except requests.exceptions.Timeout:
    print("Timeout - check your network connection")
except requests.exceptions.ConnectionError:
    print("Connection error - API may be down or blocked by firewall")
```

### "SSL certificate verification failed"

**Problem:** Corporate firewall or proxy interfering

**Solution:**
```python
# Temporary workaround (NOT recommended for production)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Use with verify=False (development only)
# Better: Get your organization's CA certificate
```

---

## 🔍 Debugging Tips

### Enable verbose logging

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('medscrub_client')
logger.setLevel(logging.DEBUG)

# Now all API calls will be logged
result = client.deidentify_fhir(patient)
```

### Inspect API responses

```python
# Check last response details
import requests

response = requests.post(
    f"{client.api_url}/api/fhir/deidentify",
    headers={"Authorization": f"Bearer {client.jwt_token}"},
    json={"resource": patient}
)

print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text[:500]}")  # First 500 chars
```

### Test with minimal example

```python
# Simplest possible test
from medscrub_client import MedScrubClient
import os

client = MedScrubClient(
    jwt_token=os.getenv('MEDSCRUB_JWT_TOKEN'),
    api_url='https://api.medscrub.dev'
)

# Minimal patient resource
minimal_patient = {
    "resourceType": "Patient",
    "name": [{"family": "Doe", "given": ["John"]}]
}

try:
    result = client.deidentify_fhir(minimal_patient)
    print("✅ Success!")
    print(f"Token count: {result['tokenCount']}")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 🆘 Still Having Issues?

### Check API Status
- **Health Endpoint:** [api.medscrub.dev/health](https://api.medscrub.dev/health)
- **Status Page:** [status.medscrub.dev](https://status.medscrub.dev) *(coming soon)*

### Get Help
- **Email:** support@medscrub.dev (24-48 hour response)
- **GitHub Issues:** [github.com/medscrub/medscrub/issues](https://github.com/medscrub/medscrub/issues)
- **Documentation:** [medscrub.dev/docs](https://medscrub.dev/docs)

### Report a Bug
Include in your report:
- Python version (`python --version`)
- Jupyter version (`jupyter --version`)
- MedScrub client version
- Error message with full stack trace
- Minimal code to reproduce issue

---

**Pro Tip:** 90% of issues are solved by:
1. Restarting Jupyter kernel
2. Getting a fresh JWT token
3. Verifying `.env` file is in correct location
