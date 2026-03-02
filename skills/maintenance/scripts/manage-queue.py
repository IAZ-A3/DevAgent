#!/usr/bin/env python3
"""
manage-queue.py
Manages the maintenance input queue (add, list, resolve bugs).
Usage:
  python3 manage-queue.py list                          # list all open bugs
  python3 manage-queue.py add <title> <severity> <desc> # add a new bug
  python3 manage-queue.py resolve <BUG-XXX> <version>   # mark bug resolved
  python3 manage-queue.py show <BUG-XXX>                # show bug details
"""

import sys
import re
from pathlib import Path
from datetime import datetime

QUEUE_PATH = Path(".claude/skills/state/maintenance/input-queue.md")
QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)

VALID_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}


def load_queue():
    if not QUEUE_PATH.exists():
        return ""
    return QUEUE_PATH.read_text()


def save_queue(content):
    QUEUE_PATH.write_text(content)


def get_next_bug_id(content):
    ids = re.findall(r'BUG-(\d{3})', content)
    if not ids:
        return "BUG-001"
    return f"BUG-{int(max(ids)) + 1:03d}"


def cmd_list():
    content = load_queue()
    if not content.strip():
        print("Maintenance queue is empty.")
        return

    bugs = re.findall(
        r'## (BUG-\d{3}): (.+?)\n.*?\*\*Severity:\*\* (\w+).*?\*\*Status:\*\* (\w+)',
        content, re.DOTALL
    )

    if not bugs:
        print("No bugs found in queue.")
        return

    print(f"\n{'='*60}")
    print(f"{'ID':<10} {'Severity':<10} {'Status':<15} {'Title'}")
    print(f"{'='*60}")
    for bug_id, title, severity, status in bugs:
        print(f"{bug_id:<10} {severity:<10} {status:<15} {title}")
    print(f"{'='*60}")
    print(f"Total: {len(bugs)} bug(s)\n")


def cmd_add(title, severity, description, reported_by="User"):
    severity = severity.upper()
    if severity not in VALID_SEVERITIES:
        print(f"[ERROR] Invalid severity. Must be one of: {', '.join(VALID_SEVERITIES)}")
        sys.exit(1)

    content = load_queue()
    bug_id = get_next_bug_id(content)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"""
## {bug_id}: {title}
**Date:** {now}  
**Severity:** {severity}  
**Reported by:** {reported_by}  
**Status:** OPEN  
**Feature:** TBD  
**Requirement:** TBD  
**Description:** {description}  
**Reproduction:** TBD  
**Suggested investigation:** TBD  

---
"""
    if not content.strip():
        content = "# Maintenance Input Queue\n\n---\n"

    content += entry
    save_queue(content)
    print(f"[OK] Bug added: {bug_id} — {title}")
    print(f"     Severity: {severity}")


def cmd_resolve(bug_id, version):
    content = load_queue()
    if bug_id not in content:
        print(f"[ERROR] {bug_id} not found in queue.")
        sys.exit(1)

    now = datetime.now().strftime("%Y-%m-%d")
    # Update status
    updated = re.sub(
        rf'(## {bug_id}:.*?\*\*Status:\*\*) \w+',
        rf'\1 RESOLVED',
        content, flags=re.DOTALL, count=1
    )
    # Add resolution note
    updated = re.sub(
        rf'(## {bug_id}:.*?---)',
        rf'\1\n**Resolved:** {now} in v{version}  ',
        updated, flags=re.DOTALL, count=1
    )
    save_queue(updated)
    print(f"[OK] {bug_id} marked as RESOLVED in v{version}")


def cmd_show(bug_id):
    content = load_queue()
    match = re.search(rf'## {bug_id}:.+?(?=\n## BUG-|\Z)', content, re.DOTALL)
    if not match:
        print(f"[ERROR] {bug_id} not found.")
        sys.exit(1)
    print(match.group(0))


# --- Main ---
if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)

cmd = sys.argv[1].lower()

if cmd == "list":
    cmd_list()
elif cmd == "add":
    if len(sys.argv) < 5:
        print("Usage: manage-queue.py add <title> <severity> <description>")
        sys.exit(1)
    cmd_add(sys.argv[2], sys.argv[3], sys.argv[4])
elif cmd == "resolve":
    if len(sys.argv) < 4:
        print("Usage: manage-queue.py resolve <BUG-XXX> <version>")
        sys.exit(1)
    cmd_resolve(sys.argv[2], sys.argv[3])
elif cmd == "show":
    if len(sys.argv) < 3:
        print("Usage: manage-queue.py show <BUG-XXX>")
        sys.exit(1)
    cmd_show(sys.argv[2])
else:
    print(f"[ERROR] Unknown command: {cmd}")
    print(__doc__)
    sys.exit(1)
