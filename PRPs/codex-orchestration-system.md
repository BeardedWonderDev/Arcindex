# CODEX Orchestration System Implementation PRP

## Goal

**Feature Goal**: Implement the CODEX orchestration system as a complete replacement for BMAD, integrating enhanced PRP methodology with intelligent workflow orchestration and language-specific agent coordination to achieve 85% one-pass implementation success rate.

**Deliverable**: Fully functional CODEX system with core orchestrator, workflow engine, enhanced PRP creation, validation gates, and MVP Swift language agent integration.

**Success Definition**: CODEX successfully orchestrates a complete Swift greenfield workflow from project brief to validated implementation, with all documents passing zero-knowledge validation and implementation achieving all 4 validation levels.

## User Persona

**Target User**: Software developers using Claude Code for AI-assisted development

**Use Case**: Developer wants to build a new Swift iOS application with minimal manual coordination between AI agents

**User Journey**:
1. Developer runs `/codex start greenfield-swift` with project idea
2. CODEX orchestrates analyst → PM → architect → PRP creator agents
3. Each phase produces zero-knowledge complete documents
4. Enhanced PRP is generated with full workflow context
5. Implementation executes with language agent coordination
6. Validation gates ensure quality at each level

**Pain Points Addressed**:
- Manual coordination between BMAD and PRP workflows
- Context loss between development phases
- Inconsistent quality without systematic validation
- Token limit constraints breaking complex workflows

## Why

- Replaces fragmented BMAD + PRP workflow with unified orchestration
- Enables context window liberation through strategic breakpoints
- Integrates language-specific agents seamlessly
- Reduces development cycle time by 40%
- Supports complex features (>2000 lines) without context overflow
- Establishes repeatable, standardized AI-assisted development patterns

## What

CODEX provides a single `/codex` command entry point that orchestrates the complete development lifecycle from concept to validated implementation, managing context breakpoints strategically while coordinating with language-specific agents for quality enhancement.

### Success Criteria

- [ ] `/codex` command successfully initializes and creates `.codex/` directory structure
- [ ] Orchestrator agent parses and executes YAML workflow definitions
- [ ] Context breakpoints prevent token overflow while maintaining handoff capability
- [ ] Enhanced PRPs pass "No Prior Knowledge" validation test (95% rate)
- [ ] Language agents coordinate through Task tool for parallel execution
- [ ] 4-level validation system catches issues progressively
- [ ] Workflow state persists and allows resumption from interruption
- [ ] Git commits created at each successful phase completion

## All Needed Context

### Context Completeness Check

_Before implementation: This PRP contains all patterns, examples, and specifications needed for a fresh Claude instance to implement CODEX without prior conversation context._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- file: docs/prd.md
  why: Complete requirements specification with all functional and non-functional requirements
  pattern: Epics 1-3 for MVP implementation scope
  gotcha: Git integration is NFR not MVP, focus on core orchestration first

- file: docs/codex-architecture.md
  why: Detailed technical architecture with agent specifications and workflow definitions
  pattern: Agent coordination protocols and YAML workflow structure
  section: Lines 250-507 for agent specifications, 349-507 for workflow YAML

- file: .bmad-core/agents/bmad-orchestrator.md
  why: Existing BMAD orchestrator pattern to adapt for CODEX
  pattern: YAML agent definition structure, activation instructions, command patterns
  gotcha: CODEX replaces distributed approach with centralized orchestration

- file: .bmad-core/workflows/greenfield-fullstack.yaml
  why: Reference workflow structure to adapt for Swift workflow
  pattern: Sequence definitions, agent handoffs, validation gates
  critical: Note how agents create documents and validate handoffs

- file: .bmad-core/tasks/create-doc.md
  why: Document creation pattern with elicitation and templates
  pattern: Interactive elicitation with 1-9 options, template processing
  gotcha: Elicitation is mandatory when elicit: true in templates

- file: .claude/commands/prp-create.md
  why: Slash command structure for Claude Code commands
  pattern: YAML frontmatter format, $ARGUMENTS usage
  critical: Commands use --- delimited frontmatter with name, description, arguments

- file: PRPs/templates/prp_base.md
  why: Enhanced PRP template structure to integrate with workflow
  pattern: All sections that need workflow context integration
  section: Lines 40-116 for context section, 183-273 for validation levels

- docfile: PRPs/ai_docs/claude-code-slash-commands.md
  why: How to create Claude Code slash commands with proper structure
  section: Command definition format and activation patterns
```

### Current Codebase tree

```bash
.
├── .bmad-core/          # Existing BMAD implementation
│   ├── agents/          # BMAD agent definitions
│   ├── workflows/       # BMAD workflow YAML files
│   ├── tasks/          # BMAD task definitions
│   ├── templates/      # Document templates
│   └── data/           # Knowledge base and methods
├── .claude/            # Claude Code configuration
│   ├── commands/       # Slash command definitions
│   │   └── BMad/      # BMAD commands (to be replaced)
│   └── agents/        # Global agent definitions
├── PRPs/              # PRP system
│   ├── templates/     # PRP templates
│   └── prp-readme.md  # PRP methodology
└── docs/              # Project documentation
    ├── prd.md         # Product requirements
    ├── codex-architecture.md  # Architecture spec
    └── brief.md       # Project brief
```

### Desired Codebase tree with files to be added

```bash
.
├── .codex/                              # NEW: CODEX system root
│   ├── agents/                          # CODEX workflow agents
│   │   ├── orchestrator.md             # Central coordinator (replaces bmad-orchestrator)
│   │   ├── analyst.md                  # Business analysis agent
│   │   ├── pm.md                       # Product management agent
│   │   ├── architect.md                # Architecture design agent
│   │   ├── prp-creator.md              # Enhanced PRP generator
│   │   ├── dev.md                      # Development coordinator
│   │   └── qa.md                       # Quality assurance agent
│   ├── workflows/                       # Workflow definitions
│   │   ├── greenfield-swift.yaml       # Swift iOS/macOS workflow
│   │   └── health-check.yaml           # System validation workflow
│   ├── templates/                       # Document templates
│   │   ├── project-brief-template.yaml # Brief generation
│   │   ├── prd-template.yaml          # PRD template
│   │   ├── architecture-template.yaml  # Architecture template
│   │   └── prp-enhanced-template.md    # Enhanced PRP template
│   ├── tasks/                          # Workflow tasks
│   │   ├── create-doc.md              # Template-driven creation
│   │   ├── context-handoff.md         # Breakpoint management
│   │   ├── prp-quality-check.md       # PRP validation
│   │   └── validation-gate.md         # 4-level validation
│   ├── state/                          # Workflow state
│   │   └── .gitkeep                    # Directory placeholder
│   ├── config/                         # Configuration
│   │   └── codex-config.yaml          # Main configuration
│   └── data/                           # Shared data
│       ├── elicitation-methods.md      # From BMAD
│       └── codex-kb.md                # CODEX patterns
└── .claude/
    └── commands/
        └── codex.md                    # NEW: Main CODEX slash command
```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: Claude Code slash commands use YAML frontmatter
# Format: --- name: command-name \n description: desc \n arguments: args ---
# The $ARGUMENTS variable contains user-provided arguments

# CRITICAL: Agents are markdown files with YAML configuration blocks
# Agents use natural language instructions, not code
# Agent coordination happens through Task tool invocation

# CRITICAL: BMAD uses mandatory elicitation format
# When elicit: true, MUST use 1-9 options and wait for user
# Option 1 is always "Proceed to next section"

# CRITICAL: Context breakpoints need explicit handoff documents
# Each breakpoint must validate with "No Prior Knowledge" test
# Breakpoint documents summarize essential context only

# CRITICAL: Task tool launches agents asynchronously
# Multiple agents launch with single Task message for parallelism
# Agent results return in single completion message
```

## Implementation Blueprint

### Data models and structure

Create the core configuration and state structures:

```yaml
# .codex/config/codex-config.yaml structure
system:
  version: "1.0.0"
  context_limit: 45000  # tokens per phase
  validation_levels: 4
  default_workflow: "greenfield-swift"

workflows:
  available:
    - greenfield-swift
    - health-check

state:
  persistence: ".codex/state/"
  checkpoint_frequency: 600  # seconds

# .codex/state/workflow.json structure
{
  "workflow_id": "uuid",
  "workflow_type": "greenfield-swift",
  "current_phase": "architect",
  "completed_phases": ["analyst", "pm"],
  "documents": {
    "project-brief": "docs/project-brief.md",
    "prd": "docs/prd.md"
  },
  "context_checkpoints": [],
  "last_updated": "ISO timestamp"
}
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE .claude/commands/codex.md
  - IMPLEMENT: Main CODEX slash command with YAML frontmatter
  - FOLLOW pattern: .claude/commands/prp-create.md (frontmatter structure)
  - CONTENT: Command router that handles start, continue, status, validate subcommands
  - NAMING: File must be exactly "codex.md" for /codex command
  - PLACEMENT: .claude/commands/ directory for slash commands

Task 2: CREATE .codex/ directory structure
  - IMPLEMENT: Complete directory tree with all subdirectories
  - CREATE: agents/, workflows/, templates/, tasks/, state/, config/, data/
  - FOLLOW pattern: Directory structure from "Desired Codebase tree"
  - ADD: .gitkeep files in empty directories for git tracking
  - PLACEMENT: Root level .codex/ directory

Task 3: CREATE .codex/agents/orchestrator.md
  - IMPLEMENT: Central orchestrator agent adapting bmad-orchestrator.md
  - FOLLOW pattern: .bmad-core/agents/bmad-orchestrator.md (YAML structure)
  - ADAPT: Commands to use /codex prefix, integrate workflow engine
  - INCLUDE: Activation instructions, persona, commands, help template
  - CRITICAL: Include workflow parsing and state management logic

Task 4: CREATE .codex/config/codex-config.yaml
  - IMPLEMENT: Main configuration file with system settings
  - STRUCTURE: System settings, workflow registry, state configuration
  - FOLLOW pattern: .bmad-core/core-config.yaml structure
  - DEFAULTS: Context limit 45000, validation levels 4
  - PLACEMENT: .codex/config/ directory

Task 5: CREATE .codex/workflows/health-check.yaml
  - IMPLEMENT: Simple validation workflow for testing
  - FOLLOW pattern: .bmad-core/workflows/greenfield-fullstack.yaml structure
  - SEQUENCE: Create test file → modify → validate → cleanup
  - PURPOSE: Verify CODEX orchestration works correctly
  - PLACEMENT: .codex/workflows/ directory

Task 6: CREATE .codex/tasks/create-doc.md
  - IMPLEMENT: Document creation task adapted from BMAD
  - FOLLOW pattern: .bmad-core/tasks/create-doc.md
  - PRESERVE: Mandatory elicitation format with 1-9 options
  - ADAPT: File paths to use .codex/ instead of .bmad-core/
  - PLACEMENT: .codex/tasks/ directory

Task 7: CREATE .codex/templates/project-brief-template.yaml
  - IMPLEMENT: YAML template for project brief generation
  - FOLLOW pattern: .bmad-core/templates/project-brief-tmpl.yaml
  - SECTIONS: Problem statement, target users, goals, success criteria
  - INCLUDE: Elicitation points for each major section
  - PLACEMENT: .codex/templates/ directory

Task 8: CREATE .codex/agents/analyst.md
  - IMPLEMENT: Business analyst agent for project brief creation
  - FOLLOW pattern: .bmad-core/agents/analyst.md structure
  - USES: create-doc task with project-brief-template
  - PERSONA: Investigative, thorough, business-focused
  - PLACEMENT: .codex/agents/ directory

Task 9: CREATE .codex/agents/pm.md
  - IMPLEMENT: Product manager agent for PRD creation
  - FOLLOW pattern: .bmad-core/agents/pm.md structure
  - INPUT: Reads project-brief.md from previous phase
  - OUTPUT: Creates PRD using prd-template.yaml
  - PLACEMENT: .codex/agents/ directory

Task 10: CREATE .codex/workflows/greenfield-swift.yaml
  - IMPLEMENT: Complete Swift workflow definition
  - FOLLOW pattern: docs/codex-architecture.md lines 352-507
  - SEQUENCE: analyst → pm → architect → prp-creator → dev
  - VALIDATION: Include 4-level validation gates
  - LANGUAGE_AGENTS: List Swift agent coordination points

Task 11: CREATE .codex/agents/prp-creator.md
  - IMPLEMENT: Enhanced PRP creation agent
  - SYNTHESIZES: project-brief, PRD, architecture documents
  - TEMPLATE: Uses PRPs/templates/prp_base.md
  - VALIDATION: Implements "No Prior Knowledge" test
  - ENRICHMENT: Integrates workflow context into PRP

Task 12: CREATE .codex/tasks/context-handoff.md
  - IMPLEMENT: Context breakpoint management task
  - DETECTS: Approaching token limit (40k threshold)
  - CREATES: Checkpoint summary documents
  - VALIDATES: Zero knowledge handoff capability
  - SAVES: Checkpoint to state/context-checkpoints.json

Task 13: CREATE .codex/tasks/validation-gate.md
  - IMPLEMENT: 4-level progressive validation execution
  - LEVEL 1: Syntax/style checks (project-specific)
  - LEVEL 2: Unit test execution
  - LEVEL 3: Integration testing
  - LEVEL 4: Language agent validation
  - REPORTS: Validation results with pass/fail status

Task 14: CREATE .codex/data/elicitation-methods.md
  - COPY: From .bmad-core/data/elicitation-methods.md
  - PURPOSE: Support mandatory 1-9 elicitation format
  - PRESERVE: All existing elicitation methods
  - PLACEMENT: .codex/data/ directory

Task 15: UPDATE .claude/commands/codex.md with full implementation
  - IMPLEMENT: Complete command routing and workflow initialization
  - SUBCOMMANDS: start, continue, status, validate, help
  - WORKFLOW: Load YAML, create initial state, launch orchestrator
  - ERROR: Handle missing workflows, invalid state gracefully
  - HELP: Display available workflows and current status
```

### Implementation Patterns & Key Details

```python
# Slash command pattern (.claude/commands/codex.md)
---
name: codex
description: CODEX orchestration system for AI-assisted development workflows
arguments: "[subcommand] [options] - e.g., 'start greenfield-swift' or 'status'"
---

# Parse $ARGUMENTS for subcommand
# Route to appropriate action:
# - start: Initialize workflow and launch orchestrator
# - continue: Resume from checkpoint
# - status: Show workflow state
# - validate: Run validation gates

# Agent activation pattern (.codex/agents/orchestrator.md)
activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE for persona
  - STEP 2: Load .codex/config/codex-config.yaml
  - STEP 3: Check .codex/state/workflow.json for state
  - STEP 4: Parse requested workflow YAML if starting
  - STEP 5: Coordinate agents per workflow sequence

# Workflow YAML pattern (.codex/workflows/greenfield-swift.yaml)
workflow:
  id: greenfield-swift
  sequence:
    - agent: analyst
      creates: docs/project-brief.md
      template: project-brief-template.yaml
      validation:
        - context_completeness: true
    - agent: pm
      creates: docs/prd.md
      requires: [docs/project-brief.md]

# Context breakpoint pattern
if token_count > 40000:
  create_checkpoint_document()
  validate_zero_knowledge_handoff()
  save_state_and_exit()

# Validation gate pattern
def execute_validation(level):
  if level == 1:
    run_syntax_checks()  # swiftlint, swift-format
  elif level == 2:
    run_unit_tests()     # swift test
  elif level == 3:
    run_integration()    # xcodebuild test
  elif level == 4:
    coordinate_language_agents()  # Task tool
```

### Integration Points

```yaml
SLASH_COMMANDS:
  - location: .claude/commands/codex.md
  - pattern: "YAML frontmatter with name, description, arguments"
  - integration: "Main entry point for all CODEX operations"

AGENT_COORDINATION:
  - tool: Task
  - pattern: "Launch multiple agents in single message"
  - example: "Task('analyst', prompt='Create project brief')"

STATE_PERSISTENCE:
  - location: .codex/state/workflow.json
  - update: "After each phase completion"
  - recovery: "Load on /codex continue"

VALIDATION_INTEGRATION:
  - swift: "swiftlint, swift-format, swift test, xcodebuild"
  - language_agents: "swift-syntax-reviewer, ios-security-auditor"
  - coordination: "Via Task tool parallel execution"

GIT_OPERATIONS:
  - branches: "codex/{workflow-type}/{feature-name}"
  - commits: "At each phase completion"
  - message: "CODEX: [phase] completed - [feature]"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# After creating each agent/task file
grep -E "^(agent|activation-instructions|persona|commands):" .codex/agents/*.md
# Verify YAML structure is valid

# Check slash command structure
head -n 5 .claude/commands/codex.md | grep -E "^(name|description|arguments):"
# Must have proper frontmatter

# Validate directory structure
tree .codex/ -L 2
# All directories must exist

# Expected: Proper YAML formatting, all directories created
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test orchestrator agent activation
echo "Testing orchestrator activation..."
# Manually: /codex help
# Should display available commands and workflows

# Test workflow parsing
cat .codex/workflows/health-check.yaml | grep -E "^workflow:|sequence:"
# Workflow structure must be valid

# Test state persistence
cat .codex/state/workflow.json 2>/dev/null || echo "{}" > .codex/state/workflow.json
# State file must be valid JSON

# Expected: All components load without errors
```

### Level 3: Integration Testing (System Validation)

```bash
# Test complete health-check workflow
# Manually: /codex start health-check
# Should complete all phases successfully

# Test workflow state persistence
# Manually: /codex status
# Should show current workflow state

# Test context handoff
# Create large test document to trigger breakpoint
# Verify checkpoint document created

# Test validation gates
# Manually: /codex validate
# Should run appropriate validation commands

# Expected: Full workflow execution works end-to-end
```

### Level 4: Creative & Domain-Specific Validation

```bash
# Test Swift workflow initialization
# Manually: /codex start greenfield-swift "Test iOS App"
# Should begin analyst phase with project brief

# Test agent coordination
# Verify multiple agents can be launched in parallel
# Check Task tool invocations work correctly

# Test PRP enhancement
# Verify PRP creator synthesizes workflow documents
# Check "No Prior Knowledge" validation passes

# Test language agent integration
# Verify Swift agents receive proper context
# Check validation feedback integrates correctly

# Expected: Complete Swift workflow executes with all enhancements
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] `/codex` command responds to all subcommands
- [ ] Workflow YAML files parse correctly
- [ ] State persistence and recovery works
- [ ] Context breakpoints trigger appropriately
- [ ] Validation gates execute project-specific commands

### Feature Validation

- [ ] Orchestrator agent activates and coordinates properly
- [ ] Document creation follows elicitation format
- [ ] PRPs include complete workflow context
- [ ] "No Prior Knowledge" test passes for generated PRPs
- [ ] Language agents coordinate through Task tool
- [ ] Health-check workflow completes successfully

### Code Quality Validation

- [ ] Follows existing BMAD patterns where appropriate
- [ ] File placement matches desired codebase structure
- [ ] Agent definitions use consistent YAML format
- [ ] Commands use proper slash command structure
- [ ] State management handles interruptions gracefully
- [ ] Error messages are clear and actionable

### Documentation & Deployment

- [ ] All agents include clear activation instructions
- [ ] Workflow definitions document all phases
- [ ] Help command provides comprehensive guidance
- [ ] State files are human-readable JSON
- [ ] Configuration allows customization
- [ ] Migration path from BMAD is clear

---

## Anti-Patterns to Avoid

- ❌ Don't create agents as code files - use markdown with natural language
- ❌ Don't skip elicitation when templates require it
- ❌ Don't ignore context limits - implement breakpoints
- ❌ Don't hardcode workflow sequences - use YAML definitions
- ❌ Don't launch agents sequentially when parallel is possible
- ❌ Don't create complete documents without user interaction
- ❌ Don't mix BMAD and CODEX commands - keep them separate
- ❌ Don't skip validation gates - they ensure quality

## Confidence Score: 9/10

This PRP provides complete implementation guidance for the CODEX MVP (Epics 1-3) with all necessary patterns, examples, and specifications for successful one-pass implementation.