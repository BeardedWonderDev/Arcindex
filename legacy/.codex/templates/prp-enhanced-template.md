# CODEX Enhanced PRP Template v1.0
<!-- This template synthesizes complete workflow context into implementation-ready guidance -->

## Goal

**Feature Goal**: [Extracted from PRD user stories and requirements - specific, measurable end state]

**Deliverable**: [Concrete implementation artifact derived from architecture document]

**Success Definition**: [Synthesized from PRD success metrics and architecture validation criteria]

## User Persona

<!-- Populated from project-brief.md and prd.md user personas -->
**Target User**: [Primary user type from user personas section]

**Use Case**: [Primary scenario from user stories in PRD]

**User Journey**: [Step-by-step flow synthesized from user flows in PRD]

**Pain Points Addressed**: [From project brief problem statement and PRD background]

## Why

<!-- Context from workflow documents -->
- [Business value from project-brief.md goals section]
- [Technical requirements from prd.md functional requirements]
- [Architecture decisions from architecture.md rationale]
- [Integration needs from architecture.md component map]

## What

<!-- User-visible behavior from PRD, technical implementation from architecture -->
[Comprehensive description synthesizing PRD requirements with architecture implementation approach]

### Success Criteria

<!-- Aggregated from all workflow phases -->
- [ ] [From PRD acceptance criteria]
- [ ] [From architecture validation requirements]
- [ ] [From project brief success metrics]
- [ ] [Implementation-specific criteria]

## All Needed Context

### Context Completeness Check

_CRITICAL: Before proceeding, validate: "If someone knew nothing about this codebase or the preceding workflow documents, would they have everything needed to implement this successfully?"_

### Workflow Context Synthesis

```yaml
# Documents synthesized into this PRP
workflow-documents:
  - document: docs/project-brief.md
    synthesized:
      - Business context and constraints
      - Target market and user needs
      - Success metrics and KPIs

  - document: docs/prd.md
    synthesized:
      - Functional requirements (FR1-FRn)
      - Non-functional requirements (NFR1-NFRn)
      - User stories and acceptance criteria
      - UI/UX requirements

  - document: docs/architecture.md
    synthesized:
      - Technology stack decisions
      - Component architecture
      - API design patterns
      - Security measures
      - Deployment strategy
```

### Documentation & References

```yaml
# MUST READ - Include these in your context window
# Architecture & Design Patterns
- file: docs/architecture.md
  why: Technology stack and architectural patterns for this implementation
  pattern: [Specific pattern from architecture - e.g., "Service layer pattern in section 4.2"]
  critical: [Key architectural constraint - e.g., "Must use async/await for all I/O operations"]

- url: [Technology documentation URL with section anchor]
  why: [Specific implementation guidance for chosen technology from architecture]
  critical: [Known limitations or requirements from architecture decisions]

# Existing Codebase Patterns
- file: [src/similar/feature.swift]
  why: Follow this pattern for [specific aspect]
  pattern: [What to replicate - class structure, error handling, etc.]
  gotcha: [Known issues to avoid from existing code]

# Domain-Specific Documentation
- docfile: PRPs/ai_docs/[technology]_patterns.md
  why: CODEX-curated patterns for [technology] implementation
  section: [Specific section relevant to this feature]

# Testing & Validation
- file: [tests/similar_test.swift]
  why: Test structure and validation approach
  pattern: Test organization and assertion patterns

# Security Requirements
- url: [Security guideline URL from architecture security section]
  why: Required security measures from architecture document
  critical: [Specific security requirement - e.g., "All user input must be sanitized"]
```

### Current Codebase Tree

```bash
# Current structure showing where implementation will fit
# [Populated from actual tree command or architecture document]
```

### Desired Codebase Tree with Files to be Added

```bash
# Based on architecture.md project structure and component design
# Each file annotated with its responsibility from architecture
src/
├── features/
│   └── [feature-name]/          # New feature module
│       ├── models/              # Data models from PRD entities
│       ├── services/            # Business logic from user stories
│       ├── views/               # UI components from PRD UI requirements
│       └── tests/               # Test coverage from NFRs
```

### Known Gotchas & Constraints

```swift
// CRITICAL: Technology-specific constraints from architecture
// Example: SwiftUI requires @MainActor for UI updates
// Example: Core Data batch operations limited to 5000 objects

// From Architecture Document:
// - [Constraint from architecture decisions]
// - [Technology limitation from stack selection]

// From PRD Non-Functional Requirements:
// - [Performance constraint from NFRs]
// - [Security requirement from NFRs]

// From Existing Codebase:
// - [Pattern that must be followed]
// - [Convention that cannot be broken]
```

## Implementation Blueprint

### Data Models and Structure

<!-- Derived from PRD data requirements and architecture data model -->
```swift
// Core entities from PRD section [X.X]
// Following architecture pattern from section [Y.Y]

// Example structure based on architecture decisions:
struct [EntityName]: Codable {
    // Properties from PRD data model
    // Validation from PRD business rules
    // Persistence strategy from architecture
}
```

### Implementation Tasks (Ordered by Dependencies)

<!-- Tasks synthesized from all workflow documents with clear traceability -->
```yaml
Task 1: CREATE [path/to/file] - [Component from architecture.md]
  - IMPLEMENT: [Functionality from PRD FR-X]
  - FOLLOW pattern: [Reference to existing pattern or architecture decision]
  - VALIDATES: [Which PRD requirement this satisfies]
  - TEST: [Test approach from architecture testing strategy]
  - CONNECTS: [How it integrates with other components per architecture]

Task 2: INTEGRATE [component] with [existing system]
  - REQUIREMENT: [From PRD FR-Y or NFR-Z]
  - ARCHITECTURE: [Pattern from architecture.md section X]
  - SECURITY: [Security requirement from architecture security layer]
  - VALIDATION: [How to verify integration works]

Task 3: IMPLEMENT [user-facing feature]
  - USER STORY: [From PRD user stories]
  - UI PATTERN: [From PRD UI requirements or architecture UI layer]
  - ACCEPTANCE: [Acceptance criteria from PRD]
  - ACCESSIBILITY: [From PRD accessibility requirements]

# Continue with all tasks needed for complete implementation
```

### Implementation Patterns & Key Details

```swift
// Pattern from architecture.md for [specific aspect]
// Example implementation following project conventions

// API Pattern (from architecture.md API design)
protocol [ServiceName] {
    // Methods derived from PRD functional requirements
    // Following architecture API standards
}

// Error Handling (from architecture coding standards)
enum [Feature]Error: Error {
    // Error cases from PRD edge cases and architecture error strategy
}

// Validation Pattern (from PRD business rules)
extension [Model] {
    func validate() throws {
        // Validation logic from PRD requirements
    }
}
```

### Integration Points

<!-- From architecture.md component interactions -->
```yaml
INTERNAL_INTEGRATION:
  - component: [Existing component name]
    interface: [API or protocol from architecture]
    data_flow: [How data moves per architecture diagram]
    error_handling: [Error propagation strategy]

EXTERNAL_INTEGRATION:
  - service: [Third-party service from architecture]
    protocol: [Integration protocol from architecture]
    authentication: [Auth method from security requirements]
    fallback: [Fallback strategy from architecture]

STATE_MANAGEMENT:
  - pattern: [State management pattern from architecture]
  - persistence: [Data persistence strategy]
  - synchronization: [Sync approach from architecture]
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Project-specific validation from architecture.md build tools
# For Swift projects:
swiftlint --strict
swift-format lint --recursive Sources/

# Expected: No errors, warnings documented
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test commands from architecture testing strategy
# For Swift:
swift test --filter [FeatureName]Tests

# Coverage requirement from PRD NFRs: [X]%
# Expected: All unit tests pass, coverage > [X]%
```

### Level 3: Integration Testing (System Validation)

```bash
# Integration test approach from architecture
# For iOS:
xcodebuild test -scheme [SchemeName] -destination 'platform=iOS Simulator,name=iPhone 15'

# Validate integration points from architecture:
# - [ ] API integration works
# - [ ] Data persistence verified
# - [ ] State management correct
```

### Level 4: Acceptance Testing (Requirements Validation)

```bash
# User story validation from PRD
# Language-specific agent validation

# Run acceptance tests for PRD user stories:
# - [ ] User story 1 acceptance criteria met
# - [ ] User story 2 acceptance criteria met
# - [ ] Performance requirements from NFRs satisfied
# - [ ] Security requirements validated
```

## Final Validation Checklist

### Requirements Traceability
<!-- Ensure every PRD requirement is addressed -->
- [ ] All functional requirements (FR) implemented
- [ ] All non-functional requirements (NFR) satisfied
- [ ] All user stories have working implementation
- [ ] All acceptance criteria pass

### Architecture Compliance
<!-- Verify architecture decisions are followed -->
- [ ] Follows architecture component structure
- [ ] Uses specified technology stack correctly
- [ ] Implements required design patterns
- [ ] Respects architectural constraints

### Code Quality
<!-- From architecture coding standards -->
- [ ] Follows project coding conventions
- [ ] Includes comprehensive error handling
- [ ] Has required documentation
- [ ] Implements logging per standards

### Testing & Validation
<!-- From PRD and architecture quality requirements -->
- [ ] Unit test coverage meets requirement ([X]%)
- [ ] Integration tests pass
- [ ] Performance benchmarks met
- [ ] Security requirements validated

### Documentation & Deployment
<!-- From architecture and PRD documentation requirements -->
- [ ] API documentation complete
- [ ] User documentation updated
- [ ] Deployment artifacts created
- [ ] Migration plan executed (if applicable)

---

## Anti-Patterns to Avoid

<!-- Synthesized from architecture decisions and PRD constraints -->
- ❌ Don't violate architecture layer boundaries
- ❌ Don't ignore PRD non-functional requirements
- ❌ Don't bypass security measures from architecture
- ❌ Don't deviate from established patterns without justification
- ❌ Don't skip validation levels
- ❌ Don't implement without tests
- ❌ Don't ignore accessibility requirements
- ❌ Don't break existing functionality

## Confidence Score: _/10

_Rate the likelihood of one-pass implementation success based on context completeness and clarity_

## Zero-Knowledge Validation Result

- [ ] Fresh Claude instance could implement with only this PRP
- [ ] All references are accessible and specific
- [ ] No implicit knowledge required
- [ ] Implementation path is unambiguous