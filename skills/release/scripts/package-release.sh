#!/usr/bin/env bash
# package-release.sh
# Creates a release package based on project type inferred from TechnologyStack.md.
# Usage: bash package-release.sh <version> [tech-stack-path] [project-name]

set -e

VERSION="${1:-0.1.0}"
TECH_STACK="${2:-docs/design/TechnologyStack.md}"
PROJECT_NAME="${3:-project}"
DIST_DIR="dist"
DATE=$(date +%Y%m%d)
PACKAGE_BASE="${PROJECT_NAME}-v${VERSION}-${DATE}"

mkdir -p "$DIST_DIR"

echo "=== Release Packager ==="
echo "Version:  $VERSION"
echo "Output:   $DIST_DIR/"
echo ""

# --- Detect project type ---
PROJECT_TYPE="generic"
if [ -f "$TECH_STACK" ]; then
    if grep -qi "swift\|xcode" "$TECH_STACK"; then
        PROJECT_TYPE="macos"
    elif grep -qi "pyproject\|setup.py\|pip" "$TECH_STACK"; then
        PROJECT_TYPE="python"
    elif grep -qi "package.json\|node\|npm" "$TECH_STACK"; then
        PROJECT_TYPE="nodejs"
    elif grep -qi "cargo\|rust" "$TECH_STACK"; then
        PROJECT_TYPE="rust"
    elif grep -qi "go.mod\|golang" "$TECH_STACK"; then
        PROJECT_TYPE="go"
    elif grep -qi "docker" "$TECH_STACK"; then
        PROJECT_TYPE="docker"
    fi
fi

echo "Detected project type: $PROJECT_TYPE"
echo ""

# --- Update VERSION file ---
echo "$VERSION" > VERSION
echo "[OK] VERSION file updated to $VERSION"

# --- Package based on type ---
case "$PROJECT_TYPE" in

    python)
        echo "Building Python package..."
        if command -v python3 &>/dev/null && [ -f "pyproject.toml" -o -f "setup.py" ]; then
            python3 -m build --outdir "$DIST_DIR" 2>&1
            echo "[OK] Python package built in $DIST_DIR/"
        else
            echo "[WARN] python3 build tools not available — creating source archive instead"
            tar -czf "$DIST_DIR/${PACKAGE_BASE}.tar.gz" \
                --exclude=".git" --exclude="__pycache__" --exclude=".venv" \
                --exclude="*.pyc" --exclude=".pytest_cache" \
                .
            echo "[OK] Source archive: $DIST_DIR/${PACKAGE_BASE}.tar.gz"
        fi
        ;;

    nodejs)
        echo "Building Node.js package..."
        if command -v npm &>/dev/null && [ -f "package.json" ]; then
            # Update version in package.json
            node -e "
                const fs = require('fs');
                const pkg = JSON.parse(fs.readFileSync('package.json'));
                pkg.version = '${VERSION}';
                fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
            "
            npm pack --pack-destination "$DIST_DIR" 2>&1
            echo "[OK] npm package built in $DIST_DIR/"
        else
            echo "[WARN] npm not available — creating archive instead"
            tar -czf "$DIST_DIR/${PACKAGE_BASE}.tar.gz" \
                --exclude=".git" --exclude="node_modules" \
                .
        fi
        ;;

    rust)
        echo "Building Rust release binary..."
        if command -v cargo &>/dev/null; then
            cargo build --release 2>&1
            cp target/release/"$PROJECT_NAME" "$DIST_DIR/${PACKAGE_BASE}" 2>/dev/null || \
            cp target/release/"$PROJECT_NAME".exe "$DIST_DIR/${PACKAGE_BASE}.exe" 2>/dev/null || \
            echo "[WARN] Binary name may differ — check target/release/"
            echo "[OK] Rust binary in $DIST_DIR/"
        else
            echo "[ERROR] cargo not available"
            exit 1
        fi
        ;;

    go)
        echo "Building Go release binary..."
        if command -v go &>/dev/null; then
            go build -o "$DIST_DIR/${PACKAGE_BASE}" ./... 2>&1
            echo "[OK] Go binary in $DIST_DIR/"
        else
            echo "[ERROR] go not available"
            exit 1
        fi
        ;;

    macos)
        echo "macOS app packaging requires Xcode — providing instructions."
        cat > "$DIST_DIR/BUILD-INSTRUCTIONS.txt" << EOF
macOS Release Build Instructions — v${VERSION}
================================================
1. Open project in Xcode
2. Set version to ${VERSION} in project settings
3. Product → Archive
4. Distribute App → select distribution method
5. Place exported .app or .pkg in dist/ folder
EOF
        echo "[OK] Build instructions written to $DIST_DIR/BUILD-INSTRUCTIONS.txt"
        ;;

    docker)
        echo "Docker packaging — creating image tag instructions."
        cat > "$DIST_DIR/DOCKER-RELEASE.txt" << EOF
Docker Release Instructions — v${VERSION}
==========================================
docker build -t ${PROJECT_NAME}:${VERSION} .
docker tag ${PROJECT_NAME}:${VERSION} ${PROJECT_NAME}:latest
# Push to registry:
docker push ${PROJECT_NAME}:${VERSION}
docker push ${PROJECT_NAME}:latest
EOF
        echo "[OK] Docker instructions written to $DIST_DIR/DOCKER-RELEASE.txt"
        ;;

    *)
        echo "Creating generic zip archive..."
        zip -r "$DIST_DIR/${PACKAGE_BASE}.zip" . \
            -x "*.git*" -x "node_modules/*" -x "__pycache__/*" \
            -x ".venv/*" -x "dist/*" -x "*.pyc" \
            -x ".claude/skills/state/*" 2>&1
        echo "[OK] Archive: $DIST_DIR/${PACKAGE_BASE}.zip"
        ;;
esac

echo ""
echo "=== Package Summary ==="
ls -lh "$DIST_DIR/"
echo ""
echo "Version file updated: VERSION = $VERSION"
echo "Release packaging complete."
