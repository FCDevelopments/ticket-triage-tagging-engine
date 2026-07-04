#!/usr/bin/env python3
"""
Ticket Triage + Tagging Rules Engine
-------------------------------------
Reads a CSV of support tickets, applies keyword-based tagging rules,
assigns priority, suggests routing, and outputs a triage report.

Usage:
    python triage_engine.py [--input path/to/tickets.csv] [--output-dir output/]

Outputs:
    output/triage_report.md   - human-readable triage summary
    output/triage_tagged.csv  - enriched ticket CSV with tags/priority/routing
"""

import csv
import os
import sys
import argparse
from datetime import datetime

# ---------------------------------------------------------------------------
# Tagging rules: (category, priority, routing, keyword_list)
# Rules are evaluated in order; first full category match wins for priority.
# A ticket can receive multiple category tags.
# ---------------------------------------------------------------------------
TAGGING_RULES = [
    {
        "category": "Security",
        "priority": "High",
        "routing": "Security/IT Lead",
        "keywords": ["phishing", "suspicious email", "malware", "ransomware", "breach", "virus", "clicked a link", "verify my account"],
    },
    {
        "category": "Account / Access",
        "priority": "High",
        "routing": "Identity & Access / Helpdesk",
        "keywords": ["password reset", "locked out", "okta", "mfa", "2fa", "access denied", "cannot log in", "can't log in", "login", "sso"],
    },
    {
        "category": "Hardware",
        "priority": "Medium",
        "routing": "IT Support / Desktop",
        "keywords": ["laptop", "desktop", "won't turn on", "not starting", "monitor", "keyboard", "mouse", "printer", "offline", "hardware"],
    },
    {
        "category": "Network / VPN",
        "priority": "Medium",
        "routing": "Network / IT Support",
        "keywords": ["vpn", "network", "wifi", "wi-fi", "internet", "disconnecting", "connection", "drops"],
    },
    {
        "category": "Software / App",
        "priority": "Medium",
        "routing": "IT Support / Desktop",
        "keywords": ["install", "adobe", "outlook", "onedrive", "sync", "error", "not working", "crashing", "update", "application"],
    },
    {
        "category": "Onboarding / Offboarding",
        "priority": "Medium",
        "routing": "IT Admin / HR Ops",
        "keywords": ["new hire", "onboarding", "offboarding", "set up accounts", "departing", "termination", "starting"],
    },
    {
        "category": "Software Request",
        "priority": "Low",
        "routing": "IT Support / Procurement",
        "keywords": ["request", "need installed", "approved", "purchase", "license"],
    },
    {
        "category": "Hardware Request",
        "priority": "Low",
        "routing": "IT Support / Procurement",
        "keywords": ["second monitor", "dual monitor", "docking station", "headset", "webcam", "equipment request"],
    },
]

UNKNOWN_CATEGORY = "General / Uncategorized"
UNKNOWN_PRIORITY = "Low"
UNKNOWN_ROUTING = "Helpdesk"


def classify_ticket(subject: str, body: str) -> dict:
    """Apply tagging rules and return tags, priority, and routing."""
    combined = (subject + " " + body).lower()
    matched_categories = []
    top_priority = None
    top_routing = UNKNOWN_ROUTING
    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    for rule in TAGGING_RULES:
        if any(kw in combined for kw in rule["keywords"]):
            matched_categories.append(rule["category"])
            if top_priority is None or priority_order[rule["priority"]] < priority_order[top_priority]:
                top_priority = rule["priority"]
                top_routing = rule["routing"]

    if not matched_categories:
        matched_categories = [UNKNOWN_CATEGORY]
        top_priority = UNKNOWN_PRIORITY
        top_routing = UNKNOWN_ROUTING

    return {
        "tags": ", ".join(matched_categories),
        "priority": top_priority or UNKNOWN_PRIORITY,
        "routing": top_routing,
    }


def load_tickets(input_path: str) -> list[dict]:
    tickets = []
    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickets.append(row)
    return tickets


def write_tagged_csv(tickets: list[dict], output_path: str):
    if not tickets:
        return
    fieldnames = list(tickets[0].keys()) + ["tags", "priority", "routing"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)


def write_report(tickets: list[dict], output_path: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    priority_counts = {"High": 0, "Medium": 0, "Low": 0}
    routing_map: dict[str, list] = {}

    for t in tickets:
        p = t.get("priority", "Low")
        priority_counts[p] = priority_counts.get(p, 0) + 1
        route = t.get("routing", UNKNOWN_ROUTING)
        routing_map.setdefault(route, []).append(t)

    lines = [
        "# Ticket Triage Report",
        f"Generated: {now}",
        f"Total tickets: {len(tickets)}",
        "",
        "## Priority Summary",
        f"- 🔴 High: {priority_counts.get('High', 0)}",
        f"- 🟡 Medium: {priority_counts.get('Medium', 0)}",
        f"- 🟢 Low: {priority_counts.get('Low', 0)}",
        "",
        "## Routing Breakdown",
    ]

    for route, route_tickets in sorted(routing_map.items()):
        lines.append(f"\n### {route} ({len(route_tickets)} ticket{'s' if len(route_tickets) != 1 else ''})")
        for t in route_tickets:
            tid = t.get("ticket_id", "?")
            subj = t.get("subject", "(no subject)")
            pri = t.get("priority", "Low")
            tags = t.get("tags", "")
            lines.append(f"- **{tid}** [{pri}] {subj}")
            lines.append(f"  - Tags: {tags}")

    lines += [
        "",
        "---",
        "## All Tickets",
        "",
        "| ID | Priority | Tags | Routing | Subject |",
        "|---|---|---|---|---|",
    ]
    for t in tickets:
        lines.append(
            f"| {t.get('ticket_id','?')} | {t.get('priority','')} | {t.get('tags','')} | {t.get('routing','')} | {t.get('subject','')} |"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Ticket Triage + Tagging Rules Engine")
    parser.add_argument("--input", default="sample_input/tickets.csv", help="Path to input tickets CSV")
    parser.add_argument("--output-dir", default="output", help="Directory for output files")
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output_dir

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    tickets = load_tickets(input_path)
    print(f"Loaded {len(tickets)} tickets from {input_path}")

    for t in tickets:
        result = classify_ticket(t.get("subject", ""), t.get("body", ""))
        t.update(result)

    tagged_csv_path = os.path.join(output_dir, "triage_tagged.csv")
    report_path = os.path.join(output_dir, "triage_report.md")

    write_tagged_csv(tickets, tagged_csv_path)
    write_report(tickets, report_path)

    print(f"Tagged CSV -> {tagged_csv_path}")
    print(f"Triage report -> {report_path}")
    print("Done.")


if __name__ == "__main__":
    main()
