#!/usr/bin/env bash
# discover-inputs.sh
# Auto-discovers input sources for the Requirements skill.
# Usage: bash discover-inputs.sh [project-root]
# Output: prints discovered sources to stdout, exits 0 if found, 1 if nothing found.

PROJECT_ROOT="${1:-.}"
FOUND=0

echo "=== Requirements Skill — Input Discovery ==="
echo "Scanning: $PROJECT_ROOT"
echo ""

check_file() {
  local file="$1"
  local label="$2"
  if [ -f "$PROJECT_ROOT/$file" ]; then
    echo "[FOUND] $label → $PROJECT_ROOT/$file"
    FOUND=1
  fi
}

check_dir() {
  local dir="$1"
  local label="$2"
  if [ -d "$PROJECT_ROOT/$dir" ]; then
    echo "[FOUND] $label → $PROJECT_ROOT/$dir"
    FOUND=1
  fi
}

# Check for existing PRD/requirements docs
check_file "docs/PRD.md"           "Existing PRD"
check_file "docs/requirements.md"  "Requirements doc"
check_file "docs/REQUIREMENTS.md"  "Requirements doc (uppercase)"

# Check for project description files
check_file "README.md"   "README"
check_file "BRIEF.md"    "Project brief"
check_file "IDEA.md"     "Project idea"
check_file "NOTES.md"    "Project notes"
check_file "brief.md"    "Project brief (lowercase)"

# Check for checkpoint (resume scenario)
check_file ".claude/skills/state/requirements/checkpoint.md" "Previous session checkpoint"

# Check for existing source code
check_dir "src"  "Source code directory"
check_dir "lib"  "Library directory"
check_dir "app"  "App directory"

echo ""
if [ $FOUND -eq 0 ]; then
  echo "[NONE FOUND] No input sources detected."
  echo "Action required: provide a project description in the prompt."
  exit 1
else
  echo "Discovery complete. Inputs ready for Requirements skill."
  exit 0
fi
