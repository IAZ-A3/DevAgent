# PROJECT.md
# Web project configuration for Claude Code.
# Copy this file to your project root as PROJECT.md and fill it in.
# This file extends the base PROJECT.md template with web-specific fields.

---

## Project Identity

- **Name:** 
- **Type:** web                 # triggers web profile in CLAUDE.md
- **Subtype:**                  # frontend-only | frontend+api | fullstack
- **One-liner:**                # what this project does in one sentence
- **Target platform:** web      # browser-based
- **Target users:**             # e.g. developers, consumers, internal team
- **Public-facing:**            # yes / no (affects SEO and security NFRs)

---

## Web Stack (fill what you know — rest inferred during Design phase)

- **Frontend framework:**       # e.g. React, Vue, Svelte, Next.js, Nuxt — or "TBD"
- **Backend:**                  # e.g. Cloudflare Workers, Node.js, none — or "TBD"
- **Database:**                 # e.g. Cloudflare D1, Supabase, none — or "TBD"
- **Auth:**                     # e.g. Clerk, Supabase Auth, custom, none — or "TBD"
- **Styling:**                  # e.g. Tailwind CSS, CSS Modules, styled-components — or "TBD"
- **Deployment target:** Cloudflare   # Pages | Workers | Both

---

## Design References

# URLs or descriptions of reference sites / design examples.
# Claude Code will extract design patterns (not copy code/assets).
- 

---

## Git Conventions

- **Commit style:**             # e.g. Conventional Commits, free-form
- **Branch strategy:**          # e.g. main only, feature branches
- **PR required:**              # yes / no
- **Protected branches:**       # e.g. main, production

---

## Quality Gates

- **Tests must pass before:**   # e.g. every commit, every release
- **Accessibility standard:**   WCAG 2.1 AA     # or AAA, or "none"
- **Performance budget:**       # e.g. LCP < 2.5s, or "default NFRs"
- **Browser targets:**          # e.g. "last 2 versions Chrome, Firefox, Safari, Edge"

---

## Claude Code Preferences

- **Ask before adding a dependency:**   yes
- **Ask before deleting any file:**     yes
- **Ask before modifying design docs:** yes
- **Ask before deploying:**             yes
- **Preferred response style:**         # e.g. concise, detailed
- **Language for all docs:**            # e.g. English

---

## Out of Scope

# List anything Claude Code must never do in this project.
- Never push to git without explicit instruction
- Never expose environment variable values in logs or reports
- Never commit .env files
- 

---

## Notes

# Any other context: constraints, third-party services, brand guidelines, etc.
#
