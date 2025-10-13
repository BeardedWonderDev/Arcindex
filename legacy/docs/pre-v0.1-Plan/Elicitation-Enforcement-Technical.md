# CODEX Elicitation Enforcement System - Technical Documentation

## Architecture Overview

The CODEX elicitation enforcement system ensures mandatory user interaction at critical workflow decision points through a multi-layer validation architecture.

```
┌─────────────────────────────────────────────────┐
│             Orchestrator Layer                   │
│  (/codex commands → workflow management)         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│          State Management Layer                  │
│  (state-manager.md → runtime/workflow.json)     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│          Validation Layer                        │
│  (validate-phase.md → enforcement gates)         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│          Elicitation Layer                       │
│  (advanced-elicitation.md → 1-9 menu)           │
└─────────────────────────────────────────────────┘
```

## Core Components

### 1. State Manager (`state-manager.md`)

**Purpose**: Persistent state tracking throughout workflow execution

**Key Functions**:
- Initialize runtime state from template
- Track elicitation completion per phase
- Maintain elicitation history
- Handle state recovery from corruption

**State Structure**:
```json
{
  "workflow_id": "codex-{timestamp}",
  "workflow_type": "greenfield-swift",
  "current_phase": "discovery",
  "operation_mode": "interactive",
  "elicitation_required": {
    "discovery": true,
    "analyst": true,
    "pm": true,
    "architect": true,
    "prp_creator": true
  },
  "elicitation_completed": {
    "discovery": false,
    "analyst": false,
    "pm": false,
    "architect": false,
    "prp_creator": false
  },
  "elicitation_history": [],
  "project_discovery": {},
  "documents": {}
}
```

### 2. Phase Validator (`validate-phase.md`)

**Purpose**: Block workflow progression until elicitation requirements met

**Validation Process**:
1. Check for runtime state file existence
2. Read operation mode from state
3. Verify elicitation requirements for current phase
4. Check completion status
5. Return pass/fail with enforcement

**Enforcement Levels**:
- **YOLO Mode**: Skip validation (log only)
- **Batch Mode**: Enforce at phase boundaries
- **Interactive Mode**: Enforce at every elicit point

### 3. Advanced Elicitation (`advanced-elicitation.md`)

**Purpose**: Present context-aware elicitation options

**Menu Format**:
```
Select 1-9 or type your feedback:
1. Proceed to next section
2. [Context-specific method]
3. [Context-specific method]
...
9. [Context-specific method]
```

**Method Selection Strategy**:
- Analyze content type and complexity
- Include 3-4 core methods always
- Add 4-5 context-specific methods
- Maintain consistent 1-9 format

### 4. Validation Gate (`validation-gate.md`)

**Purpose**: 5-level progressive validation system

**Level 0 (Highest Priority)**:
- Invokes `validate-phase.md`
- Blocks all other levels until passed
- Cannot proceed without elicitation

**Integration**:
```yaml
level_0_execution:
  trigger: "before_any_phase_transition"
  validator: "validate-phase.md"
  blocking: true
  bypass: "yolo_mode_only"
```

## Implementation Patterns

### Pattern 1: Workflow Initialization

```yaml
workflow_start:
  1. Parse command for workflow type
  2. Execute discovery questions
  3. Create runtime state via state-manager.md:
     - Set workflow_type
     - Set current_phase: "discovery"
     - Set elicitation_required[discovery]: true
     - Set elicitation_completed[discovery]: false
  4. Store discovery answers in state
  5. Present discovery summary with elicitation menu
  6. Update elicitation_completed[discovery]: true
  7. Run validate-phase.md before transformation
```

### Pattern 2: Phase Transition

```yaml
phase_transition:
  1. Current phase work complete
  2. Execute validate-phase.md for current phase
  3. If validation fails:
     - Present violation notice
     - Show elicitation menu
     - Block progression
  4. If validation passes:
     - Update current_phase in state
     - Transform to new agent
     - Continue workflow
```

### Pattern 3: Document Creation

```yaml
document_creation_with_elicitation:
  1. Load template with elicit flags
  2. For each section where elicit: true:
     - Present section content
     - Show rationale
     - Display 1-9 menu
     - Wait for user interaction
     - Apply selected method
     - Update state tracking
  3. Save completed document
  4. Update state with document metadata
```

## State File Management

### Location
```
.codex/state/runtime/workflow.json
```

### Backup Strategy
```
.codex/state/backups/{timestamp}-workflow.json
```

### Recovery Mechanisms

**Missing State**:
1. Check for backup files
2. Recreate from template
3. Initialize with safe defaults
4. Log recovery event

**Corrupted State**:
1. Backup corrupted file
2. Attempt JSON repair
3. Restore from last backup
4. Recreate if unrepairable

## Enforcement Mechanisms

### Hard Stop Implementation

When elicitation is required but not completed:

```markdown
⚠️ VIOLATION INDICATOR: Elicitation required for [phase] phase before proceeding

WORKFLOW VIOLATION DETECTED

Current State:
- Phase: [current_phase]
- Operation Mode: [operation_mode]
- Elicitation Required: true
- Elicitation Completed: false

Required Actions:
1. Complete elicitation using 1-9 menu
2. Or type #yolo to switch modes
```

### Validation Middleware

**Slash Command Interception**:
```yaml
/codex_command_validation:
  - Intercept command
  - Determine target phase
  - Execute validate-phase.md
  - Block or proceed based on result
```

**Agent Transformation Validation**:
```yaml
transformation_validation:
  - Before reading agent file
  - Run validate-phase.md
  - Only transform if passed
  - Otherwise present elicitation
```

## Operation Mode Behaviors

### Interactive Mode (Default)

```yaml
interactive_mode:
  elicitation_points:
    - Every elicit: true template section
    - Every phase transition
    - Every agent transformation
  enforcement: "mandatory"
  bypass: "none"
```

### Batch Mode

```yaml
batch_mode:
  elicitation_points:
    - Phase boundaries only
    - Batch collection of decisions
  enforcement: "phase_level"
  bypass: "within_phase"
```

### YOLO Mode

```yaml
yolo_mode:
  elicitation_points: "none"
  enforcement: "logging_only"
  bypass: "all"
  warning: "reduced_quality"
```

## Integration Points

### Orchestrator Integration

```yaml
orchestrator_hooks:
  activation:
    - Check runtime state existence
    - Verify operation mode
    - Load validation tasks

  discovery:
    - Create initial state
    - Set elicitation requirements
    - Present discovery elicitation

  transformation:
    - Run validate-phase.md
    - Block if validation fails
    - Update phase in state
```

### Agent Integration

```yaml
agent_activation:
  - Read runtime state
  - Check elicitation_completed[phase]
  - Halt if incomplete
  - Load advanced-elicitation.md
```

### Template Integration

```yaml
template_processing:
  - Parse elicit: true flags
  - For each flagged section:
    - Check state tracking
    - Enforce elicitation
    - Update completion
```

## Violation Detection & Logging

### Detection Points

1. **Pre-transformation validation**
2. **Pre-Task tool execution**
3. **Template section processing**
4. **Phase boundary crossing**

### Violation Types

```yaml
violation_types:
  elicitation_bypass:
    severity: "critical"
    action: "halt_workflow"

  phase_skip:
    severity: "critical"
    action: "block_progression"

  state_corruption:
    severity: "warning"
    action: "attempt_recovery"
```

### Logging Format

```json
{
  "timestamp": "ISO-8601",
  "phase": "current_phase",
  "violation_type": "elicitation_bypass",
  "details": "Attempted transformation without elicitation",
  "action_taken": "workflow_halted",
  "recovery_required": true
}
```

## Performance Considerations

### State Caching

```yaml
caching_strategy:
  read_operations:
    - Cache on first read
    - Invalidate on write
    - Refresh on validation failure

  write_operations:
    - Write-through to disk
    - Update cache
    - Verify integrity
```

### Validation Performance

```yaml
performance_targets:
  state_read: "< 50ms"
  validation_check: "< 100ms"
  elicitation_menu: "< 200ms"
  total_overhead: "< 500ms per operation"
```

## Testing Strategies

### Unit Testing

```bash
# Test state initialization
test_state_creation() {
  rm -f .codex/state/runtime/workflow.json
  # Trigger workflow start
  # Verify state file created
  # Check initial values
}

# Test validation enforcement
test_validation_blocking() {
  # Set elicitation_completed[phase]: false
  # Attempt phase transition
  # Verify blocking occurs
}
```

### Integration Testing

```bash
# Test full workflow with elicitation
test_workflow_with_elicitation() {
  # Start workflow
  # Complete discovery elicitation
  # Verify state updates
  # Transform to analyst
  # Verify validation passes
}
```

### Recovery Testing

```bash
# Test state corruption recovery
test_state_recovery() {
  # Corrupt state file
  # Trigger validation
  # Verify recovery mechanisms
  # Check restored state
}
```

## Debugging

### Debug Commands

```bash
# Check current state
cat .codex/state/runtime/workflow.json | jq '.'

# Verify elicitation status
cat .codex/state/runtime/workflow.json | jq '.elicitation_completed'

# View violation log
cat .codex/state/runtime/workflow.json | jq '.violation_log'

# Test validation
# Manually set elicitation_completed[phase]: false
# Attempt workflow operation
# Observe enforcement
```

### Common Issues

**Issue**: State file not created
- **Cause**: Discovery phase not properly initialized
- **Fix**: Ensure state-manager.md called after discovery questions

**Issue**: Validation not enforcing
- **Cause**: Wrong state file location
- **Fix**: Update references to `.codex/state/runtime/workflow.json`

**Issue**: Elicitation menu not appearing
- **Cause**: Operation mode set to YOLO
- **Fix**: Check mode with `/codex mode`, switch to interactive

## Extension Points

### Custom Elicitation Methods

Add new methods to `.codex/data/elicitation-methods.md`

### Custom Validation Levels

Extend `validation-gate.md` with additional levels

### Custom Operation Modes

Define new modes in state management with specific behaviors

### Workflow-Specific Requirements

Set phase-specific elicitation requirements in workflow definitions

## Security Considerations

### State File Permissions

- Ensure proper file permissions (600)
- Validate JSON structure before parsing
- Sanitize user input in elicitation responses

### Validation Bypass Prevention

- YOLO mode requires explicit user action
- No programmatic bypass in interactive mode
- Audit trail for all mode changes

## Conclusion

The CODEX elicitation enforcement system provides:

1. **Mandatory Quality Gates**: Ensures human validation at critical points
2. **Flexible Operation Modes**: Balance between control and efficiency
3. **Robust State Management**: Persistent tracking with recovery
4. **Clear Violation Detection**: Immediate feedback on bypass attempts
5. **Extensible Architecture**: Easy to add new validation types

This architecture ensures AI-generated content always receives human validation at strategic decision points, resulting in higher quality outputs aligned with user intent.