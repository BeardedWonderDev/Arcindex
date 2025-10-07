# BMAD Elicitation Implementation in CODEX

## Goal

**Feature Goal**: Implement BMAD's proven elicitation workflow patterns into CODEX to bridge the gap between elicitation documentation and runtime enforcement, ensuring mandatory user interaction at designated points.

**Deliverable**: Complete working elicitation system with state management, template-driven enforcement, and interactive workflow controls that prevents agents from bypassing user interaction requirements.

**Success Definition**: Agents will be unable to complete documents with `elicit: true` sections without presenting 1-9 options and waiting for user response. Phase transitions will be blocked until elicitation completion is validated through persistent state tracking.

## User Persona

**Target User**: CODEX users who need guided, interactive document creation with mandatory collaboration points

**Use Case**: Running CODEX workflows where strategic decisions require human input and validation before proceeding to the next phase

**User Journey**:
1. User initiates workflow (analyst, pm, architect phase)
2. Agent processes template section-by-section
3. At `elicit: true` sections, agent presents content + 1-9 options
4. User selects option or provides feedback
5. Agent processes feedback and updates content
6. State is tracked, preventing phase transitions without elicitation completion
7. Workflow continues with validated human input incorporated

**Pain Points Addressed**:
- Agents auto-completing entire documents without user input
- No enforcement of documented elicitation requirements
- Missing state tracking across agent transitions
- Inability to ensure strategic human decision points are respected

## Why

- **Proven Pattern**: BMAD has working elicitation enforcement that CODEX needs to replicate
- **Gap Bridge**: CODEX has comprehensive elicitation documentation but zero runtime enforcement
- **User Control**: Users need guaranteed interaction points for strategic decisions
- **Quality Assurance**: Human validation at critical decision points improves output quality
- **Workflow Integrity**: Maintains the designed collaborative workflow instead of pure automation

## What

### Success Criteria

- [ ] Agents halt execution at every `elicit: true` section and present 1-9 options
- [ ] State file (`workflow.json`) actively tracks elicitation completion status
- [ ] Phase transitions are blocked when `elicitation_completed[phase] = false`
- [ ] Template processing follows BMAD's section-by-section pattern with mandatory stops
- [ ] Users can type `#yolo` to explicitly bypass elicitation requirements
- [ ] Validation gates actually halt execution instead of being suggestions

## All Needed Context

### Context Completeness Check

_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_ ✅ This PRP provides complete BMAD implementation patterns, CODEX integration points, and step-by-step implementation guidance.

### Documentation & References

```yaml
# MUST READ - Critical implementation patterns
- file: .claude/commands/BMad/tasks/create-doc.md
  why: Contains exact BMAD workflow implementation that enforces elicitation
  pattern: Section-by-section processing with HARD STOP enforcement
  gotcha: Uses explicit workflow violation warnings to prevent bypassing

- file: .bmad-core/data/elicitation-methods.md
  why: 17 elicitation methods that populate 1-9 option selection
  pattern: Context-aware method selection algorithm
  gotcha: Must select exactly 8 methods plus "Proceed" option

- file: .codex/templates/project-brief-template.yaml
  why: Shows current CODEX template structure with elicit: true flags
  pattern: YAML template with sections containing elicit boolean
  gotcha: Currently documented but not enforced at runtime

- file: .codex/state/workflow.json.template
  why: Complete state management schema for tracking elicitation
  pattern: elicitation_completed array and elicitation_history tracking
  gotcha: Template exists but no runtime instances are created/maintained

- file: .codex/agents/analyst.md
  why: Shows current agent activation instructions with elicitation requirements
  pattern: "HALT IMMEDIATELY" and state checking instructions (lines 23-28)
  gotcha: These are suggestions that agents can bypass without consequences

- file: .codex/tasks/validation-gate.md
  why: Comprehensive validation system specification (808 lines)
  pattern: Level 0 elicitation as highest priority blocking gate
  gotcha: Pure specification with no runtime enforcement mechanism
```

### Current Codebase Structure

Use `Glob` tool to explore the current project structure and understand the layout:

```yaml
# Exploration approach using Claude Code tools
discover_structure:
  - Use Glob to find all .codex directories and files
  - Use Read to examine template structures
  - Use Grep to locate elicit: true flags in templates
  - Use Read to understand current agent implementations
```

### Known Gotchas & Constraints

```yaml
# CRITICAL: CODEX Task tool delegation bypasses state validation
# Current: Slash commands delegate directly to Task tool without checks
# Required: Add state validation middleware before Task execution

# CRITICAL: Agent activation instructions are suggestions, not enforced
# Current: Agents can ignore "HALT IMMEDIATELY" without consequences
# Required: Runtime validation layer that actually prevents execution

# CRITICAL: Templates exist but don't drive behavior
# Current: elicit: true flags are documented but never processed
# Required: Template parser that enforces elicitation stops

# CRITICAL: State management is template-only
# Current: workflow.json.template exists but no runtime instances
# Required: Active state persistence during workflow execution
```

## Implementation Blueprint

### Core Data Structures

The elicitation system requires persistent state tracking and method repository:

```yaml
# State management for elicitation tracking
workflow_state:
  project_id: "string"
  current_phase: "analyst|pm|architect"
  elicitation_completed:
    analyst: false
    pm: false
    architect: false
  elicitation_history: []
  workflow_mode: "interactive|batch|yolo"
  violation_log: []

# Elicitation methods repository structure
elicitation_methods:
  core_reflective:
    - "Expand or Contract for Audience"
    - "Critique and Refine"
    - "Identify Potential Risks"
  advanced_2025:
    - "Tree of Thoughts Deep Dive"
    - "ReWOO (Reasoning Without Observation)"
```

### Implementation Tasks (Natural Language Approach)

**Task 1: Create Elicitation Methods Repository**
- **Action**: Port BMAD's 17 elicitation method categories into CODEX data structure
- **Location**: Create `.codex/data/elicitation-methods.md`
- **Approach**: Use Read tool to examine BMAD's method structure, then Write tool to create CODEX version
- **Pattern**: Organize by categories (Core Reflective, Advanced 2025, etc.)
- **Validation**: Use Grep tool to count methods and verify 17+ methods are available

**Task 2: Implement State Management System**
- **Action**: Create runtime state tracking for elicitation completion
- **Location**: Create `.codex/tasks/state-manager.md` and `.codex/state/runtime/workflow.json`
- **Approach**: Define functions for reading, writing, and validating elicitation state
- **Pattern**: Follow BMAD's state persistence approach with completion tracking
- **Validation**: Use Read tool to verify state file structure matches template schema

**Task 3: Create Advanced Elicitation Engine**
- **Action**: Build the 1-9 option presentation system matching BMAD format exactly
- **Location**: Create `.codex/tasks/advanced-elicitation.md`
- **Approach**: Implement method selection algorithm and user interaction flow
- **Pattern**: Context-aware method selection with mandatory "Proceed" option
- **Validation**: Test that exactly 9 options are presented with proper formatting

**Task 4: Enhance Document Creation Workflow**
- **Action**: Modify existing create-doc task to enforce elicitation stops
- **Location**: Update `.codex/tasks/create-doc.md`
- **Approach**: Port BMAD's template parsing with elicit: true enforcement
- **Pattern**: Section-by-section processing with HARD STOP enforcement
- **Validation**: Verify templates with elicit: true flags trigger mandatory user interaction

**Task 5: Implement Phase Transition Validation**
- **Action**: Create validation gates that check elicitation completion before allowing phase changes
- **Location**: Create `.codex/tasks/validate-phase.md`
- **Approach**: Read state file and verify elicitation_completed status before progression
- **Pattern**: Block workflow transitions when requirements not met
- **Validation**: Test that incomplete elicitation prevents phase advancement

**Task 6: Update Agent Activation Instructions**
- **Action**: Enhance all agent files with runtime state checking requirements
- **Location**: Modify `.codex/agents/analyst.md`, `pm.md`, `architect.md`
- **Approach**: Add mandatory state validation calls before any document creation
- **Pattern**: Convert suggestions to enforced requirements while preserving personalities
- **Validation**: Agents must check state before proceeding with any workflow

### Implementation Workflow Patterns

Following BMAD's proven enforcement mechanisms:

```markdown
## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

When processing templates with elicitation flags:

1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - Full user interaction required
2. **MANDATORY STEP-BY-STEP EXECUTION** - Process each section sequentially
3. **ELICITATION IS REQUIRED** - When `elicit: true`, MUST use 1-9 format
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without this workflow

**VIOLATION INDICATOR:** Creating complete documents without user interaction violates this workflow.

## Template Processing with Enforcement

**Section Processing Flow:**
1. Read template section using Read tool
2. Check for `elicit: true` flag using Grep tool
3. If elicit required: HARD STOP and present content + rationale
4. Load elicitation methods using Read tool from data repository
5. Present exactly 9 options in mandatory format
6. Wait for user response - do not proceed automatically
7. Update state file using Edit tool to record interaction
8. Only proceed after user interaction completed

## State Validation Pattern

**Before Any Phase Transition:**
1. Use Read tool to load current workflow state
2. Verify elicitation_completed status for current phase
3. If incomplete: present violation warning and halt
4. Only proceed when state shows completion

## Method Selection Intelligence

**Context-Aware Selection:**
- Use Grep tool to analyze section content type
- Select appropriate elicitation methods based on context
- Always include "Proceed / No Further Actions" as option 9
- Update elicitation history with selected method and user feedback
```

### Integration Points

```yaml
AGENT_MODIFICATIONS:
  approach: Use Edit tool to update agent files with state checking
  pattern: Add mandatory state validation before document creation
  preservation: Keep existing agent personalities and capabilities

COMMAND_ROUTING:
  approach: Enhance slash command handling with validation middleware
  pattern: Check elicitation status before Task tool delegation
  enforcement: Block workflow execution until completion verified

TEMPLATE_ENHANCEMENT:
  approach: Use Read and Edit tools to ensure elicit flags are enforced
  pattern: Critical decision points require elicit: true
  validation: Templates drive actual behavior, not just documentation

STATE_PERSISTENCE:
  approach: Create runtime state instances from templates
  pattern: Active workflow.json maintained throughout conversation
  tracking: Persistent across agent transitions and interruptions
```

## Validation Approach

### Level 1: Structure & Syntax Validation

**File Structure Verification:**
- Use Glob tool to locate all required files in correct directories
- Use Read tool to verify YAML template syntax and structure
- Use Grep tool to count elicitation methods (should find 17+ methods)
- Use Read tool to validate JSON state file schema matches template

**Expected Outcomes:**
- All files exist in specified locations
- YAML templates parse correctly with proper elicit flags
- JSON state structure matches workflow.json.template schema
- Elicitation methods repository contains complete method set

### Level 2: Component Validation

**State Management Testing:**
- Use Read tool to verify workflow.json creation with proper schema
- Use Grep tool to locate elicitation_completed tracking in state
- Use Read tool to validate elicitation methods loading from repository
- Test state updates through Edit tool operations

**Template Processing Testing:**
- Use Grep tool to find templates with elicit: true flags
- Verify template parsing detects elicitation requirements
- Test that elicit flags trigger proper workflow stops
- Validate method selection algorithm works with different content types

**Expected Outcomes:**
- State file maintains elicitation completion tracking
- Templates correctly trigger elicitation when required
- Method repository accessible and provides appropriate options
- State updates persist across workflow operations

### Level 3: Integration Validation

**Workflow Execution Testing:**
- Initiate analyst phase workflow and verify state creation
- Test elicitation enforcement at elicit: true sections
- Attempt phase transition without elicitation completion
- Verify transition blocking occurs with appropriate messaging

**Agent Behavior Validation:**
- Test that agents check state before document creation
- Verify agents halt at elicit: true sections appropriately
- Test that agents present 1-9 options in correct format
- Validate user response handling and state updates

**Expected Outcomes:**
- Workflows respect elicitation requirements consistently
- Phase transitions blocked appropriately when incomplete
- Agents follow enforcement patterns without bypassing
- User interactions properly recorded and processed

### Level 4: User Experience & Anti-Pattern Validation

**BMAD Pattern Compliance:**
- Verify exact 1-9 format matches BMAD specification
- Test elicitation method selection algorithm accuracy
- Validate HARD STOP enforcement prevents bypassing
- Confirm detailed rationale provided with section content

**Anti-Bypass Testing:**
- Attempt to create complete documents without interaction
- Test efficiency optimization disabling effectiveness
- Verify violation warnings present when bypassing attempted
- Validate YOLO mode requires explicit user activation

**User Experience Quality:**
- Test user feedback integration and processing quality
- Verify state persistence across agent transitions
- Validate recovery from interrupted workflows
- Test multi-phase workflow with proper state tracking

**Expected Outcomes:**
- Full BMAD pattern compliance achieved
- Violation prevention working effectively
- Excellent user experience with proper guidance
- Robust workflow integrity maintained

## Final Validation Checklist

### Technical Implementation
- [ ] All file creation completed using Write and Edit tools
- [ ] State management functions working with Read/Edit tools
- [ ] Template processing enforces elicit flags via Grep/Read tools
- [ ] Elicitation methods accessible via Read tool from repository
- [ ] Agent modifications preserve capabilities while adding enforcement

### Feature Compliance
- [ ] Agents halt at elicit: true sections and present 1-9 options
- [ ] Phase transitions blocked when elicitation_completed[phase] = false
- [ ] YOLO mode allows explicit bypass with proper state tracking
- [ ] User feedback integration working with state updates
- [ ] Detailed rationale provided following BMAD pattern

### Workflow Integrity
- [ ] BMAD patterns replicated exactly using natural language descriptions
- [ ] State management consistent with template schema
- [ ] Anti-efficiency safeguards prevent automated bypassing
- [ ] Integration points documented and implemented correctly
- [ ] Validation approach uses Claude Code tools throughout

### Documentation Quality
- [ ] Implementation guidance uses natural language with YAML structure
- [ ] Tool usage instructions specify Claude Code tools (Read, Edit, Grep, Glob)
- [ ] Validation steps avoid bash commands, use native tools instead
- [ ] Anti-patterns section covers actual implementation risks
- [ ] Context completeness passes "No Prior Knowledge" test

---

## Anti-Patterns to Avoid

- ❌ Don't use bash commands for validation - use Claude Code tools (Read, Grep, Glob, Edit)
- ❌ Don't create new elicitation patterns - replicate BMAD's proven system exactly
- ❌ Don't make state checking optional - enforcement must be mandatory
- ❌ Don't allow agents to bypass without explicit YOLO mode activation
- ❌ Don't skip detailed rationale presentation - required for quality elicitation
- ❌ Don't use different 1-9 formats - match BMAD specification precisely