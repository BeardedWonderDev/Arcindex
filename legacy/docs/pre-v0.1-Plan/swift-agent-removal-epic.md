# Swift Agent Removal Epic - Brownfield Enhancement

**Date Created**: 2025-09-27
**Epic ID**: EPIC-SWIFT-REMOVAL-001
**Priority**: High - Blocking CODEX core development
**Status**: Ready for Implementation
**Estimated Effort**: 3 Stories, 8-12 hours total

---

## Epic Overview

### Epic Goal
Simplify CODEX development by removing Swift language agent dependencies that are causing development conflicts and debugging complexity, replacing them with command-based validation to improve development velocity and system reliability.

### Business Value
- **Development Velocity**: Reduce debugging time spent on agent coordination issues
- **System Reliability**: Eliminate complex agent interdependencies that obscure root causes
- **Architecture Simplification**: Focus development effort on core CODEX functionality
- **Future Scalability**: Create foundation for language-agnostic workflows

### Epic Description

**Existing System Context:**
- Current relevant functionality: CODEX orchestration system with integrated Swift language agents for enhanced development workflows
- Technology stack: YAML-based workflow configuration, Swift tooling integration, multi-level validation gates
- Integration points: Configuration files, greenfield-swift workflow, validation gate system, agent coordination patterns

**Enhancement Details:**
- What's being added/changed: Remove Swift agent dependencies and replace Level 4 validation with command-based Swift tooling (swift build, swift test, swiftlint, swift-format)
- How it integrates: Maintains existing workflow structure while simplifying coordination patterns and reducing external dependencies
- Success criteria: Complete greenfield workflow execution without agent coordination failures, improved debugging clarity, measurable development velocity increase

---

## Epic Compatibility Requirements

- ✅ Existing core CODEX workflow phases remain unchanged (Discovery → Analyst → PM → Architect → PRP Creator → Implementation)
- ✅ Document generation templates continue to work
- ✅ Context management and state persistence unaffected
- ✅ Levels 1-3 validation maintain current functionality
- ✅ PRP creation process remains intact

---

## Epic Risk Assessment

**Primary Risk:** Breaking existing CODEX workflow functionality during agent removal
**Mitigation:** Phased implementation with testing at each step, maintaining workflow structure while only modifying coordination patterns
**Rollback Plan:** Git branch backup (swift-agents-backup) allows complete restoration of original state

**Risk Level:** **LOW** - Swift agents are enhancement layers, not core functionality

---

## Epic Definition of Done

- ✅ All stories completed with acceptance criteria met
- ✅ CODEX configuration loads without errors (/codex status passes)
- ✅ Greenfield Swift workflow completes end-to-end without agent dependencies
- ✅ Command-based Level 4 validation provides meaningful feedback
- ✅ Documentation reflects simplified architecture
- ✅ No regression in core CODEX functionality
- ✅ Development velocity improvement is measurable

---

# Story 1: Configuration Cleanup and Safe Agent Disabling

**Story ID**: STORY-SWIFT-001
**Priority**: P0 (Must complete first)
**Estimated Effort**: 2-3 hours
**Dependencies**: None

## User Story
As a **CODEX developer**,
I want **Swift agent dependencies safely disabled in the configuration**,
So that **CODEX can load without agent coordination conflicts while maintaining a rollback path**.

## Story Context

**Existing System Integration:**
- Integrates with: CODEX configuration system (`codex-config.yaml`)
- Technology: YAML configuration management, Git version control
- Follows pattern: Configuration-based feature enablement/disabling
- Touch points: Configuration loading, workflow initialization, system status checks

## Acceptance Criteria

### Functional Requirements
1. **Configuration Modification**: Swift agent configuration section is safely disabled/commented in `.codex/config/codex-config.yaml`
2. **System Validation**: CODEX system loads configuration without errors after changes
3. **Backup Creation**: Backup branch `swift-agents-backup` is created before any modifications

### Integration Requirements
4. **Existing Functionality**: Configuration loading mechanism continues to work unchanged
5. **Pattern Consistency**: New configuration follows existing YAML commenting pattern
6. **Status Integration**: Integration with CODEX status system maintains current behavior

### Quality Requirements
7. **Verification Testing**: Configuration changes are verified through `/codex status` command
8. **Documentation**: Git backup strategy is documented for rollback
9. **Regression Testing**: No regression in core configuration functionality verified

## Technical Implementation

### Configuration Changes Required

**File**: `.codex/config/codex-config.yaml` (Lines 51-61)

**Before:**
```yaml
language_agents:
  global_agents_directory: "~/.claude/agents/"
  swift_agents:
    - swift-feature-developer
    - swift-syntax-reviewer
    - swift-architecture-reviewer
    - swift-performance-reviewer
    - swift-testing-reviewer
    - swift-refactor
    - ios-security-auditor
```

**After:**
```yaml
# language_agents:  # DISABLED - Swift agents removed for development simplification
#   global_agents_directory: "~/.claude/agents/"
#   swift_agents:  # Causing development conflicts - temporarily removed
#     - swift-feature-developer
#     - swift-syntax-reviewer
#     - swift-architecture-reviewer
#     - swift-performance-reviewer
#     - swift-testing-reviewer
#     - swift-refactor
#     - ios-security-auditor
```

### Implementation Steps
1. **Create backup branch**: `git checkout -b swift-agents-backup`
2. **Return to main**: `git checkout main`
3. **Modify configuration**: Apply changes to `.codex/config/codex-config.yaml`
4. **Test configuration**: Run `/codex status` to verify loading
5. **Document rollback**: Add rollback instructions to commit message

### Verification Commands
```bash
# Test configuration loading
/codex status

# Verify no agent references in output
/codex status | grep -i "agent"

# Confirm backup branch exists
git branch | grep swift-agents-backup
```

## Definition of Done
- ✅ Swift agents configuration section commented out with clear reasoning
- ✅ `/codex status` command executes successfully
- ✅ Backup branch `swift-agents-backup` created and verified
- ✅ Configuration follows existing commenting patterns
- ✅ No errors in CODEX configuration loading
- ✅ Documentation includes rollback instructions

**Story Risk Assessment:**
- **Primary Risk:** Breaking CODEX configuration loading
- **Mitigation:** Test configuration loading immediately after changes
- **Rollback:** Switch back to `swift-agents-backup` branch

---

# Story 2: Workflow Simplification and Command-Based Validation

**Story ID**: STORY-SWIFT-002
**Priority**: P0 (Core workflow changes)
**Estimated Effort**: 4-5 hours
**Dependencies**: Story 1 (Configuration backup must exist)

## User Story
As a **CODEX developer**,
I want **greenfield Swift workflow to use command-based validation instead of agent coordination**,
So that **the workflow completes without agent dependencies while maintaining validation quality**.

## Story Context

**Existing System Integration:**
- Integrates with: Greenfield Swift workflow system, validation gate framework
- Technology: YAML workflow definitions, bash command execution, Swift tooling
- Follows pattern: Multi-level validation gates with configurable commands
- Touch points: Workflow execution, validation orchestration, agent coordination patterns

## Acceptance Criteria

### Functional Requirements
1. **Workflow Modification**: `.codex/workflows/greenfield-swift.yaml` modified to remove agent coordination references
2. **Validation Replacement**: Level 4 validation replaced with Swift tooling commands (swift build, swift test, swiftlint, swift-format)
3. **Documentation Update**: `.codex/tasks/validation-gate.md` updated with command-based Level 4 validation approach

### Integration Requirements
4. **Phase Preservation**: Existing workflow phase structure (Discovery → Analyst → PM → Architect → PRP Creator → Implementation) continues unchanged
5. **Pattern Consistency**: New validation approach follows existing command-based validation pattern from Levels 1-3
6. **Agent Simplification**: Integration with `dev` agent coordination maintains simplified direct implementation pattern

### Quality Requirements
7. **Structure Preservation**: Workflow changes preserve existing YAML structure and phase definitions
8. **Error Reporting**: Command-based validation provides meaningful error reporting
9. **Regression Protection**: No regression in Levels 1-3 validation functionality verified

## Technical Implementation

### File 1: `.codex/workflows/greenfield-swift.yaml`

#### Section 1 - Language Support (Lines 23-33)
**Before:**
```yaml
language_support:
  primary: "swift"
  agents:
    - swift-feature-developer
    - swift-syntax-reviewer
    - swift-architecture-reviewer
    - swift-performance-reviewer
    - swift-testing-reviewer
    - swift-refactor
    - ios-security-auditor
```

**After:**
```yaml
language_support:
  primary: "swift"
  # agents: []  # DISABLED - temporarily removed for development simplification
  # Swift agents will be re-integrated in future release
  validation_method: "command_based"
  tooling:
    - swift build
    - swift test
    - swiftlint
    - swift-format
```

#### Section 2 - Implementation Coordination (Lines 136-182)
**Before:**
```yaml
- phase: implementation_coordination
  primary_agent: dev
  language_agents:
    swift-feature-developer:
      role: "Feature implementation and Swift best practices"
      coordination_method: "parallel_execution"
    swift-refactor:
      role: "Code quality and refactoring guidance"
      coordination_method: "review_handoff"
```

**After:**
```yaml
- phase: implementation_coordination
  primary_agent: dev
  description: "Direct implementation without language agent coordination"
  # language_agents: []  # DISABLED - direct implementation only

  coordination:
    - agent: dev
      action: prp_execution_prep
      description: "Prepare enhanced PRP for implementation"
      validates: ["prp_context_completeness", "referenced_files_exist", "validation_commands_tested"]

    - agent: dev
      action: direct_implementation
      description: "Direct feature implementation following Swift best practices"
      tasks: ["core_feature_implementation", "test_generation", "documentation_creation"]
      coordination_method: "direct_execution"

    - agent: dev
      action: validation_orchestration
      description: "Execute all 4 validation levels with command-based validation"
      executes: ["level_1_validation", "level_2_validation", "level_3_validation", "level_4_validation"]
      requires: "implementation_complete"
```

#### Section 3 - Level 4 Validation (Lines 211-217)
**Before:**
```yaml
level_4:
  name: "Domain-Specific Language Validation"
  agents:
    - swift-syntax-reviewer
    - swift-architecture-reviewer
    - swift-performance-reviewer
  custom_validation: true
  required: true
  timeout: 600
```

**After:**
```yaml
level_4:
  name: "Command-Based Domain Validation"
  commands:
    - "swift build --configuration Release"
    - "swift test --parallel --enable-code-coverage"
    - "swiftlint --strict --reporter json"
    - "swift-format --lint --recursive Sources/"
  # agents: []  # DISABLED - using command-based validation
  custom_validation: false
  required: true
  timeout: 600
```

### File 2: `.codex/tasks/validation-gate.md`

#### Level 4 Validation Section (Lines 460-528)
**Replace existing agent-based approach with:**

```markdown
## Level 4: Command-Based Domain Validation

### Purpose: Swift Tooling Validation

Leverage Swift development tools for domain-specific validation without agent coordination complexity.

### Execution Strategy

```yaml
level_4_execution:
  trigger: "after_all_previous_levels_pass"
  timeout: 600  # seconds (10 minutes)
  required: true
  coordination_method: "command_based"  # No agent coordination

  validation_sequence:
    1_release_build_validation:
      - purpose: "Verify release configuration builds successfully"
      - blocking: true

    2_comprehensive_testing:
      - purpose: "Run all tests with coverage in release mode"
      - coverage_threshold: 80
      - blocking: true

    3_style_enforcement:
      - purpose: "Strict style and formatting compliance"
      - auto_fix: false
      - blocking: true

    4_swift_package_validation:
      - purpose: "Validate package structure and dependencies"
      - blocking: true
```

### Command-Based Validation

```bash
# Swift Release Build Validation
swift build --configuration Release -v 2>&1 | tee .codex/state/release-build.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Release build failed"
    grep -A 5 -B 5 "error:" .codex/state/release-build.log
    exit 1
fi

# Comprehensive Test Suite with Coverage
swift test --configuration Release --enable-code-coverage --parallel 2>&1 | tee .codex/state/release-tests.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Release tests failed"
    exit 1
fi

# Strict Style Enforcement
swiftlint --strict --reporter json --config .swiftlint.yml > .codex/state/strict-lint.json
if [ $(cat .codex/state/strict-lint.json | jq 'length') -gt 0 ]; then
    echo "❌ Level 4 FAILED: Strict linting violations"
    cat .codex/state/strict-lint.json | jq -r '.[] | "VIOLATION: \(.rule) at \(.file):\(.line) - \(.reason)"'
    exit 1
fi

# Swift Package Validation
swift package resolve 2>&1 | tee .codex/state/package-resolve.log
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Level 4 FAILED: Package resolution failed"
    exit 1
fi

echo "✅ Level 4 PASSED: Command-based domain validation complete"
```
```

### File 3: `.codex/agents/dev.md`

#### Language Agent Integration Section (Lines 145-158)
**Before:**
```yaml
implementation-methods:
  - PRP pattern application
  - Test-driven development when applicable
  - Language agent parallel coordination
  - Progressive validation at each level

language-agent-integration:
  swift:
    - swift-feature-developer: Feature implementation
    - swift-refactor: Code quality and optimization
    - swift-syntax-reviewer: Modern syntax patterns
    - swift-architecture-reviewer: Design pattern compliance
```

**After:**
```yaml
implementation-methods:
  - PRP pattern application
  - Test-driven development when applicable
  # - Language agent parallel coordination  # DISABLED
  - Progressive validation at each level
  - Context checkpoint management
  - Quality gate enforcement
  - Direct implementation with tooling validation

# language-agent-integration:  # DISABLED - temporarily removed
#   swift:
#     - swift-feature-developer: Feature implementation
#     - swift-refactor: Code quality and optimization
#     - swift-syntax-reviewer: Modern syntax patterns
#     - swift-architecture-reviewer: Design pattern compliance

coordination-pattern: |
  Direct implementation approach:
  1. Read enhanced PRP for complete context
  2. Implement following PRP specifications
  3. Use Swift tooling for validation
  4. Progress through 4-level validation gates
  5. Document implementation decisions
```

## Verification Testing

### Test Workflow Initialization
```bash
# Test workflow loading
/codex start greenfield-swift test-project

# Verify workflow phases load correctly
/codex status | grep -A 10 "workflow phases"

# Test validation gate configuration
/codex validate --dry-run
```

### Test Command-Based Validation
```bash
# Create minimal Swift project for testing
mkdir -p test-swift-project/Sources/TestProject
echo 'print("Hello, World!")' > test-swift-project/Sources/TestProject/main.swift

# Test Level 4 validation commands
cd test-swift-project
swift build --configuration Release
swift test --parallel --enable-code-coverage
```

## Definition of Done
- ✅ `greenfield-swift.yaml` updated with disabled agent coordination sections
- ✅ Level 4 validation uses Swift tooling commands exclusively
- ✅ `validation-gate.md` includes comprehensive command-based validation approach
- ✅ `dev.md` agent coordination patterns simplified to direct implementation
- ✅ Workflow structure maintains existing phase progression
- ✅ Test workflow execution completes without agent coordination failures

**Story Risk Assessment:**
- **Primary Risk:** Breaking workflow execution or validation effectiveness
- **Mitigation:** Test each modified file separately, maintain existing workflow structure
- **Rollback:** Restore original files from `swift-agents-backup` branch

---

# Story 3: Documentation Updates and Generic Workflow Foundation

**Story ID**: STORY-SWIFT-003
**Priority**: P1 (Documentation and future-proofing)
**Estimated Effort**: 2-4 hours
**Dependencies**: Story 2 (Workflow changes must be tested)

## User Story
As a **CODEX developer and future contributor**,
I want **documentation updated to reflect simplified architecture and a generic workflow template created**,
So that **the system is properly documented and can support multiple languages without agent dependencies**.

## Story Context

**Existing System Integration:**
- Integrates with: Documentation system, workflow template framework
- Technology: Markdown documentation, YAML workflow templates
- Follows pattern: Comprehensive documentation with template-based workflow creation
- Touch points: Project documentation, workflow template system, user guides

## Acceptance Criteria

### Functional Requirements
1. **Documentation Updates**: All documentation files updated to remove Swift agent references and reflect command-based approach
2. **Generic Workflow**: New `greenfield-generic.yaml` workflow template created for language-agnostic development
3. **End-to-End Testing**: Complete workflow test executed successfully with simplified architecture

### Integration Requirements
4. **Structure Preservation**: Existing documentation structure and navigation continues to work unchanged
5. **Template Consistency**: New generic workflow follows existing greenfield workflow template pattern
6. **Workflow Selection**: Integration with workflow selection system supports both Swift and generic workflows

### Quality Requirements
7. **Documentation Standards**: Documentation changes maintain consistency with existing style and structure
8. **Template Guidance**: Generic workflow template includes comprehensive language customization guidance
9. **Regression Protection**: No regression in workflow discovery and selection functionality verified

## Technical Implementation

### Documentation Files to Update

#### File 1: `docs/prd.md`
**Updates Required:**
- Replace "Swift language agent coordination" with "command-based validation"
- Update Level 4 validation description
- Remove agent dependency requirements
- Add generic workflow support mention

**Section**: Level 4 Validation Requirements
**Change**:
```markdown
# Before
Level 4 validation leverages specialized Swift agents for comprehensive domain validation

# After
Level 4 validation leverages Swift development tooling for comprehensive domain validation
```

#### File 2: `docs/codex-architecture.md`
**Updates Required:**
- Update architecture diagrams to remove agent coordination
- Simplify validation flow descriptions
- Add command-based validation architecture
- Update workflow selection architecture

**Section**: Validation Architecture
**Change**:
```markdown
# Before
Agent Coordination Layer:
- Swift-specific language agents
- Parallel execution coordination
- Agent handoff protocols

# After
Validation Layer:
- Command-based validation execution
- Swift tooling integration
- Direct feedback mechanisms
```

#### File 3: `docs/brief.md`
**Updates Required:**
- Remove Swift agent mentions from project description
- Update technology stack section
- Clarify command-based approach
- Add generic workflow capabilities

#### File 4: `docs/CODEX-User-Guide.md`
**Updates Required:**
- Update workflow selection instructions
- Remove agent troubleshooting sections
- Add command-based validation guidance
- Update workflow customization instructions

#### File 5: `PRPs/codex-orchestration-system.md`
**Updates Required:**
- Update implementation requirements
- Remove agent coordination specifications
- Add command-based validation requirements
- Update testing requirements

### Generic Workflow Template

#### File: `.codex/workflows/greenfield-generic.yaml`

**Create new file with:**

```yaml
# CODEX Generic Workflow Template
# Language-agnostic development workflow for any programming language
# Customize validation commands and language-specific settings per project

workflow_id: "greenfield-generic"
version: "1.0"
description: "Generic development workflow supporting any programming language"
language_agnostic: true

# Language Configuration - Customize per project
language_support:
  primary: "{{LANGUAGE}}"  # Set to: javascript, python, go, rust, etc.
  framework: "{{FRAMEWORK}}"  # Set to: react, django, gin, actix, etc.
  validation_method: "command_based"

  # Customize these commands for your language/framework
  tooling:
    - "{{BUILD_COMMAND}}"     # e.g., npm run build, cargo build, go build
    - "{{TEST_COMMAND}}"      # e.g., npm test, cargo test, go test
    - "{{LINT_COMMAND}}"      # e.g., eslint, clippy, golangci-lint
    - "{{FORMAT_COMMAND}}"    # e.g., prettier, rustfmt, gofmt

# Project Discovery Phase
phases:
  - phase: project_discovery
    agent: discovery
    description: "Analyze existing codebase and identify enhancement requirements"
    outputs: ["project-analysis.md", "enhancement-requirements.md"]

  - phase: requirements_analysis
    agent: analyst
    description: "Create detailed requirements and technical constraints"
    outputs: ["technical-requirements.md", "integration-analysis.md"]

  - phase: product_management
    agent: pm
    description: "Create PRD with user stories and acceptance criteria"
    outputs: ["prd.md", "user-stories.md"]

  - phase: architecture_design
    agent: architect
    description: "Design system architecture and integration approach"
    outputs: ["architecture.md", "implementation-plan.md"]

  - phase: prp_creation
    agent: prp-creator
    description: "Generate enhanced PRP for implementation"
    outputs: ["enhanced-prp.md"]

  - phase: implementation
    agent: dev
    description: "Execute implementation following PRP specifications"
    coordination_method: "direct_execution"

# Validation Gates - Customize commands per language
validation_gates:
  level_1:
    name: "Syntax and Basic Validation"
    commands:
      - "{{SYNTAX_CHECK}}"      # e.g., node --check, python -m py_compile
    required: true
    timeout: 60

  level_2:
    name: "Unit Testing"
    commands:
      - "{{UNIT_TEST_COMMAND}}"  # e.g., npm run test:unit, cargo test --lib
    required: true
    timeout: 300

  level_3:
    name: "Integration Testing"
    commands:
      - "{{INTEGRATION_TEST}}"   # e.g., npm run test:integration
    required: true
    timeout: 600

  level_4:
    name: "Language-Specific Domain Validation"
    commands:
      - "{{BUILD_RELEASE}}"      # e.g., npm run build:prod, cargo build --release
      - "{{FULL_TEST_SUITE}}"    # e.g., npm run test:all, cargo test --all
      - "{{STRICT_LINT}}"        # e.g., eslint --max-warnings 0
      - "{{FORMAT_CHECK}}"       # e.g., prettier --check, rustfmt --check
    required: true
    timeout: 900

# Language-Specific Customization Examples
customization_examples:
  javascript:
    language: "javascript"
    framework: "react"
    commands:
      build: "npm run build"
      test: "npm test"
      lint: "eslint src/"
      format: "prettier --check src/"

  python:
    language: "python"
    framework: "django"
    commands:
      build: "python -m py_compile ."
      test: "python -m pytest"
      lint: "flake8 ."
      format: "black --check ."

  go:
    language: "go"
    framework: "gin"
    commands:
      build: "go build ./..."
      test: "go test ./..."
      lint: "golangci-lint run"
      format: "gofmt -d ."

  rust:
    language: "rust"
    framework: "actix"
    commands:
      build: "cargo build --release"
      test: "cargo test"
      lint: "cargo clippy -- -D warnings"
      format: "cargo fmt -- --check"

# Documentation Requirements
documentation:
  required_files:
    - "README.md"
    - "docs/architecture.md"
    - "docs/api-documentation.md"
  optional_files:
    - "docs/deployment.md"
    - "docs/contributing.md"

# Quality Gates
quality_requirements:
  code_coverage: 80  # Minimum percentage
  performance_budget: "{{PERFORMANCE_THRESHOLD}}"  # Language-specific
  security_scan: true
  dependency_audit: true
```

### Documentation Customization Guide

#### File: `docs/workflow-customization-guide.md`

**Create new file with:**

```markdown
# CODEX Workflow Customization Guide

## Generic Workflow Setup

The `greenfield-generic.yaml` workflow provides a foundation for any programming language. Follow these steps to customize it for your project:

### 1. Language Configuration

Replace placeholders in the workflow file:

```yaml
# Set your primary language
primary: "python"  # javascript, go, rust, etc.

# Set your framework (optional)
framework: "django"  # react, gin, actix, etc.
```

### 2. Command Customization

Update validation commands for your tech stack:

```yaml
tooling:
  - "python -m py_compile ."  # Build/compile command
  - "python -m pytest"        # Test command
  - "flake8 ."               # Lint command
  - "black --check ."        # Format command
```

### 3. Validation Gate Setup

Customize each validation level:

- **Level 1**: Basic syntax checking
- **Level 2**: Unit tests
- **Level 3**: Integration tests
- **Level 4**: Full validation suite

### 4. Language Examples

The workflow includes examples for:
- JavaScript/React
- Python/Django
- Go/Gin
- Rust/Actix

Copy the relevant example and modify for your specific needs.

### 5. Creating Language-Specific Workflows

For frequently used languages, create dedicated workflow files:

1. Copy `greenfield-generic.yaml`
2. Name it `greenfield-{language}.yaml`
3. Remove placeholders and add language-specific configurations
4. Add to workflow selection system

## Supported Languages

Currently tested with:
- Swift (existing)
- JavaScript/TypeScript
- Python
- Go
- Rust

Additional languages can be added by following the customization pattern.
```

## Verification Testing

### End-to-End Workflow Test
```bash
# Test workflow discovery
/codex list-workflows

# Test generic workflow initialization
/codex start greenfield-generic test-project

# Test workflow selection shows both options
/codex list-workflows | grep -E "(swift|generic)"

# Test documentation accessibility
find docs/ -name "*.md" -exec grep -l "command-based" {} \;
```

### Documentation Consistency Check
```bash
# Check for remaining agent references
grep -r "swift.*agent" docs/ --exclude="*epic*" --exclude="*analysis*"

# Verify generic workflow template
cat .codex/workflows/greenfield-generic.yaml | grep -E "(LANGUAGE|COMMAND)"

# Test workflow template validation
/codex validate-workflow greenfield-generic
```

## Definition of Done
- ✅ All documentation files updated to reflect simplified command-based architecture
- ✅ `greenfield-generic.yaml` created with language-agnostic workflow phases
- ✅ Generic workflow includes configurable validation commands and language detection
- ✅ Documentation includes guidance for customizing generic workflow per language
- ✅ End-to-end Swift workflow test completes successfully
- ✅ Workflow selection system recognizes both Swift and generic workflow options
- ✅ Workflow customization guide provides clear language-specific examples

**Story Risk Assessment:**
- **Primary Risk:** Documentation inconsistencies or breaking workflow template system
- **Mitigation:** Update documentation systematically, test workflow selection after changes
- **Rollback:** Restore documentation files from `swift-agents-backup` branch

---

# Epic Implementation Guide

## Prerequisites
1. **CODEX System**: Functional CODEX installation
2. **Git Repository**: Clean working directory with commit access
3. **Swift Environment**: Swift tooling available for validation testing
4. **Backup Strategy**: Understanding of git branch rollback procedures

## Implementation Sequence

### Phase 1: Preparation and Safety (Story 1)
1. **Create backup branch**: `git checkout -b swift-agents-backup`
2. **Document current state**: Record current workflow functionality
3. **Disable agent configuration**: Modify `.codex/config/codex-config.yaml`
4. **Verify configuration**: Test `/codex status` passes

**Success Criteria**: CODEX loads without agent-related errors

### Phase 2: Core Workflow Changes (Story 2)
1. **Modify workflow file**: Update `.codex/workflows/greenfield-swift.yaml`
2. **Update validation gates**: Modify `.codex/tasks/validation-gate.md`
3. **Simplify dev agent**: Update `.codex/agents/dev.md`
4. **Test workflow execution**: Verify workflow initialization works

**Success Criteria**: Workflow executes without agent coordination failures

### Phase 3: Documentation and Future-Proofing (Story 3)
1. **Update all documentation**: Remove agent references systematically
2. **Create generic workflow**: Add `.codex/workflows/greenfield-generic.yaml`
3. **Add customization guide**: Create workflow customization documentation
4. **Test complete system**: Run end-to-end workflow validation

**Success Criteria**: Complete system documentation and workflow options available

## Testing Strategy

### Regression Testing
- Core CODEX functionality verification
- Workflow phase progression testing
- Document generation validation
- Configuration loading verification

### Integration Testing
- Swift project workflow execution
- Validation gate command execution
- Error reporting and logging
- Rollback procedure verification

### Performance Testing
- Workflow execution time comparison
- Debugging session efficiency
- Development velocity measurement

## Rollback Procedures

### Emergency Rollback (Any Point)
```bash
git checkout swift-agents-backup
/codex status  # Verify system restoration
```

### Selective Rollback (Per Story)
```bash
# Story 1 rollback
git checkout swift-agents-backup -- .codex/config/codex-config.yaml

# Story 2 rollback
git checkout swift-agents-backup -- .codex/workflows/greenfield-swift.yaml
git checkout swift-agents-backup -- .codex/tasks/validation-gate.md
git checkout swift-agents-backup -- .codex/agents/dev.md

# Story 3 rollback
git checkout swift-agents-backup -- docs/
rm .codex/workflows/greenfield-generic.yaml
```

## Success Metrics

### Quantitative Metrics
- **Configuration Load Time**: Should remain constant or improve
- **Workflow Execution Time**: Should improve due to reduced coordination overhead
- **Error Resolution Time**: Should improve due to simplified debugging
- **Development Session Productivity**: Should increase

### Qualitative Metrics
- **Developer Experience**: Simplified debugging and clearer error messages
- **System Reliability**: Reduced failure points and coordination issues
- **Documentation Quality**: Clear, consistent documentation reflecting actual system behavior
- **Future Maintainability**: Foundation for multi-language support

## Post-Implementation Tasks

### Immediate (Week 1)
- [ ] Monitor system stability
- [ ] Collect developer feedback
- [ ] Measure performance improvements
- [ ] Document any discovered issues

### Short-term (Month 1)
- [ ] Refine command-based validation based on usage
- [ ] Add additional language support to generic workflow
- [ ] Optimize workflow execution performance
- [ ] Create additional customization examples

### Long-term (Quarter 1)
- [ ] Design future agent integration architecture
- [ ] Evaluate re-introduction of agents as optional enhancements
- [ ] Expand generic workflow to support more languages
- [ ] Create comprehensive workflow testing framework

---

## Appendix: File Change Summary

### Configuration Changes
- `.codex/config/codex-config.yaml`: Comment out swift_agents section

### Workflow Changes
- `.codex/workflows/greenfield-swift.yaml`: Remove agent coordination, add command-based validation
- `.codex/tasks/validation-gate.md`: Replace Level 4 agent validation with command execution
- `.codex/agents/dev.md`: Simplify coordination patterns

### Documentation Changes
- `docs/prd.md`: Update validation descriptions
- `docs/codex-architecture.md`: Simplify architecture diagrams
- `docs/brief.md`: Remove agent dependencies
- `docs/CODEX-User-Guide.md`: Update workflow instructions
- `PRPs/codex-orchestration-system.md`: Update implementation requirements

### New Files
- `.codex/workflows/greenfield-generic.yaml`: Language-agnostic workflow template
- `docs/workflow-customization-guide.md`: Generic workflow setup guide

---

**Epic Status**: ✅ **READY FOR IMPLEMENTATION**

This comprehensive epic provides a complete roadmap for safely removing Swift agent dependencies while maintaining CODEX functionality and laying the foundation for future multi-language support.