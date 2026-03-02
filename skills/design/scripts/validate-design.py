#!/usr/bin/env python3
"""
validate-design.py
Validates design documents for traceability and internal consistency.
Usage: python3 validate-design.py [design-dir] [prd-path]
"""

import sys
import re
from pathlib import Path

DESIGN_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/design")
PRD_PATH   = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/PRD.md")

errors   = []
warnings = []
info     = []

# --- Load PRD ---
prd_content = PRD_PATH.read_text() if PRD_PATH.exists() else ""
if not prd_content:
    warnings.append(f"PRD not found at {PRD_PATH} — skipping requirement coverage checks.")

# --- Load all design documents ---
if not DESIGN_DIR.exists():
    print(f"[ERROR] Design directory not found: {DESIGN_DIR}")
    sys.exit(1)

design_files = list(DESIGN_DIR.glob("*.md"))
if not design_files:
    print(f"[ERROR] No design documents found in {DESIGN_DIR}")
    sys.exit(1)

info.append(f"Found {len(design_files)} design document(s): {[f.name for f in design_files]}")

design_content_all = ""
for f in design_files:
    design_content_all += f.read_text() + "\n"

# --- Extract IDs ---
prd_fr_ids  = set(re.findall(r'FEAT-\d{3}-FR-\d{3}', prd_content))
prd_nfr_ids = set(re.findall(r'(?:FEAT-\d{3}-)?NFR-\d{3}', prd_content))
prd_feat_ids = set(re.findall(r'FEAT-\d{3}(?!-)', prd_content))

design_comp_ids = set(re.findall(r'COMP-\d{3}', design_content_all))
design_intf_ids = set(re.findall(r'INTF-\d{3}', design_content_all))
design_data_ids = set(re.findall(r'DATA-\d{3}', design_content_all))
design_adr_ids  = set(re.findall(r'ADR-\d{3}', design_content_all))

info.append(f"Design elements: {len(design_comp_ids)} components, {len(design_intf_ids)} interfaces, {len(design_data_ids)} data entities, {len(design_adr_ids)} ADRs")

# --- Forward traceability: all FRs covered ---
if prd_fr_ids:
    for req_id in sorted(prd_fr_ids):
        if req_id not in design_content_all:
            errors.append(f"Forward trace missing: {req_id} not referenced in any design document.")
    covered = sum(1 for r in prd_fr_ids if r in design_content_all)
    info.append(f"FR coverage: {covered}/{len(prd_fr_ids)}")

# --- Forward traceability: all NFRs covered ---
if prd_nfr_ids:
    for nfr_id in sorted(prd_nfr_ids):
        if nfr_id not in design_content_all:
            warnings.append(f"NFR not explicitly referenced in design: {nfr_id}")
    covered = sum(1 for r in prd_nfr_ids if r in design_content_all)
    info.append(f"NFR coverage: {covered}/{len(prd_nfr_ids)}")

# --- Backward traceability: all design elements have a requirement reference ---
lines = design_content_all.splitlines()
comp_definitions = [l for l in lines if re.search(r'###\s+COMP-\d{3}', l)]
intf_definitions = [l for l in lines if re.search(r'###\s+INTF-\d{3}', l)]
data_definitions = [l for l in lines if re.search(r'###\s+DATA-\d{3}', l)]

def check_backward_trace(definitions, id_pattern, doc_content):
    for defn in definitions:
        id_match = re.search(id_pattern, defn)
        if not id_match:
            continue
        elem_id = id_match.group(0)
        # Look for requirement reference near this definition (within 10 lines)
        idx = doc_content.find(defn)
        surrounding = doc_content[idx:idx+500]
        if not re.search(r'FEAT-\d{3}(?:-(?:FR|NFR)-\d{3})?|NFR-\d{3}', surrounding):
            warnings.append(f"Backward trace: {elem_id} has no requirement reference nearby — possible gold-plating.")

check_backward_trace(comp_definitions, r'COMP-\d{3}', design_content_all)
check_backward_trace(intf_definitions, r'INTF-\d{3}', design_content_all)
check_backward_trace(data_definitions, r'DATA-\d{3}', design_content_all)

# --- Check DesignIndex exists ---
index_path = DESIGN_DIR / "DesignIndex.md"
if not index_path.exists():
    errors.append("DesignIndex.md not found in design directory.")
else:
    index_content = index_path.read_text()
    for f in design_files:
        if f.name != "DesignIndex.md" and f.name not in index_content:
            warnings.append(f"Design document '{f.name}' not listed in DesignIndex.md.")

# --- Check ADR.md exists ---
adr_path = DESIGN_DIR / "ADR.md"
if not adr_path.exists():
    warnings.append("ADR.md not found — should exist even if empty.")

# --- Check for interface references that are not defined ---
referenced_intfs = set(re.findall(r'INTF-\d{3}', design_content_all))
for intf in referenced_intfs:
    # Check if it's defined (has a header)
    if not re.search(r'###\s+' + intf, design_content_all):
        errors.append(f"Interface {intf} is referenced but never defined.")

# --- Report ---
print(f"\n=== Design Validation Report ===\n")

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
    print("RESULT: PASS — Design meets quality standards.")
