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
  destination: ".codex/state/workflow.json"

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
   - Use Read tool to check for `.codex/state/workflow.json`
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

### Mode Management Operations

**Purpose**: Manage operation mode transitions and enforce mode-aware workflow behavior

**Mode Operations**:

1. **Update Operation Mode**:
```yaml
update_operation_mode:
  action: "set_operation_mode"
  parameters:
    - new_mode: "interactive" | "batch" | "yolo"
    - reason: string (optional)
  validation_required: true

  pre_update_checks:
    - Validate new_mode is one of allowed values
    - Check current workflow phase for mode change restrictions
    - Verify no blocking tasks are in progress
    - Read current mode from workflow.json

  mode_validation:
    allowed_modes:
      - "interactive": User interaction required at elicitation points
      - "batch": Minimal interaction, auto-proceed where possible
      - "yolo": Skip all elicitation, auto-generate content

    blocked_transitions:
      - Cannot change mode during active create-doc task
      - Cannot change mode during validation gate processing
      - Cannot change mode during elicitation interaction
      - Cannot change from yolo during critical document generation

  update_process:
    - Read current workflow.json state
    - Store previous mode for mode_changes tracking
    - Update operation_mode field to new_mode
    - Add mode change entry to mode_changes array
    - Add entry to transformation_history with mode context
    - Update last_updated timestamp
    - Save updated state to workflow.json

  mode_change_tracking:
    - timestamp: ISO 8601 format
    - from_mode: previous operation mode
    - to_mode: new operation mode
    - phase: current workflow phase at time of change
    - reason: user-provided or system-generated reason
    - initiated_by: "user" | "system"

  return:
    success: true
    previous_mode: string
    current_mode: string
    message: "Operation mode updated from [previous] to [current]"
```

2. **Get Operation Mode**:
```yaml
get_operation_mode:
  action: "query_operation_mode"
  blocking: false

  query_process:
    - Read .codex/state/workflow.json
    - Extract operation_mode field
    - Read mode_changes array for history
    - Get last mode change timestamp
    - Determine mode change count

  default_handling:
    - If operation_mode field missing, default to "interactive"
    - Log missing field warning to violation_log
    - Update state with default mode
    - Continue with interactive mode

  return:
    current_mode: "interactive" | "batch" | "yolo"
    mode_metadata:
      - set_at: timestamp of current mode activation
      - set_by: who initiated current mode
      - previous_mode: mode before current
      - change_count: total mode changes this session
      - mode_duration: time in current mode (calculated)
```

3. **Mode Validation Rules**:
```yaml
mode_validation_rules:
  action: "validate_mode_transition"
  enforcement: "blocking"

  allowed_transitions:
    from_interactive:
      - to_batch: allowed (reduces interaction)
      - to_yolo: allowed with user confirmation

    from_batch:
      - to_interactive: allowed (increases safety)
      - to_yolo: allowed with user confirmation

    from_yolo:
      - to_interactive: allowed (increases safety)
      - to_batch: allowed (increases safety)

  blocked_during_phases:
    create_doc_active:
      - Cannot switch from yolo to interactive
      - Cannot switch from yolo to batch
      - Reason: "Document generation in progress, mode locked"

    validation_gate_active:
      - Cannot switch to yolo
      - Can switch between interactive and batch
      - Reason: "Validation requires user oversight"

    elicitation_in_progress:
      - All mode changes blocked
      - Reason: "Complete current elicitation before changing mode"

  phase_restrictions:
    discovery:
      - All transitions allowed
      - No restrictions during initial phase

    requirements:
      - Cannot switch to yolo during requirement elicitation
      - Can switch to batch for bulk requirement entry

    design:
      - Cannot switch to yolo during architecture decisions
      - Batch mode allowed for template population

    validation:
      - Yolo mode not allowed
      - Only interactive or batch permitted

  validation_implementation:
    check_sequence:
      1. Read current phase from workflow.json
      2. Read current active tasks from agent context
      3. Check if elicitation is in progress
      4. Verify from_mode -> to_mode is allowed
      5. Check phase-specific restrictions
      6. Validate no blocking conditions exist

    failure_handling:
      - Return error with specific reason
      - Display blocked transition message to user
      - Suggest when mode change will be allowed
      - Log attempted invalid transition
```

4. **Mode Change Tracking Schema**:
```yaml
mode_change_tracking:
  action: "track_mode_changes"
  purpose: "Maintain audit trail of mode transitions"

  state_schema_addition:
    mode_changes:
      type: array
      description: "Complete history of operation mode changes"
      items:
        - timestamp: ISO 8601 string
        - from_mode: "interactive" | "batch" | "yolo"
        - to_mode: "interactive" | "batch" | "yolo"
        - phase: current workflow phase
        - reason: string (user provided or system generated)
        - initiated_by: "user" | "system"
        - context:
            - active_agent: which agent was active
            - active_task: task being performed
            - documents_in_progress: array of document names

  transformation_history_updates:
    mode_context_addition:
      - Add operation_mode field to each transformation entry
      - Track mode at time of each workflow transformation
      - Enable correlation between mode and workflow actions
      - Support mode-aware workflow analysis

  tracking_implementation:
    on_mode_change:
      - Create new mode_changes entry
      - Append to mode_changes array
      - Update transformation_history with mode context
      - Calculate mode usage statistics
      - Update last_updated timestamp

    mode_statistics:
      - time_in_interactive: total duration in interactive mode
      - time_in_batch: total duration in batch mode
      - time_in_yolo: total duration in yolo mode
      - mode_change_frequency: changes per hour
      - most_used_mode: mode with longest duration

  query_support:
    get_mode_history:
      action: "query_mode_history"
      parameters:
        - limit: number (optional, default 10)
        - phase: string (optional filter)
      returns:
        - Array of mode_changes entries
        - Mode usage statistics
        - Current mode metadata

    get_mode_statistics:
      action: "query_mode_statistics"
      returns:
        - mode_usage_breakdown: percentage by mode
        - average_mode_duration: average time per mode
        - mode_change_patterns: common transition sequences
        - phase_mode_correlation: modes used per phase
```

### Mode-Aware State Operations

**Purpose**: Ensure all state operations respect current operation mode

**Mode Integration**:

```yaml
mode_aware_validation:
  elicitation_gate_check:
    - Read current operation_mode from state
    - If mode = "yolo", bypass elicitation requirements
    - If mode = "batch", use minimal interaction elicitation
    - If mode = "interactive", enforce full elicitation workflow

  phase_transition_check:
    - Read current operation_mode
    - Apply mode-specific transition rules
    - Log mode context in transformation_history
    - Track mode at time of phase completion

  document_creation_check:
    - Read current operation_mode
    - Set document.auto_generated = true if yolo mode
    - Set document.elicitation_required based on mode
    - Track mode in document metadata
```

## Integration with CODEX Components

### Agent Integration

**Agent State Checking**:
```yaml
agent_activation_requirements:
  - MANDATORY: Check state before any document creation
  - Read .codex/state/workflow.json
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
Save: Use Write tool to create .codex/state/workflow.json
```

**Update State**:
```markdown
Action: Use Read tool to load current runtime state
Process: Apply updates to specific fields
Validate: Verify JSON structure integrity
Save: Use Edit tool to update .codex/state/workflow.json
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