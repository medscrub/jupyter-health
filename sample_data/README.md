# MedScrub Sample FHIR Data

This directory contains synthetic FHIR R4 resources for testing and learning MedScrub de-identification.

## 📋 Available Sample Files

| File | Resource Type | Description |
|------|---------------|-------------|
| `patient_john_doe.json` | Patient | Comprehensive patient demographics with all PHI types |
| `patient_jane_smith.json` | Patient | Alternative patient with different field coverage |
| `observation_blood_pressure.json` | Observation | Vital signs (blood pressure) |
| `observation_lab_glucose.json` | Observation | Laboratory result (glucose) |
| `medication_metformin.json` | MedicationRequest | Diabetes medication prescription |
| `condition_diabetes.json` | Condition | Type 2 Diabetes diagnosis |
| `bundle_patient_history.json` | Bundle | Complete patient history (Patient + Observations + Conditions) |
| `clinical_note_sample.txt` | Text | Unstructured clinical note with PHI |

## 🔒 Data Source

All data is **synthetic** and HIPAA-compliant:
- Generated using FHIR specification examples
- No real patient information
- Safe for testing, demos, and education

## 📖 Usage in Notebooks

### Load a Sample Patient

```python
import json

# Load patient resource
with open('sample_data/patient_john_doe.json', 'r') as f:
    patient = json.load(f)

# De-identify it
result = client.deidentify_fhir(patient)
```

### Load a Bundle

```python
# Load complete patient history
with open('sample_data/bundle_patient_history.json', 'r') as f:
    bundle = json.load(f)

# De-identify all resources in the bundle
result = client.deidentify_fhir(bundle)
```

### Load Clinical Text

```python
# Load unstructured clinical note
with open('sample_data/clinical_note_sample.txt', 'r') as f:
    clinical_note = f.read()

# De-identify the text
result = client.deidentify_text(clinical_note)
```

## 🎯 PHI Coverage

These samples demonstrate de-identification of all 18 HIPAA Safe Harbor identifiers:

1. **Names** - Patient names, family members
2. **Geographic** - Addresses, cities, ZIP codes
3. **Dates** - Birth dates, visit dates
4. **Phone/Fax** - Telephone numbers
5. **Email** - Email addresses
6. **SSN** - Social Security numbers (in text samples)
7. **MRN** - Medical record numbers
8. **Account** - Insurance account numbers
9. **Device** - Device identifiers
10. And 9 more...

## 📚 Related Notebooks

- **01_quickstart_api.ipynb** - Learn basic de-identification with `patient_john_doe.json`
- **03_fhir_resources.ipynb** - Explore all resource types
- **04_data_science_workflow.ipynb** - Use `bundle_patient_history.json` for analysis
- **05_mcp_demo_script.ipynb** - Demo with Synthea FHIR MCP (realistic data)

## 🔄 Creating Your Own Samples

Want to test with your own FHIR resources? Just:

1. Save your FHIR JSON to this directory
2. Load it in your notebook
3. De-identify with MedScrub

```python
# Your custom FHIR resource
with open('sample_data/my_custom_patient.json', 'r') as f:
    my_patient = json.load(f)

result = client.deidentify_fhir(my_patient)
```

---

**Note:** For realistic patient data from actual clinical workflows, combine MedScrub with the [Synthea FHIR MCP server](https://github.com/synthetichealth/synthea-mcp) which provides 117 synthetic patients with complete medical histories.
