# CHANGELOG

## v1.0.0 — 2026-03-30

Initial release.

### Features
- Reads support ticket CSV exports (subject + body + metadata)
- Applies keyword-based tagging rules across 8 categories: Security, Account/Access, Hardware, Network/VPN, Software/App, Onboarding/Offboarding, Software Request, Hardware Request
- Assigns priority (High / Medium / Low) and suggests team routing per ticket
- Outputs enriched `triage_tagged.csv` and a human-readable `triage_report.md`
- 8-case built-in test suite via `run_tests.py`
- Sample input with 10 realistic IT support tickets included

### Notes
- Keyword matching only; no ML or semantic model required
- Rules are plain Python — easy to extend without config files
- Standard library only; no pip dependencies
