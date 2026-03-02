#!/usr/bin/env python3
"""
validate-prd.py
Validates a PRD.md file for quality and consistency.
Usage: python3 validate-prd.py [path-to-PRD.md]
"""

import sys
import re
from pathlib import Path

PRD_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/PRD.md")

VAGUE_TERMS = [
    "fast", "slow", "simple", "easy", "user-friendly", "robust",
    "reliable", "efficient", "intuitive", "seamless", "powerful",
    "flexible", "scalable", "quickly", "easily", "smoothly"
]

errors = []
warnings = []
info = []

if not PRD_PATH.exists():
    print(f"[ERROR] PRD file not found: {PRD_PATH}")
    sys.exit(1)

content = PRD_PATH.read_text()
lines = content.splitlines()

# --- Check: Feature IDs present ---
feat_ids = re.findall(r'FEAT-\d{3}', content)
feat_ids_unique = set(feat_ids)
if not feat_ids_unique:
    errors.append("No FEAT-XXX IDs found. Features must be assigned IDs.")
else:
    info.append(f"Found {len(feat_ids_unique)} feature(s): {', '.join(sorted(feat_ids_unique))}")

# --- Check: Functional requirement IDs ---
fr_ids = re.findall(r'FEAT-\d{3}-FR-\d{3}', content)
global_fr_ids = re.findall(r'(?<!FEAT-\d{3}-)FR-\d{3}', content)
if not fr_ids and not global_fr_ids:
    errors.append("No functional requirement IDs (FR-XXX or FEAT-XXX-FR-XXX) found.")
else:
    info.append(f"Found {len(fr_ids)} scoped FRs, {len(global_fr_ids)} global FRs.")

# --- Check: NFR IDs present ---
nfr_ids = re.findall(r'NFR-\d{3}', content)
if not nfr_ids:
    warnings.append("No NFR IDs found. Non-functional requirements are strongly recommended.")
else:
    info.append(f"Found {len(nfr_ids)} NFR(s).")

# --- Check: Duplicate IDs ---
all_ids = re.findall(r'(?:FEAT|FR|NFR|RISK|OQ|TC)-\d{3}(?:-(?:FR|NFR|TC)-\d{3})?', content)
seen = {}
for id_ in all_ids:
    seen[id_] = seen.get(id_, 0) + 1
dupes = {k: v for k, v in seen.items() if v > 1}
if dupes:
    for id_, count in dupes.items():
        errors.append(f"Duplicate ID found: {id_} appears {count} times.")

# --- Check: Vague language ---
for i, line in enumerate(lines, 1):
    line_lower = line.lower()
    for term in VAGUE_TERMS:
        if re.search(r'\b' + term + r'\b', line_lower):
            warnings.append(f"Line {i}: Vague term '{term}' found → add measurable criterion. [{line.strip()[:80]}]")

# --- Check: NFRs have acceptance criteria ---
nfr_lines = [l for l in lines if re.search(r'NFR-\d{3}', l)]
for l in nfr_lines:
    # Simple heuristic: acceptance criterion lines usually contain < > % ms s kb mb
    if not re.search(r'[<>%]|\d+\s*(ms|s|kb|mb|gb|req|rpm|%)', l.lower()):
        warnings.append(f"NFR line may lack measurable criterion: [{l.strip()[:80]}]")

# --- Check: EARS patterns (shall/should/may) ---
req_lines = [l for l in lines if re.search(r'FR-\d{3}', l)]
for l in req_lines:
    if not re.search(r'\b(shall|should|may)\b', l.lower()):
        warnings.append(f"Requirement line missing 'shall/should/may': [{l.strip()[:80]}]")

# --- Check: Required sections present ---
required_sections = [
    "Project Overview", "Non-Functional Requirements",
    "Features", "Risks", "Open Questions"
]
for section in required_sections:
    if section.lower() not in content.lower():
        errors.append(f"Required section missing: '{section}'")

# --- Report ---
print(f"\n=== PRD Validation Report: {PRD_PATH} ===\n")

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
    print(f"RESULT: FAIL — {len(errors)} error(s) must be fixed before proceeding.")
    sys.exit(1)
elif warnings:
    print(f"RESULT: PASS WITH WARNINGS — {len(warnings)} warning(s) should be reviewed.")
    sys.exit(0)
else:
    print("RESULT: PASS — PRD meets quality standards.")
    sys.exit(0)
