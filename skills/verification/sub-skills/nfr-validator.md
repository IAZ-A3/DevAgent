# DevAgent Sub-skill: NFR Validator
**Parent:** V&V Orchestrator  
**Scope:** All NFRs (global + feature-scoped)  
**Output:** Auto-validated NFR results + manual verification checklist

---

## Purpose

Validate every NFR against its acceptance criterion. Auto-test what can be measured programmatically. For NFRs that cannot be automated, produce a clear manual verification checklist for the user to sign off.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| PRD.md (NFR sections) | docs/PRD.md | Yes |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| SecurityDesign.md | docs/design/SecurityDesign.md | If exists |
| ErrorHandling.md | docs/design/ErrorHandling.md | If exists |
| src/ | project source | Yes |

---

## 1. NFR Classification

Before testing, classify each NFR:

| Category | Auto-testable? | Method |
|----------|---------------|--------|
| Performance (response time, throughput) | Yes | Timing wrapper around operation |
| Reliability (uptime, error rate) | Partial | Run operation N times, measure failure rate |
| Security (input validation, auth) | Partial | Automated probes + manual checklist |
| Maintainability (code complexity) | Yes | Static analysis tools |
| Compatibility (OS, runtime version) | Partial | Check runtime version, manual for multi-OS |
| Usability | No | Manual checklist only |
| Scalability | Partial | Load simulation if feasible |

---

## 2. Auto-Validation Execution

### Performance NFRs
For each performance NFR with a measurable criterion (e.g. "response time < 200ms at P95"):
1. Write a timing test that executes the operation 100 times
2. Calculate P50, P95, P99 response times
3. Compare against acceptance criterion
4. PASS if criterion met, FAIL with actual measurements if not

```python
# Template: performance timing test
import time, statistics

def measure_operation(fn, iterations=100):
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        times.append((time.perf_counter() - start) * 1000)  # ms
    return {
        'p50': statistics.median(times),
        'p95': sorted(times)[int(len(times)*0.95)],
        'p99': sorted(times)[int(len(times)*0.99)],
        'max': max(times)
    }
```

### Maintainability NFRs
Run static analysis if tools are available:
- Python: `radon cc src/ -a` (cyclomatic complexity)
- JavaScript: `eslint src/ --format json`
- General: count lines per file, flag files >500 lines

### Security NFRs
Auto-testable aspects:
- Input validation: send boundary/invalid inputs, verify rejection
- No sensitive data in logs: scan log output for patterns (passwords, tokens, keys)
- Dependency versions: scan for known vulnerable versions if audit tool available

### Reliability NFRs
- Run critical operation N times (N = 100 or per NFR definition)
- Measure failure rate
- Inject a controlled error (e.g. missing file, bad input) — verify graceful handling

---

## 3. Manual Checklist Generation

For each NFR that cannot be auto-tested, generate a checklist item:

```markdown
### Manual Check: {NFR-ID}
**Category:** {Usability | Security | Compatibility | ...}
**Requirement:** {full NFR text from PRD}
**Acceptance Criterion:** {measurable criterion from PRD}
**How to verify:**
1. {step-by-step instruction}
2. {expected result}
**Pass condition:** {what the user should observe to mark this PASS}
**Status:** [ ] PENDING — awaiting user verification
```

---

## 4. Output

**Auto-results** → `.claude/skills/state/vv/nfr-auto-results.md`:
```markdown
# NFR Auto-Validation Results
## Date: {date}

| NFR ID | Category | Criterion | Result | Actual Value | Notes |
|--------|----------|-----------|--------|-------------|-------|
| NFR-001 | Performance | <200ms P95 | PASS | 143ms P95 | |
| NFR-002 | Security | No plaintext passwords in logs | PASS | None found | |
| FEAT-001-NFR-001 | Reliability | <0.1% error rate | FAIL | 2.3% error rate | See details |
```

**Manual checklist** → `docs/NFR-Checklist.md`:
```markdown
# NFR Manual Verification Checklist
## Project: {name}
## Generated: {date}
## Instructions: Review each item, perform the verification steps, mark PASS or FAIL.

---

### {NFR-ID}: {NFR title}
...{checklist items as defined above}...

---

## Sign-off
| NFR ID | Verified By | Date | Result |
|--------|-------------|------|--------|
| NFR-003 | | | |
```

---

## 5. Context Management

- Process one NFR category at a time
- Save auto-results after each category
- Checkpoint after performance and security categories (heaviest)
