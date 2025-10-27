# HIPAA-Compliant Healthcare Data Science with Jupyter

**MedScrub + Jupyter + Claude Code = Safe AI-Assisted Clinical Research**

Interactive Jupyter notebooks demonstrating FHIR de-identification, AI-assisted analysis, and HIPAA-compliant workflows for healthcare data scientists.

---

## 🎯 What Makes This Special?

**MedScrub is the only FHIR de-identification tool with native MCP (Model Context Protocol) integration** - enabling AI-assisted healthcare data analysis where Claude automatically removes PHI before processing.

### Traditional Workflow ❌
```
Load patient data → Manually de-identify → Write analysis code → Hope you didn't miss PHI
```

### MedScrub + MCP Workflow ✅
```
Load patient data → Ask Claude to analyze → Claude auto-de-identifies → Safe AI analysis
```

**Result:** 99.9% accurate PHI removal + AI assistance without exposing patient data.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get JWT token (free tier: 100 requests/hour)
# Visit: https://medscrub.dev/playground

# 3. Set up environment
cp .env.example .env
# Add your token to .env

# 4. Start Jupyter
jupyter notebook

# 5. Open notebooks/01_quickstart_api.ipynb
```

**You'll have de-identified FHIR data in under 5 minutes!**

---

## 📚 Notebooks

| Notebook | Description | Time | Best For |
|----------|-------------|------|----------|
| **[01_quickstart_api.ipynb](./notebooks/01_quickstart_api.ipynb)** | Traditional API integration | 5 min | Production pipelines, automation |
| **[02_mcp_powered_workflow.ipynb](./notebooks/02_mcp_powered_workflow.ipynb)** ⭐ | AI-assisted with Claude Code | 15 min | **Exploratory analysis, research** |
| **[03_fhir_resources.ipynb](./notebooks/03_fhir_resources.ipynb)** | All 77 FHIR resource types | 20 min | FHIR integration, EHR systems |
| **[04_data_science_workflow.ipynb](./notebooks/04_data_science_workflow.ipynb)** | End-to-end clinical research | 30 min | **Population health, ML models** |
| **[05_mcp_demo_script.ipynb](./notebooks/05_mcp_demo_script.ipynb)** | Presentation demo | 5 min | Hackathons, JupyterCon demos |

---

## 🤖 MCP + Claude Code Integration

**What is MCP?** Model Context Protocol - enables AI assistants (like Claude) to access local tools and data safely.

**How MedScrub uses it:** When you ask Claude to analyze healthcare data, it automatically uses MedScrub to remove PHI first.

### Setup (5 minutes)

See **[SETUP.md](./SETUP.md)** for complete guide, or:

```bash
# 1. Install MedScrub MCP server
npm install -g @medscrub/mcp

# 2. Configure Claude Desktop
# Add to ~/.config/Claude/claude_desktop_config.json (Linux/Mac)
# or %APPDATA%\Claude\claude_desktop_config.json (Windows)

# 3. Restart Claude Desktop

# 4. Test in Claude:
"What MCP servers are connected?"
# Should see: medscrub
```

**Now you can:** Ask Claude to de-identify patient data, analyze cohorts, generate insights - all with automatic PHI protection!

---

## 🏥 Healthcare Use Cases

### Clinical Research
```python
# Load 50 diabetic patients
cohort = load_patients("diabetes_study.json")

# De-identify for HIPAA compliance
for patient in cohort:
    result = client.deidentify_fhir(patient)
    analyze_patient(result['deidentifiedResource'])

# Safe for publication, AI analysis, sharing
```

### Population Health Analytics
- Age distribution analysis
- Medication adherence patterns
- Comorbidity analysis
- Risk stratification
- **All without exposing PHI**

### AI-Assisted Diagnosis Support
```python
# De-identify patient record
result = client.deidentify_fhir(patient)

# Send to Claude (no PHI exposed)
analysis = claude.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{
        "role": "user",
        "content": f"Analyze this patient's vitals and labs: {result['deidentifiedResource']}"
    }]
)

# Re-identify for clinical action if needed
clinical_report = client.reidentify_text(analysis.content, result['sessionId'])
```

### Quality Improvement Studies
- Readmission rate analysis
- Treatment outcome comparison
- Protocol adherence measurement
- Cost-effectiveness analysis

---

## 🔒 FHIR Resources (99.9% Accuracy)

MedScrub supports **77 FHIR R4 resource types** with deterministic field-level de-identification:

### Core Clinical Resources
- ✅ **Patient** - Demographics, contact info, identifiers
- ✅ **Practitioner** - Provider information, credentials
- ✅ **PractitionerRole** - Provider roles and specialties
- ✅ **RelatedPerson** - Family members, emergency contacts
- ✅ **Person** - Administrative person data
- ✅ **Organization** - Healthcare organizations
- ✅ **Location** - Facilities, rooms, geographic locations

### Observations & Assessments
- ✅ **Observation** - Vitals, labs, measurements
- ✅ **Condition** - Diagnoses, problems, health conditions
- ✅ **AllergyIntolerance** - Allergies and intolerances
- ✅ **FamilyMemberHistory** - Family health history
- ✅ **ClinicalImpression** - Clinical assessments
- ✅ **DetectedIssue** - Identified clinical issues
- ✅ **RiskAssessment** - Risk predictions
- ✅ **AdverseEvent** - Adverse reactions

### Medications
- ✅ **Medication** - Medication definitions
- ✅ **MedicationRequest** - Prescriptions
- ✅ **MedicationAdministration** - Medication given to patient
- ✅ **MedicationDispense** - Pharmacy dispensing
- ✅ **MedicationStatement** - Patient medication history
- ✅ **MedicationKnowledge** - Medication information

### Procedures & Services
- ✅ **Procedure** - Surgeries, interventions
- ✅ **ServiceRequest** - Orders for services
- ✅ **Immunization** - Vaccinations
- ✅ **ImagingStudy** - Radiology studies (DICOM)
- ✅ **Specimen** - Lab specimens

### Encounters & Episodes
- ✅ **Encounter** - Visits, hospitalizations
- ✅ **EpisodeOfCare** - Care episodes
- ✅ **Appointment** - Scheduled appointments
- ✅ **AppointmentResponse** - Appointment confirmations
- ✅ **Schedule** - Provider schedules
- ✅ **Slot** - Available time slots

### Diagnostics & Reports
- ✅ **DiagnosticReport** - Lab reports, imaging results
- ✅ **Media** - Photos, videos, audio
- ✅ **DocumentReference** - Clinical documents
- ✅ **Composition** - Document compositions

### Care Planning & Management
- ✅ **CarePlan** - Care plans
- ✅ **CareTeam** - Care team members
- ✅ **Goal** - Treatment goals
- ✅ **RequestGroup** - Grouped requests
- ✅ **Task** - Workflow tasks

### Financial & Billing
- ✅ **Claim** - Insurance claims
- ✅ **ClaimResponse** - Claim adjudication
- ✅ **ExplanationOfBenefit** - EOB statements
- ✅ **Coverage** - Insurance coverage
- ✅ **Account** - Patient accounts
- ✅ **PaymentNotice** - Payment notifications
- ✅ **PaymentReconciliation** - Payment reconciliation
- ✅ **EligibilityRequest** - Coverage eligibility checks
- ✅ **EligibilityResponse** - Eligibility results

### Research & Studies
- ✅ **ResearchStudy** - Clinical trials
- ✅ **ResearchSubject** - Study participants

### Communication & Consent
- ✅ **Communication** - Communications
- ✅ **CommunicationRequest** - Communication requests
- ✅ **Consent** - Patient consent records

### Nutrition & Prescriptions
- ✅ **NutritionOrder** - Dietary orders
- ✅ **VisionPrescription** - Eyewear prescriptions

### Devices & Supplies
- ✅ **Device** - Medical devices
- ✅ **DeviceRequest** - Device orders
- ✅ **DeviceUseStatement** - Device usage
- ✅ **SupplyRequest** - Supply requests
- ✅ **SupplyDelivery** - Supply delivery
- ✅ **Substance** - Chemical substances
- ✅ **HealthcareService** - Healthcare services

### Questionnaires & Surveys
- ✅ **Questionnaire** - Form definitions
- ✅ **QuestionnaireResponse** - Survey responses

### Infrastructure & Audit
- ✅ **Provenance** - Data provenance
- ✅ **AuditEvent** - Security audit events
- ✅ **Endpoint** - Technical endpoints
- ✅ **Flag** - Warning flags

### Lists & Collections
- ✅ **List** - Collections of resources
- ✅ **Bundle** - Multiple resources with reference preservation

### Referrals & Workflows
- ✅ **ReferralRequest** - Referrals to specialists
- ✅ **GuidanceResponse** - Clinical guidance
- ✅ **MeasureReport** - Quality measure reports

**Why 99.9% accurate?** Deterministic field mapping vs. pattern matching. We know exactly where PHI lives in FHIR structured data.

---

## 🧪 Sample Data

The `sample_data/` directory contains synthetic FHIR resources for testing:

- **Patients** - Comprehensive demographics with all PHI types
- **Observations** - Blood pressure, glucose, HbA1c
- **Medications** - Metformin prescription
- **Conditions** - Type 2 Diabetes
- **Bundle** - Complete patient history (8 resources)
- **Clinical Note** - Unstructured text with 18 HIPAA identifiers

**All data is synthetic and HIPAA-compliant** - safe for demos, testing, and learning.

---

## 🎓 Learning Path

**New to MedScrub?**

1. **Start:** `01_quickstart_api.ipynb` (5 min) - Learn basics
2. **FHIR Deep Dive:** `03_fhir_resources.ipynb` (20 min) - All resource types
3. **Real Research:** `04_data_science_workflow.ipynb` (30 min) - End-to-end example
4. **AI-Powered:** `02_mcp_powered_workflow.ipynb` (15 min) - MCP integration
5. **Demo Ready:** `05_mcp_demo_script.ipynb` (5 min) - Presentation script

**For JupyterCon Attendees:**
- Jump to `02_mcp_powered_workflow.ipynb` for the flagship demo
- Combine with [Synthea FHIR MCP](https://github.com/synthetichealth/synthea-mcp) for realistic patient data

---

## 🔑 Authentication

### Get JWT Token

1. Visit **[medscrub.dev/playground](https://medscrub.dev/playground)**
2. Sign up (free account)
3. Copy your JWT token
4. Add to `.env`:

```bash
MEDSCRUB_JWT_TOKEN=your-jwt-token-here
MEDSCRUB_API_URL=https://api.medscrub.dev
```

### Rate Limits
- **Free:** 100 requests/hour (perfect for learning/demos)
- **Starter:** 1,000 requests/hour - $29/month
- **Pro:** 10,000 requests/hour - $99/month
- **Self-hosted:** Unlimited (see [medscrub.dev/docs](https://medscrub.dev/docs))

---

## 🌟 What Sets MedScrub Apart

### 1. MCP Integration (Unique!)
Only FHIR de-identification tool with native Claude Code support. AI assistance with automatic PHI protection.

### 2. 99.9% FHIR Accuracy
Deterministic field-level mapping (344+ fields) vs. pattern matching. Zero ambiguity on structured data.

### 3. Reversible Tokenization
Session-based re-identification preserves clinical context when needed for follow-up.

### 4. Edge Performance
<50ms response time globally via Cloudflare Workers edge network.

### 5. Developer Experience
Jupyter notebooks, Python client, comprehensive docs, Discord community support.

---

## 📖 Documentation

- **Setup Guide:** [SETUP.md](./SETUP.md) - MCP server configuration
- **Troubleshooting:** [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Common issues
- **API Docs:** [medscrub.dev/docs](https://medscrub.dev/docs)
- **FHIR R4 Spec:** [hl7.org/fhir/R4](https://hl7.org/fhir/R4/)
- **HIPAA Safe Harbor:** [HHS.gov](https://www.hhs.gov/hipaa/for-professionals/privacy/special-topics/de-identification/index.html)
- **MCP Protocol:** [modelcontextprotocol.io](https://modelcontextprotocol.io)

---

## 💬 Community & Support

### Join the Discussion
**💬 Discord:** [Join JupyterCon Healthcare AI Community](https://discord.gg/MKF5V2C3)
- Get help with setup and integration
- Share your healthcare data science projects
- Connect with clinical researchers using Jupyter
- Discuss FHIR, HIPAA, and AI ethics

See **[COMMUNITY.md](./COMMUNITY.md)** for Discord posting guidelines.

### Get Help
- **📧 Email:** support@medscrub.dev
- **🐛 Issues:** [github.com/medscrub/medscrub/issues](https://github.com/medscrub/medscrub/issues)
- **📖 Docs:** [medscrub.dev/docs](https://medscrub.dev/docs)

---

## 🔬 Research & Citations

If you use MedScrub in academic research, please cite:

```bibtex
@software{medscrub2024,
  title = {MedScrub: HIPAA-Compliant FHIR De-identification},
  author = {MedScrub Team},
  year = {2024},
  url = {https://medscrub.dev},
  note = {99.9% accurate PHI removal for healthcare AI workflows}
}
```

---

## 🛡️ HIPAA Compliance

- **Safe Harbor Method:** Removes all 18 HIPAA identifiers
- **Business Associate Agreement (BAA):** Available for hosted API
- **Data Retention:** PHI tokens expire after 24 hours
- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **Audit Logs:** Complete compliance trail (Enterprise tier)
- **Self-Hosted Option:** Complete data control, no external API calls

---

## 🎯 JupyterCon 2024

**Submitted by:** MedScrub Team
**Category:** Healthcare Data Science
**Keywords:** FHIR, HIPAA, PHI De-identification, AI-Assisted Analysis, MCP

**What attendees will learn:**
1. HIPAA-compliant data science workflows in Jupyter
2. AI-assisted analysis with automatic PHI protection (MCP)
3. 99.9% accurate FHIR de-identification
4. Real-world clinical research examples
5. Integration with Claude Code and other AI tools

---

**Built with ❤️ for Healthcare Data Scientists**

*Enabling safe AI adoption in clinical research - from exploration to publication*
