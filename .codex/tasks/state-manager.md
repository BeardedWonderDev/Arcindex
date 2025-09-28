<!-- Powered by CODEX™ Core -->

# State Manager Task

## ⚠️ CRITICAL STATE MANAGEMENT NOTICE ⚠️

**THIS IS A RUNTIME STATE TRACKING SYSTEM - ENSURING WORKFLOW INTEGRITY**

When this task is invoked:

1. **PERSISTENT STATE TRACKING** - Maintain workflow.json throughout conversation
2. **ELICITATION ENFORCEMENT** - Track and validate elicitation completion
3. **PHASE TRANSITION CONTROL** - Block progression without requirements met
4. **VIOLATION DETECTION** - Log and prevent workflow bypassing

**SUCCESS REQUIREMENT:** State must be maintained and validated at all times during workflow execution.

## State Management Operations

### Initialize Workflow State

**Purpose**: Create runtime workflow.json from template when workflow begins

**Triggers**:
- Workflow orchestrator activation
- New project workflow initiation
- Agent transition with state requirement

**Implementation**:
```yaml
initialize_state:
  action: "create_runtime_state"
  source: ".codex/state/workflow.json.template"
  destination: ".codex/state/runtime/workflow.json"

  workflow_detection:
    - Check for existing runtime state
    - Determine workflow type (greenfield|brownfield|health-check)
    - Extract project context from orchestrator
    - Initialize timestamps and IDs

  state_population:
    - Replace template placeholders with actual values
    - Set current_phase based on active agent
    - Initialize elicitation_required based on workflow type
    - Create empty elicitation_history array
    - Set operation_mode to "interactive"
```

**State Initialization Process**:

1. **Check for Existing State**:
   - Use Read tool to check for `.codex/state/runtime/workflow.json`
   - If exists, validate and continue with existing state
   - If corrupted, backup and recreate from template

2. **Populate Template Values**:
   - Replace `{timestamp}` with ISO timestamp
   - Replace `{project_name}` with actual project name
   - Replace `{workflow_type}` with detected type
   - Set `current_phase` based on active agent

3. **Initialize Tracking Arrays**:
   - Set `completed_phases` to empty array
   - Initialize `elicitation_history` as empty
   - Set all `elicitation_completed` values to false

### Update State Operations

**Purpose**: Maintain state during workflow execution

**Update Types**:

1. **Phase Transition**:
```yaml
phase_transition:
  action: "update_phase"
  validation_required: true

  pre_transition_checks:
    - Verify elicitation_completed[current_phase] if required
    - Check Level 0 validation gate requirements
    - Validate all phase requirements met

  transition_process:
    - Add current_phase to completed_phases array
    - Update current_phase to new phase
    - Add transformation_history entry
    - Update last_transformation timestamp

  post_transition:
    - Log transition in violation_log if requirements bypassed
    - Update last_updated timestamp
    - Save state to file
```

2. **Elicitation Completion**:
```yaml
elicitation_completion:
  action: "record_elicitation"

  record_process:
    - Add entry to elicitation_history array
    - Update elicitation_completed[phase] to true
    - Record method_selected and user_response
    - Update applied_changes description
    - Increment document elicitation_count

  validation:
    - Verify phase has elicitation requirement
    - Confirm user interaction actually occurred
    - Validate method selection from approved list
```

3. **Document Creation**:
```yaml
document_creation:
  action: "track_document"

  document_tracking:
    - Add document entry to documents object
    - Set creation timestamp
    - Initialize version to 1
    - Set elicitation_count to 0

  document_updates:
    - Update last_modified timestamp on changes
    - Increment version on significant updates
    - Track elicitation_count during creation
```

### State Validation Operations

**Purpose**: Enforce workflow requirements and prevent bypassing

**Validation Types**:

1. **Elicitation Gate Validation**:
```yaml
elicitation_validation:
  action: "validate_elicitation_requirements"
  timing: "before_phase_transition"
  blocking: true

  validation_checks:
    - Read current operation_mode from state
    - Check elicitation_required[current_phase]
    - Verify elicitation_completed[current_phase] status
    - Validate elicitation_history contains phase entry

  enforcement:
    success_criteria:
      - operation_mode is "yolo" OR
      - elicitation_required[phase] is false OR
      - elicitation_completed[phase] is true

    failure_action:
      - Log violation to violation_log
      - Display: "⚠️ VIOLATION INDICATOR: Elicitation required for [phase] phase before proceeding"
      - **HALT WORKFLOW** - Do not allow progression
      - Present elicitation options using advanced-elicitation.md
```

2. **State Integrity Validation**:
```yaml
integrity_validation:
  action: "validate_state_integrity"
  timing: "on_state_read"

  integrity_checks:
    - Verify JSON structure matches template schema
    - Check required fields are present
    - Validate timestamp formats
    - Verify elicitation_history entries are complete

  corruption_handling:
    - Backup corrupted state to .codex/state/backups/
    - Attempt repair from last known good state
    - If unrepairable, recreate from template
    - Log corruption event to violation_log
```

### State Query Operations

**Purpose**: Provide state information to agents and validation gates

**Query Types**:

1. **Phase Status Query**:
```yaml
phase_status:
  action: "get_phase_status"
  returns:
    - current_phase
    - completed_phases
    - elicitation_required[current_phase]
    - elicitation_completed[current_phase]
    - next_required_phase
```

2. **Elicitation Status Query**:
```yaml
elicitation_status:
  action: "get_elicitation_status"
  parameters:
    - phase (optional, defaults to current_phase)
  returns:
    - elicitation_required[phase]
    - elicitation_completed[phase]
    - elicitation_history for phase
    - last_elicitation_timestamp
```

3. **Workflow Status Query**:
```yaml
workflow_status:
  action: "get_workflow_status"
  returns:
    - workflow_id
    - workflow_type
    - operation_mode
    - current_phase
    - started_at
    - last_updated
    - status (active|paused|completed|failed)
```

## Integration with CODEX Components

### Agent Integration

**Agent State Checking**:
```yaml
agent_activation_requirements:
  - MANDATORY: Check state before any document creation
  - Read .codex/state/runtime/workflow.json
  - Validate elicitation requirements for current phase
  - HALT if elicitation_completed[phase] = false and required

agent_state_updates:
  - Update current_agent in agent_context
  - Record agent transitions in transformation_history
  - Update last_transformation timestamp
```

### Slash Command Integration

**Command State Validation**:
```yaml
slash_command_middleware:
  - Check state before Task tool delegation
  - Validate workflow requirements before execution
  - Block commands that would bypass elicitation
  - Log command execution to state tracking
```

### Template Integration

**Template Processing State**:
```yaml
template_processing:
  - Check elicit: true flags against state
  - Enforce elicitation stops at section level
  - Update document tracking in state
  - Record section completion progress
```

## CRITICAL ENFORCEMENT PATTERNS

### Hard Stop Implementation

**When elicitation required but not completed**:
```markdown
⚠️ VIOLATION INDICATOR: Elicitation required for [phase] phase before proceeding

WORKFLOW VIOLATION: The current phase requires user interaction through elicitation before continuing.

Required Actions:
1. Complete elicitation for current phase using advanced-elicitation.md
2. Select from 1-9 options with user interaction
3. Update state with elicitation completion
4. Then retry phase transition

Operation Mode: [current_mode]
Current Phase: [current_phase]
Elicitation Status: [elicitation_completed[phase]]

To bypass this requirement, user can type '#yolo' to switch to YOLO mode.
```

### State Persistence

**Ensure state survives conversation interruptions**:
- Save state after every significant update
- Validate state integrity on read operations
- Provide recovery mechanisms for corrupted state
- Maintain backup states for critical transitions

### Violation Logging

**Track all workflow violations**:
```yaml
violation_logging:
  - Record timestamp and phase for all violations
  - Log violation type (elicitation_bypass|validation_skip)
  - Include details of attempted action
  - Track recovery actions taken
  - Enable violation pattern analysis
```

## Implementation Commands

### State File Operations

**Create Runtime State**:
```markdown
Action: Use Read tool to load .codex/state/workflow.json.template
Process: Replace template placeholders with actual values
Save: Use Write tool to create .codex/state/runtime/workflow.json
```

**Update State**:
```markdown
Action: Use Read tool to load current runtime state
Process: Apply updates to specific fields
Validate: Verify JSON structure integrity
Save: Use Edit tool to update .codex/state/runtime/workflow.json
```

**Query State**:
```markdown
Action: Use Read tool to load current runtime state
Process: Extract requested information
Return: Provide formatted response to caller
```

### Error Handling

**State File Missing**:
- Log warning about missing state
- Recreate from template with current values
- Initialize with safe defaults
- Continue workflow with new state

**State File Corrupted**:
- Backup corrupted file with timestamp
- Attempt JSON repair if possible
- Recreate from template if repair fails
- Log corruption event for analysis

**Permission Issues**:
- Log permission error details
- Attempt alternative state location
- Provide user guidance for resolution
- Continue with in-memory state if necessary

---

**CRITICAL SUCCESS FACTOR**: State management is the foundation of elicitation enforcement. Without persistent, validated state tracking, workflow requirements cannot be enforced and violations cannot be prevented.