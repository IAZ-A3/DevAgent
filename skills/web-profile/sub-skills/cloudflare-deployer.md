# DevAgent Sub-skill: Cloudflare Deployer
**Parent:** Web Profile — Phase 6 Extension  
**Scope:** Deploy web project to Cloudflare (Pages, Workers, D1)  
**Output:** Live deployment URL, DeploymentReport.md

---

## Purpose

Deploy the built web project to Cloudflare using the Cloudflare MCP server.
Infer the correct Cloudflare target from TechnologyStack.md and DeploymentDesign.md.
Verify the deployment with a smoke test before reporting success.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| TechnologyStack.md | docs/design/TechnologyStack.md | Yes |
| DeploymentDesign.md | docs/design/DeploymentDesign.md | Yes |
| Built output directory | TechnologyStack.md | Yes |
| Cloudflare MCP | .mcp.json `cloudflare` key | Yes |
| Version string | Orchestrator | Yes |

---

## 1. Deployment Target Resolution

Read TechnologyStack.md and DeploymentDesign.md to determine:

| Project Type | Cloudflare Target | Build Output | Deploy Command |
|-------------|------------------|-------------|---------------|
| Static site / SPA | Cloudflare Pages | `dist/` or `out/` or `build/` | `wrangler pages deploy {dir}` |
| SSR (Next, Nuxt, SvelteKit) | Cloudflare Pages + Functions | `.vercel/output` or `.output` | Framework adapter + wrangler |
| API only | Cloudflare Workers | `src/worker.js` or `dist/worker.js` | `wrangler deploy` |
| Fullstack | Pages (frontend) + Workers (API) | Both | Two separate deploys |
| Database | Cloudflare D1 | Migration files | `wrangler d1 execute` |

If target is ambiguous: ask user before proceeding.

---

## 2. Pre-deployment Checklist

Before deploying, verify:

- [ ] Production build succeeds (`npm run build` or equivalent)
- [ ] Build output directory exists and is non-empty
- [ ] `wrangler.toml` exists and has correct project name and account ID
- [ ] All required environment variables documented in DeploymentDesign.md are confirmed set in Cloudflare dashboard
- [ ] No `.env` file committed to git (security check)
- [ ] Cloudflare MCP server is active

**For environment variables:** list all required vars from DeploymentDesign.md and ask user to confirm they are set in the Cloudflare dashboard. Never read or display actual secret values.

---

## 3. Database Migration (Fullstack + D1 only)

If project uses Cloudflare D1:
1. List pending migrations (files in `migrations/` not yet applied)
2. Show migration list to user
3. Ask: "Apply these migrations to production D1? This cannot be undone."
4. Wait for explicit confirmation
5. Execute: `wrangler d1 execute {database-name} --file={migration} --remote`
6. Verify success before proceeding to frontend/worker deploy

---

## 4. Deployment Execution

Via Cloudflare MCP server:

**Step 1 — Build:**
```bash
{build command from TechnologyStack.md}
```
Capture output. If build fails: stop, report error, do not deploy.

**Step 2 — Deploy:**
```bash
wrangler pages deploy {build-dir} --project-name={project-name}
# or
wrangler deploy
```
Capture deployment URL from output.

**Step 3 — Workers (if fullstack):**
```bash
wrangler deploy
```
Capture Worker URL.

---

## 5. Smoke Test

After deployment, run basic smoke test against the live URL:

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| Homepage loads | HTTP GET / | Status 200, non-empty body |
| No JS errors | Playwright page load | Zero console errors |
| Auth page reachable | HTTP GET /login (if exists) | Status 200 |
| API health | HTTP GET /api/health (if exists) | Status 200 |
| HTTPS redirect | HTTP GET (non-https) | Redirects to https |

If any smoke test fails: report immediately. Do not mark release as complete.

---

## 6. Output

Write `docs/release/DeploymentReport.md`:

```markdown
# Deployment Report — v{version}
**Date:** {date}  
**Target:** Cloudflare Pages | Workers | Both  
**Project Name:** {wrangler project name}  

## URLs
- Production: {url}
- Worker API: {url} (if applicable)

## Build
- Command: {command}
- Duration: {seconds}
- Output size: {MB}

## Migrations Applied
{list or "None"}

## Smoke Test Results
| Check | Result |
|-------|--------|
| Homepage loads | PASS/FAIL |
| No JS errors | PASS/FAIL |
| API health | PASS/FAIL/N/A |
| HTTPS redirect | PASS/FAIL |

## Environment Variables
All required variables confirmed set: yes | no — missing: {list}

## Overall Result: SUCCESS | FAILED
```

Report production URL to user clearly at the end.
