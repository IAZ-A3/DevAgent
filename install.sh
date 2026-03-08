#!/usr/bin/env bash
# DevAgent installer — shell alternative to npx devagent-cc
# Usage: curl -fsSL https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop/install.sh | bash
# Or:    curl -fsSL https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop/install.sh | bash -s -- --global
#        curl -fsSL https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop/install.sh | bash -s -- --local

set -e

REPO="https://github.com/IAZ-A3/DevAgent"
RAW_BASE="https://raw.githubusercontent.com/IAZ-A3/DevAgent/develop"
BRANCH="develop"
ARCHIVE_URL="https://github.com/IAZ-A3/DevAgent/archive/refs/heads/${BRANCH}.zip"

# ─── Colors ────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# ─── Parse args ────────────────────────────────────────────────────────────
SCOPE=""
UNINSTALL=false

for arg in "$@"; do
  case $arg in
    --global|-g) SCOPE="global" ;;
    --local|-l)  SCOPE="local"  ;;
    --uninstall) UNINSTALL=true ;;
  esac
done

# ─── Banner ────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}  DevAgent — Claude Code Development Agent${RESET}"
echo -e "  ${BLUE}${REPO}${RESET}"
echo ""

# ─── Check dependencies ────────────────────────────────────────────────────
check_dep() {
  if ! command -v "$1" &> /dev/null; then
    echo -e "${RED}  ✗ Required: $1 is not installed${RESET}"
    exit 1
  fi
}

check_dep curl
check_dep unzip

# ─── Prompt for scope if not provided ──────────────────────────────────────
if [ -z "$SCOPE" ] && [ "$UNINSTALL" = false ]; then
  echo "  Where would you like to install DevAgent?"
  echo ""
  echo "    1) Global — available in ALL projects  (~/.claude/)  [recommended]"
  echo "    2) Local  — this project only          (./.claude/)"
  echo ""
  read -rp "  Enter 1 or 2: " choice
  case $choice in
    1) SCOPE="global" ;;
    2) SCOPE="local"  ;;
    *) echo -e "${RED}  Invalid choice. Exiting.${RESET}"; exit 1 ;;
  esac
fi

# ─── Resolve paths ─────────────────────────────────────────────────────────
if [ "$SCOPE" = "global" ]; then
  CLAUDE_DIR="$HOME/.claude"
  ROOT_DIR="$HOME"
else
  CLAUDE_DIR="$(pwd)/.claude"
  ROOT_DIR="$(pwd)"
fi

# ─── Uninstall ─────────────────────────────────────────────────────────────
if [ "$UNINSTALL" = true ]; then
  echo -e "  ${YELLOW}Uninstalling DevAgent from: ${CLAUDE_DIR}${RESET}"
  echo ""

  # Remove deva: commands
  if [ -d "${CLAUDE_DIR}/commands" ]; then
    find "${CLAUDE_DIR}/commands" -name "deva:*" -delete
    echo -e "  ${GREEN}✓ Removed deva: commands${RESET}"
  fi

  # Remove skills/deva
  if [ -d "${CLAUDE_DIR}/skills/deva" ]; then
    rm -rf "${CLAUDE_DIR}/skills/deva"
    echo -e "  ${GREEN}✓ Removed skills/deva/${RESET}"
  fi

  # Remove registry.md
  if [ -f "${CLAUDE_DIR}/registry.md" ]; then
    rm "${CLAUDE_DIR}/registry.md"
    echo -e "  ${GREEN}✓ Removed registry.md${RESET}"
  fi

  # Remove CLAUDE.md and templates from root
  for file in CLAUDE.md PROJECT-base-template.md PROJECT-web-template.md PROJECT-macos-template.md; do
    if [ -f "${ROOT_DIR}/${file}" ]; then
      rm "${ROOT_DIR}/${file}"
      echo -e "  ${GREEN}✓ Removed ${file}${RESET}"
    fi
  done

  echo ""
  echo -e "  ${GREEN}✅ DevAgent uninstalled.${RESET}"
  echo -e "  Your project files (docs/, PROJECT.md, .claude/skills/state/) were not touched."
  echo ""
  exit 0
fi

# ─── Download repo archive ─────────────────────────────────────────────────
echo -e "  ${BLUE}Downloading DevAgent...${RESET}"

TMP_DIR=$(mktemp -d)
TMP_ZIP="${TMP_DIR}/devagent.zip"
TMP_EXTRACT="${TMP_DIR}/extracted"

curl -fsSL "$ARCHIVE_URL" -o "$TMP_ZIP"
mkdir -p "$TMP_EXTRACT"
unzip -q "$TMP_ZIP" -d "$TMP_EXTRACT"

# The extracted folder will be named DevAgent-{branch}
EXTRACTED=$(find "$TMP_EXTRACT" -maxdepth 1 -mindepth 1 -type d | head -1)

if [ -z "$EXTRACTED" ]; then
  echo -e "${RED}  ✗ Failed to extract archive${RESET}"
  rm -rf "$TMP_DIR"
  exit 1
fi

echo -e "  ${GREEN}✓ Downloaded${RESET}"

# ─── Install ───────────────────────────────────────────────────────────────
echo ""
echo -e "  Installing to: ${BOLD}${CLAUDE_DIR}${RESET}"
echo ""

mkdir -p "${CLAUDE_DIR}/commands"
mkdir -p "${CLAUDE_DIR}/skills/deva"

# Commands — copy deva-commands/* → .claude/commands/
if [ -d "${EXTRACTED}/deva-commands" ]; then
  cp -r "${EXTRACTED}/deva-commands/." "${CLAUDE_DIR}/commands/"
  count=$(find "${EXTRACTED}/deva-commands" -type f | wc -l | tr -d ' ')
  echo -e "  ${GREEN}✓ commands/ (${count} files)${RESET}"
fi

# Skills — copy skills/* → .claude/skills/deva/
if [ -d "${EXTRACTED}/skills" ]; then
  cp -r "${EXTRACTED}/skills/." "${CLAUDE_DIR}/skills/deva/"
  count=$(find "${EXTRACTED}/skills" -type f | wc -l | tr -d ' ')
  echo -e "  ${GREEN}✓ skills/deva/ (${count} files)${RESET}"
fi

# Registry
if [ -f "${EXTRACTED}/registry.md" ]; then
  cp "${EXTRACTED}/registry.md" "${CLAUDE_DIR}/registry.md"
  echo -e "  ${GREEN}✓ registry.md${RESET}"
fi

# Root files — CLAUDE.md and templates
for file in CLAUDE.md PROJECT-base-template.md PROJECT-web-template.md PROJECT-macos-template.md; do
  if [ -f "${EXTRACTED}/${file}" ]; then
    cp "${EXTRACTED}/${file}" "${ROOT_DIR}/${file}"
    echo -e "  ${GREEN}✓ ${file}${RESET}"
  fi
done

# Write last-update-check timestamp
mkdir -p "${CLAUDE_DIR}/skills/deva"
date -u +"%Y-%m-%dT%H:%M:%SZ" > "${CLAUDE_DIR}/skills/deva/last-update-check.txt"

# ─── Cleanup ───────────────────────────────────────────────────────────────
rm -rf "$TMP_DIR"

# ─── Done ──────────────────────────────────────────────────────────────────
echo ""
echo -e "  ${GREEN}${BOLD}✅ DevAgent installed successfully!${RESET}"
echo ""

if [ "$SCOPE" = "global" ]; then
  echo -e "  ${BOLD}Get started:${RESET}"
  echo "    Open any project in Claude Code and type /deva:new or /deva:onboard"
else
  echo -e "  ${BOLD}Get started:${RESET}"
  echo "    Open this project in Claude Code and type /deva:new or /deva:onboard"
fi

echo ""
echo -e "  📖 Docs: ${BLUE}${REPO}${RESET}"
echo ""
