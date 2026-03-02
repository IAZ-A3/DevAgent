#!/usr/bin/env python3
"""
check-macos-dependencies.py
Checks whether required tools and MCP servers are present for the macOS profile.
Usage:
  python3 check-macos-dependencies.py all     # check everything
  python3 check-macos-dependencies.py tools   # check CLI tools only
  python3 check-macos-dependencies.py mcp     # check MCP servers only
"""

import sys
import json
import shutil
import subprocess
from pathlib import Path

MCP_CONFIG_PATHS = [
    Path(".mcp.json"),
    Path.home() / ".config/claude/claude_desktop_config.json"
]

REQUIRED_TOOLS = [
    {
        "name": "Xcode",
        "check": ["xcodebuild", "-version"],
        "install": "Install Xcode from the Mac App Store",
        "required_for": "build, test, archive"
    },
    {
        "name": "Xcode Command Line Tools",
        "check": ["xcode-select", "-p"],
        "install": "xcode-select --install",
        "required_for": "build tools"
    },
    {
        "name": "create-dmg",
        "check": ["which", "create-dmg"],
        "install": "brew install create-dmg",
        "required_for": "DMG packaging"
    },
    {
        "name": "notarytool",
        "check": ["xcrun", "notarytool", "--version"],
        "install": "Included with Xcode — install or update Xcode",
        "required_for": "notarization"
    },
    {
        "name": "stapler",
        "check": ["xcrun", "stapler", "--version"],
        "install": "Included with Xcode — install or update Xcode",
        "required_for": "stapling notarization ticket"
    },
    {
        "name": "codesign",
        "check": ["which", "codesign"],
        "install": "Included with Xcode Command Line Tools",
        "required_for": "code signing"
    },
    {
        "name": "spctl",
        "check": ["which", "spctl"],
        "install": "Included with macOS",
        "required_for": "Gatekeeper verification"
    }
]

REQUIRED_MCP = [
    {
        "name": "xcodebuild",
        "config_key": "xcodebuild",
        "install": "npx xcode-build-mcp@latest",
        "description": "Xcode build, test, archive, export automation",
        "required_for": "all macOS projects"
    }
]


def run_check(cmd):
    """Run a check command and return True if it succeeds."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, ""


def load_mcp_config():
    for path in MCP_CONFIG_PATHS:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                return data.get("mcpServers", {}), str(path)
            except json.JSONDecodeError:
                continue
    return {}, None


def check_signing_identity():
    """Check for Developer ID Application certificate."""
    ok, output = run_check(
        ["security", "find-identity", "-v", "-p", "codesigning"]
    )
    if ok and "Developer ID Application" in output:
        # Extract certificate name
        for line in output.splitlines():
            if "Developer ID Application" in line:
                return True, line.strip()
        return True, "Developer ID Application (found)"
    return False, None


def check_tools():
    print("\n=== macOS Tool Check ===\n")
    missing = []

    for tool in REQUIRED_TOOLS:
        ok, output = run_check(tool["check"])
        version = output.split("\n")[0] if output else ""
        status = f"✓ FOUND   {version}" if ok else "✗ MISSING"
        print(f"  {status}")
        print(f"  {tool['name']} — {tool['required_for']}")
        if not ok:
            print(f"  Install:  {tool['install']}")
            missing.append(tool)
        print()

    # Check signing identity separately
    print("  Checking Developer ID certificate...")
    ok, cert = check_signing_identity()
    if ok:
        print(f"  ✓ FOUND   {cert}")
    else:
        print("  ✗ MISSING  Developer ID Application certificate")
        print("  Install:  Download from Apple Developer portal → Certificates")
        print("            Then double-click to install into Keychain")
        missing.append({"name": "Developer ID Application certificate",
                        "required_for": "code signing and notarization"})
    print()

    return missing


def check_mcp():
    print("\n=== MCP Server Check ===\n")
    mcp_config, config_path = load_mcp_config()

    if config_path:
        print(f"  Config file: {config_path}\n")
    else:
        print("  ⚠ No MCP config file found (.mcp.json or global config)\n")

    missing = []
    for server in REQUIRED_MCP:
        configured = server["config_key"] in mcp_config
        status = "✓ CONFIGURED" if configured else "✗ MISSING"
        print(f"  {status}  {server['name']} — {server['description']}")

        if not configured:
            missing.append(server)
            snippet = {
                "mcpServers": {
                    server["config_key"]: {
                        "command": "npx",
                        "args": server["install"].replace("npx ", "").split()
                    }
                }
            }
            print(f"  Install:  {server['install']}")
            print(f"  Add to .mcp.json:")
            print(f"  {json.dumps(snippet, indent=4)}")
        print()

    return missing


def print_summary(missing_tools, missing_mcp):
    total = len(missing_tools) + len(missing_mcp)
    print("=" * 55)
    if total == 0:
        print("✓ All macOS profile dependencies satisfied.")
        print("  Ready to start development.")
    else:
        print(f"⚠ {total} dependency/dependencies missing.")
        print("  Resolve the above before proceeding with the macOS profile.")
        if any(t["name"] == "Developer ID Application certificate"
               for t in missing_tools):
            print("\n  NOTE: Developer ID certificate is only needed at Release phase.")
            print("  Development and testing can proceed without it.")
    print("=" * 55)


# --- Main ---
if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(0)

cmd = sys.argv[1].lower()

if cmd == "tools":
    mt = check_tools()
    print_summary(mt, [])
elif cmd == "mcp":
    mm = check_mcp()
    print_summary([], mm)
elif cmd == "all":
    mt = check_tools()
    mm = check_mcp()
    print_summary(mt, mm)
else:
    print(f"[ERROR] Unknown command: {cmd}")
    print(__doc__)
    sys.exit(1)
