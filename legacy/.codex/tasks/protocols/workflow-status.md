# Workflow Status Protocol

## Purpose
Display current workflow state and system health via `/codex status` command.

## Implementation Steps

1. Read `.codex/state/workflow.json` (show "No active workflow" if missing)
2. Read `.codex/config/codex-config.yaml`
3. List all `.yaml` files in `.codex/workflows/`
4. Display comprehensive status report
5. Return formatted output to main conversation

## State Reading

```yaml
validate:
  - Check .codex/state/workflow.json exists
  - Parse JSON structure and extract fields

display_fields:
  - workflow_type, project_name, current_phase
  - operation_mode, current_section
  - elicitation_completed, validation_status

config_fields:
  - default_mode, validation_enforcement
  - quality_gate_policy, enabled_workflows
```

## Output Template

```
=== CODEX System Status ===

Active Workflow:
  Type: {workflow_type} | Project: {project_name}
  Phase: {current_phase} | Mode: {operation_mode}

Progress:
  Elicitation: {elicitation_completed[current_phase]}
  Validation: {validation_results}

System Health:
  Configuration: ✅ | Workflows Available: {workflow_count}

Available Workflows:
  - {workflow_id}: {workflow_name}
    Purpose: {description}

=== Next Steps ===
{context_appropriate_guidance}
```

## Error Handling

- **No Active Workflow:** "No active workflow detected. Use /codex start"
- **Corrupted State:** Parse partial state, show system status only
- **Missing Config:** Show defaults, suggest checking codex-config.yaml
- **Read Errors:** Display troubleshooting guidance and partial data
