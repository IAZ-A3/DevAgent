# DevAgent Sub-skill: Entitlements & Privacy Configurator
**Parent:** macOS Profile — Phase 4 Extension  
**Scope:** Run once after all features are implemented  
**Output:** {AppName}.entitlements, PrivacyInfo.xcprivacy, gap report

---

## Purpose

After implementation is complete, audit the entire codebase for API usage that requires
entitlements or privacy manifest declarations. Generate or update the entitlements file
and PrivacyInfo.xcprivacy. Any gap between what the code uses and what is declared
is a FAIL — Apple will reject the app at notarization if gaps exist.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| EntitlementsDesign.md | docs/design/EntitlementsDesign.md | Yes |
| PrivacyManifest.md | docs/design/PrivacyManifest.md | Yes |
| All source files | src/ | Yes |
| Bundle ID | TechnologyStack.md or Info.plist | Yes |
| App subtype | macOS profile detection | Yes |

---

## 1. Entitlements Audit

Scan all Swift source files for these API patterns and map to required entitlements:

| API / Framework Used in Code | Required Entitlement |
|------------------------------|---------------------|
| `NSOpenPanel`, `NSSavePanel` (outside sandbox) | `com.apple.security.files.user-selected.read-write` |
| `FileManager` accessing paths outside container | `com.apple.security.files.downloads.read-write` or broader |
| `URLSession` / network requests | `com.apple.security.network.client` |
| Incoming network connections | `com.apple.security.network.server` |
| `AVCaptureDevice` (camera) | `com.apple.security.device.camera` |
| `AVAudioEngine`, microphone | `com.apple.security.device.audio-input` |
| `CoreLocation` | `com.apple.security.personal-information.location` |
| `Contacts` framework | `com.apple.security.personal-information.addressbook` |
| `EventKit` (calendar) | `com.apple.security.personal-information.calendars` |
| `Bluetooth` framework | Not sandboxed — check entitlements for BT |
| `SecKeychainItem` | `keychain-access-groups` |
| Login item / launch at login | `com.apple.security.application-groups` |
| JIT compilation | `com.apple.security.cs.allow-jit` |
| Hardened Runtime exceptions | `com.apple.security.cs.*` variants |

**Sandboxing:**
- Check if app runs sandboxed (`com.apple.security.app-sandbox = YES`)
- For direct download apps: sandboxing is recommended but not required by Apple
- If not sandboxed: note in EntitlementsDesign.md with justification

---

## 2. Privacy Manifest Audit

Apple requires `PrivacyInfo.xcprivacy` declarations for these APIs (as of 2024):

| API Category | Specific APIs | Required Declaration |
|-------------|--------------|---------------------|
| File timestamp | `NSFileCreationDate`, `NSFileModificationDate` | `NSPrivacyAccessedAPICategoryFileTimestamp` |
| System boot time | `systemUptime`, `mach_absolute_time()` | `NSPrivacyAccessedAPICategorySystemBootTime` |
| Disk space | `NSFileSystemFreeSize`, `volumeAvailableCapacity` | `NSPrivacyAccessedAPICategoryDiskSpace` |
| Active keyboard | `UITextInputMode` (less relevant for macOS) | `NSPrivacyAccessedAPICategoryActiveKeyboards` |
| User defaults | `UserDefaults` / `NSUserDefaults` | `NSPrivacyAccessedAPICategoryUserDefaults` |

**Data collection declarations required if app collects:**
- Name, email, phone, address → `NSPrivacyCollectedDataTypes`
- Usage data, diagnostics, crash data → declare with purpose

---

## 3. Gap Analysis

After audit:

```
For each API found in code:
  → Check if corresponding entitlement exists in EntitlementsDesign.md
  → Check if corresponding privacy declaration exists in PrivacyManifest.md
  → If missing → add to gap list (FAIL)

For each entitlement in EntitlementsDesign.md:
  → Check if corresponding API is actually used in code
  → If not used → flag as unnecessary (WARN — remove to minimize attack surface)
```

**Gap = FAIL.** No entitlement gaps or privacy manifest gaps allowed before proceeding to V&V.

---

## 4. File Generation

### {AppName}.entitlements
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>     <!-- or false with justification -->
    
    <!-- Add only entitlements actually required -->
    <key>com.apple.security.network.client</key>
    <true/>
    
    <!-- Hardened Runtime — required for notarization -->
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <false/>    <!-- only set true if absolutely needed -->
</dict>
</plist>
```

### PrivacyInfo.xcprivacy
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <!-- Add one dict per accessed API category -->
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>  <!-- read/write own defaults -->
            </array>
        </dict>
    </array>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <!-- Add if app collects user data, else leave empty -->
    </array>
    <key>NSPrivacyTracking</key>
    <false/>    <!-- true only if app does cross-app tracking -->
</dict>
</plist>
```

Place `PrivacyInfo.xcprivacy` in the app bundle root (same level as Info.plist).
Add to Xcode project as a resource file.

---

## 5. Output

Write gap report to `.claude/skills/state/implementation/entitlements-audit.md`:
```markdown
# Entitlements & Privacy Audit
## Date: {date}
## Result: PASS | FAIL

### Entitlements
| API Used | Entitlement | Status |
|----------|------------|--------|
| URLSession | network.client | ✓ declared |
| FileManager (Downloads) | files.downloads | ✗ MISSING |

### Privacy Manifest
| API Used | Declaration | Status |
|----------|------------|--------|
| UserDefaults | UserDefaults category | ✓ declared |

### Gaps (must fix before V&V)
{list of missing entitlements and privacy declarations, or "None"}

### Unnecessary Entitlements (recommended to remove)
{list, or "None"}

### Files Written
- {AppName}.entitlements
- {AppName}/PrivacyInfo.xcprivacy
```
