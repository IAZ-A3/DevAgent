#!/usr/bin/env python3
"""
validate-plan.py
Validates Plan.md for completeness and consistency against PRD.md.
Usage: python3 validate-plan.py [plan-path] [prd-path]
"""

import sys
import re
from pathlib import Path

PLAN_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/Plan.md")
PRD_PATH  = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/PRD.md")

errors   = []
warnings = []
info     = []

# --- Load files ---
if not PLAN_PATH.exists():
    print(f"[ERROR] Plan not found: {PLAN_PATH}")
    sys.exit(1)

plan = PLAN_PATH.read_text()
prd  = PRD_PATH.read_text() if PRD_PATH.exists() else None

if not prd:
    warnings.append("PRD not found — skipping cross-reference checks.")

# --- Extract feature IDs from PRD ---
prd_feats = set(re.findall(r'FEAT-\d{3}', prd)) if prd else set()

# --- Extract feature IDs from Plan ---
plan_feats = set(re.findall(r'FEAT-\d{3}', plan))

# --- Check all PRD features are covered ---
if prd_feats:
    missing = prd_feats - plan_feats
    if missing:
        for f in sorted(missing):
            errors.append(f"Feature {f} exists in PRD but has no tasks in Plan.")
    extra = plan_feats - prd_feats
    if extra:
        for f in sorted(extra):
            warnings.append(f"Feature {f} exists in Plan but not found in PRD.")
    info.append(f"PRD features: {len(prd_feats)}, Plan features: {len(plan_feats)}")

# --- Extract all task IDs ---
task_ids = re.findall(r'FEAT-\d{3}-TASK-\d{3}', plan)
task_ids_unique = set(task_ids)

if not task_ids_unique:
    errors.append("No task IDs (FEAT-XXX-TASK-YYY) found in plan.")
else:
    info.append(f"Total tasks found: {len(task_ids_unique)}")

# --- Check for duplicate task IDs ---
seen = {}
for t in task_ids:
    seen[t] = seen.get(t, 0) + 1
dupes = {k: v for k, v in seen.items() if v > 1}
for t, count in dupes.items():
    errors.append(f"Duplicate task ID: {t} appears {count} times.")

# --- Check complexity scores present ---
lines = plan.splitlines()
task_lines = [l for l in lines if re.search(r'FEAT-\d{3}-TASK-\d{3}', l)]
for l in task_lines:
    if not re.search(r'\b(XS|S|M|L|XL|XXL)\b', l):
        warnings.append(f"Task line missing complexity score: [{l.strip()[:80]}]")
    if not re.search(r'\b(Critical|High|Medium|Low)\b', l):
        warnings.append(f"Task line missing priority: [{l.strip()[:80]}]")
    if not re.search(r'\b(TODO|IN_PROGRESS|DONE|BLOCKED|SKIPPED)\b', l):
        warnings.append(f"Task line missing status: [{l.strip()[:80]}]")

# --- Check XXL tasks ---
xxl_tasks = [l for l in task_lines if 'XXL' in l]
if xxl_tasks:
    for l in xxl_tasks:
        errors.append(f"XXL task must be broken down: [{l.strip()[:80]}]")

# --- Check required sections ---
required = ["Execution Waves", "Feature Progress", "Blocked Items", "Change Log", "Plan Summary"]
for section in required:
    if section not in plan:
        errors.append(f"Required section missing: '{section}'")

# --- Check Change Log initialized ---
if "Change Log" in plan:
    changelog_section = plan[plan.index("Change Log"):]
    if "Planning Skill" not in changelog_section and "update-plan" not in changelog_section:
        warnings.append("Change Log appears empty — should have at least initial entry.")

# --- Report ---
print(f"\n=== Plan Validation Report: {PLAN_PATH} ===\n")

if info:
    print("INFO:")
    for i in info:
        print(f"  ✓ {i}")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  ⚠ {w}")

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ✗ {e}")

print(f"\n{'='*50}")
if errors:
    print(f"RESULT: FAIL — {len(errors)} error(s) must be fixed.")
    sys.exit(1)
elif warnings:
    print(f"RESULT: PASS WITH WARNINGS — {len(warnings)} warning(s) to review.")
else:
    print("RESULT: PASS — Plan meets quality standards.")
