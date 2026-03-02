#!/usr/bin/env python3
"""
check-dependencies.py
Checks whether required skills and MCP servers are present for a given profile.
Reads from .claude/registry.md and .mcp.json.

Usage:
  python3 check-dependencies.py skills              # check all skills
  python3 check-dependencies.py mcp                 # check MCP servers
  python3 check-dependencies.py all                 # check both
  python3 check-dependencies.py skill frontend-design  # check specific skill
  python3 check-dependencies.py mcp playwright         # check specific MCP
"""

import sys
import json
import re
from pathlib import Path

REGISTRY_PATH = Path(".claude/registry.md")
MCP_CONFIG_PATHS = [
    Path(".mcp.json"),
    Path.home() / ".config/claude/claude_desktop_config.json"
]

# --- Web profile known dependencies (hardcoded) ---
WEB_SKILLS = [
    {
        "name": "frontend-design",
        "local_path": ".claude/skills/frontend-design/SKILL.md",
        "description": "UI/UX component design, Tailwind, accessible markup"
    },
    {
        "name": "web-artifacts-builder",
        "local_path": ".claude/skills/web-artifacts-builder/SKILL.md",
        "description": "Multi-component web artifact generation"
    }
]

WEB_MCP = [
    {
        "name": "playwright",
        "config_key": "playwright",
        "install": "npx @playwright/mcp@latest",
        "description": "Browser automation for E2E testing",
        "required_for": "all web projects"
    },
    {
        "name": "cloudflare",
        "config_key": "cloudflare",
        "install": "npx @cloudflare/mcp-server-cloudflare@latest",
        "description": "Cloudflare deployment (Pages, Workers, D1)",
        "required_for": "all web projects"
    },
    {
        "name": "supabase",
        "config_key": "supabase",
        "install": "npx @supabase/mcp-server-supabase@latest",
        "description": "Supabase DB, auth, storage",
        "required_for": "fullstack projects only"
    }
]


def load_mcp_config():
    """Load MCP config from .mcp.json or global config."""
    for path in MCP_CONFIG_PATHS:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                # Normalize: both .mcp.json and claude_desktop_config use mcpServers
                servers = data.get("mcpServers", {})
                return servers, str(path)
            except json.JSONDecodeError:
                continue
    return {}, None


def check_skills(names=None):
    """Check if required skills are installed locally."""
    skills = WEB_SKILLS if names is None else [s for s in WEB_SKILLS if s["name"] in names]

    print("\n=== Skill Dependency Check ===\n")
    missing = []
    for skill in skills:
        path = Path(skill["local_path"])
        status = "✓ FOUND" if path.exists() else "✗ MISSING"
        print(f"  {status}  {skill['name']}")
        print(f"           {skill['local_path']}")
        if not path.exists():
            missing.append(skill)

    if missing:
        print(f"\n⚠ {len(missing)} skill(s) missing:\n")
        for skill in missing:
            print(f"  {skill['name']} — {skill['description']}")
            # Look up URL from registry
            url = lookup_registry_skill(skill["name"])
            if url:
                print(f"  Source: {url}")
            print(f"  Install: download SKILL.md from source to {skill['local_path']}\n")
    else:
        print("\n✓ All required skills are installed.\n")

    return missing


def check_mcp(names=None):
    """Check if required MCP servers are configured."""
    servers = WEB_MCP if names is None else [s for s in WEB_MCP if s["name"] in names]
    mcp_config, config_path = load_mcp_config()

    print("\n=== MCP Server Dependency Check ===\n")
    if config_path:
        print(f"  Config file: {config_path}\n")
    else:
        print("  ⚠ No MCP config file found (.mcp.json or global config)\n")

    missing = []
    for server in servers:
        configured = server["config_key"] in mcp_config
        status = "✓ CONFIGURED" if configured else "✗ MISSING"
        print(f"  {status}  {server['name']}  ({server['required_for']})")
        if not configured:
            missing.append(server)

    if missing:
        print(f"\n⚠ {len(missing)} MCP server(s) not configured:\n")
        for server in missing:
            print(f"  {server['name']} — {server['description']}")
            print(f"  Install: {server['install']}")
            print(f"  Add to .mcp.json:")
            snippet = {
                "mcpServers": {
                    server["config_key"]: {
                        "command": "npx",
                        "args": server["install"].replace("npx ", "").split()
                    }
                }
            }
            print(f"  {json.dumps(snippet, indent=4)}\n")
    else:
        print("\n✓ All required MCP servers are configured.\n")

    return missing


def lookup_registry_skill(name):
    """Look up skill URL from registry.md."""
    if not REGISTRY_PATH.exists():
        return None
    content = REGISTRY_PATH.read_text()
    pattern = rf'\|\s*`{re.escape(name)}`\s*\|[^|]*\|\s*(https?://[^\s|]+)'
    match = re.search(pattern, content)
    return match.group(1) if match else None


def print_summary(missing_skills, missing_mcp):
    total_missing = len(missing_skills) + len(missing_mcp)
    print("=" * 50)
    if total_missing == 0:
        print("✓ All dependencies satisfied. Ready to proceed.")
    else:
        print(f"⚠ {total_missing} dependency/dependencies missing.")
        print("  Claude Code will ask you to install these before proceeding.")
    print("=" * 50)


# --- Main ---
if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)

cmd = sys.argv[1].lower()

if cmd == "skills":
    missing_s = check_skills()
    print_summary(missing_s, [])

elif cmd == "mcp":
    missing_m = check_mcp()
    print_summary([], missing_m)

elif cmd == "all":
    missing_s = check_skills()
    missing_m = check_mcp()
    print_summary(missing_s, missing_m)

elif cmd == "skill" and len(sys.argv) >= 3:
    missing_s = check_skills([sys.argv[2]])
    print_summary(missing_s, [])

elif cmd == "mcp" and len(sys.argv) >= 3:
    missing_m = check_mcp([sys.argv[2]])
    print_summary([], missing_m)

else:
    print(f"[ERROR] Unknown command: {' '.join(sys.argv[1:])}")
    print(__doc__)
    sys.exit(1)
