# MedScrub Community Guidelines

## 💬 Join the Discussion

**Discord:** [Join JupyterCon Healthcare AI Community](https://discord.gg/MKF5V2C3)

Connect with healthcare data scientists, clinical researchers, and AI developers using MedScrub for HIPAA-compliant analysis.

---

## ✅ Great Posts Include

- **Clear title** - "Rate limit error on /deidentify endpoint" not "Help!"
- **What you tried** - Code snippets, steps taken
- **Error messages** - Full stack trace or HTTP response
- **Environment** - Python version, JWT vs API key, local vs hosted

---

## 📝 Post Template

```
**Issue:** [One sentence description]
**Environment:** [Python 3.x, Jupyter, JWT token, etc.]
**Code:**
[Code snippet that reproduces the issue]
**Error:**
[Error message or unexpected behavior]
**What I tried:** [Steps you've already taken]
```

---

## 🎯 Best Practices

✅ **Search first** - Your question may already be answered
✅ **Share de-identified code only** - No PHI in posts
✅ **Mark solutions** - Help others find answers
✅ **Share wins** - Show off your healthcare AI projects!
✅ **Be respectful** - We're all learning together
✅ **Give context** - Healthcare workflows vary widely

---

## 💡 Quick Self-Help

Before posting, try these common fixes:

**JWT token issues?**
→ Get fresh token from [medscrub.dev/playground](https://medscrub.dev/playground)

**Rate limits?**
→ Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

**MCP setup?**
→ See [SETUP.md](./SETUP.md)

**Notebook not running?**
→ Verify: `pip install -r requirements.txt` and `.env` configured

---

## 🏥 Healthcare-Specific Etiquette

### DO:
- ✅ Use synthetic/sample data when sharing code
- ✅ Discuss FHIR resources, HIPAA compliance questions
- ✅ Share de-identification strategies and best practices
- ✅ Ask about clinical research workflows
- ✅ Propose new FHIR resource types to support

### DON'T:
- ❌ Post actual patient data (even "de-identified")
- ❌ Ask for medical/clinical advice (we're engineers!)
- ❌ Share PHI in screenshots or code snippets
- ❌ Expect instant responses (community-driven support)

---

## 🎓 Good Question Examples

**Example 1: Technical Issue**
```
**Issue:** Getting 401 error when calling /api/fhir/deidentify
**Environment:** Python 3.11, Jupyter, JWT token from playground
**Code:**
client = MedScrubClient(jwt_token=os.getenv('MEDSCRUB_JWT_TOKEN'))
result = client.deidentify_fhir(patient)  # Fails here

**Error:** MedScrubAuthError: Invalid or missing authentication
**What I tried:**
- Verified token is in .env file
- Checked token hasn't expired (generated 1 hour ago)
- Tried with sample patient from notebook 01
```

**Example 2: Feature Request**
```
I'm working with FHIR Medication resources and noticed they're not
currently supported. Would it be possible to add them? I'm happy to
help test if you need beta users.

Use case: Analyzing medication adherence patterns in diabetes patients.
```

**Example 3: Workflow Question**
```
I have 500 patient FHIR Bundles to de-identify for a research study.
What's the recommended approach for batch processing to stay within
rate limits? Should I use the same session ID for all patients or
create separate sessions?
```

---

## 🚫 What Gets Removed

Posts will be removed if they:
- Contain real patient data (even "anonymized")
- Violate HIPAA or healthcare privacy regulations
- Are spam or promotional (unless MedScrub-related)
- Are off-topic (unrelated to healthcare data science)
- Contain harassment or discriminatory content

---

## 🏆 Be a Great Community Member

### Help Others
- Answer questions when you can
- Share your use cases and projects
- Contribute to documentation
- Report bugs you find

### Share Knowledge
- **Project showcases welcome!** Show us what you built
- **Notebook examples appreciated** - Help others learn
- **FHIR insights valuable** - Share healthcare domain expertise
- **Performance tips helpful** - Optimization strategies

### Stay Updated
- Star the repo: [github.com/medscrub/medscrub](https://github.com/medscrub/medscrub)
- Watch for release announcements in Discord
- Participate in JupyterCon discussions

---

## 🎯 JupyterCon Attendees

Welcome! This community supports:
- Healthcare data scientists using Jupyter
- Clinical researchers learning FHIR
- AI/ML engineers building HIPAA-compliant workflows
- Academic researchers publishing with de-identified data

**First time here?**
1. Introduce yourself in #introductions
2. Share your research interests
3. Ask questions - we were all beginners once!

---

## 📧 Other Support Channels

**Community (Discord):** Best for questions, discussions, sharing projects
**GitHub Issues:** Bug reports, feature requests
**Email (support@medscrub.dev):** Account issues, billing, enterprise inquiries
**Docs (medscrub.dev/docs):** API reference, guides, tutorials

---

**Thank you for being part of the healthcare AI community!** 🏥 🤖

*Together we're making AI safer for clinical research.*
