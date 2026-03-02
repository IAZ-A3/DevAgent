# DevAgent Sub-skill: Web V&V
**Parent:** Web Profile — Phase 5 Extension  
**Scope:** Web-specific validation after base V&V completes  
**Output:** E2E results, accessibility report, performance report, security headers report

---

## Purpose

Run web-specific verification layers that the base V&V skill does not cover:
E2E user flows, accessibility audit, Core Web Vitals performance check, and security headers.
Requires Playwright MCP server to be configured.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| VV-Report.md | docs/VV-Report.md | Yes — base V&V must be complete |
| PRD.md | docs/PRD.md | Yes — user flows for E2E |
| RoutingDesign.md | docs/design/RoutingDesign.md | Yes |
| UIDesign.md | docs/design/UIDesign.md | Yes |
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| NFR-Checklist.md | docs/NFR-Checklist.md | Yes — append results |
| Playwright MCP | .mcp.json `playwright` key | Yes |
| Deployed URL or local dev server | TechnologyStack.md or user | Yes |

---

## 1. Pre-flight Check

Before running any test:
1. Verify Playwright MCP is configured in `.mcp.json`
2. Verify a testable URL is available (local dev server or staging deployment)
3. If URL not available: ask user to start dev server or provide staging URL

---

## 2. E2E Test Suite

**Write and execute one E2E test per critical user flow.**

Critical user flows are identified from PRD.md — any FR marked as critical or any flow
that crosses multiple components/pages.

**Minimum E2E coverage:**
- Happy path for each critical feature
- Auth flow: login, logout, protected route redirect (if auth exists)
- Error states: form validation, API error handling
- Navigation: all primary routes reachable and render correctly

**E2E test structure (Playwright):**
```javascript
// E2E: {Flow name} — covers {FR-XXX}
test('{flow description}', async ({ page }) => {
  // arrange
  // act
  // assert
});
```

**Pass criteria:** All E2E tests pass. Any failure = FAIL result for this layer.

---

## 3. Accessibility Audit

**Run axe-core via Playwright on each primary page.**

```javascript
// Inject axe-core and run audit
const { violations } = await new AxeBuilder({ page }).analyze();
```

**Severity mapping:**
| axe-core Impact | Action |
|----------------|--------|
| critical | FAIL — must fix before release |
| serious | FAIL — must fix before release |
| moderate | WARN — document in NFR-Checklist |
| minor | INFO — log only |

**Pass criteria:** Zero critical or serious violations across all audited pages.

---

## 4. Performance Audit

**Run Lighthouse CI against the testable URL.**

Target metrics (from NFR-Checklist defaults, override if project NFRs differ):

| Metric | Pass Threshold |
|--------|---------------|
| LCP (Largest Contentful Paint) | < 2.5s |
| CLS (Cumulative Layout Shift) | < 0.1 |
| INP (Interaction to Next Paint) | < 100ms |
| Lighthouse Performance Score | > 80 |

**If Lighthouse not available in environment:**
- Note in report: "Lighthouse not available — manual performance verification required"
- Add to NFR-Checklist as manual item

---

## 5. Security Headers Check

**Verify HTTP response headers on production/staging URL.**

| Header | Required Value | Severity if Missing |
|--------|---------------|-------------------|
| `Content-Security-Policy` | Any defined policy | HIGH |
| `X-Frame-Options` | DENY or SAMEORIGIN | HIGH |
| `X-Content-Type-Options` | nosniff | MEDIUM |
| `Referrer-Policy` | strict-origin-when-cross-origin | MEDIUM |
| `Permissions-Policy` | Any defined policy | LOW |
| `Strict-Transport-Security` | max-age ≥ 31536000 | HIGH (production only) |

---

## 6. Output

Append to `docs/VV-Report.md` under a new section:

```markdown
## Web V&V Results

### E2E Tests
| Flow | Test | Result | Duration |
|------|------|--------|----------|
| {flow} | {test name} | PASS/FAIL | {ms} |

**E2E Result: PASS | FAIL**

### Accessibility Audit
| Page | Violations (critical/serious) | Result |
|------|------------------------------|--------|
| /home | 0 | PASS |

**Accessibility Result: PASS | FAIL**

### Performance Audit
| Metric | Value | Threshold | Result |
|--------|-------|-----------|--------|
| LCP | {value} | < 2.5s | PASS/FAIL |
| CLS | {value} | < 0.1 | PASS/FAIL |

**Performance Result: PASS | FAIL | SKIPPED**

### Security Headers
| Header | Present | Value | Result |
|--------|---------|-------|--------|
| CSP | yes | ... | PASS |

**Security Result: PASS | FAIL**

---
### Web V&V Overall: PASS | PASS_WITH_WARNINGS | FAIL
```

Update `docs/NFR-Checklist.md` web section with actual results.
