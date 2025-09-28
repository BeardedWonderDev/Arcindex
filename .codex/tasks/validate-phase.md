<!-- Powered by CODEX™ Core -->

# Phase Transition Validation Task

## ⚠️ CRITICAL VALIDATION GATE NOTICE ⚠️

**THIS IS A BLOCKING VALIDATION LAYER - PREVENTING WORKFLOW VIOLATIONS**

When this task is invoked:

1. **MANDATORY STATE CHECKING** - Validate elicitation completion before any phase progression
2. **HARD STOP ENFORCEMENT** - Block Task tool delegation until requirements met
3. **VIOLATION DETECTION** - Log and prevent workflow bypassing attempts
4. **USER GUIDANCE** - Provide clear instructions for requirement completion

**ENFORCEMENT RULE:** No phase transitions, document creation, or workflow progression allowed without elicitation completion validation.

## Validation Gate Implementation

### Primary Validation Function

**Purpose**: Check elicitation completion status before allowing workflow progression

**Execution Process**:

1. **State File Detection**:
   - Use Read tool to check for `.codex/state/runtime/workflow.json`
   - If missing, create from template using state-manager.md
   - If corrupted, attempt recovery or recreation

2. **Operation Mode Check**:
   - Read `operation_mode` from workflow state
   - If mode is `"yolo"`, skip elicitation validation (but log)
   - If mode is `"batch"` or `"interactive"`, continue validation

3. **Elicitation Requirements Check**:
   - Read `elicitation_required[current_phase]` from state
   - If false, pass validation and allow progression
   - If true, proceed to completion status check

4. **Completion Status Validation**:
   - Read `elicitation_completed[current_phase]` from state
   - If true, pass validation and allow progression
   - If false, **HALT WORKFLOW** and present violation notice

### Validation Execution Commands

#### Check Elicitation Status
```yaml
check_elicitation_status:
  action: "validate_current_phase_elicitation"

  state_reading:
    - Use Read tool: ".codex/state/runtime/workflow.json"
    - Extract current_phase value
    - Extract operation_mode value
    - Extract elicitation_required[current_phase]
    - Extract elicitation_completed[current_phase]

  validation_logic:
    yolo_mode_check:
      - If operation_mode == "yolo": PASS (with log entry)

    requirement_check:
      - If elicitation_required[current_phase] == false: PASS

    completion_check:
      - If elicitation_completed[current_phase] == true: PASS
      - If elicitation_completed[current_phase] == false: FAIL

  result_actions:
    PASS:
      - Log successful validation
      - Allow workflow progression
      - Return validation_passed: true

    FAIL:
      - Log validation failure
      - Present violation notice
      - Block workflow progression
      - Return validation_passed: false
```

#### Phase Transition Validation
```yaml
phase_transition_validation:
  action: "validate_phase_transition"
  parameters:
    - from_phase: current phase
    - to_phase: target phase

  pre_transition_validation:
    - Check elicitation_completed[from_phase] if required
    - Verify all phase requirements documented in state
    - Validate transformation_history completeness

  transition_authorization:
    success_criteria:
      - Elicitation requirements met for current phase
      - No blocking validation failures
      - State integrity verified

    failure_handling:
      - Present detailed violation notice
      - Provide specific remediation steps
      - Block transition until resolution
```

### Violation Notice Implementation

**Violation Display Format**:
```markdown
⚠️ VIOLATION INDICATOR: Elicitation required for {current_phase} phase before proceeding

WORKFLOW VIOLATION DETECTED

Current State:
- Phase: {current_phase}
- Operation Mode: {operation_mode}
- Elicitation Required: {elicitation_required[current_phase]}
- Elicitation Completed: {elicitation_completed[current_phase]}
- Last Updated: {last_updated}

Required Actions:
1. Complete elicitation for current phase using advanced-elicitation.md
2. Select from 1-9 options with user interaction
3. Wait for state update with elicitation completion
4. Retry workflow operation

Bypass Option:
- User can type '#yolo' to switch to YOLO mode and bypass elicitation
- This will log the bypass but allow progression

Workflow cannot proceed until elicitation requirements are satisfied.
```

### Middleware Integration Points

#### Slash Command Middleware

**Purpose**: Intercept slash commands before Task tool delegation

**Implementation Pattern**:
```yaml
slash_command_interception:
  commands_requiring_validation:
    - /analyst (document creation phases)
    - /pm (PRD creation phases)
    - /architect (architecture phases)
    - /prp-creator (PRP creation phases)

  validation_process:
    1. Parse incoming slash command
    2. Determine target phase from command
    3. Execute validate-phase.md for current phase
    4. If validation FAILS: Present violation notice, halt
    5. If validation PASSES: Proceed with Task tool delegation

  logging:
    - Record all command attempts with validation results
    - Log bypasses and violations for analysis
    - Track user behavior patterns
```

#### Agent Activation Middleware

**Purpose**: Validate requirements before agent document creation

**Implementation Pattern**:
```yaml
agent_activation_validation:
  trigger: "before_document_creation_tasks"

  validation_sequence:
    1. Agent reads current workflow state
    2. Checks elicitation requirements for phase
    3. Validates completion status
    4. If incomplete: Present elicitation options immediately
    5. If complete: Proceed with agent workflow

  enforcement_points:
    - Before template-based document creation
    - Before section-by-section processing
    - Before any elicit: true section handling
```

#### Template Processing Middleware

**Purpose**: Enforce elicitation at template section level

**Implementation Pattern**:
```yaml
template_section_validation:
  trigger: "before_elicit_true_section_processing"

  section_level_enforcement:
    1. Parse template section for elicit: true flag
    2. Check section completion in state tracking
    3. If section not elicited: **HARD STOP**
    4. Present elicitation options using advanced-elicitation.md
    5. Wait for user interaction and state update
    6. Only proceed after elicitation completion

  state_updates:
    - Track section-level elicitation completion
    - Update document elicitation_count
    - Record method selected and user feedback
```

### Integration with Validation Gates

#### Level 0 Validation Integration

**Purpose**: Integrate with existing validation-gate.md Level 0

**Integration Points**:
```yaml
level_0_integration:
  validation_gate_enhancement:
    - Level 0 calls validate-phase.md as primary check
    - Inherits all violation detection and logging
    - Uses same state management patterns
    - Maintains consistent violation notices

  execution_order:
    1. Level 0 triggers validate-phase.md
    2. validate-phase.md performs core validation
    3. Results passed back to Level 0
    4. Level 0 proceeds or halts based on results
```

### State Management Integration

#### State Updates After Validation

**Purpose**: Maintain state consistency after validation events

**Update Operations**:
```yaml
post_validation_state_updates:
  successful_validation:
    - Update last_validation timestamp
    - Log successful validation to history
    - Clear any pending violation flags

  failed_validation:
    - Log violation to violation_log
    - Update violation_count metrics
    - Set violation_pending flag
    - Record remediation requirements

  elicitation_completion:
    - Update elicitation_completed[phase] = true
    - Add elicitation_history entry
    - Clear violation_pending flag
    - Update last_updated timestamp
```

### Error Handling and Recovery

#### State File Issues

**Missing State File**:
```yaml
missing_state_recovery:
  detection: "Read tool returns file not found error"

  recovery_process:
    1. Log missing state warning
    2. Use state-manager.md to recreate from template
    3. Initialize with safe default values
    4. Set all elicitation_completed to false
    5. Continue validation with new state
```

**Corrupted State File**:
```yaml
corrupted_state_recovery:
  detection: "JSON parsing error on state read"

  recovery_process:
    1. Backup corrupted file with timestamp
    2. Attempt JSON repair if possible
    3. If unrepairable, recreate from template
    4. Log corruption event for analysis
    5. Continue with recovered or new state
```

#### Permission and Access Issues

**File Permission Errors**:
```yaml
permission_error_handling:
  detection: "Permission denied on state file operations"

  recovery_process:
    1. Log permission error details
    2. Attempt alternative file locations
    3. Provide user guidance for resolution
    4. Fall back to in-memory state tracking
    5. Warn about persistence limitations
```

### Validation Performance Optimization

#### Caching and Efficiency

**State Caching**:
```yaml
state_caching:
  cache_strategy:
    - Cache state in memory after first read
    - Invalidate cache on state file updates
    - Refresh cache on validation failures
    - Clear cache on phase transitions

  performance_targets:
    - Validation check: < 100ms
    - State file read: < 50ms
    - Violation notice generation: < 200ms
```

### Testing and Validation

#### Validation Testing Commands

**Test Validation Enforcement**:
```bash
# Test elicitation requirement enforcement
echo "Testing validation enforcement..."

# Simulate incomplete elicitation state
# Attempt phase transition
# Verify violation notice appears
# Confirm workflow halts

echo "Validation enforcement test complete"
```

**Test Recovery Mechanisms**:
```bash
# Test state file recovery
echo "Testing state recovery..."

# Simulate missing state file
# Trigger validation
# Verify state recreation
# Confirm workflow continues

echo "State recovery test complete"
```

## CRITICAL SUCCESS FACTORS

### Enforcement Effectiveness

**Hard Stop Requirements**:
- Validation MUST actually halt workflow progression
- Violation notices MUST be clearly visible to user
- Bypass options MUST be explicit (YOLO mode only)
- State MUST be persistent across conversation interruptions

### User Experience

**Clear Guidance**:
- Violation messages include specific remediation steps
- Elicitation options presented immediately when needed
- Progress tracking visible to user
- Bypass mechanisms clearly documented

### System Reliability

**Robust Operation**:
- Validation works even with corrupted state
- Recovery mechanisms handle all error conditions
- Performance impact minimal on normal operation
- Integration seamless with existing components

---

**CRITICAL ENFORCEMENT RULE**: This validation layer is the cornerstone of elicitation enforcement. It transforms documented requirements into runtime behavior that agents cannot bypass without explicit user authorization.