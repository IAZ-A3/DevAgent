# PROJECT.md
# macOS app project configuration for Claude Code.
# Copy this file to your project root as PROJECT.md and fill it in.

---

## Project Identity

- **Name:** 
- **Type:** macos                  # triggers macOS profile in CLAUDE.md
- **Subtype:**                     # standard | menubar | menubar+window | document
- **One-liner:**                   # what this app does in one sentence
- **Target platform:** macOS       # macOS 13 Ventura minimum (M-silicon)
- **Target users:**                # e.g. developers, power users, general consumers
- **Distribution:** direct-download  # DMG via your own hosting

---

## Xcode Project

- **Xcode project/workspace:**    # e.g. MyApp.xcodeproj or MyApp.xcworkspace
- **Scheme:**                     # e.g. MyApp
- **Bundle ID:**                  # e.g. com.yourname.myapp
- **Minimum macOS version:**      # e.g. 13.0
- **Swift version:**              # e.g. 5.9

---

## Apple Developer Account

- **Team ID:**                    # 10-character alphanumeric from developer.apple.com
- **Team name:**                  # e.g. "John Smith" or company name
- **Certificate:**                Developer ID Application
- **Notarization method:**        # App-specific password | API key (notarytool)

---

## App Capabilities

# List capabilities the app uses — these drive entitlements generation
- Network access:       # yes / no
- File system access:   # sandbox only / user-selected / downloads / full
- Camera:               # yes / no
- Microphone:           # yes / no
- Location:             # yes / no
- Contacts:             # yes / no
- Calendar:             # yes / no
- Keychain:             # yes / no
- Launch at login:      # yes / no
- Bluetooth:            # yes / no
- Other:                # describe

---

## SwiftUI Design References

# URLs or descriptions of reference apps / design examples.
# Claude Code will extract design patterns, not copy assets or code.
- 

---

## Git Conventions

- **Commit style:**               # e.g. Conventional Commits, free-form
- **Branch strategy:**            # e.g. main only, feature branches
- **PR required:**                # yes / no
- **Protected branches:**         # e.g. main

---

## Quality Gates

- **Tests must pass before:**     # e.g. every release
- **Clean build required:**       yes   # zero warnings policy
- **Accessibility:**              VoiceOver compatible

---

## Claude Code Preferences

- **Ask before adding SPM dependency:**   yes
- **Ask before modifying entitlements:**  yes
- **Ask before deleting any file:**       yes
- **Ask before archiving/notarizing:**    yes
- **Language for all docs:**              # e.g. English

---

## Out of Scope

- Never push to git without explicit instruction
- Never run notarization without explicit instruction
- Never commit credentials or app-specific passwords
- 

---

## Notes

# Any constraints, known issues, or context Claude Code should know.
#
