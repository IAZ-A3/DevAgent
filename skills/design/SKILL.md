# DevAgent Skill: Design & Architecture
**Phase:** 3 of 7  
**Output:** `docs/design/DesignIndex.md` + variable set of design documents  
**Imports:** `../_shared/context-manager.md`, `../_shared/subagent-patterns.md`, `../_shared/artifact-schema.md`

---

## Purpose

Produce a complete, traceable design that bridges requirements and implementation. The skill analyzes the PRD to determine which design documents are actually needed for the project, generates only those, and validates that every requirement has a corresponding design element and that the design is internally consistent.

---

## 1. Input Discovery

### If inputs are explicitly provided:
Use them directly. Accepted forms:
- Path to `docs/PRD.md`
- Path to `docs/Plan.md`
- Any existing design notes or sketches

### If inputs are NOT explicitly provided (auto-discovery):
Scan in this order:
1. `docs/PRD.md` — primary input (required)
2. `docs/Plan.md` — for context on task sequencing
3. `.claude/skills/state/artifact-registry.md` — confirm PRD is COMPLETED
4. `docs/design/` — any existing partial design documents
5. `.claude/skills/state/design/checkpoint.md` — resume from previous session

**If PRD is not found:** halt and inform the user. Suggest running Requirements skill first.

---

## 2. Clarification Protocol

### Mandatory clarification triggers:
- Technology stack is not specified and multiple viable options exist
- A requirement implies a design choice with significant trade-offs
- Interface between two components is ambiguous
- Data model has conflicting interpretations across requirements
- A proposed design element has no traceable requirement (gold-plating risk)

### How to ask:
- Single grouped list, numbered, with suggested answers
- Mark [BLOCKING] or [OPTIONAL]
- Example:
```
Before proceeding with design, I need to clarify:

1. [BLOCKING] No persistence mechanism is specified. The requirements imply 
   local storage is needed. Should this use: SQLite, flat files, or system 
   keychain? (Suggested: SQLite for structured data, flat files for config)
2. [OPTIONAL] FEAT-002 could use either polling or event-driven monitoring. 
   (Suggested: event-driven — more efficient, fits the NFR-001 performance target)
```

---

## 3. Internal Sub-Phases

```
Sub-phase A: PRD & Plan Analysis        [sequential]
Sub-phase B: Design Scope Definition    [sequential — user confirms]
Sub-phase C: Document Generation        [PARALLEL per document]
Sub-phase D: ADR Capture                [sequential — orchestrator]
Sub-phase E: Traceability Matrix        [PARALLEL: forward + backward]
Sub-phase F: Consistency Validation     [sequential — orchestrator]
Sub-phase G: Index Assembly             [sequential]
```

### Sub-phase A — PRD & Plan Analysis
Read and internalize PRD and Plan. Produce an internal summary:
- Project type classification (CLI tool / desktop app / service / library / etc.)
- Technology domain (systems, frontend, backend, embedded, etc.)
- Complexity indicators (number of features, external dependencies, concurrency needs)
- Identified design concerns (performance-sensitive areas, security boundaries, data flows)
- Known technology constraints from PRD

### Sub-phase B — Design Scope Definition
Based on Sub-phase A analysis, determine which design documents are needed.

**Candidate document types** (select only what applies):

| Document | When to include |
|----------|----------------|
| `SystemArchitecture.md` | Always — every project needs a top-level architecture view |
| `ComponentDesign.md` | When project has 2+ distinct components or modules |
| `InterfaceContracts.md` | When components communicate via defined APIs or protocols |
| `DataModel.md` | When project has persistent data or complex data structures |
| `TechnologyStack.md` | When technology choices are non-trivial or need justification |
| `SecurityDesign.md` | When PRD has security NFRs or sensitive data handling |
| `ErrorHandling.md` | When PRD has reliability/availability NFRs |
| `DeploymentDesign.md` | When project has deployment, packaging, or distribution concerns |
| `ConcurrencyDesign.md` | When project involves parallel processing, threading, or async operations |

**Present the proposed document list to the user:**
- Explain why each document was included or excluded
- Ask user to confirm, add, or remove documents
- Do not proceed to Sub-phase C until confirmed

### Sub-phase C — Document Generation (Parallel per document)
Spawn one subagent per confirmed design document. Each subagent:
- Reads the full PRD and relevant sections of Plan.md
- Generates its assigned document following the template in Section 5
- Tags every design element with the requirement IDs it implements: `[FEAT-001-FR-002]`
- Flags any design decision that involves trade-offs → candidate for ADR
- Output: `docs/design/{DocumentName}.md`

### Sub-phase D — ADR Capture
Orchestrator reviews all design documents for flagged trade-off decisions.
For each genuine trade-off (not trivial decisions):
- Create one ADR entry in `docs/design/ADR.md`
- Format per Section 6
- Link ADR from the relevant design document

### Sub-phase E — Traceability Matrix (Parallel)
Run two subagents simultaneously:

**Subagent E1 — Forward Traceability (Requirements → Design):**
For every FR and NFR in the PRD, verify at least one design element covers it.
Missing coverage = error.
Output: `.claude/skills/state/design/forward-trace.md`

**Subagent E2 — Backward Traceability (Design → Requirements):**
For every design element, verify it traces to at least one requirement.
Untraced design elements = gold-plating warning.
Output: `.claude/skills/state/design/backward-trace.md`

### Sub-phase F — Consistency Validation
Orchestrator runs consistency checks across all design documents:
- No circular component dependencies
- All interfaces referenced in one document are defined in another
- Data types used across interfaces are consistent
- No component is both producer and consumer of the same data without explicit reason
- Technology choices are compatible with each other and with PRD constraints
- NFR targets (performance, security) are addressed in the design

Flag all inconsistencies. Resolve or escalate to user before proceeding.

### Sub-phase G — Index Assembly
Assemble `docs/design/DesignIndex.md` per Section 7.

---

## 4. Design Element ID Convention

Every named design element (component, interface, data entity, service) gets an ID for traceability:

| Entity | ID Format | Example |
|--------|-----------|---------|
| Component | `COMP-001` | `COMP-001: FileWatcher` |
| Interface | `INTF-001` | `INTF-001: WatcherNotifierAPI` |
| Data Entity | `DATA-001` | `DATA-001: WatchEvent` |
| ADR | `ADR-001` | `ADR-001: Storage mechanism selection` |

---

## 5. Design Document Templates

### SystemArchitecture.md
```markdown
# System Architecture
## Traceability: {list of FEAT-XXX covered}
## Last Updated: {date}

### 1. Overview
High-level description of the system.

### 2. Architectural Style
(e.g. event-driven, layered, pipeline, monolithic, plugin-based)
Rationale: why this style fits the requirements.

### 3. Component Overview
| ID | Component | Responsibility | Key Requirements |
|----|-----------|---------------|-----------------|
| COMP-001 | ... | ... | FEAT-001-FR-001, NFR-002 |

### 4. Component Interaction Diagram (text)
Describe data/control flow between components in structured text:
COMP-001 → [event: FileChanged] → COMP-002 → [call: INTF-001] → COMP-003

### 5. External Dependencies
| Dependency | Version | Purpose | License |
|------------|---------|---------|---------|

### 6. Key Constraints & Assumptions
```

### ComponentDesign.md
```markdown
# Component Design
## Last Updated: {date}

### COMP-001: {Component Name}
**Responsibility:** ...  
**Implements:** {FEAT-XXX-FR-YYY, ...}  
**Language/Technology:** ...  

#### Public Interface
| Method/Property | Signature | Description |
|----------------|-----------|-------------|

#### Internal Structure
Key internal logic, algorithms, or state management approach.

#### Dependencies
| Depends On | Type | Reason |
|------------|------|--------|

#### Error Handling
How this component handles and propagates errors.
```

### InterfaceContracts.md
```markdown
# Interface Contracts
## Last Updated: {date}

### INTF-001: {Interface Name}
**Between:** COMP-XXX → COMP-YYY  
**Implements:** {requirement IDs}  
**Protocol:** (function call / event / message / file / etc.)

#### Contract Definition
Input: {type, constraints}
Output: {type, constraints}
Preconditions: {list}
Postconditions: {list}
Error cases: {list}
```

### DataModel.md
```markdown
# Data Model
## Last Updated: {date}

### DATA-001: {Entity Name}
**Purpose:** ...  
**Implements:** {requirement IDs}  
**Storage:** {where this data lives}

#### Fields
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|

#### Relationships
{relationships to other DATA entities}

#### Lifecycle
Created by: {COMP-XXX}
Read by: {COMP-XXX, COMP-YYY}
Updated by: {COMP-XXX}
Deleted by: {COMP-XXX}
```

### TechnologyStack.md
```markdown
# Technology Stack
## Last Updated: {date}

| Layer | Technology | Version | Rationale | Alternatives Considered |
|-------|-----------|---------|-----------|------------------------|
| Language | ... | ... | ... | ... |
| Framework | ... | ... | ... | ... |
| Storage | ... | ... | ... | ... |
| Testing | ... | ... | ... | ... |
| Build | ... | ... | ... | ... |

### Compatibility Matrix
Confirm all chosen technologies work together and meet NFR constraints.
```

### SecurityDesign.md
```markdown
# Security Design
## Implements: {NFR IDs}
## Last Updated: {date}

### 1. Security Boundaries
### 2. Authentication & Authorization approach
### 3. Sensitive Data Handling
### 4. Input Validation Strategy
### 5. Threat Model (key threats and mitigations)
```

### ErrorHandling.md
```markdown
# Error Handling Design
## Implements: {NFR IDs}
## Last Updated: {date}

### 1. Error Classification
| Class | Severity | Recovery Strategy |
|-------|----------|------------------|

### 2. Error Propagation Model
How errors flow between components.

### 3. User-Facing Error Handling
### 4. Logging Strategy
### 5. Recovery & Resilience patterns used
```

---

## 6. ADR Format

```markdown
# ADR Log
---

## ADR-001: {Decision Title}
**Date:** {date}  
**Status:** Decided | Superseded by ADR-XXX  
**Context:** What situation forced this decision?  
**Decision:** What was decided?  
**Rationale:** Why this option over alternatives?  
**Alternatives Considered:**
- Option A: ... — rejected because ...
- Option B: ... — rejected because ...
**Consequences:** What does this decision imply going forward?  
**Traceability:** {requirement or NFR IDs that drove this decision}

---
```

---

## 7. DesignIndex.md Structure

```markdown
# Design Index
## Project: {name}
## Generated: {date}
## Last Updated: {date}

---

## Design Documents
| Document | Path | Purpose | Status | Last Updated |
|----------|------|---------|--------|-------------|
| System Architecture | docs/design/SystemArchitecture.md | Top-level system structure | COMPLETE | {date} |
| Component Design | docs/design/ComponentDesign.md | Detailed component specs | COMPLETE | {date} |
| ... | ... | ... | ... | ... |

---

## Traceability Summary
| Requirement ID | Covered By | Design Element |
|----------------|------------|---------------|
| FEAT-001-FR-001 | ComponentDesign.md | COMP-001 |
| NFR-001 | SystemArchitecture.md, ConcurrencyDesign.md | COMP-002, COMP-003 |

---

## Open Design Issues
| ID | Issue | Document | Status |
|----|-------|----------|--------|
| DI-001 | ... | ... | OPEN |

---

## ADR Summary
| ID | Decision | Status |
|----|----------|--------|
| ADR-001 | ... | Decided |
```

---

## 8. Context Management (Phase-Specific)

Imports rules from `../_shared/context-manager.md`, plus:

- After Sub-phase B (scope confirmed by user): save checkpoint
- After Sub-phase C (all documents generated): save checkpoint
- After Sub-phase E (traceability complete): save checkpoint before validation
- State folder: `.claude/skills/state/design/`
- If context runs low mid Sub-phase C: complete current document subagent, checkpoint, resume with remaining documents in fresh session

---

## 9. Output & Phase Gate

On completion:
1. Write all design documents to `docs/design/`
2. Write `docs/design/DesignIndex.md`
3. Write `docs/design/ADR.md` (even if empty, initialize the file)
4. Update `.claude/skills/state/artifact-registry.md`
5. Produce phase gate summary:

```
# Phase Gate — Design & Architecture
## Result: PASS | NEEDS_REVIEW
## Artifacts: docs/design/DesignIndex.md + {list of documents}
## Requirements Coverage: N/N (100%) | N/M (warn if <100%)
## ADRs Captured: N
## Open Design Issues: {count}
## Recommended Next Phase: implementation
## Blockers: {list or "None"}
```

6. Inform user: Design is ready for review. Suggest running the **Implementation** skill next.

---

## 10. Quality Checklist (Self-Assessment before delivery)

- [ ] All design documents confirmed by user before generation
- [ ] Every design element has a unique ID (COMP, INTF, DATA)
- [ ] Every design element traces to at least one requirement
- [ ] Every requirement (FR and NFR) is covered by at least one design element
- [ ] No circular component dependencies
- [ ] All interfaces referenced are defined
- [ ] ADRs written for all genuine trade-off decisions
- [ ] Technology choices are mutually compatible
- [ ] NFR targets explicitly addressed in design
- [ ] DesignIndex.md accurately reflects all generated documents
- [ ] All BLOCKING clarifications resolved before generation
