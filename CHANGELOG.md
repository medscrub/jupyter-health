# Changelog

All notable changes to the MedScrub Jupyter Health notebooks will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-11-01

### Added
- Environment configuration file (`.env`) with demo API key for immediate testing
- JWT authentication test script (`test_jwt_auth.py`) for validating token functionality
- Support for both JWT token and API key authentication methods in all notebooks
- Quick start guide (`QUICKSTART.md`) with both authentication options
- Comprehensive troubleshooting documentation

### Changed
- Updated Notebook 04 client initialization to support both JWT and API key authentication methods
- Improved documentation structure with separate guides for setup, quickstart, and troubleshooting

### Fixed
- **Authentication**: Demo API key (`msk_test_demo0000000000000000000000000000`) validation bug - moved demo key check before regex validation in Worker
- **JWT Infrastructure**: JWT_SECRET configuration in Cloudflare Worker (production, staging, and dev environments)
- **Type Safety**: TypeScript compilation errors in FHIR deidentifier module
- **Deployment**: Successful deployment to all Cloudflare Worker environments

### Security
- **IMPORTANT**: Configured JWT_SECRET in all Cloudflare Worker environments to match Next.js app secret
- **Breaking Change**: JWT tokens generated before 2025-11-01 00:00 UTC are invalid due to JWT_SECRET infrastructure fix
  - **Action Required**: Users must obtain fresh JWT tokens from [medscrub.dev/playground](https://medscrub.dev/playground)
  - **Reason**: Previous tokens were signed when Worker had no JWT_SECRET configured
  - **Alternative**: Continue using demo API key for testing (no action required)

### Technical Details

#### Authentication Flow
- **Demo API Key**: Works immediately with staging environment (`stage.api.medscrub.dev`)
- **JWT Tokens**: Require fresh token from playground after infrastructure fix
- **API Keys**: Stored in Cloudflare KV, no JWT_SECRET dependency

#### Deployment
- Production: `api.medscrub.dev`
- Staging: `stage.api.medscrub.dev`
- Dev: Local Wrangler environment

## [0.1.0] - 2025-10-27

### Added
- Initial release of MedScrub Jupyter Health notebooks
- Five progressive notebooks covering FHIR de-identification workflows:
  - `01_quickstart_api.ipynb` - Basic API integration
  - `02_mcp_powered_workflow.ipynb` - AI-assisted workflow with Claude Code
  - `03_fhir_resources.ipynb` - Comprehensive FHIR R4 resource coverage
  - `04_data_science_workflow.ipynb` - End-to-end clinical research workflow
  - `05_mcp_demo_script.ipynb` - Quick demo for presentations
- Python client library (`medscrub_client.py`) with full API coverage
- Sample synthetic patient data for testing
- Comprehensive documentation (README, SETUP, TROUBLESHOOTING)
- MCP (Model Context Protocol) integration for Claude Desktop

### Supported Features
- FHIR R4 de-identification for 10 resource types:
  - Patient, Practitioner, Observation, Condition
  - MedicationRequest, Encounter, AllergyIntolerance
  - DiagnosticReport, Procedure, Immunization
- Bundle support with reference preservation
- Session-based re-identification
- 99.9% accuracy on structured FHIR data
- HIPAA Safe Harbor compliant (18 identifier types)

---

## Migration Notes

### Upgrading from Pre-1.0.0

If you were using the notebooks before 2025-11-01:

1. **JWT Token Users:**
   ```bash
   # Get fresh token from playground
   # Visit: https://medscrub.dev/playground

   # Update .env file
   MEDSCRUB_JWT_TOKEN=your-fresh-token-here
   MEDSCRUB_API_URL=https://api.medscrub.dev
   ```

2. **Demo API Key Users:**
   ```bash
   # No changes needed - continue using existing configuration
   MEDSCRUB_API_KEY=msk_test_demo0000000000000000000000000000
   MEDSCRUB_API_URL=https://stage.api.medscrub.dev
   ```

3. **Verify Configuration:**
   ```bash
   python3 test_jwt_auth.py
   ```

### Known Issues

- None currently reported

### Future Roadmap

- [ ] ML-enhanced text de-identification (target 97%+ accuracy)
- [ ] Expand FHIR resource support from 10 to 50+ types
- [ ] Enterprise features (SSO, audit logs, custom de-identification rules)
- [ ] Additional notebook examples for specialized use cases
- [ ] Performance optimizations for large datasets

---

## Support

- **Documentation**: [docs.medscrub.dev](https://docs.medscrub.dev)
- **Issues**: [GitHub Issues](https://github.com/medscrub/medscrub/issues)
- **Community**: See [COMMUNITY.md](./COMMUNITY.md)
- **Email**: support@medscrub.dev
