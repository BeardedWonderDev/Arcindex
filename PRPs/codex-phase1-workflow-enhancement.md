---
name: "CODEX Phase 1 Workflow Enhancement Implementation"
description: "Comprehensive PRP for implementing BMAD-inspired UX improvements to CODEX Phase 1 workflow initialization, focusing on project discovery, agent transformation patterns, and proper elicitation menus"
---

## Goal

**Feature Goal**: Transform CODEX Phase 1 workflow initialization to provide intuitive project discovery, seamless agent transformation, and properly formatted elicitation menus that guide users effectively through workflow phases.

**Deliverable**: Enhanced orchestrator and analyst agents with universal discovery protocol, transformation patterns, corrected elicitation menus (1-9 format), and improved workflow state management.

**Success Definition**: Users can start any CODEX workflow with natural project discovery (no multiple confirmations), receive context-appropriate elicitation options in correct format, and experience smooth agent transformations throughout workflow execution.

## User Persona

**Target User**: Developers using CODEX to orchestrate complete development workflows from concept to implementation

**Use Case**: Starting a new greenfield project or enhancing an existing brownfield project with CODEX orchestration

**User Journey**:
1. User types `/codex start greenfield-swift ProjectName`
2. CODEX asks natural discovery questions about the project
3. Orchestrator transforms into analyst with full context
4. Analyst creates project brief with section-by-section elicitation
5. User selects elicitation options using simple 1-9 menu format

**Pain Points Addressed**:
- Multiple confirmation dialogs before workflow starts
- Complex domain-specific menus appearing before basic discovery
- Incorrect menu format (0-8 + 9) instead of BMAD's proven 1-9 format
- No project concept discovery before elicitation

## Why

- **Business Value**: Dramatically improved developer experience leading to higher CODEX adoption and successful workflow completion rates
- **Integration**: Maintains existing Level 0 validation enforcement while fixing UX issues discovered in testing session
- **Problems Solved**: Eliminates user confusion, reduces workflow abandonment, provides intuitive onboarding matching BMAD's proven patterns

## What

Transform the Phase 1 experience from technically correct but user-hostile to intuitive and guided, matching BMAD's successful UX patterns while maintaining CODEX's validation enforcement.

### Success Criteria

- [ ] No multiple confirmations before workflow starts
- [ ] Basic project discovery happens before any complex elicitation
- [ ] Elicitation menus show correct 1-9 format throughout
- [ ] Agent transformations are announced clearly
- [ ] Content sections include rationale, trade-offs, and assumptions
- [ ] Workflow state properly tracks discovery and elicitation completion
- [ ] All three workflow types (greenfield/brownfield/health-check) properly supported

## All Needed Context

### Context Completeness Check

_This PRP contains all patterns, file locations, and implementation details needed to successfully implement the Phase 1 enhancements without prior CODEX knowledge._

### Documentation & References

```yaml
# MUST READ - Core implementation files to modify
- file: .codex/agents/orchestrator.md
  why: Primary file for implementing universal discovery protocol and transformation pattern
  pattern: Lines 118-151 contain workflow-management and agent-coordination sections to modify
  gotcha: Must maintain Level 0 validation enforcement while adding discovery

- file: .codex/agents/analyst.md
  why: Needs workflow-aware activation and content creation pattern
  pattern: Lines 19-39 activation instructions, lines 133-141 business analysis methods
  gotcha: Must integrate with orchestrator's discovery context passing

- file: .codex/tasks/advanced-elicitation.md
  why: Contains elicitation menu format that needs correction
  pattern: Lines 83-98 show current menu format, lines 99-104 show response handling
  gotcha: Must change to 1-9 format while maintaining all existing functionality

- file: .codex/tasks/validation-gate.md
  why: Level 0 validation that must be preserved during implementation
  pattern: Lines 54-98 contain Level 0 elicitation validation logic
  gotcha: CRITICAL - Do not weaken validation, only improve UX around it

# BMAD patterns to replicate
- file: .bmad-core/agents/bmad-orchestrator.md
  why: Source of transformation pattern and command structure
  pattern: Lines 36-48 persona definition, 113-117 transformation behavior
  gotcha: Adapt pattern to CODEX's Task tool usage, not direct transformation

- file: .bmad-core/templates/project-brief-tmpl.yaml
  why: Interactive workflow pattern with mode selection
  pattern: Lines 11-26 workflow mode, lines 28-38 introduction with mode choice
  gotcha: Must adapt to CODEX's YAML workflow structure

- file: .bmad-core/tasks/advanced-elicitation.md
  why: Correct elicitation menu format to copy
  pattern: Lines 83-98 show proper 1-9 menu format
  gotcha: BMAD uses different numbering - adapt to CODEX's needs

# Workflow configurations to update
- file: .codex/workflows/greenfield-swift.yaml
  why: Needs discovery phase added to workflow sequence
  pattern: Lines 34-51 show current analyst phase configuration
  gotcha: Must add discovery phase before analyst without breaking validation

- file: .codex/workflows/brownfield-enhancement.yaml
  why: Needs brownfield-specific discovery questions
  pattern: Similar structure to greenfield workflow
  gotcha: Must detect and load existing project context

# State management
- file: .codex/state/workflow.json
  why: Template for new state structure with discovery tracking
  pattern: Current structure needs project_discovery and enhancement_discovery sections
  gotcha: Must maintain backward compatibility with existing state files

# Documentation for implementation
- docfile: PRPs/ai_docs/claude-code-slash-commands.md
  why: Understanding how CODEX slash commands work and are routed
  section: Implementation Pattern for CODEX and Agent Activation Pattern
```

### Current Codebase tree (relevant portions)

```bash
.codex/
├── agents/
│   ├── orchestrator.md      # Main orchestrator to modify
│   ├── analyst.md           # Analyst agent to enhance
│   ├── pm.md
│   ├── architect.md
│   └── prp-creator.md
├── tasks/
│   ├── advanced-elicitation.md  # Menu format to fix
│   ├── validation-gate.md       # Level 0 validation to preserve
│   └── create-doc.md
├── workflows/
│   ├── greenfield-swift.yaml    # Add discovery phase
│   ├── brownfield-enhancement.yaml  # Add brownfield discovery
│   └── health-check.yaml
├── state/
│   └── workflow.json            # State tracking structure
└── config/
    └── codex-config.yaml

.bmad-core/  # Reference implementation
├── agents/
│   └── bmad-orchestrator.md
├── templates/
│   └── project-brief-tmpl.yaml
└── tasks/
    └── advanced-elicitation.md
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
.codex/
├── agents/
│   ├── orchestrator.md      # MODIFIED: Universal discovery, transformation pattern
│   ├── analyst.md           # MODIFIED: Workflow-aware activation, content pattern
│   └── [others unchanged]
├── tasks/
│   ├── advanced-elicitation.md  # MODIFIED: Corrected 1-9 menu format
│   └── [others unchanged]
├── workflows/
│   ├── greenfield-swift.yaml    # MODIFIED: Discovery phase added
│   ├── brownfield-enhancement.yaml  # MODIFIED: Brownfield discovery added
│   └── [others unchanged]
├── state/
│   └── workflow.json            # MODIFIED: New structure with discovery tracking
└── [others unchanged]

# No new files needed - only modifications to existing files
```

### Known Gotchas of our codebase & Library Quirks

```yaml
# CRITICAL: Level 0 validation enforcement must remain intact
# The current validation blocks workflow progression if elicitation incomplete
# Our changes must improve UX without weakening this enforcement

# CODEX uses Task tool for agent launching, not direct transformation
# When implementing BMAD's transformation pattern, must adapt to:
# - Use Task tool with subagent_type parameter
# - Pass context via prompt parameter
# - Cannot directly "become" another agent file

# Workflow state management is distributed
# - .codex/state/workflow.json tracks current state
# - Each agent checks state independently
# - Must ensure state consistency across transformations

# Elicitation menu selection uses different patterns
# - Current CODEX uses 0-8 + 9 format (incorrect)
# - BMAD uses 1-9 format (correct, what we're implementing)
# - Must update ALL response handling logic to match

# Claude Code slash command routing
# - All CODEX commands must start with /codex prefix
# - Subcommands parsed from $ARGUMENTS variable
# - Must maintain backward compatibility with existing commands
```

## Implementation Blueprint

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: MODIFY .codex/agents/orchestrator.md - Add Universal Discovery Protocol
  - LOCATION: Lines 118-137 (workflow-management section)
  - IMPLEMENT: Universal Workflow Discovery Protocol with 3 workflow types
  - ADD: STEP 2 discovery for greenfield (project name, concept, inputs)
  - ADD: STEP 2 discovery for brownfield (check existing context, get enhancement details)
  - ADD: STEP 2 discovery for health-check (bypass discovery, proceed directly)
  - FOLLOW pattern: .bmad-core/agents/bmad-orchestrator.md lazy loading approach
  - PRESERVE: Lines 122-129 MANDATORY PRE-LAUNCH VALIDATION PROTOCOL
  - CRITICAL: Keep Level 0 validation intact, add discovery BEFORE it

Task 2: MODIFY .codex/agents/orchestrator.md - Add Agent Transformation Protocol
  - LOCATION: After line 151 (new section after agent-coordination)
  - IMPLEMENT: Agent transformation pattern from BMAD
  - ADD: transformation protocol matching workflow phase to specialized agent
  - ADD: Read agent definition file directly (not Task tool for transformation)
  - ADD: Announcement of transformation with emoji and role
  - ADD: Context passing to transformed agent
  - PATTERN: .bmad-core/agents/bmad-orchestrator.md lines 113-117
  - NOTE: This is for direct transformation, Task tool still used for parallel work

Task 3: MODIFY .codex/agents/analyst.md - Add Workflow-Aware Activation
  - LOCATION: Lines 23-28 (activation-instructions STEP 3.5)
  - ADD: After existing STEP 3.5, new STEP 3.6 for workflow-aware activation
  - CHECK: workflow type from state (greenfield vs brownfield)
  - USE: discovery context passed from orchestrator
  - PREPARE: project brief creation workflow for greenfield
  - LOAD: existing project context for brownfield
  - BEGIN: section-by-section content creation with elicitation

Task 4: MODIFY .codex/agents/analyst.md - Add Content Creation Pattern
  - LOCATION: After line 141 (new section after business-analysis-methods)
  - IMPLEMENT: BMAD-style rich content creation pattern
  - ADD: content-creation-pattern section with substantial content requirements
  - INCLUDE: Main content, Rationale & Trade-offs, Key decisions, Assumptions, Validation areas
  - PRESENT: elicitation menu using correct 1-9 format after each section
  - WAIT: for user selection (1-9) before proceeding
  - EXECUTE: selected elicitation method if 2-9, continue if 1

Task 5: MODIFY .codex/tasks/advanced-elicitation.md - Fix Menu Format
  - LOCATION: Lines 83-98 (menu format specification)
  - CHANGE: From 0-8 + 9 format to 1-9 format
  - UPDATE: "Choose a number (0-8) or 9" to "Select 1-9 or type your feedback"
  - MODIFY: Option list to start with "1. Proceed to next section"
  - ADJUST: Methods to fill slots 2-9 (not 0-8)
  - LOCATION: Lines 99-104 (response handling)
  - UPDATE: Response handling for new 1-9 format
  - CHANGE: "Number 9" to "Number 1" for proceed action
  - ADJUST: Method execution for numbers 2-9 (not 0-8)

Task 6: MODIFY .codex/workflows/greenfield-swift.yaml - Add Discovery Phase
  - LOCATION: Before line 35 (before analyst phase in sequence)
  - ADD: discovery phase as first phase in workflow
  - IMPLEMENT: id: discovery, agent: orchestrator, required: true
  - ADD: tasks: project_discovery, context_capture
  - ADD: outputs: project_context, discovery_completed
  - MODIFY: analyst phase to require discovery.completed
  - ADD: inputs: project_context to analyst phase
  - ENSURE: validation level_0 still enforces elicitation

Task 7: CREATE workflow.json template for new state structure
  - LOCATION: .codex/state/workflow.json (template, not actual state)
  - IMPLEMENT: Complete new structure from plan lines 199-246
  - ADD: project_discovery section with concept, inputs, timestamp
  - ADD: enhancement_discovery section for brownfield workflows
  - ADD: agent_context section with transformation history
  - INCLUDE: elicitation_completed tracking per phase
  - INCLUDE: elicitation_history array for audit trail
  - PRESERVE: backward compatibility with existing state files
```

### Implementation Patterns & Key Details

```yaml
# Universal Discovery Protocol Pattern (orchestrator.md)
workflow-initialization:
  - STEP 1: Parse command to get workflow type and optional project name
    # Format: /codex start [workflow-type] [project-name]

  - STEP 2: Workflow-specific discovery based on type:

    GREENFIELD workflows:
      a. Capture project name from command (if provided)
      b. Ask comprehensive discovery questions:
         - "What's your project name/working title?" (if not provided)
         - "Brief project concept: (describe what you're building)"
         - "Any existing inputs? (research, brainstorming, or starting fresh?)"
      c. Transform to analyst for project brief creation

    BROWNFIELD workflows:
      a. Check for existing CODEX project context:
         - Read .codex/docs/*.md for project documentation
         - Read .codex/state/workflow.json for previous history
      b. Summarize understanding and get confirmation
      c. Ask enhancement-specific questions:
         - "What enhancement/feature are you adding?"
         - "Which component/area does this affect?"
         - "Any constraints or requirements?"
      d. Transform to analyst for enhancement documentation

    HEALTH-CHECK workflows:
      a. No discovery needed - proceed directly
      b. Execute validation checks immediately
      c. Report results without agent transformation

# Agent Transformation Pattern (orchestrator.md)
agent-transformation:
  - Match workflow phase to specialized agent
  - Read agent definition file directly (.codex/agents/{agent}.md)
  - Announce transformation: "📊 Transforming into Business Analyst"
  - Adopt complete agent persona and capabilities
  - Pass discovered project context to agent
  - Maintain workflow state through transformation
  - Execute agent until phase completion or exit
  - Return to orchestrator for next phase transition

# Content Creation Pattern (analyst.md)
content-creation-pattern:
  - Create substantial section content (match BMAD depth)
  - Include for each section:
    * Main content
    * Rationale & Trade-offs
    * Key decisions made
    * Assumptions
    * Areas for validation
  - Present elicitation menu using 1-9 format:
    * "1. Proceed to next section"
    * "2-9. Context-appropriate elicitation methods"
  - Wait for user selection before proceeding
  - Execute elicitation method if 2-9 selected
  - Continue to next section if 1 selected

# Correct Elicitation Menu Format
Please select an option:

1. Proceed to next section
2. Expand or Contract for Audience
3. Critique and Refine
4. Identify Potential Risks
5. Challenge from Critical Perspective
6. [Context-appropriate method]
7. [Context-appropriate method]
8. [Context-appropriate method]
9. [Context-appropriate method]

Select 1-9 or just type your question/feedback:
```

### Integration Points

```yaml
STATE_MANAGEMENT:
  - update: .codex/state/workflow.json structure
  - track: discovery_completed boolean per workflow
  - store: project_discovery and enhancement_discovery objects
  - maintain: elicitation_history array with timestamps

VALIDATION_INTEGRATION:
  - preserve: Level 0 validation in validation-gate.md
  - check: elicitation_completed[phase] before agent launch
  - block: workflow progression if validation fails
  - log: violations to .codex/debug-log.md

WORKFLOW_CONFIGS:
  - add: discovery phase to all non-health-check workflows
  - require: discovery.completed for analyst phase
  - pass: project_context as input to analyst
  - maintain: existing validation requirements
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Since we're modifying markdown and YAML files, check for:
# Valid YAML syntax in workflow files
yamllint .codex/workflows/greenfield-swift.yaml
yamllint .codex/workflows/brownfield-enhancement.yaml

# Valid JSON structure in state template
python -m json.tool .codex/state/workflow.json > /dev/null
if [ $? -ne 0 ]; then
    echo "Invalid JSON structure in workflow.json template"
    exit 1
fi

# Markdown formatting consistency
# No automated tool needed for .md files, but ensure:
# - Consistent indentation in YAML blocks
# - Proper code fence formatting
# - No broken internal references
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test discovery protocol with different workflow types
echo "Testing greenfield discovery..."
# Simulate: /codex start greenfield-swift TestProject
# Verify: Discovery questions are asked
# Verify: State contains project_discovery section

echo "Testing brownfield discovery..."
# Simulate: /codex start brownfield-enhancement
# Verify: Existing context is detected
# Verify: Enhancement questions are asked

echo "Testing health-check bypass..."
# Simulate: /codex start health-check
# Verify: No discovery questions asked
# Verify: Proceeds directly to validation
```

### Level 3: Integration Testing (System Validation)

```bash
# Full workflow execution test
echo "Testing complete greenfield workflow with discovery..."

# Step 1: Initialize workflow
# /codex start greenfield-swift "AgDealership"

# Step 2: Verify discovery executes
# - Project name captured
# - Concept question asked
# - Inputs question asked

# Step 3: Verify transformation to analyst
# - Announcement of transformation
# - Context passed correctly

# Step 4: Verify elicitation menu format
# - Shows 1-9 format
# - Option 1 is "Proceed to next section"
# - Options 2-9 are elicitation methods

# Step 5: Test menu selection
# - Select 2 (elicitation method)
# - Verify method executes
# - Verify menu re-appears
# - Select 1 (proceed)
# - Verify continues to next section

# Step 6: Verify state persistence
# Check .codex/state/workflow.json contains:
# - project_discovery with all fields
# - elicitation_completed["analyst"] = true
# - elicitation_history entries
```

### Level 4: Creative & Domain-Specific Validation

```bash
# User Experience Validation
echo "UX Flow Validation..."

# Test 1: Natural conversation flow
# - No multiple confirmations at start
# - Questions feel conversational not robotic
# - Clear what's being asked for

# Test 2: Error recovery
# - Invalid workflow type suggestion
# - Empty project name handling
# - Corrupted state file recovery

# Test 3: Elicitation quality
# - Methods selected are contextually appropriate
# - Rich content sections include rationale
# - Trade-offs are explicitly discussed

# BMAD Pattern Compliance Check
echo "Verifying BMAD pattern implementation..."
# - Transformation announcements present
# - Lazy loading (no pre-loading)
# - Numbered selection lists throughout
# - Command prefix consistency (* for BMAD, /codex for CODEX)
```

## Final Validation Checklist

### Technical Validation

- [ ] All YAML files have valid syntax
- [ ] JSON state template is valid
- [ ] No broken file references in code
- [ ] All modifications preserve existing functionality
- [ ] Level 0 validation remains fully enforced

### Feature Validation

- [ ] Greenfield workflow shows project discovery questions
- [ ] Brownfield workflow detects existing context
- [ ] Health-check workflow bypasses discovery
- [ ] Elicitation menus show 1-9 format (not 0-8 + 9)
- [ ] Agent transformations are announced clearly
- [ ] Content sections include rationale and trade-offs
- [ ] State properly tracks discovery and elicitation

### Code Quality Validation

- [ ] Changes follow existing CODEX patterns
- [ ] BMAD patterns properly adapted (not copied blindly)
- [ ] State management maintains backward compatibility
- [ ] Validation enforcement not weakened
- [ ] Clear separation between discovery and elicitation

### User Experience Validation

- [ ] No multiple confirmations before workflow starts
- [ ] Natural conversational flow for discovery
- [ ] Context-appropriate elicitation methods offered
- [ ] Clear progression through workflow phases
- [ ] Recovery from errors handled gracefully

---

## Anti-Patterns to Avoid

- ❌ Don't weaken Level 0 validation enforcement
- ❌ Don't skip discovery for greenfield workflows
- ❌ Don't use 0-8 + 9 menu format (use 1-9)
- ❌ Don't pre-load resources (lazy loading only)
- ❌ Don't forget to announce agent transformations
- ❌ Don't create sparse content sections (need depth)
- ❌ Don't break existing state file compatibility
- ❌ Don't mix BMAD and CODEX command prefixes