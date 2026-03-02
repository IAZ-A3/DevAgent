# DevAgent — Skill & MCP Registry
# DevAgent reads this file when it needs to install a missing skill or MCP server.
# Format: name, type, source URL, description, install command (if applicable).
# Add your own entries in the "Custom" sections below.

---

## How the Registry Works

When Claude Code detects a required skill or MCP server is missing, it:
1. Checks this registry for a matching entry
2. Shows the user the name, source, and install method
3. Asks for confirmation before downloading/installing anything
4. Only proceeds after explicit user approval

---

## Built-in Skills

These skills are known dependencies of the web profile and other built-in profiles.

| Name | Local Path | Source URL | Description |
|------|-----------|------------|-------------|
| `frontend-design` | `.claude/skills/frontend-design/` | https://raw.githubusercontent.com/anthropics/claude-code-skills/main/frontend-design/SKILL.md | UI/UX component design, Tailwind, accessible markup |
| `web-artifacts-builder` | `.claude/skills/web-artifacts-builder/` | https://raw.githubusercontent.com/anthropics/claude-code-skills/main/web-artifacts-builder/SKILL.md | Multi-component web artifact generation |
| `canvas-design` | `.claude/skills/canvas-design/` | https://raw.githubusercontent.com/anthropics/claude-code-skills/main/canvas-design/SKILL.md | Visual design assets for web projects |

> Note: URLs above are illustrative. Verify actual URLs from Anthropic's skills documentation
> before installing. Claude Code will show you the URL and ask for confirmation first.

---

## Built-in MCP Servers

These MCP servers are known dependencies of specific profiles.

| Name | Config Key | Install Command | Description | Required By |
|------|-----------|-----------------|-------------|-------------|
| `playwright` | `playwright` | `npx @playwright/mcp@latest` | Browser automation for E2E testing | web-profile |
| `cloudflare` | `cloudflare` | `npx @cloudflare/mcp-server-cloudflare@latest` | Cloudflare Workers, Pages, D1, R2 deploy | web-profile |
| `github` | `github` | `npx @modelcontextprotocol/server-github@latest` | GitHub repo, issues, PRs | any |
| `filesystem` | `filesystem` | `npx @modelcontextprotocol/server-filesystem@latest` | Local file system access | any |
| `supabase` | `supabase` | `npx @supabase/mcp-server-supabase@latest` | Supabase DB, auth, storage | web-profile (fullstack) |
| `xcodebuild` | `xcodebuild` | `npx xcode-build-mcp@latest` | Xcode build, test, archive, export | macos-profile |

---

## Custom Skills
<!-- Add your own skills here as you discover them -->
<!-- Format:
| `skill-name` | `.claude/skills/skill-name/` | https://... | Description |
-->

---

## Custom MCP Servers
<!-- Add your own MCP servers here -->
<!-- Format:
| `server-name` | `config-key` | `npx install-command` | Description | Required By |
-->

---

## MCP Configuration File Location

Claude Code checks for MCP configuration in this order:
1. `.mcp.json` in project root (project-scoped)
2. `~/.config/claude/claude_desktop_config.json` (global)

When installing an MCP server, Claude Code will tell you which file to update
and provide the exact JSON snippet to add. It will never modify these files automatically.
