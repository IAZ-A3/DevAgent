#!/usr/bin/env python3
"""
validate-implementation.py
Validates that implementation is complete against Plan.md and PRD.md.
Checks: all tasks DONE, requirement traceability in code, test coverage headers.
Usage: python3 validate-implementation.py [plan-path] [prd-path] [src-dir] [tests-dir]
"""

import sys
import re
from pathlib import Path

PLAN_PATH  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/Plan.md")
PRD_PATH   = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/PRD.md")
SRC_DIR    = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("src")
TESTS_DIR  = Path(sys.argv[4]) if len(sys.argv) > 4 else Path("tests")

errors   = []
warnings = []
info     = []

# --- Load files ---
plan = PLAN_PATH.read_text() if PLAN_PATH.exists() else ""
prd  = PRD_PATH.read_text()  if PRD_PATH.exists()  else ""

if not plan:
    print(f"[ERROR] Plan not found: {PLAN_PATH}")
    sys.exit(1)

# --- Check all tasks are DONE ---
task_pattern = re.compile(r'(FEAT-\d{3}-TASK-\d{3}).*?\|\s*(TODO|IN_PROGRESS|BLOCKED|SKIPPED|DONE)\s*\|')
tasks = task_pattern.findall(plan)
task_status = {t[0]: t[1] for t in tasks}

not_done = {k: v for k, v in task_status.items() if v not in ("DONE", "SKIPPED")}
if not_done:
    for task_id, status in sorted(not_done.items()):
        errors.append(f"Task {task_id} is {status} — not complete.")
else:
    info.append(f"All {len(task_status)} tasks are DONE or SKIPPED.")

# --- Check source files exist ---
if not SRC_DIR.exists():
    errors.append(f"Source directory not found: {SRC_DIR}")
else:
    src_files = list(SRC_DIR.rglob("*.*"))
    src_files = [f for f in src_files if f.is_file()]
    info.append(f"Source files found: {len(src_files)}")

# --- Check test files exist ---
if not TESTS_DIR.exists():
    errors.append(f"Tests directory not found: {TESTS_DIR}")
else:
    test_files = list(TESTS_DIR.rglob("*.*"))
    test_files = [f for f in test_files if f.is_file()]
    info.append(f"Test files found: {len(test_files)}")

# --- Check requirement traceability in source ---
if prd and SRC_DIR.exists():
    fr_ids = set(re.findall(r'FEAT-\d{3}-FR-\d{3}', prd))
    src_content = ""
    for f in SRC_DIR.rglob("*.*"):
        try:
            src_content += f.read_text(errors='ignore')
        except:
            pass

    covered = set()
    for fr_id in fr_ids:
        if fr_id in src_content:
            covered.add(fr_id)

    uncovered = fr_ids - covered
    if uncovered:
        for fr_id in sorted(uncovered):
            warnings.append(f"FR {fr_id} has no traceability comment in source code.")
    info.append(f"FR traceability: {len(covered)}/{len(fr_ids)} referenced in source.")

# --- Check test files have requirement references ---
if TESTS_DIR.exists():
    test_content = ""
    for f in TESTS_DIR.rglob("*.*"):
        try:
            test_content += f.read_text(errors='ignore')
        except:
            pass

    if prd:
        fr_ids = set(re.findall(r'FEAT-\d{3}-FR-\d{3}', prd))
        tested = {fr for fr in fr_ids if fr in test_content}
        untested = fr_ids - tested
        if untested:
            for fr_id in sorted(untested):
                warnings.append(f"FR {fr_id} has no test referencing it.")
        info.append(f"FR test coverage: {len(tested)}/{len(fr_ids)} referenced in tests.")

# --- Check integration report exists ---
integration_report = Path(".claude/skills/state/implementation/integration-report.md")
if not integration_report.exists():
    warnings.append("Integration report not found — integrator sub-skill may not have run.")
else:
    report_content = integration_report.read_text()
    if "FAIL" in report_content and "PASS" not in report_content:
        errors.append("Integration report shows FAIL status.")
    else:
        info.append("Integration report found and status is acceptable.")

# --- Report ---
print(f"\n=== Implementation Validation Report ===\n")

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
    print("RESULT: PASS — Implementation complete and traceable.")
