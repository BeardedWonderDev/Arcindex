<!-- Powered by CODEX™ Core -->

# Invoke Quality Gate Task

## Purpose
Reusable task for invoking quality gate validation at phase transitions.

## Inputs
- **phase**: string (discovery|analyst|pm|architect|prp)
- **document**: string (path to document to validate)
- **mode**: string (interactive|batch|yolo|from_config)

## Execution Steps

### Step 1: Read Configuration
Read `.codex/config/codex-config.yaml` to get enforcement mode and minimum score for the current phase.

### Step 2: Invoke Quality Gate Agent
Use Task tool to spawn quality-gate agent with `validate-{phase}` command:

```
Task(
  subagent_type: "general-purpose",
  description: "Quality gate validation for {phase}",
  prompt: "Execute .codex/agents/quality-gate.md with validate-{phase} command on {document}"
)
```

### Step 3: Parse Results
Extract from quality gate agent output:
- **score**: 0-100 numeric score
- **status**: APPROVED | CONDITIONAL | REJECTED
- **recommendations**: array of improvement suggestions
- **evidence**: validation evidence collected

### Step 4: Apply Enforcement Policy
Based on `config.enforcement` setting (strict|conditional|advisory):

**strict mode**:
- APPROVED (score ≥90): Allow progression
- CONDITIONAL (70-89): Allow progression with warnings
- REJECTED (score <70): BLOCK progression, halt workflow

**conditional mode**:
- APPROVED: Allow progression
- CONDITIONAL: Prompt user for decision
- REJECTED: Prompt user for decision (with strong warning)

**advisory mode**:
- All statuses: Allow progression, display recommendations

### Step 5: Update State
Save results to `workflow.json` via state-manager:

```json
{
  "quality_gate_results": {
    "{phase}": {
      "score": 85,
      "status": "CONDITIONAL",
      "timestamp": "2025-10-08T21:00:00Z",
      "recommendations": [...],
      "allow_progression": true
    }
  }
}
```

## Output
Returns structured result:
```json
{
  "success": true,
  "score": 85,
  "status": "CONDITIONAL",
  "allow_progression": true,
  "recommendations": [...]
}
```

## Usage Examples

### Example 1: From Orchestrator
```
When orchestrator completes analyst phase:
invoke-quality-gate(
  phase: "analyst",
  document: "docs/project-brief.md",
  mode: "from_config"
)
```

### Example 2: From Validation Gate
```
After Level 0 validation passes:
invoke-quality-gate(
  phase: "discovery",
  document: "docs/discovery-notes.md",
  mode: "interactive"
)
```

### Example 3: Manual Execution
```
User requests quality check:
invoke-quality-gate(
  phase: "architect",
  document: "docs/architecture.md",
  mode: "batch"
)
```

## Error Handling
- Missing document: Return error, do not proceed
- Invalid phase: Return error with valid phase list
- Quality gate agent failure: Log error, apply fallback policy (allow/block based on config)
- Timeout: Apply timeout policy (default: allow with warning)

## Notes
- This task is optional - controlled by configuration
- Does not replace other validation levels (0-4)
- Provides quality metrics and continuous improvement
- Can be disabled without affecting core workflow
