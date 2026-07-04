# Ticket Triage + Tagging Rules Engine

A lightweight Python tool that reads support ticket exports (CSV), applies keyword-based tagging rules, assigns priority levels, and routes each ticket to the right team. Outputs a structured markdown report and an enriched CSV ready for import or review.

Built for IT support teams, helpdesks, and operations teams that need fast, consistent triage without a full ITSM platform.

---

## What It Does

- Reads a CSV of support tickets (subject + body + metadata)
- Applies a configurable ruleset to tag each ticket by category (Hardware, Security, Account/Access, Network/VPN, Onboarding, Software, etc.)
- Assigns priority (High / Medium / Low) based on category match
- Suggests routing (e.g., Security/IT Lead, Identity & Access / Helpdesk)
- Outputs:
  - `output/triage_tagged.csv` — original tickets enriched with tags, priority, and routing
  - `output/triage_report.md` — human-readable report with priority summary and routing breakdown

---

## Quick Start

```bash
python triage_engine.py
```

Uses `sample_input/tickets.csv` by default.

```bash
python triage_engine.py --input path/to/your/tickets.csv --output-dir results/
```

---

## Input Format

CSV with at minimum these columns:

| Column | Description |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `subject` | Ticket subject line |
| `body` | Full ticket body text |
| `submitted_at` | Timestamp (optional, passed through) |

See `sample_input/tickets.csv` for an example.

---

## Output Sample

**triage_report.md** — priority + routing breakdown:

```
## Priority Summary
- High: 2
- Medium: 8
- Low: 0

## Routing Breakdown
### Security/IT Lead (1 ticket)
- T-1008 [High] Suspicious email received
  - Tags: Security
```

**triage_tagged.csv** — original CSV + added columns:

| ticket_id | subject | tags | priority | routing |
|---|---|---|---|---|
| T-1008 | Suspicious email received | Security | High | Security/IT Lead |

---

## Tagging Rules

Rules live in `triage_engine.py` as a plain Python list — no config files needed. Each rule has:

- `category` — label applied to the ticket
- `priority` — High / Medium / Low
- `routing` — suggested team or queue
- `keywords` — list of substrings to match (case-insensitive, subject + body)

Add or edit rules directly in the `TAGGING_RULES` list.

---

## Running Tests

```bash
python run_tests.py
```

---

## Limitations

- Keyword matching only — no ML or semantic understanding
- One ticket can match multiple categories; highest-priority rule wins for routing
- Designed for internal triage previews, not as a replacement for a full ITSM platform

---

## Tech Stack

- Python 3.8+
- Standard library only (csv, os, argparse)
- No dependencies to install

---

## License

MIT
