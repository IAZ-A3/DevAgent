# DevAgent Sub-skill: Project Detector
**Parent:** Onboarding — Sub-phase A
**Output:** `.claude/skills/state/onboarding/detection-report.md`

---

## Purpose

Detect the project's language, framework, architecture style, and exact source
code locations without assuming any particular folder structure. Drives all
subsequent sub-phases by telling them where to look.

---

## Detection Procedure

Work through all detection layers in order. Stop at the first definitive match
per category. Combine signals across layers for confidence scoring.

---

### Layer 1 — Build System & Package Manifests (highest confidence)

| File Found | Language | Ecosystem |
|-----------|---------|-----------|
| `Package.swift` | Swift | Swift Package Manager |
| `*.xcodeproj` or `*.xcworkspace` | Swift/ObjC | Xcode project |
| `package.json` | JavaScript/TypeScript | Node.js |
| `pyproject.toml` or `setup.py` or `setup.cfg` | Python | Python package |
| `Cargo.toml` | Rust | Cargo |
| `go.mod` | Go | Go modules |
| `pom.xml` or `build.gradle` | Java/Kotlin | JVM |
| `*.csproj` or `*.sln` | C# | .NET |
| `Gemfile` | Ruby | Bundler |
| `composer.json` | PHP | Composer |
| `pubspec.yaml` | Dart | Flutter/Dart |

**For each manifest found:** read its contents to extract:
- Project name
- Dependencies → framework signals (see Layer 2)
- Target platform declarations
- Build targets / entry points

---

### Layer 2 — Framework Detection (from manifests + config files)

**Web frameworks:**
| Signal File/Dependency | Framework |
|-----------------------|-----------|
| `next.config.js` / `next.config.ts` | Next.js |
| `nuxt.config.*` | Nuxt.js |
| `vite.config.*` + React dep | React + Vite |
| `vite.config.*` + Vue dep | Vue + Vite |
| `svelte.config.*` | SvelteKit |
| `angular.json` | Angular |
| `remix.config.*` | Remix |
| `astro.config.*` | Astro |

**Mobile/Desktop:**
| Signal | Framework |
|--------|-----------|
| `Package.swift` + SwiftUI import | SwiftUI macOS/iOS |
| `*.xcodeproj` + `Info.plist` | Native Apple app |
| `LSUIElement` in `Info.plist` | macOS menu bar app |
| `pubspec.yaml` + flutter dep | Flutter |

**Backend:**
| Signal | Framework |
|--------|-----------|
| `package.json` + express/fastify dep | Node.js API |
| `pyproject.toml` + fastapi/django/flask dep | Python API |
| `Cargo.toml` + axum/actix dep | Rust API |
| `go.mod` + gin/echo dep | Go API |

---

### Layer 3 — Source Location Mapping

After identifying language and framework, map to source locations:

| Language/Framework | Source locations to scan |
|-------------------|------------------------|
| Swift (Xcode) | `{AppName}/`, `{AppName}Tests/`, `{AppName}UITests/` — find by `*.xcodeproj` target names |
| Swift (SPM) | `Sources/`, `Tests/` |
| Next.js | `app/`, `pages/`, `components/`, `lib/`, `utils/`, `hooks/` |
| Nuxt.js | `pages/`, `components/`, `composables/`, `server/` |
| React/Vite | `src/` (common), `components/`, `pages/` |
| Vue/Vite | `src/` (common), `components/`, `views/` |
| Python | `{package-name}/` (matches name in pyproject.toml), root `.py` files |
| Rust | `src/` (always — cargo standard) |
| Go | root `.go` files, `cmd/`, `internal/`, `pkg/` |
| Node.js API | `src/`, `routes/`, `controllers/`, `middleware/`, `services/` |

**Fallback if none of the above match:**
```bash
# Find all source files by extension, exclude node_modules, .git, dist, build
find . -type f \( -name "*.swift" -o -name "*.py" -o -name "*.ts" -o -name "*.js" \
  -o -name "*.rs" -o -name "*.go" -o -name "*.kt" -o -name "*.dart" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.build/*" \
  -not -path "*/DerivedData/*" | head -50
```
Group results by directory → those directories are the source locations.

---

### Layer 4 — Architecture Signal Detection

Scan source locations for architectural patterns:

| Pattern | Signal |
|---------|--------|
| MVVM | `*ViewModel.swift`, `*ViewModel.ts`, `viewModel` references |
| MVC | `*Controller.*`, `*Model.*`, `*View.*` triad |
| Clean/Hexagonal | `domain/`, `infrastructure/`, `application/`, `ports/`, `adapters/` |
| Redux/Flux | `store/`, `reducers/`, `actions/`, `slices/` |
| Feature-based | Top-level folders named after features (not layers) |
| Flat | Most files at same depth, no clear separation |

---

### Layer 5 — Test Location Detection

| Language/Framework | Common test locations |
|-------------------|--------------------|
| Swift (Xcode) | `{AppName}Tests/`, `{AppName}UITests/` |
| Swift (SPM) | `Tests/` |
| JavaScript/TypeScript | `__tests__/`, `*.test.ts`, `*.spec.ts`, `cypress/`, `e2e/` |
| Python | `tests/`, `test_*.py` |
| Rust | inline `#[cfg(test)]` + `tests/` |
| Go | `*_test.go` files alongside source |

**Test coverage estimation:**
```bash
# Count test files vs source files (rough ratio)
find {test_locations} -type f -name "*.{ext}" | wc -l
find {source_locations} -type f -name "*.{ext}" | wc -l
```

---

## Output Format

Write to `.claude/skills/state/onboarding/detection-report.md`:

```markdown
# Detection Report
## Timestamp: {date}

## Language: {language}
## Framework: {framework or "None detected"}
## Ecosystem: {e.g. Xcode, SPM, Node.js, Python/pip}
## Project type: {e.g. macOS menu bar app, Next.js web app, Python CLI}
## Profile to activate: web-profile | macos-profile | none

## Source Locations:
- {path} — {what it contains}
- {path} — {what it contains}

## Test Locations:
- {path} — {framework, e.g. XCTest, Jest, pytest}
- (or "No tests found")

## Test coverage estimate: {ratio or "Unknown"}

## Architecture pattern: {detected pattern} — confidence: HIGH | MEDIUM | LOW

## Config files found:
- {file} — {what it declares}

## Build targets (if applicable):
- {target name} — {platform}

## Git repo: YES | NO
## Uncommitted changes: YES | NO | N/A

## Confidence: HIGH | MEDIUM | LOW
## Notes: {anything unusual or ambiguous}
```
