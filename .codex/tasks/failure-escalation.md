# Failure Escalation Protocol

## Purpose

4-level escalation protocol for PRP execution failures. Automatically retries, analyzes patterns, requests intervention, and creates checkpoints based on failure count.

## Escalation Levels

```yaml
levels:
  level_1:
    range: "0-3 failures"
    action: "Automatic retry with same approach"
    rationale: "Transient issues, no pattern yet"

  level_2:
    range: "4-6 failures"
    action: "Pattern analysis and approach modification"
    rationale: "Systematic issue, need different strategy"

  level_3:
    range: "7+ failures"
    action: "User intervention required"
    rationale: "Blocking issue beyond automation"

  level_4:
    trigger: "User abort or unrecoverable error"
    action: "Create checkpoint and halt gracefully"
    rationale: "Preserve work, enable later resumption"
```

## Inputs

```yaml
inputs:
  required:
    failure_context:
      validation_level: "1|2|3|4"  # Which validation level failed
      error_message: string
      failed_task: string  # PRP task that failed
      attempt_count: integer

  optional:
    prp_file: string  # For pattern analysis
    implementation_files: array  # Files modified so far
```

## Workflow

### Level 1: Auto-Retry (0-3 failures)

```bash
if [ "$ATTEMPT_COUNT" -le 3 ]; then
    echo "🔄 Level 1 Escalation: Auto-Retry"
    echo "Attempt: $ATTEMPT_COUNT/3"
    echo "Action: Retrying with same approach"
    echo ""
    echo "Error: $ERROR_MESSAGE"
    echo ""

    # Brief pause before retry
    sleep 2

    # Retry same command
    exit 2  # Signal retry
fi
```

### Level 2: Pattern Analysis (4-6 failures)

```bash
if [ "$ATTEMPT_COUNT" -ge 4 ] && [ "$ATTEMPT_COUNT" -le 6 ]; then
    echo "🔍 Level 2 Escalation: Pattern Analysis"
    echo "Attempt: $ATTEMPT_COUNT"
    echo "Action: Analyzing failure pattern and modifying approach"
    echo ""

    # Pattern analysis
    echo "Analyzing common failure patterns..."

    # Check error type
    if echo "$ERROR_MESSAGE" | grep -qi "not found\|missing\|no such file"; then
        echo "  Pattern: Missing file/dependency"
        echo "  Strategy: Verify file paths, check prerequisites"
    elif echo "$ERROR_MESSAGE" | grep -qi "syntax\|parse\|compile"; then
        echo "  Pattern: Syntax error"
        echo "  Strategy: Review PRP syntax requirements, check examples"
    elif echo "$ERROR_MESSAGE" | grep -qi "permission\|access denied"; then
        echo "  Pattern: Permission issue"
        echo "  Strategy: Check file permissions, run with appropriate access"
    elif echo "$ERROR_MESSAGE" | grep -qi "timeout\|timed out"; then
        echo "  Pattern: Timeout"
        echo "  Strategy: Increase timeout, optimize operation"
    else
        echo "  Pattern: Unknown (custom analysis needed)"
        echo "  Strategy: Review PRP gotchas, consult anti-patterns"
    fi

    echo ""
    echo "Recommended Actions:"
    echo "  1. Review PRP gotchas section for this specific issue"
    echo "  2. Check anti-patterns to avoid known failures"
    echo "  3. Consult PRP Context for alternative approaches"
    echo "  4. Verify all prerequisites are met"
    echo ""

    exit 3  # Signal pattern-based retry
fi
```

### Level 3: User Intervention (7+ failures)

```bash
if [ "$ATTEMPT_COUNT" -ge 7 ]; then
    echo "⚠️  Level 3 Escalation: User Intervention Required"
    echo "Attempt: $ATTEMPT_COUNT"
    echo "Status: BLOCKED - Cannot proceed automatically"
    echo ""
    echo "════════════════════════════════════════"
    echo "FAILURE ESCALATION - USER ACTION NEEDED"
    echo "════════════════════════════════════════"
    echo ""
    echo "Failed Task: $FAILED_TASK"
    echo "Validation Level: Level $VALIDATION_LEVEL"
    echo "Error: $ERROR_MESSAGE"
    echo ""
    echo "After 7 attempts, automatic resolution has failed."
    echo "This indicates a blocking issue requiring human intervention."
    echo ""
    echo "Options:"
    echo "  1. Review error and PRP guidance, then manually fix"
    echo "  2. Request feedback from PRP creator (*request-feedback)"
    echo "  3. Create checkpoint and pause for later (*checkpoint)"
    echo "  4. Abort implementation and report issues (*abort)"
    echo ""
    echo "Recommendation: Review PRP Context and Gotchas sections"
    echo "for guidance specific to this validation level."
    echo ""

    # Create escalation record
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")
    ESCALATION_FILE=".codex/state/escalations/escalation-${TIMESTAMP}.md"
    mkdir -p .codex/state/escalations

    cat > "$ESCALATION_FILE" <<EOF
# Escalation Report

**Timestamp:** $TIMESTAMP
**Level:** 3 (User Intervention)
**Attempt Count:** $ATTEMPT_COUNT
**Status:** BLOCKED

---

## Failure Context

**Failed Task:** $FAILED_TASK
**Validation Level:** Level $VALIDATION_LEVEL
**Error Message:**
\`\`\`
$ERROR_MESSAGE
\`\`\`

---

## Escalation History

- Attempts 1-3: Auto-retry
- Attempts 4-6: Pattern analysis and modified approach
- Attempt 7+: USER INTERVENTION REQUIRED

---

## Recommended Actions

1. Review PRP file: $PRP_FILE
   - Check Gotchas section for this specific error
   - Review Anti-Patterns to avoid known failures
   - Consult Context section for alternative approaches

2. Analyze implementation so far:
EOF

    if [ -n "$IMPLEMENTATION_FILES" ]; then
        echo "   - Files modified:" >> "$ESCALATION_FILE"
        for file in $IMPLEMENTATION_FILES; do
            echo "     - $file" >> "$ESCALATION_FILE"
        done
    fi

    cat >> "$ESCALATION_FILE" <<EOF

3. Consider feedback request:
   - *request-feedback prp-creator "Level $VALIDATION_LEVEL failing after $ATTEMPT_COUNT attempts: $ERROR_MESSAGE"

4. Create checkpoint for later:
   - *checkpoint "Blocked at Level $VALIDATION_LEVEL - user intervention needed"

---

## Next Steps

- [ ] Review PRP guidance
- [ ] Analyze error in context
- [ ] Attempt manual fix
- [ ] OR request feedback
- [ ] OR create checkpoint and pause
EOF

    echo "📄 Escalation report created: $ESCALATION_FILE"
    echo ""

    exit 4  # Signal user intervention needed
fi
```

### Level 4: Checkpoint & Abort (Unrecoverable)

```bash
# Triggered by user abort or unrecoverable error
create_checkpoint_and_abort() {
    echo "🛑 Level 4 Escalation: Checkpoint & Abort"
    echo "Action: Creating checkpoint and halting gracefully"
    echo ""

    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")
    CHECKPOINT_DIR=".codex/state/checkpoints"
    mkdir -p "$CHECKPOINT_DIR"

    CHECKPOINT_ID="checkpoint-${TIMESTAMP}"
    CHECKPOINT_FILE="$CHECKPOINT_DIR/${CHECKPOINT_ID}.json"

    # Create checkpoint with current state
    cat > "$CHECKPOINT_FILE" <<EOF
{
  "checkpoint_id": "$CHECKPOINT_ID",
  "timestamp": "$TIMESTAMP",
  "reason": "Escalation Level 4 - Unrecoverable failure",
  "context": {
    "failed_task": "$FAILED_TASK",
    "validation_level": $VALIDATION_LEVEL,
    "attempt_count": $ATTEMPT_COUNT,
    "error_message": "$ERROR_MESSAGE",
    "prp_file": "$PRP_FILE"
  },
  "implementation_progress": {
    "files_modified": $(echo "$IMPLEMENTATION_FILES" | jq -R -s 'split("\n") | map(select(length > 0))'),
    "validation_levels_passed": [],
    "current_level": $VALIDATION_LEVEL,
    "current_level_status": "failed"
  },
  "resumption_guidance": {
    "review_escalation_report": ".codex/state/escalations/latest",
    "review_prp_gotchas": true,
    "consider_prp_update": true,
    "user_intervention_required": true
  }
}
EOF

    echo "✅ Checkpoint created: $CHECKPOINT_ID"
    echo "📁 Location: $CHECKPOINT_FILE"
    echo ""
    echo "Work preserved. Implementation can be resumed later with:"
    echo "  /codex continue --from-checkpoint $CHECKPOINT_ID"
    echo ""

    exit 5  # Signal checkpoint created, graceful abort
}
```

## Integration with workflow.json

```yaml
workflow_integration:
  escalation_tracking:
    field: "workflow.json → failure_escalations[]"
    structure:
      - escalation_id: "esc-{timestamp}"
      - level: "1|2|3|4"
      - failed_task: string
      - attempt_count: integer
      - resolution: "retried|modified|user_intervention|checkpointed"
      - timestamp: ISO-8601

  state_updates:
    on_escalation:
      - Add entry to failure_escalations array
      - Update validation_results for current level
      - Log transformation_history event
```

## Usage Examples

### Dev Agent Integration

```yaml
dev_agent_validation:
  on_validation_failure:
    step_1: "Capture failure context"
    step_2: "Invoke failure-escalation.md with context"
    step_3: "Handle exit code:"
      2: "Retry same approach (Level 1)"
      3: "Modify approach based on pattern analysis (Level 2)"
      4: "Request user intervention (Level 3)"
      5: "Checkpoint created, halt execution (Level 4)"
```

### Pattern-Based Retry Example

```bash
# After Level 2 pattern analysis identifies missing file
if [ "$EXIT_CODE" -eq 3 ]; then
    echo "Applying pattern-based fix: Verifying file paths"

    # Re-read PRP to find correct file path
    CORRECT_PATH=$(grep "FOLLOW pattern:" "$PRP_FILE" | head -1 | awk '{print $3}')

    if [ -f "$CORRECT_PATH" ]; then
        echo "✅ Found reference file: $CORRECT_PATH"
        # Retry with corrected understanding
    else
        echo "❌ Reference file still not found, escalating further"
        ATTEMPT_COUNT=$((ATTEMPT_COUNT + 1))
    fi
fi
```

## Success Indicators

```yaml
success_criteria:
  level_1:
    - Retry succeeds within 3 attempts
    - Transient issue resolved

  level_2:
    - Pattern identified correctly
    - Modified approach succeeds
    - Issue documented for future prevention

  level_3:
    - User receives clear escalation report
    - Actionable guidance provided
    - Feedback mechanism available

  level_4:
    - Checkpoint created successfully
    - All work preserved
    - Resumption instructions clear
```

## Anti-Patterns

```yaml
anti_patterns:
  infinite_retry:
    bad: "Retry indefinitely without escalation"
    good: "Escalate after 3 attempts, analyze after 6"

  no_pattern_analysis:
    bad: "Keep trying same approach at Level 2"
    good: "Analyze error pattern, modify strategy"

  unclear_user_guidance:
    bad: "Just say 'failed, need help'"
    good: "Provide specific escalation report with actions"

  lose_work_on_abort:
    bad: "Exit without saving progress"
    good: "Create checkpoint with all context before abort"
```
