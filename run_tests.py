#!/usr/bin/env python3
"""
Built-in test suite for the Ticket Triage + Tagging Rules Engine.
Run: python run_tests.py
"""

import sys
from triage_engine import classify_ticket

TESTS = [
    # (description, subject, body, expected_category_substring, expected_priority, expected_routing_substring)
    ("Security phishing", "Suspicious email received", "I clicked a link to verify my account", "Security", "High", "Security"),
    ("Account lockout", "Password reset request", "I'm locked out of Okta and can't log in", "Account / Access", "High", "Identity"),
    ("Hardware failure", "Laptop won't turn on", "My laptop stopped working this morning", "Hardware", "Medium", "Desktop"),
    ("VPN issue", "VPN keeps disconnecting", "The VPN drops every 20 minutes at home", "Network / VPN", "Medium", "Network"),
    ("Onboarding", "New hire onboarding", "Please set up accounts for new hire starting next week", "Onboarding", "Medium", "HR"),
    ("Software install", "Need Adobe installed", "Can you install Adobe Acrobat on my machine", "Software", "Medium", "Desktop"),
    ("Hardware request", "Dual monitor setup", "I'd like a second monitor for my workstation", "Hardware", "Medium", "Desktop"),
    ("Unknown ticket", "Random question", "I have a general inquiry about the office", "General", "Low", "Helpdesk"),
]

passed = 0
failed = 0

for desc, subject, body, exp_cat, exp_pri, exp_route in TESTS:
    result = classify_ticket(subject, body)
    ok_cat = exp_cat.lower() in result["tags"].lower()
    ok_pri = result["priority"] == exp_pri
    ok_route = exp_route.lower() in result["routing"].lower()

    if ok_cat and ok_pri and ok_route:
        print(f"  PASS  {desc}")
        passed += 1
    else:
        print(f"  FAIL  {desc}")
        if not ok_cat:
            print(f"         category: expected '{exp_cat}' in '{result['tags']}'")
        if not ok_pri:
            print(f"         priority: expected '{exp_pri}', got '{result['priority']}'")
        if not ok_route:
            print(f"         routing:  expected '{exp_route}' in '{result['routing']}'")
        failed += 1

print(f"\n{passed}/{passed + failed} tests passed")
if failed:
    sys.exit(1)
