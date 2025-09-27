# CODEX Agent Architecture Specification

## Overview

CODEX (Context Oriented Development and Engineering Experience) Protocol is a complete replacement for BMAD that integrates the proven PRP (Product Requirements Prompt) methodology with enhanced workflow orchestration, zero prior knowledge context management, and command-based validation with language-specific tooling.

## Core Architecture Principles

### 1. Zero Prior Knowledge Architecture
- Every workflow phase produces a complete, standalone artifact that enables fresh Claude instances to continue work
- Enhanced PRP creation with systematic validation using the "No Prior Knowledge" test
- Strategic context breakpoints prevent context window overflow while maintaining complete handoff capability
- All documents pass rigorous completeness validation before phase transitions

### 2. Proven Workflow Orchestration
- Builds upon BMAD's successful agent coordination patterns
- YAML-driven workflow definitions with clear agent handoffs
- Template-driven document generation with interactive elicitation
- Progressive validation gates ensure quality at each phase

### 3. Integrated PRP Enhancement
- PRP creation is seamlessly integrated into the workflow after architecture phase
- Enhanced PRP templates with systematic context completeness validation
- Automatic integration of research findings from workflow agents
- 4-level validation system (syntax/style, unit tests, integration, creative) built into execution

### 4. Language-Specific Command-Based Validation
- Direct execution of language tooling (swift build, swift test, swiftlint, etc.)
- Standardized command execution protocols for validation
- Efficient execution capabilities for independent validation tasks
- Quality feedback loops between tooling validation and PRP execution

## Directory Structure

```
.codex/
├── agents/                          # CODEX workflow agents (BMAD replacement)
│   ├── analyst.md                   # Business analysis and research
│   ├── architect.md                 # Technical architecture design
│   ├── pm.md                        # Product management and PRD creation
│   ├── prp-creator.md               # Enhanced PRP generation from PRD + Architecture
│   ├── dev.md                       # Development coordination and execution
│   ├── qa.md                        # Quality assurance and validation
│   └── orchestrator.md              # Main workflow orchestrator
├── workflows/                       # Workflow definitions (YAML-driven)
│   ├── greenfield-swift.yaml        # Swift iOS/macOS project workflow
│   ├── greenfield-fullstack.yaml    # Full-stack web application workflow
│   ├── brownfield-enhancement.yaml  # Adding features to existing projects
│   └── custom-workflow.yaml         # User-defined workflow patterns
├── templates/                       # Document and PRP templates
│   ├── project-brief-template.yaml  # Enhanced project brief generation
│   ├── prd-template.yaml           # Product requirements document
│   ├── architecture-template.yaml   # Architecture specification
│   ├── prp-enhanced-template.md     # Enhanced PRP with zero knowledge validation
│   └── validation-checklist.yaml   # Quality gate validations
├── tasks/                          # Workflow task definitions
│   ├── create-doc.md               # Template-driven document creation (from BMAD)
│   ├── context-handoff.md          # Context breakpoint management
│   ├── prp-quality-check.md        # PRP completeness validation
│   ├── language-agent-coord.md     # Multi-agent coordination
│   └── validation-gate.md          # 4-level validation execution
├── state/                          # Workflow state management
│   ├── current-workflow.json       # Active workflow tracking
│   ├── phase-status.json           # Workflow phase completion status
│   ├── context-checkpoints.json    # Context breakpoint validation records
│   └── agent-coordination.json     # Language agent execution status
├── config/                         # Configuration and settings
│   ├── codex-config.yaml          # Main CODEX configuration
│   ├── workflow-patterns.yaml     # Standard workflow definitions
│   └── language-agents.yaml       # Global agent integration settings
├── data/                           # Shared data and knowledge
│   ├── elicitation-methods.md      # Interactive elicitation techniques (from BMAD)
│   ├── codex-kb.md                 # CODEX knowledge base and patterns
│   └── prp-patterns.md             # Successful PRP patterns and examples
└── utils/                          # Shared utilities
    ├── zero-knowledge-validator.md  # "No Prior Knowledge" test executor
    ├── workflow-executor.md         # YAML workflow interpreter
    └── prp-enhancer.md             # PRP quality enhancement utilities
```

## Complete CODEX Workflow

### Phase 1: Research and Analysis
**Agent:** `analyst.md`
**Input:** Project concept or requirements
**Output:** `docs/project-brief.md`

**Process:**
- Interactive elicitation using BMAD's proven 1-9 option format
- Market research and competitive analysis
- Stakeholder requirement gathering
- Business case development with measurable goals

**Zero Knowledge Validation:**
- Project brief contains complete context for PM to create PRD
- All research findings documented with specific references
- Business requirements clearly articulated with success criteria

### Phase 2: Product Requirements Definition
**Agent:** `pm.md`
**Input:** `docs/project-brief.md`
**Output:** `docs/prd.md`

**Process:**
- Transform project brief into detailed product requirements
- Define features, user stories, and acceptance criteria
- Establish scope boundaries and MVP definition
- Create implementation priority and dependency mapping

**Enhancement for CODEX:**
- PRD sections specifically designed to feed into enhanced PRP creation
- Technical requirements with sufficient detail for architecture design
- User stories with complete acceptance criteria for implementation

### Phase 3: Architecture Design
**Agent:** `architect.md`
**Input:** `docs/prd.md`
**Output:** `docs/architecture.md`

**Process:**
- Design system architecture based on requirements
- Define technology stack and integration patterns
- Establish coding standards and development conventions
- Create file structure and module organization plans

**Enhancement for CODEX:**
- Architecture document includes specific patterns and examples for PRP context
- File structure with exact paths and naming conventions
- Technology-specific implementation guidance
- Integration patterns with code examples

### Phase 4: Enhanced PRP Creation
**Agent:** `prp-creator.md`
**Input:** `docs/prd.md` + `docs/architecture.md`
**Output:** `PRPs/{feature-name}.md`

**Process:**
1. **Context Synthesis:**
   - Combine PRD requirements with architecture design
   - Gather codebase patterns and existing implementations
   - Research technology-specific best practices and documentation

2. **Enhanced PRP Generation:**
   - Use enhanced PRP template with zero knowledge validation
   - Include comprehensive context from workflow phases
   - Add specific file patterns, naming conventions, and implementation guidance
   - Integrate architecture decisions and technology constraints

3. **Quality Validation:**
   - Apply "No Prior Knowledge" test rigorously
   - Validate all URL references and file patterns
   - Ensure implementation tasks are dependency-ordered and specific
   - Verify 4-level validation commands are project-appropriate

**Enhanced PRP Template Structure:**
```markdown
## Goal
**Feature Goal**: [From PRD - specific, measurable]
**Deliverable**: [From Architecture - concrete implementation]
**Success Definition**: [Combined from PRD acceptance criteria]

## Context from Workflow (Zero Knowledge Section)
**Project Brief Summary**: [Key business context]
**PRD Feature Details**: [Complete feature specification]
**Architecture Decisions**: [Relevant technical decisions and patterns]
**Technology Stack**: [Complete stack with versions and configuration]

## All Needed Context
### Workflow-Generated Context
```yaml
# Documentation from workflow phases
- file: docs/architecture.md
  section: "File Structure"
  why: "Exact placement and naming conventions"

- file: docs/architecture.md
  section: "Coding Standards"
  why: "Project-specific patterns and conventions"

# Research findings
- url: [specific_technology_docs_with_anchors]
  why: [specific_implementation_patterns_needed]
  research_by: "architect_agent"
```

### Codebase Intelligence
[Current and desired codebase trees]
[Known gotchas specific to this project]
[Library quirks and constraints]

## Implementation Blueprint
[Enhanced task sequence with workflow intelligence]
[Integration with architecture patterns]
[Language-specific implementation guidance]

## Validation Loop
### Level 1-4 Validation System
[Project-specific validation commands]
[Progressive quality gates]
[Language agent coordination points]

## Final Validation Checklist
[Comprehensive validation combining PRD acceptance criteria with architecture compliance]
```

### Phase 5: Implementation with Language Agent Coordination
**Agent:** `dev.md` + Language-Specific Agents
**Input:** Enhanced PRP
**Output:** Validated implementation

**Process:**
1. **PRP Execution Preparation:**
   - Load enhanced PRP with complete workflow context
   - Verify all referenced files and patterns exist
   - Validate context completeness using zero knowledge test

2. **Coordinated Implementation:**
   - Execute PRP using proven execution process
   - Coordinate with language-specific agents for enhancements:
     - `swift-feature-developer` for complete feature implementation
     - `swift-syntax-reviewer` for code quality and modern patterns
     - `swift-architecture-reviewer` for architecture compliance
     - `swift-performance-reviewer` for optimization
     - `swift-security-auditor` for security validation

3. **Progressive Validation:**
   - **Level 1**: Syntax & Style (immediate feedback)
   - **Level 2**: Unit Tests (component validation)
   - **Level 3**: Integration Testing (system validation)
   - **Level 4**: Creative & Domain-Specific Validation (enhanced by language agents)

4. **Quality Gate Validation:**
   - Verify all PRD acceptance criteria met
   - Confirm architecture compliance
   - Validate zero knowledge handoff capability

## Agent Specifications

### Workflow Agents (BMAD Replacement)

#### 1. Orchestrator Agent (`orchestrator.md`)
**Role:** Central workflow coordinator replacing BMAD's distributed approach

**Key Capabilities:**
- Parse and execute YAML workflow definitions
- Coordinate agent handoffs with context validation
- Manage workflow state and recovery from interruptions
- Handle context breakpoints and fresh instance handoffs

**Commands:**
- `/codex start {workflow-type}` - Initialize workflow
- `/codex continue` - Resume from last checkpoint
- `/codex status` - Show current workflow state
- `/codex validate-handoff` - Test zero knowledge handoff
- `/codex enhance-prp {prp-file}` - Coordinate language agent enhancement

#### 2. PRP Creator Agent (`prp-creator.md`)
**Role:** Enhanced PRP generation integrating workflow intelligence

**Key Capabilities:**
- Synthesize context from project brief, PRD, and architecture documents
- Generate enhanced PRPs with comprehensive zero knowledge context
- Coordinate with language-specific agents for context enrichment
- Apply rigorous quality validation before PRP approval

**Integration Points:**
- Receives structured input from PM and Architect agents
- Coordinates with global language agents for context enhancement
- Produces PRPs that pass the "No Prior Knowledge" test
- Hands off to Dev agent for coordinated implementation

#### 3. Enhanced Dev Agent (`dev.md`)
**Role:** Implementation coordination with language agent orchestration

**Key Capabilities:**
- Execute enhanced PRPs with complete workflow context
- Coordinate parallel execution with language-specific agents
- Manage 4-level validation system with agent feedback integration
- Ensure implementation meets both PRD requirements and architecture standards

**Language Agent Coordination:**
```yaml
coordination_pattern:
  prp_execution:
    primary: dev_agent
    enhancers:
      - swift-feature-developer    # Primary implementation
      - swift-syntax-reviewer      # Code quality enhancement
      - swift-architecture-reviewer # Architecture compliance
      - swift-security-auditor     # Security validation

  validation_gates:
    level_1: dev_agent              # Syntax/style validation
    level_2: dev_agent              # Unit testing
    level_3: dev_agent              # Integration testing
    level_4: language_agents        # Creative/domain validation
```

### Language Agent Integration

#### Global Agent Coordination Protocol
```yaml
language_agent_request:
  workflow_context:
    workflow_id: "codex_workflow_uuid"
    current_phase: "implementation"
    source_documents: ["docs/prd.md", "docs/architecture.md"]
    prp_content: "{{ complete_enhanced_prp }}"

  agent_task:
    agent_id: "swift-feature-developer"
    task_type: "feature_implementation"
    context_type: "enhanced_prp"

  expected_output:
    implementation: "code_files_with_tests"
    quality_feedback: "enhancement_recommendations"
    validation_status: "self_check_results"
    workflow_integration: "handoff_ready_artifacts"
```

#### Enhanced Agent Response Format
```yaml
language_agent_response:
  agent_id: "swift-feature-developer"
  workflow_id: "codex_workflow_uuid"

  implementation:
    files: [{ path, content, purpose, dependencies }]
    tests: [{ path, content, coverage_area }]
    documentation: "implementation_decisions_and_patterns"

  quality_metrics:
    architecture_compliance: "passed" | "passed_with_notes" | "failed"
    performance_assessment: "optimized" | "acceptable" | "needs_improvement"
    security_validation: "secure" | "minor_issues" | "major_concerns"

  workflow_handoff:
    zero_knowledge_ready: true | false
    context_completeness: "validation_notes"
    next_phase_recommendations: "guidance_for_qa_or_next_steps"

  enhancement_contributions:
    patterns_learned: "new_patterns_for_future_prps"
    gotchas_discovered: "project_specific_constraints_found"
    recommendations: "suggested_improvements_for_architecture"
```

## Workflow Definition (YAML-Driven)

### Enhanced Greenfield Swift Workflow
```yaml
# .codex/workflows/greenfield-swift.yaml
workflow:
  id: greenfield-swift-ios
  name: "Greenfield Swift iOS/macOS Application Development"
  description: "Complete workflow from concept to validated implementation for Swift projects"

  context_management:
    breakpoint_strategy: "document_driven"
    validation_required: "zero_knowledge_test"
    max_context_per_phase: 45000  # tokens

  language_support:
    primary: "swift"
    agents: ["swift-feature-developer", "swift-syntax-reviewer", "swift-architecture-reviewer", "swift-performance-reviewer", "swift-testing-reviewer", "swift-refactor", "ios-security-auditor"]

  sequence:
    - agent: analyst
      creates: "docs/project-brief.md"
      template: "project-brief-template.yaml"
      validation:
        - context_completeness_for_pm: true
        - business_case_clarity: true
        - target_user_definition: true

    - agent: pm
      creates: "docs/prd.md"
      template: "prd-template.yaml"
      requires: ["docs/project-brief.md"]
      validation:
        - feature_specifications_complete: true
        - acceptance_criteria_measurable: true
        - architecture_input_sufficient: true

    - agent: architect
      creates: "docs/architecture.md"
      template: "architecture-template.yaml"
      requires: ["docs/prd.md"]
      enhancements:
        - swift_patterns_research: true
        - ios_architecture_patterns: true
        - technology_stack_validation: true
      validation:
        - implementation_guidance_specific: true
        - swift_conventions_defined: true
        - file_structure_complete: true

    - agent: prp-creator
      creates: "PRPs/{feature-name}.md"
      template: "prp-enhanced-template.md"
      requires: ["docs/prd.md", "docs/architecture.md"]
      enhancements:
        - codebase_pattern_analysis: true
        - swift_documentation_research: true
        - technology_gotchas_identification: true
      validation:
        - zero_knowledge_test: true
        - url_accessibility_check: true
        - implementation_task_specificity: true
        - validation_commands_project_specific: true

    - phase: implementation_coordination
      primary_agent: dev
      language_agents:
        - swift-feature-developer
        - swift-syntax-reviewer
        - swift-architecture-reviewer
        - swift-performance-reviewer
        - ios-security-auditor

      coordination:
        - agent: dev
          action: prp_execution_prep
          validates: ["prp_context_completeness", "referenced_files_exist"]

        - agents: [dev, swift-feature-developer]
          action: parallel_implementation
          tasks: ["core_feature_implementation", "test_generation"]

        - agents: [swift-syntax-reviewer, swift-architecture-reviewer]
          action: quality_enhancement
          input: "implementation_files"
          output: "enhanced_implementation"

        - agent: swift-performance-reviewer
          action: performance_optimization
          condition: "performance_requirements_in_prd"

        - agent: ios-security-auditor
          action: security_validation
          mandatory: true

        - agent: dev
          action: validation_orchestration
          executes: ["level_1_validation", "level_2_validation", "level_3_validation", "level_4_validation"]
          requires: "all_language_agents_complete"

      validation_gates:
        level_1:
          commands: ["swiftlint", "swift build", "swift-format --lint"]
          required: true

        level_2:
          commands: ["swift test", "xcodebuild test"]
          coverage_threshold: 80
          required: true

        level_3:
          commands: ["integration_test_suite", "end_to_end_validation"]
          required: true

        level_4:
          agents: ["swift-performance-reviewer", "ios-security-auditor"]
          custom_validation: true
          required: true

      completion_criteria:
        - all_validation_levels_pass: true
        - prd_acceptance_criteria_met: true
        - architecture_compliance_verified: true
        - zero_knowledge_handoff_ready: true

  context_breakpoints:
    after_project_brief:
      validation: "pm_can_create_prd_without_analyst_context"
      checkpoint_file: "docs/project-brief.md"

    after_prd:
      validation: "architect_can_design_without_pm_context"
      checkpoint_file: "docs/prd.md"

    after_architecture:
      validation: "prp_creator_has_complete_technical_context"
      checkpoint_file: "docs/architecture.md"

    after_enhanced_prp:
      validation: "dev_agent_can_implement_without_workflow_context"
      checkpoint_file: "PRPs/{feature-name}.md"

    after_implementation:
      validation: "qa_can_validate_without_implementation_context"
      checkpoint_files: ["implementation_summary.md", "validation_results.md"]

  error_recovery:
    validation_failure:
      strategy: "return_to_source_agent_with_specific_feedback"
      max_iterations: 3

    context_overflow:
      strategy: "create_emergency_breakpoint_with_summary"
      fallback: "manual_context_curation"

    agent_coordination_failure:
      strategy: "sequential_fallback_execution"
      isolation: "execute_problematic_agent_separately"
```

## Context Management and Validation

### Zero Knowledge Validation System

#### Enhanced "No Prior Knowledge" Test
```yaml
validation_criteria:
  document_completeness:
    - all_referenced_files_include_specific_paths_and_patterns: true
    - technical_decisions_include_complete_rationale: true
    - implementation_requirements_specify_exact_acceptance_criteria: true
    - dependencies_list_complete_installation_and_configuration: true

  workflow_context_integration:
    - project_brief_business_context_preserved: true
    - prd_requirements_fully_translated: true
    - architecture_decisions_and_patterns_included: true
    - technology_stack_completely_specified: true

  actionability:
    - fresh_claude_instance_can_execute_without_additional_context: true
    - all_urls_include_specific_sections_not_just_domains: true
    - code_examples_include_complete_runnable_implementations: true
    - error_scenarios_include_specific_troubleshooting_guidance: true

  language_specificity:
    - swift_conventions_explicitly_defined: true
    - ios_specific_patterns_and_constraints_documented: true
    - xcode_project_structure_requirements_clear: true
    - app_store_compliance_considerations_included: true
```

#### Automated Validation Tools
```yaml
validation_tools:
  url_accessibility_checker:
    - verify_all_documentation_urls_are_accessible: true
    - validate_specific_sections_exist: true
    - check_for_404_or_moved_content: true

  file_reference_validator:
    - confirm_all_referenced_files_exist_in_codebase: true
    - validate_patterns_match_actual_implementations: true
    - check_naming_conventions_are_consistent: true

  context_completeness_scorer:
    - measure_information_density_per_token: true
    - identify_generic_references_for_specificity_improvement: true
    - score_actionability_of_implementation_tasks: true

  prp_quality_metrics:
    - zero_knowledge_test_pass_rate: "target: 95%"
    - implementation_success_rate_from_prp: "target: 85%"
    - validation_gate_pass_rate: "target: 90%"
```

## Implementation and Deployment Strategy

### MVP Implementation Order

1. **Core Orchestrator and Workflow Engine**
   - YAML workflow parser and executor
   - Agent coordination system
   - Context breakpoint management

2. **Enhanced PRP Creation System**
   - PRP template with workflow context integration
   - Zero knowledge validation tools
   - Quality gate automation

3. **Swift Language Agent Integration**
   - Coordination protocols with existing swift agents
   - Enhanced communication formats
   - Parallel execution management

4. **Validation and Quality Assurance**
   - 4-level validation system
   - Automated quality metrics
   - Error recovery and retry mechanisms

### Success Metrics and Monitoring

#### Workflow Efficiency Metrics
- **Context Breakpoint Effectiveness:** Average number of breakpoints per feature (target: ≤3)
- **Zero Knowledge Validation Pass Rate:** Percentage of documents passing validation (target: 95%)
- **Agent Coordination Overhead:** Time spent coordinating vs. implementing (target: <20%)
- **Workflow Completion Rate:** Percentage of workflows completing without manual intervention (target: 85%)

#### Quality and Outcome Metrics
- **One-Pass Implementation Success:** Features correctly implemented on first PRP execution (target: 85%)
- **Validation Gate Pass Rate:** Percentage of implementations passing all 4 levels (target: 90%)
- **Language Agent Enhancement Value:** Quality improvement from agent coordination (measurable via code analysis)
- **Context Reusability:** PRPs successfully executed by fresh Claude instances (target: 95%)

#### User Experience Metrics
- **Workflow Learning Curve:** Time to proficiency for new users (target: <2 hours)
- **Error Recovery Success:** Successful resumption after workflow interruption (target: 95%)
- **Developer Satisfaction:** User rating of workflow efficiency and effectiveness (target: 4.5/5)

## Future Enhancement Areas

### Advanced Context Management
- **AI-Powered Context Compression:** Machine learning for optimal information density
- **Dynamic Breakpoint Prediction:** Automatic identification of optimal context boundaries
- **Intelligent Context Pre-loading:** Predictive loading of likely-needed context

### Enhanced Agent Ecosystem
- **Multi-Language Project Support:** Coordinated development across language boundaries
- **Custom Agent Creation Framework:** User-defined specialized agents
- **Agent Performance Learning:** Continuous improvement from validation outcomes

### Enterprise and Team Features
- **Team Workflow Customization:** Organization-specific workflow patterns
- **Audit and Compliance Integration:** Automated compliance validation
- **Performance Analytics Dashboard:** Detailed metrics and optimization recommendations

---

This comprehensive architecture specification provides the complete foundation for implementing CODEX as a unified, intelligent replacement for BMAD that seamlessly integrates enhanced PRP creation and execution with sophisticated language-specific agent coordination, all built on proven workflow orchestration patterns.