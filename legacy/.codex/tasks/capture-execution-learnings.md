# Capture Execution Learnings Task

## Purpose

Capture execution learnings during PRP implementation to improve future PRP quality and enable progressive learning across epics.

## Inputs

```yaml
inputs:
  required:
    prp_file:
      type: string
      description: "Path to the PRP being executed"
      example: "PRPs/epic-1/user-authentication.md"

    epic_number:
      type: integer
      description: "Epic number being implemented"
      example: 1

    story_number:
      type: integer
      description: "Story number within epic"
      example: 3

    action:
      type: string
      values: [start, level_complete, final]
      description: "Execution tracking action"

  optional:
    validation_level:
      type: integer
      values: [0, 1, 2, 3, 4]
      description: "Validation level completed (for level_complete action)"

    validation_passed:
      type: boolean
      description: "Whether validation level passed"

    attempts:
      type: integer
      description: "Number of attempts for this validation level"

    issues_encountered:
      type: array
      description: "Issues found during validation"

    estimated_hours:
      type: number
      description: "Estimated duration from PRP (for start action)"

    actual_hours:
      type: number
      description: "Actual duration (for final action)"
```

## Prerequisites

```yaml
prerequisites:
  - Workflow state exists (.codex/state/workflow.json)
  - PRP file exists and is accessible
  - execution-reports directory exists (.codex/state/execution-reports/)
```

## Workflow Steps

### Step 1: Initialize or Load Execution Report

```bash
# Determine report file path
REPORT_FILE=".codex/state/execution-reports/epic-${EPIC_NUM}-story-${STORY_NUM}.json"

# Check if report exists
if [ "$ACTION" == "start" ]; then
    # Create new execution report
    cat > "$REPORT_FILE" <<EOF
{
  "report_id": "report-$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "prp_file": "$PRP_FILE",
  "epic": "Epic $EPIC_NUM",
  "story": "Story $STORY_NUM",
  "start_time": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "end_time": null,
  "estimated_duration_hours": ${ESTIMATED_HOURS:-0},
  "actual_duration_hours": null,
  "validation_results": {
    "level_0": {"passed": false, "attempts": 0, "issues": []},
    "level_1": {"passed": false, "attempts": 0, "issues": []},
    "level_2": {"passed": false, "attempts": 0, "issues": []},
    "level_3": {"passed": false, "attempts": 0, "issues": []},
    "level_4": {"passed": false, "attempts": 0, "issues": []}
  },
  "prp_quality_issues": [],
  "patterns_that_worked": [],
  "missing_or_incorrect_info": [],
  "gotchas_discovered": [],
  "prp_quality_assessment": 0,
  "improvements_for_next_prp": [],
  "patterns_to_reuse": [],
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"
}
EOF
    echo "✅ Initialized execution report: $REPORT_FILE"
else
    # Load existing report
    if [ ! -f "$REPORT_FILE" ]; then
        echo "❌ ERROR: Execution report not found: $REPORT_FILE"
        echo "   Run with action=start first to initialize report"
        exit 1
    fi
    echo "✅ Loaded existing execution report: $REPORT_FILE"
fi
```

### Step 2: Update Validation Results (level_complete action)

```bash
if [ "$ACTION" == "level_complete" ]; then
    echo "📝 Updating validation results for Level $VALIDATION_LEVEL..."
    
    # Read current report
    REPORT=$(cat "$REPORT_FILE")
    
    # Create issues array for jq
    if [ -n "$ISSUES_ENCOUNTERED" ]; then
        ISSUES_JSON=$(echo "$ISSUES_ENCOUNTERED" | jq -R 'split(",") | map(. | gsub("^\\s+|\\s+$";""))')
    else
        ISSUES_JSON="[]"
    fi
    
    # Update validation results for this level
    UPDATED_REPORT=$(echo "$REPORT" | jq \
        --arg level "level_$VALIDATION_LEVEL" \
        --argjson passed "$VALIDATION_PASSED" \
        --argjson attempts "$ATTEMPTS" \
        --argjson issues "$ISSUES_JSON" \
        ".validation_results[\$level].passed = \$passed |
         .validation_results[\$level].attempts = \$attempts |
         .validation_results[\$level].issues = \$issues |
         .updated_at = \"$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")\"")
    
    # Write updated report
    echo "$UPDATED_REPORT" > "$REPORT_FILE"
    
    echo "✅ Updated Level $VALIDATION_LEVEL: passed=$VALIDATION_PASSED, attempts=$ATTEMPTS"
fi
```

### Step 3: Capture PRP Quality Issues

```bash
# Prompt dev to capture PRP quality issues encountered
if [ "$ACTION" == "level_complete" ] && [ "$VALIDATION_PASSED" == "false" ]; then
    echo ""
    echo "📋 PRP Quality Issue Capture"
    echo "Were any issues caused by PRP quality (missing info, incorrect references, unclear instructions)?"
    echo "If yes, please describe (or press Enter to skip):"
    read -r PRP_ISSUE
    
    if [ -n "$PRP_ISSUE" ]; then
        # Add PRP quality issue to report
        REPORT=$(cat "$REPORT_FILE")
        UPDATED_REPORT=$(echo "$REPORT" | jq \
            --arg issue "$PRP_ISSUE" \
            --arg level "$VALIDATION_LEVEL" \
            '.prp_quality_issues += [{"level": $level, "issue": $issue, "timestamp": "'"$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"'"}]')
        echo "$UPDATED_REPORT" > "$REPORT_FILE"
        echo "✅ Captured PRP quality issue"
    fi
fi
```

### Step 4: Capture Working Patterns

```bash
if [ "$ACTION" == "level_complete" ] && [ "$VALIDATION_PASSED" == "true" ]; then
    echo ""
    echo "✨ Pattern Capture"
    echo "Did you use any particularly effective patterns or approaches?"
    echo "If yes, please describe (or press Enter to skip):"
    read -r PATTERN
    
    if [ -n "$PATTERN" ]; then
        REPORT=$(cat "$REPORT_FILE")
        UPDATED_REPORT=$(echo "$REPORT" | jq \
            --arg pattern "$PATTERN" \
            --arg level "$VALIDATION_LEVEL" \
            '.patterns_that_worked += [{"level": $level, "pattern": $pattern, "timestamp": "'"$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"'"}]')
        echo "$UPDATED_REPORT" > "$REPORT_FILE"
        echo "✅ Captured working pattern"
    fi
fi
```

### Step 5: Generate Final Report (final action)

```bash
if [ "$ACTION" == "final" ]; then
    echo "📊 Generating final execution report..."
    
    # Read current report
    REPORT=$(cat "$REPORT_FILE")
    
    # Calculate PRP quality assessment (0-100)
    # Base: 100
    # - Each validation failure: -10 points
    # - Each PRP quality issue: -15 points
    # - Missing/incorrect info: -20 points per issue
    
    VALIDATION_FAILURES=$(echo "$REPORT" | jq '[.validation_results[] | select(.passed == false)] | length')
    PRP_ISSUES_COUNT=$(echo "$REPORT" | jq '.prp_quality_issues | length')
    MISSING_INFO_COUNT=$(echo "$REPORT" | jq '.missing_or_incorrect_info | length')
    
    QUALITY_SCORE=$((100 - (VALIDATION_FAILURES * 10) - (PRP_ISSUES_COUNT * 15) - (MISSING_INFO_COUNT * 20)))
    if [ $QUALITY_SCORE -lt 0 ]; then
        QUALITY_SCORE=0
    fi
    
    # Update final report
    FINAL_REPORT=$(echo "$REPORT" | jq \
        --argjson actual "$ACTUAL_HOURS" \
        --argjson quality "$QUALITY_SCORE" \
        ".end_time = \"$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")\" |
         .actual_duration_hours = \$actual |
         .prp_quality_assessment = \$quality |
         .updated_at = \"$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")\"")
    
    echo "$FINAL_REPORT" > "$REPORT_FILE"
    
    echo "✅ Final execution report generated"
    echo "   PRP Quality Score: $QUALITY_SCORE/100"
    echo "   Actual Duration: ${ACTUAL_HOURS}h (Estimated: ${ESTIMATED_HOURS}h)"
fi
```

### Step 6: Extract Improvements for Next PRP

```bash
if [ "$ACTION" == "final" ]; then
    echo ""
    echo "🔍 Improvement Analysis"
    echo "Based on this execution, what improvements should be made to future PRPs?"
    echo "Enter improvements (comma-separated, or press Enter to skip):"
    read -r IMPROVEMENTS
    
    if [ -n "$IMPROVEMENTS" ]; then
        REPORT=$(cat "$REPORT_FILE")
        IMPROVEMENTS_ARRAY=$(echo "$IMPROVEMENTS" | jq -R 'split(",") | map(. | gsub("^\\s+|\\s+$";""))')
        UPDATED_REPORT=$(echo "$REPORT" | jq \
            --argjson improvements "$IMPROVEMENTS_ARRAY" \
            '.improvements_for_next_prp = $improvements')
        echo "$UPDATED_REPORT" > "$REPORT_FILE"
        echo "✅ Captured improvements for next PRP"
    fi
    
    # Extract patterns to reuse
    PATTERNS_COUNT=$(echo "$REPORT" | jq '.patterns_that_worked | length')
    if [ $PATTERNS_COUNT -gt 0 ]; then
        PATTERNS=$(echo "$REPORT" | jq '[.patterns_that_worked[].pattern]')
        UPDATED_REPORT=$(cat "$REPORT_FILE" | jq \
            --argjson patterns "$PATTERNS" \
            '.patterns_to_reuse = $patterns')
        echo "$UPDATED_REPORT" > "$REPORT_FILE"
    fi
fi
```

### Step 7: Update workflow.json

```bash
if [ "$ACTION" == "final" ]; then
    echo "📝 Updating workflow.json with execution report..."
    
    # Add report path to workflow.json execution_reports array
    WORKFLOW=$(cat .codex/state/workflow.json)
    UPDATED_WORKFLOW=$(echo "$WORKFLOW" | jq \
        --arg report "$REPORT_FILE" \
        '.execution_reports += [$report]')
    echo "$UPDATED_WORKFLOW" > .codex/state/workflow.json
    
    # Log to transformation history
    HISTORY_ENTRY=$(cat <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "type": "execution_report_generated",
  "epic": "Epic $EPIC_NUM",
  "story": "Story $STORY_NUM",
  "report_file": "$REPORT_FILE",
  "quality_score": $(cat "$REPORT_FILE" | jq '.prp_quality_assessment')
}
EOF
)
    
    UPDATED_WORKFLOW=$(cat .codex/state/workflow.json | jq \
        --argjson entry "$HISTORY_ENTRY" \
        '.agent_context.transformation_history += [$entry]')
    echo "$UPDATED_WORKFLOW" > .codex/state/workflow.json
    
    echo "✅ Updated workflow.json with execution report"
fi
```

## Outputs

```yaml
outputs:
  execution_report:
    file: .codex/state/execution-reports/epic-{N}-story-{M}.json
    contains:
      - Validation results per level
      - PRP quality issues discovered
      - Patterns that worked
      - Missing or incorrect information
      - Time estimate vs actual
      - Quality assessment score
      - Improvements for next PRP
      - Patterns to reuse
      - Gotchas discovered

  workflow_update:
    file: .codex/state/workflow.json
    changes:
      - execution_reports array updated (on final)
      - transformation_history entry added (on final)
```

## Integration with Epic Learning

The execution reports generated by this task are consumed by:
- `epic-learning-integration.md` - Analyzes reports across an epic
- PRP Creator - Uses learnings to improve Epic N+1 PRPs

## Usage Examples

### Starting PRP Execution

```bash
# At the beginning of PRP execution
PRP_FILE="PRPs/epic-1/user-authentication.md"
EPIC_NUM=1
STORY_NUM=3
ESTIMATED_HOURS=4
ACTION="start"

bash .codex/tasks/capture-execution-learnings.md
```

### After Validation Level Completion

```bash
# After completing Level 2 (Unit Tests)
ACTION="level_complete"
VALIDATION_LEVEL=2
VALIDATION_PASSED=true
ATTEMPTS=2
ISSUES_ENCOUNTERED=""

bash .codex/tasks/capture-execution-learnings.md
```

### After PRP Completion

```bash
# After all validation levels pass
ACTION="final"
ACTUAL_HOURS=5.5

bash .codex/tasks/capture-execution-learnings.md
```

## Success Criteria

```yaml
success_indicators:
  - Execution report created at start
  - Validation results updated per level
  - PRP quality issues captured when failures occur
  - Working patterns captured when levels pass
  - Final report generated with quality assessment
  - workflow.json updated with report reference
  - Improvements extracted for future PRPs
```

## Anti-Patterns

```yaml
anti_patterns:
  skip_capturing:
    bad: "Skip capturing learnings to save time"
    good: "Capture learnings even if quick - future PRPs benefit"

  vague_issues:
    bad: "PRP had problems"
    good: "PRP referenced line 45 in UserService.swift but file is at Services/User/UserService.swift"

  no_patterns:
    bad: "Everything worked as expected"
    good: "Using protocol-oriented approach for dependency injection worked well, reduced test setup time"
```
