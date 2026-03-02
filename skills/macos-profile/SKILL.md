# macOS Profile
# Profile type: Extension — loads on top of base skills when project type is macOS app
# CLAUDE.md Section 4 activates this profile and runs check-macos-dependencies.py before any phase work.
# Extension mode: adds to base 7-phase skills — does not replace them.
# Triggered by: CLAUDE.md detecting "macos", "mac app", "swift", "swiftui" in PROJECT.md or prompt
# Scope: SwiftUI macOS apps targeting Apple Silicon (M-series), distributed via DMG/direct download

---

## Purpose

Extend the base 7-phase engineering agent with macOS-specific skills, design documents,
Xcode build integration, XCTest automation, and direct download distribution support
(code signing, notarization, stapling, DMG packaging). SwiftUI only. M-silicon target.

---

## 1. Profile Activation

CLAUDE.md activates this profile when any of the following are true:
- `PROJECT.md` → Type field contains: "macos", "mac app", "menubar app", "swift", "swiftui"
- User prompt contains: "macOS app", "Mac app", "SwiftUI", "menubar", "notch", "Swift"
- `TechnologyStack.md` references Swift or SwiftUI

On activation:
1. Run dependency check (Section 2)
2. Load subtype detection (Section 3)
3. Apply phase extensions

---

## 2. Dependency Check Protocol

### Required MCP Servers

| MCP Server | Config Key | Install Command | Description |
|-----------|-----------|-----------------|-------------|
| `xcodebuild` | `xcodebuild` | `npx xcode-build-mcp@latest` | Xcode build, test, archive, export |

**Check procedure:**
```
1. Check .mcp.json for `xcodebuild` config key
2. If found → OK
3. If missing → look up in .claude/registry.md
4. Present to user:
   "Required MCP server 'xcodebuild' is not configured.
    Install command: npx xcode-build-mcp@latest
    Add to .mcp.json? I will show you the exact config snippet."
5. If yes → show JSON snippet, ask user to add it, then verify
6. If no → warn that build/test/archive automation will be unavailable
            Claude Code will provide manual Xcode instructions instead
```

**Never install or modify config files automatically.**

### Required Tools (verified via shell, not MCP)

| Tool | Check Command | Required For |
|------|-------------|-------------|
| Xcode | `xcodebuild -version` | Build, test, archive |
| Xcode Command Line Tools | `xcode-select -p` | Build tools |
| `create-dmg` | `which create-dmg` | DMG packaging |
| `xcrun notarytool` | `xcrun notarytool --version` | Notarization |
| `xcrun stapler` | `xcrun stapler --version` | Stapling |

**Check procedure:**
```
For each required tool:
  1. Run its check command via shell
  2. If found → OK
  3. If missing → look up install instruction in .claude/registry.md
  4. Present to user:
     "Required tool '{name}' is not installed.
      Install: {install command}
      Please install it before proceeding."
  5. Do not proceed with steps that depend on the missing tool
```

**Never install tools automatically. Always inform and ask first.**

> Tip: run `python3 .claude/skills/macos-profile/scripts/check-macos-dependencies.py all`
> to check all tools and MCP servers in one pass.

---

## 3. macOS App Subtype Detection

| Subtype | Indicators | Notes |
|---------|-----------|-------|
| Standard app | Regular window-based app | Most common |
| Menu bar app | `LSUIElement = YES` in Info.plist, no Dock icon | e.g. NotchPlus |
| Menu bar + window | Both menu bar and regular windows | Hybrid |
| Document-based | `NSDocument` subclass | File-centric apps |

Ask user if not determinable from PROJECT.md:
```
What type of macOS app is this?
A) Standard window app (appears in Dock)
B) Menu bar app only (no Dock icon)
C) Menu bar + window (both)
D) Document-based app
```

---

## 4. Phase Extensions

---

### Phase 1 Extension: Requirements

**Additional NFRs to always include for macOS apps:**

| NFR | Default Acceptance Criterion |
|-----|---------------------------|
| macOS version compatibility | macOS 13 Ventura minimum (M-silicon target) |
| Performance | App launch < 2s cold start on M1 |
| Memory | Idle memory footprint < 100MB (adjust per app type) |
| Accessibility | VoiceOver compatible, all controls labeled |
| Privacy | All sensitive API usage declared in PrivacyInfo.xcprivacy |
| Security | Hardened Runtime enabled, no deprecated API usage |
| Sandboxing | Entitlements declared for all accessed resources |
| Notarization | App passes Apple notarization scan |

**Additional questions for Requirements clarification protocol:**
- Which macOS APIs does the app use? (camera, microphone, location, contacts, calendar, files outside sandbox, network)
- Does the app run at login? (affects entitlements and sandboxing)
- Does the app require internet access?
- Any third-party Swift packages (SPM dependencies)?
- Target minimum macOS version? (default: macOS 13)

---

### Phase 2 Extension: Planning

**Additional task types for macOS projects:**

| Task Type | Example | Complexity |
|-----------|---------|-----------|
| SwiftUI view | Implement SettingsView with form controls | M |
| Menu bar setup | Configure NSStatusItem and popover | M |
| AppDelegate/lifecycle | Configure app lifecycle and launch behavior | S |
| SPM dependency | Add and integrate {package} via Swift Package Manager | S |
| Entitlements | Configure entitlements for {capability} | S |
| Privacy manifest | Declare API usage in PrivacyInfo.xcprivacy | S |
| XCTest unit | Write XCTest for {component} | M |
| XCUITest flow | Write UI test for {user flow} | M |
| Archive + export | Xcode archive and export signed app | M |
| Notarization | Submit to Apple, wait, staple | L |
| DMG packaging | Create distributable DMG with create-dmg | M |

---

### Phase 3 Extension: Design & Architecture

**Additional design documents for macOS apps:**

| Document | Required For | Contents |
|----------|-------------|----------|
| `SwiftUIDesign.md` | All | View hierarchy, component library, design tokens (colors, fonts, spacing), SF Symbols usage |
| `AppArchitecture.md` | All | App lifecycle, scene management, ObservableObject/StateObject graph, data flow |
| `EntitlementsDesign.md` | All | Required entitlements, sandbox strategy, justification per entitlement |
| `PrivacyManifest.md` | All | APIs requiring privacy declaration, usage descriptions, data collection policy |
| `MenuBarDesign.md` | Menu bar apps | Status item configuration, popover vs window, menu structure |
| `SPMDependencies.md` | If SPM used | Package list, versions, justification per package |

**SwiftUIDesign.md must be generated first** — all other view-related documents reference its component names and design tokens.

**Design tokens for SwiftUI (always define these):**
- Color palette using `Color` assets (light + dark mode variants)
- Typography: SF Pro sizes mapped to semantic roles (title, body, caption)
- Spacing scale: 4pt base grid
- Corner radius values
- SF Symbols used (with accessibility labels)

---

### Phase 4 Extension: Implementation

**Swift/SwiftUI coding rules (enforced by Code Generator and Code Reviewer):**

| Rule | Detail |
|------|--------|
| Architecture | MVVM — Views are dumb, logic in ViewModels |
| State management | `@StateObject` for owned models, `@ObservedObject` for injected, `@AppStorage` for persisted preferences |
| Concurrency | Swift Concurrency (`async/await`, `Task`, `@MainActor`) — no GCD/DispatchQueue unless unavoidable |
| Error handling | Never use `try!` or `force unwrap (!)` in production code |
| Memory | No retain cycles — use `[weak self]` in closures capturing self |
| Accessibility | Every interactive SwiftUI element must have `.accessibilityLabel()` |
| Dark mode | All colors from asset catalog with dark mode variants — never hardcoded |
| Privacy | No API access without corresponding entry in PrivacyInfo.xcprivacy |
| Entitlements | No capability used in code without matching entitlement declaration |

**Additional sub-skill: SwiftUI Component Builder**
- Invoked by Implementation orchestrator for view tasks
- Follows SwiftUIDesign.md component specs
- Generates: View file, ViewModel file (if needed), Preview, XCTest
- Every view must: support dark mode, support VoiceOver, use design tokens from SwiftUIDesign.md

**Additional sub-skill: Entitlements & Privacy Configurator**
- Run once after all features are implemented
- Reads EntitlementsDesign.md and PrivacyManifest.md
- Verifies: every API used in code has a matching entitlement + privacy declaration
- Generates or updates: `{AppName}.entitlements`, `PrivacyInfo.xcprivacy`
- Reports any gaps — missing entitlement = FAIL, must fix before V&V

---

### Phase 5 Extension: Verification & Validation

**Build verification via XcodeBuildMCP:**

| Step | Command | Pass Criteria |
|------|---------|--------------|
| Clean build | `xcodebuild clean build` | Exit 0, no errors |
| Unit tests | `xcodebuild test -scheme {scheme}` | All XCTests pass |
| UI tests | `xcodebuild test -scheme {scheme} -testPlan UITests` | All XCUITests pass |
| Archive (dry run) | `xcodebuild archive` | Archive succeeds |

**Additional NFR checks for macOS:**

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| Memory footprint | Instruments (manual) or `leaks` tool | < NFR threshold |
| Launch time | `xcodebuild` + timing | < 2s cold start |
| Entitlements completeness | Parse .entitlements file vs API usage | No gaps |
| Privacy manifest completeness | Parse PrivacyInfo.xcprivacy vs API usage | No gaps |
| Dark mode | XCUITest screenshot comparison | No hardcoded colors visible |
| VoiceOver | Manual checklist | All controls labeled |

**NFR-Checklist.md additions for macOS:**
```markdown
## macOS-Specific NFR Checklist
- [ ] Clean build with 0 errors, 0 warnings
- [ ] All XCUnit tests pass
- [ ] All XCUITests pass
- [ ] Archive succeeds
- [ ] Launch time < 2s (measured)
- [ ] Memory footprint within NFR threshold (measured)
- [ ] Dark mode: no hardcoded colors
- [ ] VoiceOver: all interactive elements labeled
- [ ] Entitlements: all capabilities declared
- [ ] PrivacyInfo.xcprivacy: all API usages declared
- [ ] No force unwraps (!) in production code
- [ ] No deprecated API warnings
```

---

### Phase 6 Extension: Release

**macOS direct download release pipeline:**

```
Step 1: Archive                    → .xcarchive
Step 2: Export signed app          → .app (Developer ID signed)
Step 3: Verify signing             → codesign --verify
Step 4: Notarize                   → xcrun notarytool submit
Step 5: Wait for notarization      → poll status (can take 1-15 min)
Step 6: Staple                     → xcrun stapler staple
Step 7: Verify staple              → xcrun stapler validate
Step 8: Create DMG                 → create-dmg
Step 9: Sign DMG                   → codesign DMG
Step 10: Final verification        → spctl --assess
```

Each step is gated — failure stops the pipeline and reports to user.

**Invoke sub-skill: macOS Release Builder** (see `sub-skills/macos-release-builder.md`)

**Additional release artifact:** `docs/release/ReleaseChecklist.md`
```markdown
# macOS Release Checklist — v{version}
- [ ] Archive: PASS
- [ ] Export (Developer ID signed): PASS
- [ ] codesign --verify: PASS
- [ ] Notarization submitted: {submission UUID}
- [ ] Notarization status: Accepted
- [ ] Staple: PASS
- [ ] stapler validate: PASS
- [ ] DMG created: {filename}
- [ ] DMG signed: PASS
- [ ] spctl --assess: PASS
- [ ] Distribution URL updated: {url or "manual upload"}
```

---

### Phase 7 Extension: Maintenance

**Additional bug categories for macOS apps:**

| Category | Investigation Start |
|----------|-------------------|
| Crash on launch | Crash log + AppDelegate + scene lifecycle |
| Memory leak | Instruments → Leaks, check retain cycles |
| UI not updating | ViewModel binding, @Published, @MainActor |
| Entitlement denied | Console.app sandbox violation logs |
| Notarization rejection | Notarization log from Apple |
| Dark mode regression | Asset catalog + hardcoded color search |
| VoiceOver broken | Accessibility Inspector |
| Gatekeeper block | Signing/stapling verification |

**After bug fix:** run targeted XCTest covering the affected component, plus full clean build.

---

## 5. Apple Developer Account Requirements

Inform user at profile activation if not already noted in PROJECT.md:

Direct download distribution requires:
- Apple Developer Program membership ($99/year)
- Developer ID Application certificate (for app signing)
- Developer ID Installer certificate (for PKG, if used)
- App-specific password or API key for `notarytool`

If user does not have these: flag early in Requirements phase, not at Release phase.