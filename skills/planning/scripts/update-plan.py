#!/usr/bin/env python3
"""
update-plan.py
Updates a task status in Plan.md. Called by other skills when work progresses.
Usage: python3 update-plan.py <task-id> <new-status> [notes] [plan-path]

Status values: TODO | IN_PROGRESS | DONE | BLOCKED | SKIPPED
Example: python3 update-plan.py FEAT-001-TASK-001 DONE "Implemented in src/feature1.py"
"""

import sys
import re
from pathlib import Path
from datetime import datetime

if len(sys.argv) < 3:
    print("Usage: update-plan.py <task-id> <new-status> [notes] [plan-path]")
    sys.exit(1)

TASK_ID   = sys.argv[1]
NEW_STATUS = sys.argv[2].upper()
NOTES     = sys.argv[3] if len(sys.argv) > 3 else ""
PLAN_PATH = Path(sys.argv[4]) if len(sys.argv) > 4 else Path("docs/Plan.md")

VALID_STATUSES = {"TODO", "IN_PROGRESS", "DONE", "BLOCKED", "SKIPPED"}

if NEW_STATUS not in VALID_STATUSES:
    print(f"[ERROR] Invalid status '{NEW_STATUS}'. Must be one of: {', '.join(VALID_STATUSES)}")
    sys.exit(1)

if not PLAN_PATH.exists():
    print(f"[ERROR] Plan file not found: {PLAN_PATH}")
    sys.exit(1)

content = PLAN_PATH.read_text()
lines = content.splitlines()

# --- Find and update the task row ---
task_found = False
updated_lines = []
old_status = None

for line in lines:
    if TASK_ID in line and "|" in line:
        # Parse table row — find status column (6th pipe-delimited column)
        parts = line.split("|")
        if len(parts) >= 7:
            for i, part in enumerate(parts):
                part_stripped = part.strip()
                if part_stripped in VALID_STATUSES:
                    old_status = part_stripped
                    parts[i] = f" {NEW_STATUS} "
                    if NOTES and len(parts) > i+1:
                        parts[i+1] = f" {NOTES} "
                    task_found = True
                    break
            line = "|".join(parts)
    updated_lines.append(line)

if not task_found:
    print(f"[ERROR] Task ID '{TASK_ID}' not found in {PLAN_PATH}")
    sys.exit(1)

# --- Update Last Updated header ---
now = datetime.now().strftime("%Y-%m-%d %H:%M")
result_lines = []
for line in updated_lines:
    if line.startswith("## Last Updated:"):
        line = f"## Last Updated: {now} by update-plan.py"
    result_lines.append(line)

# --- Append to Change Log ---
change_entry = f"| {now} | update-plan.py | {TASK_ID}: {old_status} → {NEW_STATUS}{' — ' + NOTES if NOTES else ''} |"
final_lines = []
in_changelog = False
changelog_appended = False

for line in result_lines:
    final_lines.append(line)
    if "## Change Log" in line:
        in_changelog = True
    if in_changelog and line.startswith("| {date}") or (in_changelog and line.strip() == "" and not changelog_appended):
        # Insert after the header row and separator
        pass

# Simpler approach: append change entry before last blank line in changelog
changelog_idx = None
for i, line in enumerate(final_lines):
    if "## Change Log" in line:
        changelog_idx = i
        break

if changelog_idx is not None:
    # Find end of changelog table
    insert_idx = len(final_lines)
    for i in range(changelog_idx, len(final_lines)):
        if i > changelog_idx and final_lines[i].strip() == "" :
            insert_idx = i
            break
    final_lines.insert(insert_idx, change_entry)

# --- Write back ---
PLAN_PATH.write_text("\n".join(final_lines))
print(f"[OK] {TASK_ID}: {old_status} → {NEW_STATUS}")
if NOTES:
    print(f"     Notes: {NOTES}")
print(f"     Plan updated: {PLAN_PATH}")
