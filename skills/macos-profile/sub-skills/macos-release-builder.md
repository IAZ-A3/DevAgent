# DevAgent Sub-skill: macOS Release Builder
**Parent:** macOS Profile — Phase 6 Extension  
**Scope:** Archive → Sign → Notarize → Staple → DMG  
**Output:** Signed, notarized, stapled DMG ready for distribution

---

## Purpose

Execute the complete macOS direct download release pipeline using XcodeBuildMCP
and Xcode command line tools. Each step is verified before proceeding to the next.
Never skips signing, notarization, or stapling — these are mandatory for direct download.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| Xcode project/workspace | project root | Yes |
| Scheme name | TechnologyStack.md or user | Yes |
| Bundle ID | TechnologyStack.md or Info.plist | Yes |
| Version string | Orchestrator (from VERSION file) | Yes |
| Developer ID certificate name | User (from Keychain) | Yes |
| Apple ID or API key | User (for notarytool) | Yes |
| Team ID | User (Apple Developer account) | Yes |
| XcodeBuildMCP | .mcp.json `xcodebuild` key | Yes |

**Collect missing inputs before starting. Ask user in one grouped question.**

---

## 1. Pre-flight Verification

```bash
# Verify signing identity is available
security find-identity -v -p codesigning | grep "Developer ID Application"

# Verify Xcode version
xcodebuild -version

# Verify create-dmg is available
which create-dmg || echo "MISSING: install with 'brew install create-dmg'"

# Verify notarytool is available
xcrun notarytool --version
```

If Developer ID certificate is not found: halt and instruct user to install it from
Apple Developer portal into Keychain before proceeding.

---

## 2. Step 1 — Archive

Via XcodeBuildMCP:
```bash
xcodebuild archive \
  -scheme {scheme} \
  -configuration Release \
  -archivePath build/{AppName}-v{version}.xcarchive \
  -destination "generic/platform=macOS" \
  CODE_SIGN_IDENTITY="Developer ID Application: {team}" \
  DEVELOPMENT_TEAM={team-id}
```

**Pass criteria:** Exit 0, `.xcarchive` file exists.  
**On failure:** Show full build log. Common causes: missing entitlements, provisioning, code errors.

---

## 3. Step 2 — Export Signed App

Create `ExportOptions.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>developer-id</string>
    <key>teamID</key>
    <string>{team-id}</string>
    <key>signingStyle</key>
    <string>manual</string>
    <key>signingCertificate</key>
    <string>Developer ID Application</string>
</dict>
</plist>
```

```bash
xcodebuild -exportArchive \
  -archivePath build/{AppName}-v{version}.xcarchive \
  -exportPath build/export/ \
  -exportOptionsPlist ExportOptions.plist
```

**Pass criteria:** `build/export/{AppName}.app` exists.

---

## 4. Step 3 — Verify Code Signing

```bash
codesign --verify --deep --strict --verbose=2 build/export/{AppName}.app
codesign -dv --verbose=4 build/export/{AppName}.app 2>&1 | grep "Authority\|TeamIdentifier\|Hardened"
```

**Pass criteria:** No errors. Output shows Developer ID certificate. Hardened Runtime enabled.  
**On failure:** Common cause — missing entitlement or unsigned framework inside app bundle.

---

## 5. Step 4 — Notarize

```bash
# Create zip for submission (notarytool accepts zip or dmg)
ditto -c -k --keepParent build/export/{AppName}.app build/{AppName}-v{version}-notarize.zip

# Submit to Apple Notary Service
xcrun notarytool submit build/{AppName}-v{version}-notarize.zip \
  --apple-id {apple-id} \
  --password {app-specific-password} \
  --team-id {team-id} \
  --wait \
  --output-format json
```

`--wait` polls until complete (typically 1-10 minutes). Capture submission ID from output.

**Pass criteria:** `status: Accepted` in JSON response.  
**On failure:** Fetch full log:
```bash
xcrun notarytool log {submission-id} \
  --apple-id {apple-id} \
  --password {app-specific-password} \
  --team-id {team-id}
```
Show log to user. Common causes: unsigned binary inside bundle, missing privacy manifest,
hardened runtime not enabled, entitlement not declared.

---

## 6. Step 5 — Staple

```bash
xcrun stapler staple build/export/{AppName}.app
xcrun stapler validate build/export/{AppName}.app
```

**Pass criteria:** `stapler validate` exits 0 with "The validate action worked!".

---

## 7. Step 6 — Create DMG

```bash
create-dmg \
  --volname "{AppName} {version}" \
  --volicon "assets/{AppName}.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "{AppName}.app" 175 190 \
  --hide-extension "{AppName}.app" \
  --app-drop-link 425 190 \
  "dist/{AppName}-v{version}.dmg" \
  "build/export/"
```

If `assets/{AppName}.icns` does not exist: create DMG without custom icon, warn user.

**Pass criteria:** `dist/{AppName}-v{version}.dmg` exists and is non-zero size.

---

## 8. Step 7 — Sign DMG

```bash
codesign --sign "Developer ID Application: {team}" \
  --verbose \
  "dist/{AppName}-v{version}.dmg"
```

**Pass criteria:** Exit 0.

---

## 9. Step 8 — Final Gatekeeper Verification

```bash
spctl --assess --type open --context context:primary-signature \
  --verbose "dist/{AppName}-v{version}.dmg"

spctl --assess --verbose "dist/{AppName}-v{version}.dmg"
```

**Pass criteria:** Output contains "accepted" or "source=Notarized Developer ID".  
**This is the final gate.** If this fails, the DMG will be blocked by Gatekeeper on user machines.

---

## 10. Output

Write `docs/release/ReleaseChecklist.md` with actual results for each step.

Report to user:
```
✓ macOS Release Build Complete — v{version}

  Archive:        PASS
  Export:         PASS
  Code signing:   PASS (Developer ID: {name})
  Notarization:   PASS (submission: {uuid})
  Staple:         PASS
  DMG:            dist/{AppName}-v{version}.dmg ({size}MB)
  DMG signing:    PASS
  Gatekeeper:     PASS (Notarized Developer ID)

Ready for distribution. Upload dist/{AppName}-v{version}.dmg to your download host.
```

Write artifact entry to `.claude/skills/state/artifact-registry.md`.
