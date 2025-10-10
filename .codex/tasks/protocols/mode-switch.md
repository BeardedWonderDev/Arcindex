# Mode Switch Protocol

purpose: "Handle mode switching commands (/codex interactive|batch|yolo)"

## Implementation

triggers: ["/codex interactive", "/codex batch", "/codex yolo"]

### Execution Steps

1. **Validate mode change request**:
   - Check if workflow is active (workflow.json exists)
   - Identify target mode from command
   - Check current mode to detect no-op switches

2. **Warn on destructive switches**:
   - interactive → yolo: Show warning about skipping all remaining elicitation
   - batch → yolo: Show warning about disabling all validation gates
   - Wait for user confirmation before proceeding

3. **Update state via state-manager**:
   - Read current .codex/state/workflow.json
   - Update operation_mode field to new mode
   - Add entry to transformation_history:
     ```json
     {
       "timestamp": "{ISO_timestamp}",
       "type": "mode_change",
       "from_mode": "{old_mode}",
       "to_mode": "{new_mode}",
       "changed_by": "user",
       "reason": "mode_switch_command"
     }
     ```
   - Save updated state

4. **Display confirmation**:
   - Show successful mode change
   - Display new mode behavior summary
   - Show next steps with new mode context

5. **Log mode change**:
   - Add to transformation_history in workflow.json
   - Include timestamp and reason
   - Track mode changes for audit trail

## Error Handling

### No Active Workflow
- Message: "No active workflow. Start a workflow first with /codex start"
- Action: halt

### Invalid Mode
- Message: "Invalid mode. Use: /codex interactive, /codex batch, or /codex yolo"
- Action: show_valid_modes

### State File Error
- Message: "Unable to update workflow state. Check .codex/state/workflow.json"
- Action: show_manual_edit_instructions

## Output Template

```
✅ Operation mode changed: {old_mode} → {new_mode}

{new_mode_description}

=== New Behavior ===
{behavior_changes}

=== Current Workflow State ===
Workflow: {workflow_type}
Phase: {current_phase}
Mode: {new_mode}

{next_steps_guidance}
```

## Warning Templates

### Interactive to YOLO Warning

```
⚠️ WARNING: Switching to YOLO Mode

This will disable ALL elicitation confirmations for the remainder of the workflow.
Agents will proceed automatically through all phases without user validation.

Current phase: {current_phase}
Remaining phases: {remaining_phases}

Are you sure you want to proceed? (Type 'yes' to confirm, 'no' to cancel)
```

### Batch to YOLO Warning

```
⚠️ WARNING: Switching to YOLO Mode

This will disable validation gates and automatic quality checks.
The workflow will complete with minimal oversight.

Recommended: Keep batch mode for balanced speed/quality tradeoff.

Continue to YOLO mode? (Type 'yes' to confirm, 'no' to cancel)
```

## State Update Integration

All mode switches use state-manager.md to:
- Update operation_mode field
- Log change to transformation_history
- Maintain audit trail with timestamps
- Preserve workflow state consistency

## Confirmation Display

After successful mode switch, display:
- Mode change confirmation with icon
- New mode behavior characteristics
- Current workflow state (type, phase, mode)
- Next steps guidance for user
