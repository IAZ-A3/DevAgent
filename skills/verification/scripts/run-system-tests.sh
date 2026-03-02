#!/usr/bin/env bash
# run-system-tests.sh
# Executes system tests using the test runner defined in TechnologyStack.md.
# Usage: bash run-system-tests.sh [test-dir] [tech-stack-path]

set -e

TEST_DIR="${1:-.vv-workspace/system-tests}"
TECH_STACK="${2:-docs/design/TechnologyStack.md}"
RESULTS_DIR=".claude/skills/state/vv"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$RESULTS_DIR"
mkdir -p "$TEST_DIR"

echo "=== V&V System Test Runner ==="
echo "Test dir:   $TEST_DIR"
echo "Timestamp:  $TIMESTAMP"
echo ""

# --- Detect test runner from TechnologyStack.md ---
TEST_RUNNER=""
if [ -f "$TECH_STACK" ]; then
    if grep -qi "pytest" "$TECH_STACK"; then
        TEST_RUNNER="pytest"
    elif grep -qi "jest" "$TECH_STACK"; then
        TEST_RUNNER="jest"
    elif grep -qi "go test" "$TECH_STACK"; then
        TEST_RUNNER="go test"
    elif grep -qi "cargo test" "$TECH_STACK"; then
        TEST_RUNNER="cargo test"
    elif grep -qi "npm test" "$TECH_STACK"; then
        TEST_RUNNER="npm test"
    elif grep -qi "mocha" "$TECH_STACK"; then
        TEST_RUNNER="mocha"
    fi
fi

if [ -z "$TEST_RUNNER" ]; then
    echo "[ERROR] No test runner found in $TECH_STACK"
    echo "Please specify the test runner in TechnologyStack.md under the 'Testing' row."
    exit 1
fi

echo "Test runner: $TEST_RUNNER"

# --- Verify test runner is available ---
if ! command -v "$(echo $TEST_RUNNER | awk '{print $1}')" &> /dev/null; then
    echo "[ERROR] Test runner '$TEST_RUNNER' is not installed or not in PATH."
    echo "Please install it and retry."
    exit 1
fi

# --- Run tests ---
RESULTS_FILE="$RESULTS_DIR/system-test-run-$TIMESTAMP.txt"
EXIT_CODE=0

echo "Running: $TEST_RUNNER $TEST_DIR"
echo "Output:  $RESULTS_FILE"
echo ""

$TEST_RUNNER "$TEST_DIR" 2>&1 | tee "$RESULTS_FILE" || EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "[RESULT] ALL TESTS PASSED"
else
    echo "[RESULT] SOME TESTS FAILED (exit code: $EXIT_CODE)"
fi

echo "Full output saved to: $RESULTS_FILE"
exit $EXIT_CODE
