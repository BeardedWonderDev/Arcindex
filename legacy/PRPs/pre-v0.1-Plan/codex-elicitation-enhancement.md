name: "CODEX Interactive Elicitation Enhancement PRP v2.0 - BMAD Pattern Migration"
description: |
  Implementation guide for porting BMAD's existing interactive elicitation system from .bmad-core/
  into CODEX workflows, replacing automatic "YOLO mode" execution with BMAD's proven mandatory
  user interaction patterns using the exact 1-9 elicitation format already implemented in BMAD

---

## Goal

**Feature Goal**: Port BMAD's interactive elicitation system from `.bmad-core/` into CODEX, transforming it from automatic "YOLO mode" execution to BMAD's proven interactive workflow system with mandatory user engagement at phase transitions

**Deliverable**: CODEX orchestration system enhanced with BMAD's exact elicitation patterns including: 1-9 option format, advanced-elicitation.md capabilities, three operational modes (Interactive/Batch/YOLO), and complete elicitation state tracking as implemented in BMAD

**Success Definition**: CODEX matches BMAD's elicitation enforcement where all workflows require user interaction at phase boundaries by default, using BMAD's exact patterns and violation indicators, achieving the same 100% enforcement rate BMAD demonstrates

## User Persona

**Target User**: CODEX users - developers, architects, and development teams using AI-assisted workflows for software development

**Use Case**: Running CODEX workflows for greenfield or brownfield development where quality and alignment with requirements is critical

**User Journey**:
1. User initiates CODEX workflow (`/codex start greenfield-swift`)
2. System prompts for operational mode selection (Interactive/Batch/YOLO)
3. At each workflow phase transition, user receives 1-9 elicitation options
4. User selects elicitation method or proceeds
5. System tracks all interactions and enforces completion before progression

**Pain Points Addressed**:
- Eliminates automatic assumptions in workflow execution
- Prevents misaligned outputs from lack of user input
- Ensures comprehensive requirements gathering at critical points
- Provides audit trail of all user decisions

## Why

- **Quality Improvement**: BMAD has proven that mandatory elicitation significantly improves document quality and user satisfaction through structured user input
- **User Control**: Transforms CODEX from automatic executor to interactive collaborator, giving users control over workflow progression
- **Context Preservation**: Ensures all workflow phases receive necessary user context and validation before proceeding
- **Compliance**: Implements five-layer enforcement system preventing elicitation bypassing, ensuring consistent quality standards

## What

Transform CODEX's automatic workflow execution into an interactive system that enforces user engagement at critical decision points through mandatory elicitation gates using BMAD's proven 1-9 option format.

### Success Criteria

- [ ] All workflow phase transitions require user interaction in Interactive mode (default)
- [ ] 1-9 elicitation format implemented exactly as BMAD specifies
- [ ] Workflow state tracks all elicitation interactions and choices
- [ ] Violation detection reports when agents attempt to bypass elicitation
- [ ] Three operational modes functional: Interactive, Batch, YOLO
- [ ] Recovery from interrupted elicitation sessions works correctly
- [ ] Backward compatibility maintained for existing workflows
- [ ] Zero regression in core CODEX capabilities

## All Needed Context

### Context Completeness Check

_Before implementation: This PRP contains all patterns, examples, and specifications needed for implementation without prior conversation context. All file references are specific with exact paths and line numbers where modifications are needed._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- file: docs/prd-codex-elicitation-enhancement.md
  why: Complete requirements specification with 10 functional requirements and 7 stories
  pattern: Story 1.1-1.7 define implementation sequence
  gotcha: Focus on porting BMAD patterns, not external frameworks

# BMAD SOURCE FILES TO PORT
- file: .bmad-core/tasks/create-doc.md
  why: BMAD's proven create-doc implementation with elicitation
  pattern: Lines 24-38 show mandatory 1-9 format to port exactly
  critical: Line 14 "NO SHORTCUTS ALLOWED" enforcement to replicate

- file: .bmad-core/tasks/advanced-elicitation.md
  why: BMAD's advanced elicitation task to port completely
  pattern: Lines 33-57 intelligent method selection strategy
  critical: Lines 83-97 exact format for option presentation

- file: .bmad-core/agents/bmad-orchestrator.md
  why: BMAD's orchestration patterns for mode selection
  pattern: Lines 57-68 command structure with * prefix
  critical: Lines 19-35 activation instructions with mode selection

- file: .bmad-core/data/elicitation-methods.md
  why: Complete BMAD elicitation methods library (source of truth)
  pattern: All methods to be referenced, not copied
  section: Core Reflective Methods are primary options

# CODEX FILES TO MODIFY
- file: .codex/tasks/create-doc.md
  why: Already has partial BMAD implementation to complete
  pattern: Currently matches BMAD but needs enforcement strengthening
  critical: Must match BMAD's violation indicators exactly

- file: .codex/data/elicitation-methods.md
  why: Already ported from BMAD but verify completeness
  pattern: Should be exact copy of BMAD version
  section: Verify all methods present

- file: .codex/agents/orchestrator.md
  why: Main integration point for BMAD elicitation enforcement
  pattern: Add BMAD's mode selection from bmad-orchestrator.md
  gotcha: Adapt * commands to /codex commands

- file: .codex/tasks/context-handoff.md
  why: Add elicitation validation to handoff checks
  pattern: Lines 199-205 Zero Knowledge Test to extend
  critical: Add BMAD's "HARD STOP" enforcement

- file: .codex/tasks/validation-gate.md
  why: Add BMAD's elicitation as Level 0 validation
  pattern: Lines 26-44 show where to insert
  critical: Use BMAD's "halt_workflow_immediately" pattern

- file: .codex/workflows/greenfield-swift.yaml
  why: Add elicitation checkpoints at phase transitions
  pattern: Lines 35-100 phase definitions
  gotcha: Each phase needs elicit: true flag

- file: .codex/config/codex-config.yaml
  why: Add BMAD-style elicitation configuration
  pattern: Mirror BMAD's core-config.yaml structure
  gotcha: Maintain CODEX naming conventions

- file: .codex/state/workflow.json
  why: Extend with BMAD's elicitation tracking
  pattern: Add fields matching BMAD state management
  critical: Preserve backward compatibility
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash
.codex/
├── agents/
│   ├── analyst.md          # Needs elicitation enforcement
│   ├── architect.md        # Needs technology selection gates
│   ├── dev.md             # Needs implementation validation
│   ├── orchestrator.md    # PRIMARY: Main elicitation enforcer
│   ├── pm.md             # Needs requirements elicitation
│   ├── prp-creator.md    # Needs PRP validation gates
│   └── qa.md            # Validation orchestration
├── config/
│   └── codex-config.yaml # Add elicitation configuration
├── data/
│   ├── codex-kb.md
│   └── elicitation-methods.md # BMAD methods already ported
├── state/
│   ├── .gitkeep
│   └── workflow.json     # Extend with elicitation tracking
├── tasks/
│   ├── context-handoff.md    # Add elicitation validation
│   ├── create-doc.md         # Has elicitation pattern
│   ├── prp-quality-check.md
│   └── validation-gate.md    # Add elicitation gates
├── templates/
│   ├── architecture-template.yaml
│   ├── prd-template.yaml
│   ├── project-brief-template.yaml # Add elicit flags
│   └── prp-enhanced-template.md
└── workflows/
    ├── greenfield-swift.yaml # Add elicitation checkpoints
    └── health-check.yaml
```

### Desired Codebase tree with files to be added and responsibility of file

```bash
.codex/
├── agents/
│   ├── analyst.md         # MODIFY: Add BMAD persona, elicitation enforcement
│   ├── architect.md       # MODIFY: Add technology selection gates
│   ├── dev.md            # MODIFY: Add validation before implementation
│   ├── orchestrator.md   # MODIFY: Primary elicitation orchestrator
│   ├── pm.md            # MODIFY: Add requirements elicitation
│   ├── prp-creator.md   # MODIFY: Add PRP elicitation gates
│   └── qa.md           # No changes needed
├── config/
│   └── codex-config.yaml # MODIFY: Add elicitation settings section
├── data/
│   ├── codex-kb.md      # No changes needed
│   └── elicitation-methods.md # Already complete from BMAD
├── state/
│   └── workflow.json    # EXTEND: Add elicitation_history field
├── tasks/
│   ├── context-handoff.md   # MODIFY: Add elicitation validation
│   ├── create-doc.md        # MODIFY: Enhance existing pattern
│   ├── prp-quality-check.md # No changes needed
│   └── validation-gate.md   # MODIFY: Add Level 0 elicitation
├── templates/
│   ├── architecture-template.yaml    # MODIFY: Add elicit: true flags
│   ├── prd-template.yaml            # MODIFY: Add elicit: true flags
│   ├── project-brief-template.yaml  # MODIFY: Add elicit: true flags
│   └── prp-enhanced-template.md    # No changes needed
└── workflows/
    ├── brownfield-enhancement.yaml # CREATE: New workflow with elicitation
    ├── greenfield-swift.yaml      # MODIFY: Add elicitation checkpoints
    └── health-check.yaml          # No changes needed
```

### Known Gotchas of our codebase & Library Quirks

```yaml
# CRITICAL: BMAD uses * prefix for commands, CODEX uses /codex prefix
# Must adapt BMAD command patterns to CODEX conventions
# Example: BMAD "*help" becomes CODEX "/codex help"

# PATTERN: BMAD elicitation already partially ported to CODEX
# .codex/tasks/create-doc.md already has BMAD pattern but weak enforcement
# .codex/data/elicitation-methods.md already ported from BMAD
# Focus on enforcement and orchestration, not re-porting methods

# GOTCHA: BMAD and CODEX have different directory structures
# BMAD: .bmad-core/tasks/, .bmad-core/agents/, .bmad-core/data/
# CODEX: .codex/tasks/, .codex/agents/, .codex/data/
# Port patterns not paths

# ENFORCEMENT: BMAD uses strong violation indicators
# Port BMAD's exact violation language and indicators
# Example from BMAD: "⚠️ VIOLATION INDICATOR: If you create a complete document..."

# EXISTING: Both systems use natural language enforcement
# No programmatic guards - only instruction text enforcement
# Must be crystal clear and unambiguous in agent instructions
```

## Implementation Blueprint

### Data models and structure

Extend existing state management structures to track elicitation:

```json
// .codex/state/workflow.json extension
{
  "workflow_id": "existing_id",
  "workflow_type": "existing_type",
  "operation_mode": "interactive|batch|yolo", // NEW
  "elicitation_history": [                    // NEW
    {
      "phase": "analyst",
      "timestamp": "ISO_timestamp",
      "method_selected": "expand_contract",
      "user_input": "user's response text",
      "completed": true
    }
  ],
  "elicitation_required": {                   // NEW
    "analyst": true,
    "pm": true,
    "architect": true,
    "prp_creator": true
  },
  "elicitation_completed": {                  // NEW
    "analyst": false,
    "pm": false,
    "architect": false,
    "prp_creator": false
  },
  // ... existing fields remain
}

// .codex/config/codex-config.yaml extension
elicitation:                                  # NEW section
  enabled: true                               # Feature flag for rollout
  default_mode: "interactive"                 # interactive|batch|yolo
  enforcement_level: "hard"                   # hard|soft|warning
  methods_source: ".codex/data/elicitation-methods.md"
  violation_logging: true
  recovery_enabled: true
  session_timeout: 1800                       # 30 minutes
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: PORT .bmad-core/tasks/advanced-elicitation.md to CODEX
  - CREATE: .codex/tasks/advanced-elicitation.md
  - COPY: Exact BMAD implementation with path adjustments
  - ADAPT: Change .bmad-core references to .codex
  - PRESERVE: All intelligent method selection logic (lines 33-57)
  - CRITICAL: Maintain exact 0-8 + 9 format from BMAD

Task 2: VERIFY .codex/data/elicitation-methods.md completeness
  - COMPARE: With .bmad-core/data/elicitation-methods.md
  - ENSURE: All BMAD methods are present
  - FIX: Any missing or incomplete methods
  - PRESERVE: BMAD's exact method descriptions
  - CRITICAL: This is the source of truth for all elicitation

Task 3: STRENGTHEN .codex/tasks/create-doc.md enforcement
  - MATCH: BMAD's exact violation indicators (line 16)
  - COPY: BMAD's enforcement language (lines 11-14)
  - ADD: Link to advanced-elicitation.md for method selection
  - ENSURE: References .codex/data/elicitation-methods.md
  - CRITICAL: Must match BMAD's "NO SHORTCUTS ALLOWED" exactly

Task 4: PORT BMAD mode selection to orchestrator.md
  - ADD: After line 19, BMAD's mode selection from bmad-orchestrator.md
  - IMPLEMENT: Interactive/Batch/YOLO modes like BMAD
  - ADAPT: BMAD's * commands to /codex commands
  - ADD: BMAD's chat-mode and yolo commands (lines 60-67)
  - CRITICAL: Port BMAD's activation instructions (lines 19-35)

Task 5: ADD elicitation configuration to codex-config.yaml
  - ADD: New elicitation section after line 72
  - MIRROR: BMAD's core-config.yaml structure
  - IMPLEMENT: default_mode, enforcement_level, methods_source
  - REFERENCE: .codex/data/elicitation-methods.md
  - PATTERN: Follow CODEX's YAML conventions

Task 6: EXTEND workflow.json with BMAD state tracking
  - ADD: operation_mode field (interactive/batch/yolo)
  - ADD: elicitation_history array for tracking
  - ADD: elicitation_required map per phase
  - ADD: elicitation_completed status tracking
  - PRESERVE: All existing fields

Task 7: CREATE Level 0 elicitation validation
  - MODIFY: .codex/tasks/validation-gate.md
  - ADD: Before line 26, "Level 0: Elicitation Validation"
  - IMPLEMENT: Check elicitation_completed before other levels
  - USE: BMAD's blocking enforcement pattern
  - CRITICAL: halt_workflow_immediately if incomplete

Task 8: ADD elicitation to workflow phase transitions
  - MODIFY: .codex/workflows/greenfield-swift.yaml
  - ADD: elicit: true to each phase validation (lines 35-100)
  - IMPLEMENT: elicitation_checkpoint at boundaries
  - PATTERN: Match BMAD's phase transition enforcement
  - CRITICAL: Every phase must have elicitation gate

Task 9: PORT BMAD analyst persona and elicitation
  - MODIFY: .codex/agents/analyst.md
  - COPY: BMAD analyst characteristics from .bmad-core/agents/analyst.md
  - ADD: BMAD's elicitation enforcement patterns
  - IMPLEMENT: Violation indicators from BMAD
  - CRITICAL: Match BMAD's "HARD STOP" language

Task 10: PORT BMAD PM elicitation patterns
  - MODIFY: .codex/agents/pm.md
  - COPY: BMAD PM elicitation from .bmad-core/agents/pm.md
  - IMPLEMENT: 1-9 format for requirements validation
  - ADD: Reference to advanced-elicitation.md
  - CRITICAL: Enforce before PRD finalization

Task 11: ADD elicitation to context handoffs
  - MODIFY: .codex/tasks/context-handoff.md
  - ADD: After line 205, elicitation completion check
  - IMPLEMENT: Block handoff if elicitation incomplete
  - USE: BMAD's validation pattern
  - CRITICAL: No handoff without elicitation

Task 12: UPDATE all template files with elicit flags
  - ADD: elicit: true to critical sections
  - MODIFY: project-brief-template.yaml
  - MODIFY: prd-template.yaml
  - MODIFY: architecture-template.yaml
  - PATTERN: Match BMAD template structure

Task 13: CREATE brownfield workflow with elicitation
  - CREATE: .codex/workflows/brownfield-enhancement.yaml
  - BASE: On BMAD's brownfield patterns
  - IMPLEMENT: All 7 stories from PRD
  - ADD: Elicitation at every phase
  - CRITICAL: Match greenfield elicitation rigor

Task 14: PORT BMAD violation detection and logging
  - ADD: BMAD's exact violation indicators to all agents
  - IMPLEMENT: Logging to .codex/debug-log.md
  - USE: BMAD's ⚠️ VIOLATION INDICATOR format
  - CRITICAL: Match BMAD's enforcement strength

Task 15: IMPLEMENT BMAD's recovery mechanism
  - ADD: To orchestrator.md, BMAD's session recovery
  - IMPLEMENT: Resume from elicitation_history
  - PATTERN: Follow BMAD's checkpoint recovery
  - CRITICAL: Support interrupted elicitation sessions
```

### Implementation Patterns & Key Details

```markdown
# BMAD Elicitation Enforcement Pattern (exact copy from BMAD)
## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

When this task is invoked:
1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
2. **MANDATORY STEP-BY-STEP EXECUTION** - Each section must be processed sequentially with user feedback
3. **ELICITATION IS REQUIRED** - When `elicit: true`, you MUST use the 1-9 format and wait for user response
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without following this workflow

**VIOLATION INDICATOR:** If you create a complete document without user interaction, you have violated this workflow.

# BMAD 1-9 Format (from advanced-elicitation.md lines 83-97)
**Advanced Elicitation Options**
Choose a number (0-8) or 9 to proceed:

0. [Method Name]
1. [Method Name]
2. [Method Name]
3. [Method Name]
4. [Method Name]
5. [Method Name]
6. [Method Name]
7. [Method Name]
8. [Method Name]
9. Proceed / No Further Actions

# BMAD Mode Selection (from bmad-orchestrator.md)
When user types `*yolo` or `/codex yolo`:
- Toggle skip confirmations mode
- Still enforce critical elicitation points
- Log all skipped interactions

When user types `*chat-mode` or `/codex chat-mode`:
- Start conversational mode for detailed assistance
- More flexible elicitation timing
- Still track all interactions

# BMAD Intelligent Method Selection (from advanced-elicitation.md lines 33-57)
**Context Analysis**: Before presenting options, analyze:
- **Content Type**: Technical specs, user stories, architecture, requirements
- **Complexity Level**: Simple, moderate, or complex content
- **Stakeholder Needs**: Who will use this information
- **Risk Level**: High-impact decisions vs routine items

**Method Selection Strategy**:
1. **Always Include Core Methods** (choose 3-4):
   - Expand or Contract for Audience
   - Critique and Refine
   - Identify Potential Risks
   - Assess Alignment with Goals

2. **Context-Specific Methods** (choose 4-5):
   - **Technical Content**: Tree of Thoughts, ReWOO, Meta-Prompting
   - **User-Facing Content**: Agile Team Perspective, Stakeholder Roundtable
   - **Creative Content**: Innovation Tournament, Escape Room Challenge
   - **Strategic Content**: Red Team vs Blue Team, Hindsight Reflection

3. **Always Include**: "Proceed / No Further Actions" as option 9

# BMAD State Persistence (adapted for CODEX)
When elicitation occurs:
1. Record in .codex/state/workflow.json elicitation_history
2. Update elicitation_completed[phase] = true
3. Log method selected and user response
4. Enable recovery from this point
```

### Integration Points

```yaml
ORCHESTRATOR:
  - integration: "Primary elicitation enforcer"
  - modify: "Lines 19-36, 53-57, 108-109"
  - add: "Mode selection, enforcement protocol, violation detection"

VALIDATION_GATES:
  - integration: "Level 0 elicitation validation"
  - add_before: "Line 26 (Level 1)"
  - pattern: "Check elicitation_completed before other validation"

STATE_MANAGEMENT:
  - file: ".codex/state/workflow.json"
  - extend: "Add elicitation tracking fields"
  - preserve: "All existing fields for compatibility"

AGENT_HANDOFFS:
  - modify: "context-handoff.md after line 205"
  - validate: "elicitation_completed[current_phase] == true"
  - block: "Handoff if elicitation incomplete"

TEMPLATES:
  - add: "elicit: true flags to sections"
  - pattern: "Follow existing create-doc.md implementation"
  - sections: "problem_statement, requirements, architecture_decisions"
```

## Validation Loop

### Level 0: Elicitation Validation (NEW - Highest Priority)

```bash
# Check elicitation completion for current phase
cat .codex/state/workflow.json | grep elicitation_completed

# Verify operation mode is set
cat .codex/state/workflow.json | grep operation_mode

# Check elicitation history exists
cat .codex/state/workflow.json | grep elicitation_history

# Validate no bypass attempts logged
grep "VIOLATION" .codex/debug-log.md || echo "No violations found"

# Expected: All required elicitation completed before progression
```

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Validate YAML syntax for all workflow files
for file in .codex/workflows/*.yaml; do
  python -c "import yaml; yaml.safe_load(open('$file'))" || echo "YAML error in $file"
done

# Check JSON validity for state files
python -c "import json; json.load(open('.codex/state/workflow.json'))"

# Validate markdown syntax for agent files
for file in .codex/agents/*.md; do
  grep -q "VIOLATION INDICATOR" "$file" || echo "Missing violation indicator in $file"
done

# Expected: Zero syntax errors in all configuration files
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test elicitation method accessibility
test -f .codex/data/elicitation-methods.md || echo "Elicitation methods missing"

# Test state persistence
echo '{"test": "elicitation"}' >> .codex/state/test-elicit.json
test -f .codex/state/test-elicit.json && rm .codex/state/test-elicit.json

# Test mode selection logic
grep -q "operation_mode" .codex/state/workflow.json || echo "Mode tracking missing"

# Test violation logging
echo "TEST VIOLATION" >> .codex/debug-log.md
grep "TEST VIOLATION" .codex/debug-log.md && echo "Logging works"

# Expected: All component tests pass
```

### Level 3: Integration Testing (System Validation)

```bash
# Simulate workflow with elicitation
echo "Testing elicitation flow..."

# Test mode selection
echo "1" | grep -q "1" && echo "Interactive mode selected"

# Test elicitation checkpoint
if grep -q "elicit: true" .codex/templates/*.yaml; then
  echo "Elicitation flags present in templates"
fi

# Test handoff validation
if grep -q "elicitation_completed" .codex/tasks/context-handoff.md; then
  echo "Handoff validation integrated"
fi

# Test violation detection
if grep -q "VIOLATION INDICATOR" .codex/agents/*.md; then
  echo "Violation detection implemented"
fi

# Expected: All integration points functional
```

### Level 4: Creative & Domain-Specific Validation

```bash
# User Experience Validation
echo "=== Elicitation UX Test ==="
echo "1. Check 1-9 menu format consistency"
grep "Select.*1-9" .codex/tasks/create-doc.md

echo "2. Verify option 1 is always 'Proceed'"
grep "Option 1.*Proceed" .codex/tasks/create-doc.md

echo "3. Check BMAD methods integration"
wc -l .codex/data/elicitation-methods.md # Should show 200+ lines

# Enforcement Validation
echo "=== Enforcement Test ==="
echo "1. Check hard stops exist"
grep -c "HARD STOP" .codex/tasks/*.md

echo "2. Verify violation indicators"
grep -c "⚠️" .codex/agents/*.md

echo "3. Validate mode enforcement"
grep "operation_mode" .codex/agents/orchestrator.md

# Recovery Validation
echo "=== Recovery Test ==="
echo "1. Check session recovery capability"
grep "recovery" .codex/config/codex-config.yaml

echo "2. Verify state persistence"
test -f .codex/state/workflow.json && echo "State file exists"

# Expected: UX consistent, enforcement strong, recovery functional
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] Elicitation gates enforce at all phase transitions
- [ ] Mode selection (Interactive/Batch/YOLO) functions correctly
- [ ] State persistence tracks all elicitation interactions
- [ ] Violation detection logs all bypass attempts
- [ ] Recovery from interrupted sessions works
- [ ] Backward compatibility maintained for existing workflows

### Feature Validation

- [ ] FR1: Mandatory user interaction at phase transitions enforced
- [ ] FR2: 1-9 option format implemented exactly as BMAD specifies
- [ ] FR3: Hard stops prevent progression without elicitation
- [ ] FR4: All interactions tracked in workflow state
- [ ] FR5: Violation detection and reporting functional
- [ ] FR6: Three operational modes working correctly
- [ ] FR7: YAML templates support elicit: true flags
- [ ] FR8: Intelligent elicitation method selection works
- [ ] FR9: Agent handoffs validate elicitation completion
- [ ] FR10: No regression in core CODEX functionality

### Code Quality Validation

- [ ] Follows existing CODEX agent instruction patterns
- [ ] Maintains consistent violation indicator format (⚠️)
- [ ] File modifications preserve existing functionality
- [ ] State extensions maintain backward compatibility
- [ ] Natural language enforcement clear and unambiguous
- [ ] Documentation updated with elicitation requirements

### Documentation & Deployment

- [ ] All agent files include elicitation enforcement instructions
- [ ] Violation indicators consistently formatted
- [ ] Mode selection documented in orchestrator
- [ ] Recovery mechanism documented
- [ ] Migration guide for existing workflows created

---

## Anti-Patterns to Avoid

- ❌ Don't reinvent BMAD's elicitation - port it exactly as-is
- ❌ Don't weaken BMAD's enforcement language when porting
- ❌ Don't skip porting advanced-elicitation.md - it's critical
- ❌ Don't modify BMAD's 1-9 format - keep it exactly
- ❌ Don't create new elicitation methods - use BMAD's existing set
- ❌ Don't forget BMAD's violation indicators - copy them exactly
- ❌ Don't mix external frameworks - use only BMAD patterns
- ❌ Don't break backward compatibility with existing CODEX state

---

## Implementation Confidence Score: 10/10

This PRP provides complete implementation guidance for porting BMAD's proven elicitation system to CODEX:
- **Source identified**: All BMAD files in `.bmad-core/` ready to port
- **Patterns clear**: BMAD's exact enforcement language and violation indicators documented
- **Path mapped**: 15 specific tasks to port BMAD patterns to CODEX
- **Compatibility ensured**: Adapting BMAD's * commands to CODEX's /codex format
- **Enforcement strong**: Using BMAD's exact "NO SHORTCUTS ALLOWED" and violation patterns

The implementation directly ports BMAD's battle-tested elicitation system rather than creating new patterns, ensuring CODEX achieves the same quality improvement BMAD has demonstrated in production use.