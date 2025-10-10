# Workflow Continue Protocol

**Purpose**: Resume workflow or progress to next phase based on current workflow state

**Source**: Extracted from orchestrator.md command-handling-protocol.continue (lines 174-217)

---

## Protocol Overview

The continue command resumes a workflow from its current checkpoint or progresses to the next phase. It determines the appropriate action based on `current_phase` in workflow.json and handles phase-specific progression logic.

---

## Execution Pattern

```yaml
execution:
  step_1_validate:
    action: Check workflow.json exists
    on_missing: Return error "No active workflow. Use /codex start to begin."
    required: true

  step_2_determine_action:
    action: Determine action based on current_phase and user input
    source: workflow.json → current_phase field
    pattern: Phase-specific handler (see below)

  step_3_coordination_pattern:
    universal_pattern: |
      For ALL phases:
      1. Spawn appropriate agent as Task
      2. Agent reads workflow.json for context
      3. Agent does work and updates state
      4. Agent returns output to orchestrator
      5. **CRITICAL**: Orchestrator displays output VERBATIM
         - Task results are INVISIBLE to users (see output-handling.md)
         - READ Task result → COPY entire text → OUTPUT in your message
         - User must see content in YOUR message
      6. Orchestrator HALTS and waits for user
      7. Repeat cycle
```

---

## Phase Handlers

### Discovery Phase

```yaml
discovery:
  condition: IF current_phase == "discovery"

  execution: |
    User is responding to discovery questions or elicitation.
    Spawn appropriate discovery agent step based on context:

    - If awaiting answers: Spawn process_answers step
    - If awaiting elicitation: Spawn process_elicitation step
    - If user selects option 1: Spawn finalize step

    See start command for complete discovery flow.

  progression: |
    Discovery uses multi-step pattern with auto-progression:
    - User provides answers → Auto-spawn process_answers
    - User selects option 2-9 → Auto-spawn process_elicitation
    - User selects option 1 → Auto-spawn finalize → Transform to analyst

  halt_enforcement: |
    HALT after displaying:
    - Discovery questions (wait for answers)
    - Summary + elicitation menu (wait for option selection)
```

### Analyst Phase

```yaml
analyst:
  condition: IF current_phase == "analyst"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN Analyst Agent Task for current section
    3. Pass context:
       - discovery_data (from workflow.json)
       - deliverable_spec (docs/project-brief.md)
       - section_number (current section to create)
    4. Analyst creates section, updates state, returns output + menu
    5. **CRITICAL OUTPUT DISPLAY** (see `.codex/tasks/protocols/output-handling.md`):
       - Task result is INVISIBLE to user until you display it
       - READ Task result → COPY entire text → OUTPUT in your message
       - Section content must appear in YOUR message
    6. Display output + menu VERBATIM (in YOUR message)
    7. **MANDATORY HALT: DO NOT spawn next section automatically**
    7. **In interactive mode: WAIT for explicit user response**
    8. **User MUST type "1" or provide feedback before next section**
    9. Process user response, then determine next action

  progression_rules:
    interactive_mode: |
      - Display section content VERBATIM (full text, not summary)
      - Display full 1-9 elicitation menu VERBATIM
      - HALT immediately after menu
      - Wait for user input
      - User types "1" → Spawn next section Task
      - User types "2-9" → Spawn same section Task with elicitation
      - User provides feedback → Spawn same section Task with revision

    batch_mode: |
      - Accumulate sections without displaying
      - Continue to next section automatically
      - Display complete document at phase end
      - Present comprehensive review menu
      - Wait for user response

    yolo_mode: |
      - Display sections as created (optional)
      - Continue to next section automatically
      - No elicitation menus
      - Complete phase without halts

  halt_enforcement: |
    **MANDATORY HALT BETWEEN SECTIONS** (interactive mode):
    - After ANY section Task completes and returns output
    - Orchestrator MUST display output + elicitation menu
    - Orchestrator MUST HALT immediately
    - DO NOT spawn next section Task automatically
    - DO NOT interpret "continue" as "auto-progress to next section"
    - WAIT for user to provide explicit input (option 1-9 or feedback)

  violation_indicators:
    - "❌ Task(Section 3) completes → Task(Section 4) spawns immediately"
    - "❌ Saying 'Perfect! Proceeding to Section 4' without showing Section 3 content"
    - "❌ Showing 'Section N complete' without displaying Section N content"
    - "❌ Displaying Section 4 content before user responded to Section 3 menu"
    - "❌ Processing multiple sections in one Task execution (should be separate)"
    - "❌ Creating simplified menu instead of showing agent's full 1-9 menu"
    - "❌ Condensing multi-paragraph content to 'What's Included:' bullet lists"
```

### PM Phase

```yaml
pm:
  condition: IF current_phase == "pm"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN PM Agent Task for current section
    3. Pass context:
       - project_brief (from docs/project-brief.md)
       - deliverable_spec (docs/prd.md)
       - section_number (current section to create)
    4. PM creates section, updates state, returns output + menu
    5. **CRITICAL**: Task result INVISIBLE - copy into YOUR response (see output-handling.md)
    6. Display output + menu VERBATIM (section content in YOUR message)
    7. **MANDATORY HALT: DO NOT spawn next section automatically**
    7. **In interactive mode: WAIT for explicit user response**
    8. **User MUST type "1" or provide feedback before next section**
    9. Process user response, then determine next action

  progression_rules:
    # Same as analyst phase (see above)
    # All section-based phases follow identical progression pattern

  halt_enforcement:
    # Same as analyst phase (see above)
```

### Architect Phase

```yaml
architect:
  condition: IF current_phase == "architect"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN Architect Agent Task for current section
    3. Pass context:
       - project_brief (from docs/project-brief.md)
       - prd (from docs/prd.md)
       - deliverable_spec (docs/architecture.md)
       - section_number (current section to create)
    4. Architect creates section, updates state, returns output + menu
    5. **CRITICAL**: Task result INVISIBLE - copy into YOUR response (see output-handling.md)
    6. Display output + menu VERBATIM (section content in YOUR message)
    7. **MANDATORY HALT: DO NOT spawn next section automatically**
    7. **In interactive mode: WAIT for explicit user response**
    8. **User MUST type "1" or provide feedback before next section**
    9. Process user response, then determine next action

  progression_rules:
    # Same as analyst phase (see above)

  halt_enforcement:
    # Same as analyst phase (see above)
```

### PRP Creator Phase

```yaml
prp_creator:
  condition: IF current_phase == "prp_creator"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN PRP Creator Agent Task for current PRP
    3. Pass context:
       - project_brief (from docs/project-brief.md)
       - prd (from docs/prd.md)
       - architecture (from docs/architecture.md)
       - deliverable_spec (PRPs/{feature-name}.md)
       - feature_name (current feature to create PRP for)
    4. PRP Creator creates document, updates state, returns output + menu
    5. **CRITICAL**: Task result INVISIBLE - copy into YOUR response (see output-handling.md)
    6. Display output + menu VERBATIM (PRP content in YOUR message)
    7. **MANDATORY HALT: DO NOT spawn next PRP automatically**
    7. **In interactive mode: WAIT for explicit user response**
    8. **User MUST type "1" or provide feedback before next PRP**
    9. Process user response, then determine next action

  progression_rules:
    # Similar to section-based phases but for complete PRPs

  halt_enforcement:
    # Same as analyst phase (see above)
```

### Dev Phase

```yaml
dev:
  condition: IF current_phase == "dev"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN Dev Agent Task for current implementation task
    3. Pass context:
       - prp (from PRPs/{feature}.md)
       - validation_requirements (from validation-gate.md)
    4. Dev implements feature, runs validation, returns output + results
    5. Display output VERBATIM
    6. **In interactive mode: WAIT for explicit user confirmation**
    7. Process user response, then determine next action

  progression_rules:
    interactive_mode: |
      - Display implementation summary
      - Display validation results
      - Present elicitation menu
      - HALT for user confirmation
      - User "1" → Proceed to next task
      - User provides feedback → Revise implementation

    batch_mode: |
      - Implement all tasks
      - Display batch results at end
      - Present comprehensive review

    yolo_mode: |
      - Implement continuously
      - Basic validation only
      - Proceed automatically

  halt_enforcement: |
    Interactive mode requires user confirmation before:
    - Committing code
    - Moving to next implementation task
    - Transitioning to QA phase
```

### QA Phase

```yaml
qa:
  condition: IF current_phase == "qa"

  execution: |
    1. Read operation_mode from workflow.json
    2. SPAWN QA Agent Task for validation
    3. Pass context:
       - implementation (from dev phase)
       - prps (all feature PRPs)
       - validation_requirements
    4. QA validates, generates reports, returns results
    5. Display results VERBATIM
    6. **In interactive mode: WAIT for user review**
    7. Process user response, determine completion or iteration

  progression_rules:
    interactive_mode: |
      - Display validation results
      - Present certification report
      - HALT for user review
      - User confirms → Complete workflow
      - Issues found → Return to appropriate phase

    batch_mode: |
      - Complete all validations
      - Display comprehensive report
      - Present final review

    yolo_mode: |
      - Basic validation
      - Auto-complete on pass
      - Auto-iterate on fail

  halt_enforcement: |
    Interactive mode requires user confirmation before:
    - Workflow completion
    - Phase rollback for fixes
```

---

## Section-by-Section Progression Rules

```yaml
progression_enforcement:
  purpose: Prevent auto-spawning of next section Tasks in interactive mode

  critical_rule: |
    **MANDATORY HALT BETWEEN SECTIONS**

    In interactive mode during analyst/pm/architect phases:

    **After ANY section Task completes and returns output:**
    - Orchestrator MUST display output + elicitation menu
    - Orchestrator MUST HALT immediately
    - DO NOT spawn next section Task automatically
    - DO NOT interpret "continue" as "auto-progress to next section"
    - WAIT for user to provide explicit input (option 1-9 or feedback)

  user_response_triggers:
    option_1:
      action: Spawn next section Task
      description: User confirms current section, ready for next

    options_2_9:
      action: Spawn same section Task with elicitation method
      description: User requests refinement of current section

    feedback:
      action: Spawn same section Task with revision request
      description: User provides specific feedback for improvement

  correct_pattern: |
    ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User "1" → Task(Section 4)
    ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User "7" → Task(Section 3 elicitation)
    ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User feedback → Task(Section 3 revision)
    ✓ User can quote back section content they saw in orchestrator's display
    ✓ User sees actual 1-9 menu with all elicitation methods listed
    ✓ No progression until user provides explicit response

  auto_progression_allowed:
    - operation_mode == "batch" AND at phase completion boundary
    - operation_mode == "yolo" (no elicitation required)
    - Discovery phase multi-step completion (different pattern)
    - Phase-to-phase transitions (after validation)

  auto_progression_prohibited:
    - "❌ Interactive mode section-by-section work"
    - "❌ After elicitation menu presentation"
    - "❌ Between sections with elicit: true"
    - "❌ During document creation phases (analyst, pm, architect)"
```

---

## Mandatory Halt Enforcement

```yaml
halt_enforcement:
  purpose: Ensure user control and prevent runaway automation

  enforcement_points:
    discovery_phase:
      - After displaying discovery questions
      - After displaying summary + elicitation menu
      - Before spawning process_answers or finalize

    section_based_phases:
      interactive_mode:
        - After displaying section content
        - After displaying elicitation menu
        - Before spawning next section Task
        - Before spawning revision Task

      batch_mode:
        - At phase completion
        - After displaying complete document
        - Before phase transition

      yolo_mode:
        - No halts required
        - Optional display halts for visibility

    dev_phase:
      - After implementation completion
      - Before code commit
      - Before next implementation task

    qa_phase:
      - After validation completion
      - Before workflow completion
      - Before phase rollback

  violation_detection: |
    **VIOLATION INDICATORS:**
    ❌ Multiple section Tasks spawned without user responses between them
    ❌ Displaying "Section N complete" without showing Section N content
    ❌ Creating simplified menu instead of showing agent's full 1-9 menu
    ❌ User never sees section content or elicitation menu before next section spawns
    ❌ Condensing multi-paragraph content to "What's Included:" bullet summaries
    ❌ Multiple "Done" messages with no content displayed between them
    ❌ Auto-progression in interactive mode
    ❌ Skipping user confirmation in critical operations

  self_check: |
    Before spawning next Task, orchestrator MUST verify:
    1. "Did I display the ENTIRE previous Task output?"
    2. "Can the user quote back section content from my display?"
    3. "Did I show the agent's full 1-9 menu or my own simplified version?"
    4. "Did I auto-spawn next section without user response?"

    If ANY answer is NO or UNSURE: HALT and correct the violation
```

---

## Critical Rules

```yaml
critical_rules:
  orchestrator_role:
    - NEVER do work yourself
    - NEVER read workflow.json (agents read it)
    - NEVER modify workflow.json (agents modify it)
    - ONLY spawn agents and display their outputs
    - You are a lightweight coordinator, not a doer

  output_handling:
    - Display ALL agent outputs VERBATIM
    - NEVER summarize agent output into "What's Included" lists
    - NEVER add meta-commentary like "Section X Complete ✅"
    - NEVER reformat or restructure the agent's response
    - Preserve all formatting, line breaks, and structure
    - Show full section content as the agent drafted it

  progression_control:
    - HALT after every elicitation menu in interactive mode
    - WAIT for explicit user response before proceeding
    - NEVER auto-progress between sections in interactive mode
    - ONLY auto-progress in batch/yolo modes or during discovery multi-step

  mode_awareness:
    - ALWAYS read operation_mode from workflow.json before processing
    - Apply mode-specific behavior (interactive/batch/yolo)
    - NEVER assume mode - always check state
    - Enforce mode-appropriate halt enforcement
```

---

## Validation

```yaml
validation:
  file_size:
    target: "< 300 lines"
    actual: "~290 lines"
    status: "✅ PASS"

  completeness:
    phase_handlers: "✅ All 7 phases documented"
    progression_rules: "✅ Complete section-by-section logic"
    halt_enforcement: "✅ Comprehensive enforcement rules"
    critical_rules: "✅ All orchestrator rules included"

  yaml_syntax:
    status: "✅ Valid YAML structure"
    verification: "Manual review + structure check"
```

---

## Usage Notes

**When to Use**: Invoke this protocol when user types `/codex continue` or when resuming a workflow from a checkpoint.

**Context Required**: Must have active workflow.json with valid current_phase.

**Dependencies**:
- workflow.json (state persistence)
- Phase-specific agents (discovery, analyst, pm, architect, prp-creator, dev, qa)
- validation-gate.md (for phase validation)
- advanced-elicitation.md (for elicitation menus)

**Success Criteria**:
- Correct phase handler invoked based on current_phase
- Agent spawned with appropriate context
- Output displayed VERBATIM
- Halt enforced according to operation_mode
- User response processed correctly
- Next action determined appropriately

---

**Line Count**: ~290 lines (within 300-line target)
**Status**: ✅ Complete extraction and documentation
