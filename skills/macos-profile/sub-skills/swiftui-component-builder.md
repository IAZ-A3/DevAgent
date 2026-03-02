# DevAgent Sub-skill: SwiftUI Component Builder
**Parent:** macOS Profile — Phase 4 Extension  
**Scope:** One SwiftUI component or view at a time  
**Output:** View file, ViewModel file (if needed), Preview, XCTest

---

## Purpose

Generate SwiftUI views and ViewModels following MVVM architecture, SwiftUIDesign.md
design tokens, accessibility requirements, and dark mode support. Invoked by the
Implementation orchestrator for all view-related tasks.

---

## Required Inputs

| Input | Source | Required |
|-------|--------|----------|
| Task description | Plan.md task | Yes |
| Feature requirements | PRD.md feature section | Yes |
| SwiftUIDesign.md | docs/design/SwiftUIDesign.md | Yes |
| AppArchitecture.md | docs/design/AppArchitecture.md | Yes |
| ComponentDesign.md | docs/design/ComponentDesign.md | Yes |
| Existing views in src/ | src/Views/ | For consistency |
| Coding standards | SwiftUI rules from macOS profile | Yes |

---

## 1. Component Analysis

Before writing any code:

1. Identify component type:
   - Reusable component (Button, Card, TextField variant) → goes in `src/Components/`
   - Feature view (SettingsView, MainView) → goes in `src/Views/{FeatureName}/`
   - Menu bar view (PopoverView, StatusMenuView) → goes in `src/MenuBar/`

2. Determine if ViewModel is needed:
   - Simple display view with no logic → View only
   - View with state, user interaction, or data → View + ViewModel

3. Identify design tokens to use from SwiftUIDesign.md:
   - Colors, spacing, typography, corner radii
   - SF Symbols needed (with accessibility labels)

---

## 2. File Structure

```
src/
├── Views/
│   └── {FeatureName}/
│       ├── {Name}View.swift
│       └── {Name}ViewModel.swift   (if needed)
├── Components/
│   └── {Name}.swift                (reusable components)
└── MenuBar/
    └── {Name}View.swift            (menu bar specific)

Tests/
└── {FeatureName}Tests/
    └── {Name}Tests.swift
```

---

## 3. View Generation Rules

**Every generated View must:**

```swift
// Header comment (required)
// {Name}View.swift
// Feature: {FEAT-XXX} — {feature name}
// Implements: {FR-XXX list}
// Design ref: SwiftUIDesign.md #{component-name}

import SwiftUI

struct {Name}View: View {
    // MARK: - Properties
    // Use @StateObject, @ObservedObject, @Binding, @AppStorage appropriately
    
    // MARK: - Body
    var body: some View {
        // Implementation
    }
}

// MARK: - Preview
#Preview {
    {Name}View()
        .preferredColorScheme(.light)
    {Name}View()
        .preferredColorScheme(.dark)    // Always include dark mode preview
}
```

**Accessibility requirements (every interactive element):**
```swift
Button("Save") { save() }
    .accessibilityLabel("Save settings")
    .accessibilityHint("Saves your current preferences")

Image(systemName: "gear")
    .accessibilityLabel("Settings")
    .accessibilityHidden(false)         // never hide meaningful icons
```

**Design token usage (never hardcode values):**
```swift
// ✓ Correct — use asset catalog colors
Color("PrimaryBackground")
Color("AccentColor")

// ✗ Wrong — hardcoded
Color(.white)
Color(hex: "#FF5733")

// ✓ Correct — use spacing from design tokens
.padding(DesignTokens.spacing.md)       // or .padding(16) if tokens not defined yet

// ✗ Wrong — arbitrary magic numbers
.padding(13)
```

---

## 4. ViewModel Generation Rules

```swift
// {Name}ViewModel.swift
// Feature: {FEAT-XXX}
// Implements: {FR-XXX list}

import Foundation
import Combine     // only if using Combine publishers

@MainActor                              // always mark ViewModels @MainActor
final class {Name}ViewModel: ObservableObject {
    
    // MARK: - Published Properties
    @Published private(set) var {state}: {Type}
    
    // MARK: - Private Properties
    private let {dependency}: {DependencyType}
    
    // MARK: - Init
    init({dependency}: {DependencyType} = {DefaultImpl}()) {
        self.{dependency} = {dependency}
    }
    
    // MARK: - Intent Methods (called from View)
    func {userAction}() async {
        // Implementation using async/await
        // Never use DispatchQueue.main.async — @MainActor handles this
    }
}
```

**Concurrency rules:**
- All ViewModels marked `@MainActor`
- Background work: `Task { await heavyWork() }` inside intent methods
- No `DispatchQueue` usage
- No `[weak self]` needed inside `async` methods (structured concurrency handles it)
- `[weak self]` required in escaping closures (completion handlers, NotificationCenter)

---

## 5. XCTest Generation

```swift
// {Name}Tests.swift
// Tests for: {Name}View / {Name}ViewModel
// Covers: {FR-XXX list}

import XCTest
@testable import {AppName}

final class {Name}Tests: XCTestCase {
    
    var sut: {Name}ViewModel!   // System Under Test
    
    override func setUp() {
        super.setUp()
        sut = {Name}ViewModel()
    }
    
    override func tearDown() {
        sut = nil
        super.tearDown()
    }
    
    // Minimum: 1 positive + 1 negative test per FR
    
    // [UNIT] FR-XXX — happy path
    func test_{feature}_{action}_succeeds() async throws {
        // Arrange
        // Act
        await sut.{action}()
        // Assert
        XCTAssertEqual(sut.{state}, {expected})
    }
    
    // [UNIT] FR-XXX — error/edge case
    func test_{feature}_{action}_withInvalidInput_fails() async throws {
        // Arrange
        // Act + Assert
        // ...
    }
}
```

---

## 6. Output Report

Write to `.claude/skills/state/implementation/{task-id}-component.md`:
```markdown
# Component Build Report
## Task: {task-id}
## Component: {Name}View
## Files Generated:
- src/Views/{feature}/{Name}View.swift
- src/Views/{feature}/{Name}ViewModel.swift (if applicable)
- Tests/{feature}Tests/{Name}Tests.swift
## Design tokens used: {list}
## Accessibility: labeled / not applicable
## Dark mode: supported via asset catalog
## FR coverage: {list}
## Notes: {any deviations or warnings}
```
