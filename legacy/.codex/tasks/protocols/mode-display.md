# Mode Display Protocol

purpose: "Handle /codex mode command to show current operation mode and its behavior characteristics"

## Implementation

```yaml
mode_display_command:
  trigger: "/codex mode"

  implementation_steps:
    - step: "Read workflow state"
      actions:
        - "Use Read tool on .codex/state/workflow.json"
        - "Extract operation_mode field (default: 'interactive' if not set)"
        - "Handle missing/invalid state gracefully"

    - step: "Display mode information"
      actions:
        - "Show current mode with icon and description"
        - "Explain mode-specific behavior"
        - "Provide mode switching instructions"
        - "Show elicitation enforcement level"

    - step: "Error handling"
      conditions:
        - "If workflow.json missing: 'No active workflow. Start with /codex start'"
        - "If state corrupted: 'State file corrupted. Showing default mode (interactive)'"
        - "If mode field missing: Default to interactive mode"
```

## Output Template

```
=== Current Operation Mode ===

Mode: {mode_name} {mode_icon}

{mode_description}

Behavior Characteristics:
{behavior_summary}

Elicitation: {elicitation_behavior}
Validation: {validation_behavior}
User Interaction: {interaction_level}

=== Switch Modes ===
/codex interactive ... Full elicitation mode (recommended)
/codex batch ......... Batch elicitation at phase end
/codex yolo .......... Skip all elicitation (⚠️ use with caution)

Current workflow: {workflow_type}
Current phase: {current_phase}
```

## Mode Descriptions

### Interactive Mode

```yaml
name: "Interactive Mode"
icon: "🔄"
description: "Full elicitation at each phase transition with validation gates"

behavior:
  - "Elicitation menu presented after each agent completes work"
  - "User must select option 1-9 before proceeding to next phase"
  - "Highest quality output through iterative refinement"
  - "Recommended for critical projects and learning workflows"

elicitation: "Required at every phase transition"
validation: "Full Level 0-4 validation enforcement"
interaction: "High - active participation required"
```

### Batch Mode

```yaml
name: "Batch Mode"
icon: "📦"
description: "Minimal interaction with batch elicitation at phase end"

behavior:
  - "Agents complete work without interruption"
  - "Elicitation presented at natural breakpoints only"
  - "Faster workflow with reduced context switching"
  - "Good for experienced users with clear requirements"

elicitation: "Batched at major phase boundaries"
validation: "Focused validation at breakpoints"
interaction: "Medium - periodic confirmation"
```

### YOLO Mode

```yaml
name: "YOLO Mode"
icon: "⚡"
description: "Skip all elicitation confirmations - proceed automatically"

behavior:
  - "⚠️ No elicitation menus or user confirmations"
  - "Agents proceed directly through all phases"
  - "Maximum speed with minimal oversight"
  - "Use only when you fully trust the workflow and inputs"

elicitation: "Disabled - all phases proceed automatically"
validation: "Basic validation only"
interaction: "Minimal - mostly automated"
```
