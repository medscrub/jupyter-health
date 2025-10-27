# Claude Code + MCP Setup for Jupyter Notebooks

Step-by-step guide to configure the MedScrub MCP server with Claude Desktop for AI-assisted healthcare data analysis in Jupyter notebooks.

## 🎯 Why Use MCP with Jupyter?

The combination of **Jupyter + Claude Code + MedScrub MCP** enables:

- **AI-assisted data analysis** - Ask Claude to analyze your healthcare data
- **Automatic PHI de-identification** - Claude uses MCP tools to remove PHI before processing
- **Interactive exploration** - Chat with Claude about your Jupyter notebooks
- **Safe AI workflows** - HIPAA-compliant AI assistance for clinical research

**Example workflow:**
```
You: "Analyze this patient cohort for diabetes medication patterns"
Claude: [Uses medscrub__deidentify_fhir automatically]
Claude: [Performs analysis on de-identified data]
Claude: [Shows insights without exposing PHI]
```

---

## Prerequisites

- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Claude Desktop** - [Download here](https://claude.ai/download)
- **MedScrub JWT Token** - [Get from medscrub.dev/playground](https://medscrub.dev/playground)
- **Python 3.8+** and **Jupyter** - Already installed for Jupyter notebooks

---

## Step 1: Install MedScrub MCP Server

Open a terminal and install the MedScrub MCP server globally:

```bash
npm install -g @medscrub/mcp
```

**Verify installation:**
```bash
# Check if package is installed
npm list -g @medscrub/mcp

# You should see something like:
# └── @medscrub/mcp@1.0.0
```

---

## Step 2: Find Your System Paths

Claude Desktop needs to know where Node.js and the MCP server are installed.

### Find Node.js Path

```bash
# macOS/Linux
which node

# Windows (PowerShell)
where.exe node
```

**Example outputs:**
- **macOS (nvm):** `/Users/username/.nvm/versions/node/v22.15.0/bin/node`
- **macOS (Homebrew):** `/opt/homebrew/bin/node`
- **Windows:** `C:\Program Files\nodejs\node.exe`
- **Linux:** `/usr/bin/node`

### Find Global npm Packages Path

```bash
npm root -g
```

**Example outputs:**
- **macOS (nvm):** `/Users/username/.nvm/versions/node/v22.15.0/lib/node_modules`
- **macOS (Homebrew):** `/opt/homebrew/lib/node_modules`
- **Windows:** `C:\Users\username\AppData\Roaming\npm\node_modules`
- **Linux:** `/usr/lib/node_modules`

**The MCP server will be at:** `{npm-root}/@medscrub/mcp/dist/index.js`

---

## Step 3: Configure Claude Desktop

### Locate Claude Desktop Config File

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Create/Edit Configuration

Open the file in your text editor and add the MedScrub MCP server configuration:

```json
{
  "mcpServers": {
    "medscrub": {
      "command": "/path/to/node",
      "args": ["/path/to/global/node_modules/@medscrub/mcp/dist/index.js"],
      "env": {
        "MEDSCRUB_API_URL": "https://api.medscrub.dev",
        "MEDSCRUB_JWT_TOKEN": "your-jwt-token-from-medscrub.dev-playground"
      }
    }
  }
}
```

### Configuration Examples

**macOS (nvm):**
```json
{
  "mcpServers": {
    "medscrub": {
      "command": "/Users/cj/.nvm/versions/node/v22.15.0/bin/node",
      "args": ["/Users/cj/.nvm/versions/node/v22.15.0/lib/node_modules/@medscrub/mcp/dist/index.js"],
      "env": {
        "MEDSCRUB_API_URL": "https://api.medscrub.dev",
        "MEDSCRUB_JWT_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      }
    }
  }
}
```

**macOS (Homebrew):**
```json
{
  "mcpServers": {
    "medscrub": {
      "command": "/opt/homebrew/bin/node",
      "args": ["/opt/homebrew/lib/node_modules/@medscrub/mcp/dist/index.js"],
      "env": {
        "MEDSCRUB_API_URL": "https://api.medscrub.dev",
        "MEDSCRUB_JWT_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "medscrub": {
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": ["C:\\Users\\username\\AppData\\Roaming\\npm\\node_modules\\@medscrub\\mcp\\dist\\index.js"],
      "env": {
        "MEDSCRUB_API_URL": "https://api.medscrub.dev",
        "MEDSCRUB_JWT_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Important:** Replace:
- `/path/to/node` with your actual Node.js path from Step 2
- `/path/to/global/node_modules/@medscrub/mcp/dist/index.js` with your actual MCP path
- `your-jwt-token-from-medscrub.dev-playground` with your JWT token from [medscrub.dev/playground](https://medscrub.dev/playground)

---

## Step 4: Validate JSON Syntax

**Common mistakes:**
- Missing commas between objects
- Extra commas at end of objects
- Incorrect quote types (use `"` not `'`)
- Backslashes not escaped in Windows paths (use `\\` or `/`)

**Validate your JSON:**
1. Copy your config file content
2. Paste into [jsonlint.com](https://jsonlint.com)
3. Fix any syntax errors

---

## Step 5: Restart Claude Desktop

**Completely quit and restart** Claude Desktop:

**macOS:**
```bash
# Quit Claude Desktop (Cmd+Q)
# Then relaunch from Applications
```

**Windows:**
- Right-click Claude Desktop in system tray
- Select "Quit"
- Relaunch from Start Menu

**Linux:**
```bash
killall claude-desktop
claude-desktop &
```

---

## Step 6: Verify MCP Connection

Open Claude Desktop and test the connection:

### Test 1: List MCP Servers
```
What MCP servers are connected?
```

**Expected response:**
```
I can see the following MCP servers connected:
- medscrub
```

### Test 2: List MedScrub Tools
```
What tools are available from the medscrub server?
```

**Expected response:**
```
The medscrub server provides:
- medscrub__deidentify_fhir
- medscrub__reidentify_fhir
- medscrub__deidentify_text
- medscrub__reidentify_text
- medscrub__get_session_info
- medscrub__list_phi_types
```

### Test 3: Use a Tool
```
Use medscrub__list_phi_types to show all PHI types
```

**Expected response:**
```
MedScrub detects 18 HIPAA Safe Harbor identifiers:
1. Names
2. Geographic subdivisions...
[etc.]
```

---

## Step 7: Use with Jupyter Notebooks

### Workflow 1: De-identify Data in Jupyter

1. Open Jupyter notebook in your browser
2. Load patient data in a cell
3. Open Claude Desktop
4. Ask Claude to de-identify the data

**Example:**
```python
# In Jupyter notebook
patient = {
    "resourceType": "Patient",
    "name": [{"family": "Smith", "given": ["John"]}],
    "birthDate": "1985-03-15"
}
```

**In Claude Desktop:**
```
I have a FHIR Patient resource with PHI in my Jupyter notebook.
Use medscrub__deidentify_fhir to remove the PHI.
[paste the patient JSON]
```

### Workflow 2: AI-Assisted Analysis

**In Jupyter:** Load a patient cohort (10 patients)

**In Claude Desktop:**
```
I have 10 diabetic patients in my Jupyter notebook.
First, de-identify all patient data using medscrub__deidentify_fhir.
Then analyze the cohort for common medication patterns.
```

Claude will:
1. De-identify each patient (using MCP)
2. Analyze the de-identified data
3. Show insights without exposing PHI

---

## 🛠️ Troubleshooting

### Problem: "MCP server not found"

**Cause:** Node.js or MCP path is incorrect

**Solution:**
1. Verify paths from Step 2
2. Check file exists: `ls /path/to/node_modules/@medscrub/mcp/dist/index.js`
3. Update `claude_desktop_config.json` with correct paths
4. Restart Claude Desktop

### Problem: "Cannot connect to MedScrub API"

**Cause:** JWT token expired or invalid

**Solution:**
1. Get new JWT token from [medscrub.dev/playground](https://medscrub.dev/playground)
2. Update token in `claude_desktop_config.json`
3. Restart Claude Desktop

### Problem: "Rate limit exceeded"

**Cause:** Hit 100 requests/hour limit (free tier)

**Solution:**
- Wait for rate limit to reset (1 hour)
- Or upgrade to Starter plan ($29/month for 1K requests/hour)
- Or deploy MedScrub locally (unlimited requests)

### Problem: JSON syntax error

**Cause:** Invalid JSON in config file

**Solution:**
1. Validate JSON at [jsonlint.com](https://jsonlint.com)
2. Common fixes:
   - Remove trailing commas
   - Escape backslashes: `C:\\Path\\To\\File`
   - Use double quotes `"` not single quotes `'`

### Problem: "npx command failed"

**Cause:** npm corruption across Node versions

**Solution:** Use direct node execution (already done in this guide!)

---

## 🎓 Example Use Cases

### Use Case 1: De-identify Patient Cohort

```
I have 20 patients in a CSV file. Load them, de-identify all PHI using
medscrub__deidentify_fhir, and save to a new CSV safe for sharing.
```

### Use Case 2: Analyze Lab Results

```
I have glucose lab results for 50 diabetic patients. De-identify the data,
then analyze trends and create a visualization.
```

### Use Case 3: Generate Synthetic Test Data

```
Take this real patient record, de-identify it completely, then help me
create 10 variations for testing our application.
```

---

## 📚 Additional Resources

- **MCP Server:** [@medscrub/mcp on npm](https://www.npmjs.com/package/@medscrub/mcp)
- **MCP Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **API Documentation:** [medscrub.dev/docs](https://medscrub.dev/docs)
- **Python/JS/TS Examples:** [github.com/medscrub/medscrub (samples/ directory)](https://github.com/medscrub/medscrub/tree/main/samples)

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/medscrub/medscrub/issues)
- **Email:** support@medscrub.dev
- **Documentation:** [medscrub.dev/docs](https://medscrub.dev/docs)

---

**Ready to use AI-assisted healthcare data analysis!** 🎉

See [02_mcp_powered_workflow.ipynb](./02_mcp_powered_workflow.ipynb) for interactive examples.
