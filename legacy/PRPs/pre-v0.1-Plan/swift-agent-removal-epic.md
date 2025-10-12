name: "Swift Agent Removal Epic PRP - Command-Based Validation Implementation"
description: |
  Comprehensive PRP for safely removing Swift language agent dependencies from CODEX
  and replacing them with command-based validation to improve development velocity
  and eliminate debugging complexity while maintaining quality assurance.

---

## Goal

**Feature Goal**: Remove Swift language agent dependencies from CODEX system and replace Level 4 validation with comprehensive command-based Swift tooling validation

**Deliverable**: Simplified CODEX architecture with command-based validation that maintains quality while eliminating agent coordination complexity

**Success Definition**: Complete greenfield Swift workflow execution without agent dependencies, improved debugging clarity, and measurable development velocity increase

## User Persona

**Target User**: CODEX developers working on core orchestration system functionality

**Use Case**: Daily development on CODEX core features without Swift agent coordination conflicts and debugging overhead

**User Journey**:
1. Developer starts CODEX workflow without agent coordination setup
2. Workflow executes with clear command-based validation feedback
3. Debugging focuses on core functionality rather than agent coordination
4. Development velocity increases due to simplified architecture

**Pain Points Addressed**:
- Agent coordination debugging complexity
- Development conflicts from architecture mismatch
- Slower iteration cycles due to coordination failures
- Obscured root causes in error scenarios

## Why

- **Development Velocity**: Eliminate time spent troubleshooting agent coordination issues that impede core CODEX development
- **System Reliability**: Remove complex agent interdependencies that create multiple failure points and obscure root causes
- **Architecture Simplification**: Focus development effort on core CODEX orchestration functionality rather than agent coordination
- **Debugging Clarity**: Enable direct error diagnosis without coordination layer complexity
- **Future Scalability**: Create foundation for language-agnostic workflows without agent dependencies

## What

Remove Swift language agents from CODEX configuration and workflows, replacing agent-based Level 4 validation with comprehensive command-based Swift tooling validation while maintaining all quality assurance capabilities.

### Success Criteria

- [ ] CODEX loads configuration without Swift agent errors
- [ ] Greenfield Swift workflow completes end-to-end without agent dependencies
- [ ] Level 4 validation provides equivalent quality assurance through Swift tooling
- [ ] Command-based validation gives clear, actionable error feedback
- [ ] Development velocity improves measurably (faster debugging, clearer errors)
- [ ] All existing CODEX core functionality remains intact
- [ ] Generic workflow template created for future language support

## All Needed Context

### Context Completeness Check

_This PRP provides complete context for implementing Swift agent removal based on comprehensive codebase analysis. An implementing agent would have all necessary information to complete this safely without prior CODEX knowledge._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- file: docs/swift-agent-removal-epic.md
  why: Complete epic specification with 3 stories and implementation requirements
  pattern: Story-based implementation with clear acceptance criteria
  gotcha: Must create backup branch before any modifications

- file: docs/swift-agent-removal-analysis.md
  why: Technical analysis of all Swift agent integration points and safe removal strategies
  pattern: Phase-based removal approach with risk assessment
  gotcha: Level 4 validation requires command-based replacement strategy

- file: .codex/config/codex-config.yaml
  why: Primary configuration file with Swift agent definitions (lines 51-60)
  pattern: YAML configuration with language_agents section
  gotcha: Comment out rather than delete for safe rollback

- file: .codex/workflows/greenfield-swift.yaml
  why: Main workflow file with agent coordination patterns (lines 25-32, 139-175, 213-217)
  pattern: Multi-section agent integration with coordination specifications
  gotcha: Must preserve existing workflow structure while removing agent references

- file: .codex/tasks/validation-gate.md
  why: 4-level validation system with Level 4 agent dependencies (lines 495-528)
  pattern: Progressive validation with agent coordination protocol
  gotcha: Level 4 requires complete command-based replacement strategy

- file: .codex/agents/dev.md
  why: Development coordinator with language agent integration patterns (lines 145-158)
  pattern: Agent coordination methods and integration specifications
  gotcha: Simplify to direct implementation without breaking coordination structure
```

### Current Codebase tree

```bash
CODEX/
├── .codex/
│   ├── config/
│   │   └── codex-config.yaml          # ⚠️ PRIMARY CONFIG - Contains swift_agents
│   ├── workflows/
│   │   ├── greenfield-swift.yaml      # ⚠️ MAIN WORKFLOW - Agent coordination
│   │   └── health-check.yaml          # ✅ COMMAND-BASED REFERENCE
│   ├── tasks/
│   │   └── validation-gate.md         # ⚠️ LEVEL 4 VALIDATION - Agent dependent
│   └── agents/
│       └── dev.md                     # ⚠️ DEV COORDINATOR - Language agent refs
├── docs/                              # 📝 DOCUMENTATION UPDATES REQUIRED
│   ├── swift-agent-removal-epic.md    # Epic specification
│   ├── swift-agent-removal-analysis.md # Technical analysis
│   ├── prd.md                         # ⚠️ Swift agent references
│   ├── codex-architecture.md          # ⚠️ Architecture patterns
│   └── CODEX-User-Guide.md            # ⚠️ User guidance
└── PRPs/                              # 📝 PRP UPDATES REQUIRED
    └── codex-orchestration-system.md  # ⚠️ Implementation requirements
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
CODEX/
├── .codex/
│   ├── config/
│   │   └── codex-config.yaml          # 🔧 MODIFIED - Swift agents commented out
│   ├── workflows/
│   │   ├── greenfield-swift.yaml      # 🔧 MODIFIED - Command-based Level 4
│   │   └── greenfield-generic.yaml    # ➕ NEW - Language-agnostic template
│   ├── tasks/
│   │   └── validation-gate.md         # 🔧 MODIFIED - Command-based Level 4
│   └── agents/
│       └── dev.md                     # 🔧 MODIFIED - Direct implementation
├── docs/
│   ├── workflow-customization-guide.md # ➕ NEW - Generic workflow setup
│   ├── prd.md                         # 🔧 UPDATED - Command-based references
│   ├── codex-architecture.md          # 🔧 UPDATED - Simplified architecture
│   └── CODEX-User-Guide.md            # 🔧 UPDATED - Command-based guidance
└── PRPs/
    └── codex-orchestration-system.md  # 🔧 UPDATED - No agent requirements
```

### Known Gotchas of our codebase & Library Quirks

```yaml
# CRITICAL: CODEX configuration loading
# Configuration system reads language_agents section at startup
# Commenting out rather than deleting enables safe rollback
# Must test with /codex status after configuration changes

# CRITICAL: Workflow coordination requirements
# Greenfield workflow expects agent coordination in multiple sections
# Lines 25-32, 139-175, 213-217 must be modified as cohesive unit
# Existing workflow structure must be preserved to avoid breaking orchestration

# CRITICAL: Level 4 validation system
# Current system expects Task tool coordination with Swift agents
# Replacement must provide equivalent quality assurance
# Command-based validation must handle error reporting and aggregation

# CRITICAL: Git backup strategy required
# Create swift-agents-backup branch before any modifications
# All changes must be reversible via git branch switching
# Backup enables complete restoration if issues discovered

# CRITICAL: Swift tooling dependencies
# Command-based validation requires: swift, swiftlint, swift-format, xcodebuild
# All tooling must be available in execution environment
# Validation commands must be project-specific and tested
```

## Implementation Blueprint

### Data models and structure

The implementation focuses on configuration and workflow modifications rather than new data models. The existing CODEX state management and configuration structures remain intact.

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE backup branch and safety preparation
  - EXECUTE: git checkout -b swift-agents-backup && git checkout main
  - DOCUMENT: Current CODEX functionality state for rollback reference
  - VERIFY: /codex status passes with current configuration
  - PURPOSE: Ensure complete rollback capability before any modifications
  - PLACEMENT: Git repository management

Task 2: MODIFY .codex/config/codex-config.yaml configuration
  - FIND: Lines 51-60 language_agents section with swift_agents list
  - COMMENT OUT: Swift agents section with clear reasoning comments
  - PATTERN: # language_agents: # DISABLED - Swift agents removed for development simplification
  - PRESERVE: All other configuration sections unchanged
  - VALIDATE: /codex status passes after modification
  - PLACEMENT: Configuration layer modification

Task 3: MODIFY .codex/workflows/greenfield-swift.yaml workflow definition
  - SECTION 1: Lines 25-32 language_support.agents - comment out agent list
  - SECTION 2: Lines 139-175 implementation_coordination - replace with direct execution
  - SECTION 3: Lines 213-217 level_4 validation - replace agents with commands
  - PATTERN: Follow existing health-check.yaml command-based approach
  - PRESERVE: Existing workflow phase structure and orchestration
  - PLACEMENT: Workflow definition layer

Task 4: MODIFY .codex/tasks/validation-gate.md validation system
  - REPLACE: Lines 495-528 Level 4 agent coordination with command-based validation
  - IMPLEMENT: Comprehensive Swift tooling validation script
  - COMMANDS: swift build --configuration Release, swift test --parallel, swiftlint --strict
  - PATTERN: Progressive command execution with error handling and reporting
  - PRESERVE: Levels 0-3 validation remain unchanged
  - PLACEMENT: Validation system core

Task 5: MODIFY .codex/agents/dev.md development coordinator
  - SIMPLIFY: Lines 145-158 language agent integration to direct implementation
  - REMOVE: Task tool coordination references for Swift agents
  - PATTERN: Direct implementation approach with tooling validation
  - PRESERVE: Core development coordination and PRP execution capabilities
  - PLACEMENT: Agent definition modification

Task 6: CREATE .codex/workflows/greenfield-generic.yaml generic workflow template
  - IMPLEMENT: Language-agnostic workflow based on greenfield-swift structure
  - PARAMETERIZE: {{LANGUAGE}}, {{BUILD_COMMAND}}, {{TEST_COMMAND}} placeholders
  - INCLUDE: Examples for JavaScript, Python, Go, Rust customization
  - PATTERN: Template-based workflow with language-specific command customization
  - PLACEMENT: New workflow template for future language support

Task 7: UPDATE documentation files for consistency
  - MODIFY: docs/prd.md, docs/codex-architecture.md, docs/CODEX-User-Guide.md
  - REPLACE: "Swift agent coordination" references with "command-based validation"
  - UPDATE: Architecture diagrams to reflect simplified structure
  - PATTERN: Systematic documentation updates maintaining existing structure
  - PLACEMENT: Documentation layer consistency

Task 8: CREATE docs/workflow-customization-guide.md
  - IMPLEMENT: Comprehensive guide for customizing generic workflow
  - INCLUDE: Language-specific examples and command customization
  - PROVIDE: Step-by-step workflow setup for different tech stacks
  - PATTERN: Tutorial-style documentation with practical examples
  - PLACEMENT: New documentation for workflow extensibility

Task 9: VALIDATE end-to-end workflow execution
  - EXECUTE: Complete greenfield Swift workflow test without agent dependencies
  - VERIFY: All validation levels (0-4) execute successfully with command-based approach
  - TEST: Configuration loading, workflow initialization, validation execution
  - CONFIRM: Error handling provides clear, actionable feedback
  - PLACEMENT: Integration testing and validation
```

### Implementation Patterns & Key Details

```yaml
# Configuration Modification Pattern
language_agents:
  # global_agents_directory: "~/.claude/agents/"  # DISABLED
  # swift_agents: []  # DISABLED - temporarily removed for development simplification
  #   - swift-feature-developer
  #   - swift-syntax-reviewer
  #   # ... etc

# Workflow Direct Implementation Pattern
coordination:
  - agent: dev
    action: direct_implementation
    description: "Direct feature implementation following Swift best practices"
    coordination_method: "direct_execution"
    # REMOVED: parallel agent coordination complexity

# Command-Based Level 4 Validation Pattern
level_4:
  name: "Command-Based Domain Validation"
  commands:
    - "swift build --configuration Release -v"
    - "swift test --parallel --enable-code-coverage"
    - "swiftlint --strict --reporter json"
  # agents: []  # DISABLED - using command-based validation
  custom_validation: false

# Error Handling Enhancement Pattern
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Release build failed"
    grep -A 5 -B 5 "error:" .codex/state/release-build.log
    exit 1
fi

# Generic Workflow Template Pattern
language_support:
  primary: "{{LANGUAGE}}"  # javascript, python, go, rust, etc.
  validation_method: "command_based"
  tooling:
    - "{{BUILD_COMMAND}}"     # npm run build, cargo build, go build
```

### Integration Points

```yaml
CONFIGURATION:
  - modify: .codex/config/codex-config.yaml
  - pattern: "Comment out language_agents section with clear reasoning"
  - preserve: "All other CODEX configuration sections unchanged"

WORKFLOW_ORCHESTRATION:
  - modify: .codex/workflows/greenfield-swift.yaml
  - pattern: "Replace agent coordination with direct implementation"
  - preserve: "Existing workflow phase structure and state management"

VALIDATION_SYSTEM:
  - modify: .codex/tasks/validation-gate.md
  - pattern: "Command-based Level 4 validation with Swift tooling"
  - preserve: "Levels 0-3 validation remain unchanged"

STATE_MANAGEMENT:
  - preserve: .codex/state/ directory and workflow.json structure
  - pattern: "No changes to state persistence or context breakpoints"
  - maintain: "All existing CODEX orchestration capabilities"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Test configuration changes immediately
/codex status | grep -i "error\|fail"
if [ $? -eq 0 ]; then
    echo "❌ Configuration Error: CODEX failed to load properly"
    echo "Check .codex/config/codex-config.yaml for syntax errors"
    exit 1
fi

# Validate workflow loading
/codex list-workflows | grep -E "(swift|generic)"
if [ $? -ne 0 ]; then
    echo "❌ Workflow Error: Expected workflows not found"
    exit 1
fi

echo "✅ Level 1 PASSED: Configuration and workflow syntax validation"
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test configuration loading functionality
/codex start health-check test-validation 2>&1 | tee .codex/state/health-test.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Health Check Failed: Basic workflow execution broken"
    cat .codex/state/health-test.log
    exit 1
fi

# Test Swift workflow initialization without agents
/codex start greenfield-swift test-swift-project 2>&1 | tee .codex/state/swift-init-test.log
if grep -q "agent.*error\|coordination.*fail" .codex/state/swift-init-test.log; then
    echo "❌ Swift Workflow Failed: Agent references still causing errors"
    exit 1
fi

echo "✅ Level 2 PASSED: Workflow execution validation"
```

### Level 3: Integration Testing (System Validation)

```bash
# Create minimal Swift project for testing
mkdir -p test-swift-validation/Sources/TestProject
echo 'print("Hello, CODEX!")' > test-swift-validation/Sources/TestProject/main.swift
cd test-swift-validation

# Test command-based Level 4 validation execution
swift build --configuration Release 2>&1 | tee ../release-build-test.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Swift Build Failed: Command-based validation not working"
    exit 1
fi

swift test 2>&1 | tee ../swift-test.log
swiftlint --version > ../swiftlint-test.log
swift-format --version > ../swift-format-test.log

cd ..
rm -rf test-swift-validation

echo "✅ Level 3 PASSED: Command-based Swift tooling validation"
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Test complete workflow with validation gates
/codex validate --dry-run greenfield-swift 2>&1 | tee .codex/state/validation-dry-run.log
if grep -q "level.*fail\|agent.*missing" .codex/state/validation-dry-run.log; then
    echo "❌ Validation Gates Failed: Level 4 command-based validation issues"
    exit 1
fi

# Test error handling and recovery
echo "# Test invalid Swift syntax" > test-syntax-error.swift
echo "invalid swift syntax here" >> test-syntax-error.swift

swift build test-syntax-error.swift 2>&1 | tee syntax-error-test.log
if ! grep -q "error:" syntax-error-test.log; then
    echo "❌ Error Handling Failed: Swift tooling not providing expected error feedback"
    exit 1
fi

rm test-syntax-error.swift syntax-error-test.log

# Validate rollback capability
git branch | grep swift-agents-backup > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Rollback Failed: Backup branch not available"
    exit 1
fi

echo "✅ Level 4 PASSED: Complete system validation with error handling"
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] CODEX configuration loads without errors: `/codex status`
- [ ] Swift workflow initializes without agent dependencies
- [ ] Level 4 validation executes with command-based approach
- [ ] Error handling provides clear, actionable feedback

### Feature Validation

- [ ] Greenfield Swift workflow completes end-to-end without agent coordination
- [ ] Command-based Level 4 validation provides equivalent quality assurance
- [ ] All existing CODEX core functionality remains intact
- [ ] Generic workflow template created for future language support
- [ ] Documentation reflects simplified architecture

### Code Quality Validation

- [ ] Configuration follows existing YAML commenting patterns
- [ ] Workflow modifications preserve existing orchestration structure
- [ ] File placement matches desired codebase tree structure
- [ ] Rollback strategy tested and functional via backup branch
- [ ] All changes are reversible through git branch restoration

### Documentation & Deployment

- [ ] All documentation updated to reflect command-based approach
- [ ] Generic workflow customization guide provides clear examples
- [ ] Architecture documentation reflects simplified structure
- [ ] Rollback instructions clearly documented for emergency restoration

---

## Anti-Patterns to Avoid

- ❌ Don't delete configuration sections - comment them out for rollback safety
- ❌ Don't modify workflow structure - only replace agent coordination with direct implementation
- ❌ Don't skip backup branch creation - ensure complete rollback capability
- ❌ Don't ignore validation command testing - verify all Swift tooling is available
- ❌ Don't break existing orchestration - preserve all core CODEX functionality
- ❌ Don't remove error handling - enhance feedback quality with command-based validation