#!/usr/bin/env python3
"""
assemble-vv-report.py
Assembles the final VV-Report.md from all sub-skill state files.
Usage: python3 assemble-vv-report.py [output-path]
"""

import sys
import re
from pathlib import Path
from datetime import datetime

OUTPUT_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/VV-Report.md")
STATE_DIR   = Path(".claude/skills/state/vv")

def read_file(path):
    return path.read_text() if path.exists() else ""

system_results  = read_file(STATE_DIR / "system-test-results.md")
nfr_results     = read_file(STATE_DIR / "nfr-auto-results.md")
coverage_audit  = read_file(STATE_DIR / "coverage-audit.md")

# --- Extract summary counts ---
def count_pattern(content, pattern):
    matches = re.findall(pattern, content)
    return len(matches)

sys_pass  = len(re.findall(r'\|\s*PASS\s*\|', system_results))
sys_fail  = len(re.findall(r'\|\s*FAIL\s*\|', system_results))
nfr_pass  = len(re.findall(r'\|\s*PASS\s*\|', nfr_results))
nfr_fail  = len(re.findall(r'\|\s*FAIL\s*\|', nfr_results))
cov_full  = system_results.count('FULL')
cov_warn  = system_results.count('PARTIAL')
cov_miss  = system_results.count('MISSING')

total_sys   = sys_pass + sys_fail
total_nfr   = nfr_pass + nfr_fail
overall     = "PASS" if sys_fail == 0 and nfr_fail == 0 and cov_miss == 0 else \
              "PASS_WITH_WARNINGS" if sys_fail == 0 and nfr_fail == 0 else "FAIL"

now = datetime.now().strftime("%Y-%m-%d %H:%M")

report = f"""# Verification & Validation Report
## Project: (see PRD)
## Date: {now}
## Overall Result: {overall}

---

## Executive Summary
| Category | Result | Pass | Fail |
|----------|--------|------|------|
| System Tests | {'PASS' if sys_fail == 0 else 'FAIL'} | {sys_pass} | {sys_fail} |
| NFR Auto-Validation | {'PASS' if nfr_fail == 0 else 'FAIL'} | {nfr_pass} | {nfr_fail} |
| Requirement Coverage | {'PASS' if cov_miss == 0 else 'FAIL'} | {cov_full} full | {cov_miss} missing |

---

## System Test Results

{system_results if system_results else "_System test results not found._"}

---

## NFR Auto-Validation Results

{nfr_results if nfr_results else "_NFR validation results not found._"}

---

## Requirement Coverage Audit

{coverage_audit if coverage_audit else "_Coverage audit not found._"}

---

## NFR Manual Checklist
See: docs/NFR-Checklist.md

---

## Bugs Found
See: .claude/skills/state/maintenance/input-queue.md

---

## Sign-off
| Role | Name | Date | Result |
|------|------|------|--------|
| Developer | | | |
"""

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(report)
print(f"[OK] VV Report written to {OUTPUT_PATH}")
print(f"     Overall Result: {overall}")
print(f"     System Tests: {sys_pass}/{total_sys} passed")
print(f"     NFR Auto-Validation: {nfr_pass}/{total_nfr} passed")
