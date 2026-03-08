# Web Profile
# Profile type: Extension — loads on top of base skills when project type is a web project
# CLAUDE.md Section 4 activates this profile and runs check-dependencies.py before any phase work.
# Triggered by: CLAUDE.md detecting "web" project type from PROJECT.md or user prompt
# Scope: Frontend-only, Fullstack (frontend + API), or Fullstack + Database
# Extension mode: adds to base 7-phase skills — does not replace them.

---

## Purpose

Extend the base 7-phase engineering agent with web-specific skills, design documents,
testing tools, and Cloudflare deployment support. Framework-agnostic. Infers stack
from TechnologyStack.md when available, or asks the user during Requirements phase.

---

## 1. Profile Activation

CLAUDE.md activates this profile when any of the following are true:
- `PROJECT.md` → Type field contains: "web", "webapp", "SPA", "frontend", "fullstack", "site"
- User prompt contains: "website", "web app", "frontend", "React", "Vue", "Svelte", "Next", "Nuxt", "landing page", "dashboard", "web"
- `TechnologyStack.md` references a web framework

On activation:
1. Run dependency check (Section 2) — verify required skills and MCP servers are present
2. Determine web project subtype (Section 3)
3. Load subtype-specific extensions for each phase

---

## 2. Dependency Check Protocol

Before any web profile work begins, verify all required dependencies.

### Required Skills

| Skill | Local Path | Required For |
|-------|-----------|-------------|
| `frontend-design` | `.claude/skills/frontend-design/SKILL.md` | All web projects |
| `web-artifacts-builder` | `.claude/skills/web-artifacts-builder/SKILL.md` | Component-heavy projects |

**Check procedure:**
```
For each required skill:
  1. Check if SKILL.md exists at local path
  2. If exists → OK, load on demand
  3. If missing → look up in .claude/registry.md
  4. Present to user:
     "Required skill '{name}' is not installed.
      Source: {url}
      Install it now? (yes/no)"
  5. If yes → download SKILL.md to local path, confirm success
  6. If no → warn that web profile functionality will be reduced, continue
```

### Required MCP Servers

| MCP Server | Config Key | Required For |
|-----------|-----------|-------------|
| `playwright` | `playwright` | E2E testing (all web projects) |
| `cloudflare` | `cloudflare` | Deployment (Cloudflare target) |
| `supabase` | `supabase` | Fullstack + Database projects only |

**Check procedure:**
```
For each required MCP server:
  1. Check .mcp.json in project root for config key
  2. If found → OK
  3. If missing → look up in .claude/registry.md
  4. Present to user:
     "Required MCP server '{name}' is not configured.
      Install command: {command}
      Add to .mcp.json? I will show you the exact config snippet."
  5. If yes → show JSON snippet, ask user to add it, then verify
  6. If no → warn which features will be unavailable, continue
```

**Never install or modify config files automatically. Always show and ask first.**

---

## 3. Web Project Subtype Detection

After dependency check, classify the project:

| Subtype | Indicators | Phases Affected |
|---------|-----------|----------------|
| Frontend-only | No backend, no API, static output | All phases — frontend extensions only |
| Frontend + API | Backend API (REST/GraphQL), no DB | All phases — frontend + API extensions |
| Fullstack | Frontend + API + Database | All phases — all web extensions |

**Detection order:**
1. Read PROJECT.md type field
2. Read TechnologyStack.md if it exists
3. If still unclear, ask user:
   ```
   What type of web project is this?
   A) Frontend only (static site, SPA — no backend)
   B) Frontend + API (with a backend, no database)
   C) Fullstack (frontend + backend + database)
   ```

---

## 4. Phase Extensions

Each base skill is extended with web-specific additions. The base skill runs normally;
these extensions add web-specific steps, documents, and validations.

---

### Phase 1 Extension: Requirements

**NFR defaults can be overridden in PROJECT.md Quality Gates section.**
Read PROJECT.md first:
- `Accessibility standard:` → overrides WCAG default
- `Performance budget:` → overrides LCP/FID/CLS defaults
- `Browser targets:` → overrides browser compatibility default

If a field is set in PROJECT.md, use that value.
If blank or "default NFRs", apply the table below.

**Additional NFRs to always include for web projects:**

| NFR | Default Acceptance Criterion |
|-----|---------------------------|
| Accessibility | WCAG 2.1 AA compliance |
| Performance | Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1 |
| Browser compatibility | Last 2 versions of Chrome, Firefox, Safari, Edge |
| Responsive design | Functional on mobile (375px), tablet (768px), desktop (1280px+) |
| Security | OWASP Top 10 — no critical/high vulnerabilities |
| SEO | If public-facing: meta tags, semantic HTML, sitemap |

**Additional questions for Requirements skill clarification protocol:**
- Is this public-facing or internal (auth-gated)?
- Are there existing brand guidelines or a design system to follow?
- Any third-party integrations? (analytics, payments, auth providers)
- Any reference sites or examples the user wants to share?

---

### Phase 2 Extension: Planning

**Additional task types to generate for web projects:**

| Task Type | Example | Complexity |
|-----------|---------|-----------|
| Component design | Design reusable Button, Card, Modal components | S-M |
| Page layout | Implement HomePage layout and routing | M |
| API integration | Connect frontend to {endpoint} | M-L |
| Auth flow | Implement login/logout/session management | L |
| Responsive pass | Apply responsive breakpoints to {feature} | S |
| Accessibility pass | Audit and fix accessibility for {feature} | M |
| E2E test | Write Playwright E2E for {user flow} | M |
| Deployment | Deploy to Cloudflare Pages/Workers | M |

---

### Phase 3 Extension: Design & Architecture

**Additional design documents for web projects:**

| Document | Required For | Contents |
|----------|-------------|----------|
| `UIDesign.md` | All web | Component library, design tokens, spacing, typography, color system |
| `RoutingDesign.md` | All web | Page routes, navigation structure, URL patterns, protected routes |
| `StateManagement.md` | Frontend-only, Fullstack | State strategy, data flow, caching approach |
| `APIContracts.md` | Frontend + API, Fullstack | Endpoint definitions, request/response schemas, auth headers |
| `DatabaseSchema.md` | Fullstack only | Tables, relationships, indexes, RLS policies |
| `DeploymentDesign.md` | All web | Cloudflare target (Pages vs Workers), environment strategy, env vars |
| `SecurityDesign.md` | All web | Auth strategy, CORS policy, CSP headers, input validation approach |

**UIDesign.md must always be generated first** — other documents reference its component names and design tokens.

**Invoke `frontend-design` skill** when generating UIDesign.md:
- Check if `.claude/skills/frontend-design/SKILL.md` exists (dependency check already ran)
- Load it and follow its guidelines for component design, Tailwind usage, and accessibility markup

---

### Phase 4 Extension: Implementation

**Additional sub-skill: Component Builder**
- Invoked by Implementation orchestrator for frontend tasks
- Uses `frontend-design` skill guidelines
- Generates: component file, component test, Storybook story (if Storybook in TechnologyStack)
- Every component must: be accessible (ARIA roles, keyboard nav), be responsive, accept props defined in UIDesign.md

**Additional sub-skill: API Route Builder** (Frontend + API, Fullstack only)
- Generates API route handlers per APIContracts.md
- Includes: input validation, error responses, auth middleware hook
- Writes integration test per endpoint

**Additional sub-skill: Database Migration Writer** (Fullstack only)
- Generates migration files per DatabaseSchema.md
- Includes RLS policies if Supabase
- Never modifies existing migrations — creates new ones only

**Coding rules specific to web:**
- No inline styles — use design tokens from UIDesign.md
- No hardcoded colors, spacing, or font sizes
- All images must have alt text
- All interactive elements must be keyboard accessible
- Environment variables never hardcoded — always from `.env` / platform config

---

### Phase 5 Extension: Verification & Validation

**Additional testing layers for web projects:**

| Test Type | Tool | Invoked By | When |
|-----------|------|-----------|------|
| E2E tests | Playwright (via MCP) | Web V&V sub-skill | After system tests |
| Accessibility audit | Playwright + axe-core | Web V&V sub-skill | After E2E tests |
| Performance audit | Lighthouse CI | Web V&V sub-skill | After deployment to staging |
| Visual regression | Playwright screenshots | Web V&V sub-skill | After E2E tests |

**Web V&V sub-skill** (see `sub-skills/web-vv.md`) runs after base V&V completes:
1. E2E test suite via Playwright MCP
2. Accessibility audit — report WCAG violations, fail if any AA violations found
3. Performance check — report Core Web Vitals against NFR acceptance criteria
4. Security headers check — verify CSP, CORS, X-Frame-Options, HSTS

**NFR-Checklist.md additions for web:**
```markdown
## Web-Specific NFR Checklist
- [ ] WCAG 2.1 AA: 0 violations (axe-core audit)
- [ ] LCP < 2.5s (Lighthouse)
- [ ] CLS < 0.1 (Lighthouse)
- [ ] FID/INP < 100ms (Lighthouse)
- [ ] All E2E flows passing (Playwright)
- [ ] CSP header present
- [ ] No mixed content warnings
- [ ] Responsive at 375px, 768px, 1280px
- [ ] Browser tested: Chrome, Firefox, Safari
```

---

### Phase 6 Extension: Release

**Cloudflare deployment — inferred from TechnologyStack.md:**

| Project Type | Cloudflare Target | Deploy Method |
|-------------|------------------|--------------|
| Static site / SPA | Cloudflare Pages | `wrangler pages deploy` |
| SSR / Edge rendering | Cloudflare Pages + Functions | `wrangler pages deploy` |
| API / Backend | Cloudflare Workers | `wrangler deploy` |
| Fullstack | Pages (frontend) + Workers (API) | Both |
| Database | Cloudflare D1 | Migration via `wrangler d1 execute` |

**Release steps added for web projects:**
1. Run production build — verify it succeeds with no errors
2. Check environment variables — confirm all required vars are set in Cloudflare dashboard
3. Deploy via Cloudflare MCP (using `cloudflare` MCP server)
4. Run smoke test on deployed URL — verify homepage loads, auth works, API responds
5. Invalidate CDN cache if needed
6. Add deployment URL to RELEASE-NOTES.md

**Additional release artifact:** `docs/release/DeploymentReport.md`
```markdown
# Deployment Report — v{version}
## Date: {date}
## Target: Cloudflare Pages | Workers
## Production URL: {url}
## Build duration: {seconds}
## Deploy duration: {seconds}
## Smoke test: PASS | FAIL
## Environment variables verified: yes | no
```

---

### Phase 7 Extension: Maintenance

**Additional bug categories for web projects:**

| Category | Example | Investigation Start |
|----------|---------|-------------------|
| UI regression | Component renders incorrectly | UIDesign.md + component file |
| Routing bug | Page not found, redirect loop | RoutingDesign.md + router config |
| API contract violation | Frontend/backend mismatch | APIContracts.md + both sides |
| Performance regression | LCP increased after change | Lighthouse before/after comparison |
| Accessibility regression | New element not keyboard accessible | axe-core targeted audit |
| Cloudflare deployment issue | Worker error, Pages build fail | Wrangler logs via Cloudflare MCP |

**After bug fix:** run targeted E2E test (not full suite) covering the affected user flow.

---

## 5. Reference Examples Protocol

When the user provides reference sites or design examples:
1. Note the references in `docs/design/UIDesign.md` under a "References" section
2. Extract design patterns to inform (not copy): layout approach, color tone, component patterns, typography scale
3. Never copy CSS, assets, or code from reference sites
4. Treat references as inspiration input to the `frontend-design` skill, not as source material
