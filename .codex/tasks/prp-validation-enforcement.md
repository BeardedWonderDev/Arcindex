# PRP Validation Enforcement Task

## Purpose

**Phase 0 Validation Gate**: Enforce comprehensive PRP quality validation BEFORE execution begins. Ensures PRPs meet minimum quality standards (≥90 score) through automated checks and verification logging.

## Context

This is the **Phase 0** gate from the 4-level progressive validation system, executed BEFORE dev agent begins implementation. Prevents poor-quality PRPs from entering execution phase.

## Inputs

```yaml
inputs:
  required:
    prp_file:
      type: string
      format: "PRPs/{feature-name}.md"
      description: "Path to PRP file to validate"
      example: "PRPs/user-authentication.md"

    validation_checklist:
      type: string
      format: ".codex/data/prp-quality-checklist.md"
      description: "PRP quality gate checklist"
      default: ".codex/data/prp-quality-checklist.md"

  optional:
    min_score:
      type: integer
      default: 90
      range: [0, 100]
      description: "Minimum passing score (default: 90)"

    create_log:
      type: boolean
      default: true
      description: "Create verification log file"
```

## Prerequisites

```yaml
prerequisites:
  - PRP file exists and is readable
  - PRP quality checklist exists (.codex/data/prp-quality-checklist.md)
  - workflow.json exists with current workflow state
  - Dev agent NOT yet started (pre-execution gate)
```

## Workflow Steps

### Step 1: Initialize Validation

```bash
echo "🔍 Phase 0: PRP Validation Enforcement"
echo "=========================================="
echo ""
echo "PRP File: $PRP_FILE"
echo "Minimum Score: ${MIN_SCORE:-90}"
echo ""

# Check PRP file exists
if [ ! -f "$PRP_FILE" ]; then
    echo "❌ ERROR: PRP file not found: $PRP_FILE"
    exit 1
fi

# Check checklist exists
CHECKLIST="${VALIDATION_CHECKLIST:-.codex/data/prp-quality-checklist.md}"
if [ ! -f "$CHECKLIST" ]; then
    echo "❌ ERROR: Quality checklist not found: $CHECKLIST"
    exit 1
fi

echo "✅ Validation prerequisites met"
echo ""
```

### Step 2: File Reference Validation

```bash
echo "📋 Validating File References..."
echo ""

# Extract file paths from PRP (looking for patterns like src/path/to/file.swift)
FILE_REFS=$(grep -oP '(?<=FOLLOW pattern: |CREATE |MODIFY )[^\s:]+\.(swift|py|js|ts|go|java|kt|rs|md|yaml|json)' "$PRP_FILE" || true)

MISSING_FILES=0
TOTAL_REFS=0

if [ -n "$FILE_REFS" ]; then
    while IFS= read -r file_path; do
        TOTAL_REFS=$((TOTAL_REFS + 1))

        # Check if file exists (for FOLLOW pattern references)
        if echo "$file_path" | grep -q "^src/\|^lib/\|^app/\|^tests/\|^docs/"; then
            if [ -f "$file_path" ]; then
                echo "  ✅ $file_path (exists)"
            else
                echo "  ⚠️  $file_path (not found - may be created during execution)"
            fi
        else
            echo "  ℹ️  $file_path (reference noted)"
        fi
    done <<< "$FILE_REFS"

    echo ""
    echo "Total file references: $TOTAL_REFS"
else
    echo "  ℹ️  No specific file references found"
fi

echo ""
```

### Step 3: URL Accessibility Validation

```bash
echo "🌐 Validating URL References..."
echo ""

# Extract URLs from PRP
URLS=$(grep -oP 'https?://[^\s\)]+' "$PRP_FILE" || true)

INVALID_URLS=0
TOTAL_URLS=0

if [ -n "$URLS" ]; then
    while IFS= read -r url; do
        TOTAL_URLS=$((TOTAL_URLS + 1))

        # Check if URL has section anchor (good practice)
        if echo "$url" | grep -q '#'; then
            echo "  ✅ $url (has section anchor)"
        else
            echo "  ⚠️  $url (no section anchor - consider adding for specificity)"
        fi

        # Optional: Actually check URL accessibility (can be slow)
        # if curl --output /dev/null --silent --head --fail "$url" 2>/dev/null; then
        #     echo "  ✅ $url (accessible)"
        # else
        #     echo "  ❌ $url (not accessible)"
        #     INVALID_URLS=$((INVALID_URLS + 1))
        # fi
    done <<< "$URLS"

    echo ""
    echo "Total URL references: $TOTAL_URLS"

    if [ $INVALID_URLS -gt 0 ]; then
        echo "⚠️  WARNING: $INVALID_URLS URLs not accessible"
    fi
else
    echo "  ℹ️  No URL references found"
fi

echo ""
```

### Step 4: Implementation Task Validation

```bash
echo "📝 Validating Implementation Tasks..."
echo ""

# Extract task count from PRP
TASK_COUNT=$(grep -c "^Task [0-9]\+:" "$PRP_FILE" || echo "0")

echo "Total implementation tasks: $TASK_COUNT"

if [ "$TASK_COUNT" -eq 0 ]; then
    echo "❌ ERROR: No implementation tasks found in PRP"
    echo "PRPs must have at least one implementation task"
    exit 1
elif [ "$TASK_COUNT" -lt 3 ]; then
    echo "⚠️  WARNING: Very few tasks ($TASK_COUNT) - consider breaking down further"
else
    echo "✅ Task count appropriate"
fi

# Check for task specificity (CREATE/MODIFY keywords)
SPECIFIC_TASKS=$(grep -c "^Task [0-9]\+:.*\(CREATE\|MODIFY\|ADD\|UPDATE\|DELETE\|IMPLEMENT\)" "$PRP_FILE" || echo "0")

if [ "$SPECIFIC_TASKS" -lt "$((TASK_COUNT / 2))" ]; then
    echo "⚠️  WARNING: Many tasks lack specific action verbs (CREATE/MODIFY/etc.)"
else
    echo "✅ Tasks use specific action verbs"
fi

echo ""
```

### Step 5: Validation Command Verification

```bash
echo "🔧 Validating Validation Commands..."
echo ""

# Check for validation level commands in PRP
HAS_LEVEL_1=$(grep -q "Level 1.*Validation\|Syntax.*Style" "$PRP_FILE" && echo "yes" || echo "no")
HAS_LEVEL_2=$(grep -q "Level 2.*Validation\|Unit.*Test" "$PRP_FILE" && echo "yes" || echo "no")
HAS_LEVEL_3=$(grep -q "Level 3.*Validation\|Integration.*Test" "$PRP_FILE" && echo "yes" || echo "no")
HAS_LEVEL_4=$(grep -q "Level 4.*Validation\|Domain.*Specific" "$PRP_FILE" && echo "yes" || echo "no")

echo "Validation level coverage:"
echo "  Level 1 (Syntax/Style): $HAS_LEVEL_1"
echo "  Level 2 (Unit Tests): $HAS_LEVEL_2"
echo "  Level 3 (Integration): $HAS_LEVEL_3"
echo "  Level 4 (Domain Specific): $HAS_LEVEL_4"

VALIDATION_SCORE=0
[ "$HAS_LEVEL_1" = "yes" ] && VALIDATION_SCORE=$((VALIDATION_SCORE + 25))
[ "$HAS_LEVEL_2" = "yes" ] && VALIDATION_SCORE=$((VALIDATION_SCORE + 25))
[ "$HAS_LEVEL_3" = "yes" ] && VALIDATION_SCORE=$((VALIDATION_SCORE + 25))
[ "$HAS_LEVEL_4" = "yes" ] && VALIDATION_SCORE=$((VALIDATION_SCORE + 25))

echo ""
echo "Validation coverage score: $VALIDATION_SCORE/100"

if [ "$VALIDATION_SCORE" -lt 75 ]; then
    echo "⚠️  WARNING: Incomplete validation coverage (< 75%)"
else
    echo "✅ Good validation coverage"
fi

echo ""
```

### Step 6: Context Completeness Check

```bash
echo "📊 Context Completeness Check..."
echo ""

# Check for essential PRP sections
SECTIONS_FOUND=0
SECTIONS_TOTAL=7

grep -q "## Goal\|##  Goal" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Goal section" || echo "  ❌ Missing Goal section"
grep -q "## Why\|##  Why" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Why section" || echo "  ❌ Missing Why section"
grep -q "## What\|##  What" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ What section" || echo "  ❌ Missing What section"
grep -q "## Context\|##  Context" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Context section" || echo "  ❌ Missing Context section"
grep -q "## Implementation\|##  Implementation" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Implementation section" || echo "  ❌ Missing Implementation section"
grep -q "## Validation\|##  Validation" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Validation section" || echo "  ❌ Missing Validation section"
grep -q "## Final.*Checklist\|##  Final.*Checklist" "$PRP_FILE" && SECTIONS_FOUND=$((SECTIONS_FOUND + 1)) && echo "  ✅ Final Checklist" || echo "  ❌ Missing Final Checklist"

echo ""
echo "Essential sections: $SECTIONS_FOUND/$SECTIONS_TOTAL"

SECTION_SCORE=$((SECTIONS_FOUND * 100 / SECTIONS_TOTAL))
echo "Section completeness: $SECTION_SCORE%"

if [ "$SECTION_SCORE" -lt 85 ]; then
    echo "❌ ERROR: Missing critical PRP sections (< 85%)"
    exit 1
else
    echo "✅ All essential sections present"
fi

echo ""
```

### Step 7: Calculate Overall Score

```bash
echo "🎯 Calculating Overall PRP Quality Score..."
echo ""

# Scoring components (weighted)
FILE_REF_SCORE=100  # Assume perfect unless issues found
URL_SCORE=100       # Assume perfect unless issues found
TASK_SCORE=$((TASK_COUNT >= 3 ? 100 : TASK_COUNT * 33))
CONTEXT_SCORE=$SECTION_SCORE
VALIDATION_SCORE=$VALIDATION_SCORE

# Weighted average
OVERALL_SCORE=$(( (FILE_REF_SCORE * 15 + URL_SCORE * 15 + TASK_SCORE * 20 + CONTEXT_SCORE * 25 + VALIDATION_SCORE * 25) / 100 ))

echo "Score Breakdown:"
echo "  File References: $FILE_REF_SCORE/100 (weight: 15%)"
echo "  URL References: $URL_SCORE/100 (weight: 15%)"
echo "  Task Quality: $TASK_SCORE/100 (weight: 20%)"
echo "  Context Completeness: $CONTEXT_SCORE/100 (weight: 25%)"
echo "  Validation Coverage: $VALIDATION_SCORE/100 (weight: 25%)"
echo ""
echo "═══════════════════════════════════════"
echo "OVERALL PRP QUALITY SCORE: $OVERALL_SCORE/100"
echo "═══════════════════════════════════════"
echo ""
```

### Step 8: Enforce Minimum Score

```bash
MIN_SCORE=${MIN_SCORE:-90}

if [ "$OVERALL_SCORE" -lt "$MIN_SCORE" ]; then
    echo "❌ VALIDATION FAILED: Score $OVERALL_SCORE < minimum $MIN_SCORE"
    echo ""
    echo "PRP quality is below acceptable threshold."
    echo "Improvements needed before execution can begin."
    echo ""
    echo "Recommended actions:"
    echo "  1. Review missing sections and add them"
    echo "  2. Enhance task specificity with action verbs"
    echo "  3. Add comprehensive validation commands for all 4 levels"
    echo "  4. Include specific file paths and URL section anchors"
    echo "  5. Run PRP creator *validate command for detailed feedback"
    echo ""
    exit 1
else
    echo "✅ VALIDATION PASSED: Score $OVERALL_SCORE >= minimum $MIN_SCORE"
    echo ""
    echo "PRP meets quality standards for execution."
fi
```

### Step 9: Create Verification Log

```bash
if [ "${CREATE_LOG:-true}" = "true" ]; then
    echo "📄 Creating Verification Log..."

    LOG_DIR=".codex/state/validation-logs"
    mkdir -p "$LOG_DIR"

    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")
    LOG_FILE="$LOG_DIR/prp-validation-${TIMESTAMP}.log"

    cat > "$LOG_FILE" <<EOF
# PRP Validation Log

**Timestamp:** $TIMESTAMP
**PRP File:** $PRP_FILE
**Min Score:** $MIN_SCORE
**Overall Score:** $OVERALL_SCORE
**Result:** $([ "$OVERALL_SCORE" -ge "$MIN_SCORE" ] && echo "PASSED" || echo "FAILED")

---

## Score Breakdown

- File References: $FILE_REF_SCORE/100 (15%)
- URL References: $URL_SCORE/100 (15%)
- Task Quality: $TASK_SCORE/100 (20%)
- Context Completeness: $CONTEXT_SCORE/100 (25%)
- Validation Coverage: $VALIDATION_SCORE/100 (25%)

**Overall:** $OVERALL_SCORE/100

---

## Section Coverage

EOF

    grep -q "## Goal" "$PRP_FILE" && echo "- [x] Goal" >> "$LOG_FILE" || echo "- [ ] Goal" >> "$LOG_FILE"
    grep -q "## Why" "$PRP_FILE" && echo "- [x] Why" >> "$LOG_FILE" || echo "- [ ] Why" >> "$LOG_FILE"
    grep -q "## What" "$PRP_FILE" && echo "- [x] What" >> "$LOG_FILE" || echo "- [ ] What" >> "$LOG_FILE"
    grep -q "## Context" "$PRP_FILE" && echo "- [x] Context" >> "$LOG_FILE" || echo "- [ ] Context" >> "$LOG_FILE"
    grep -q "## Implementation" "$PRP_FILE" && echo "- [x] Implementation" >> "$LOG_FILE" || echo "- [ ] Implementation" >> "$LOG_FILE"
    grep -q "## Validation" "$PRP_FILE" && echo "- [x] Validation" >> "$LOG_FILE" || echo "- [ ] Validation" >> "$LOG_FILE"
    grep -q "## Final.*Checklist" "$PRP_FILE" && echo "- [x] Final Checklist" >> "$LOG_FILE" || echo "- [ ] Final Checklist" >> "$LOG_FILE"

    cat >> "$LOG_FILE" <<EOF

---

## Validation Level Coverage

- Level 1 (Syntax/Style): $HAS_LEVEL_1
- Level 2 (Unit Tests): $HAS_LEVEL_2
- Level 3 (Integration): $HAS_LEVEL_3
- Level 4 (Domain Specific): $HAS_LEVEL_4

---

## Summary

- Total Implementation Tasks: $TASK_COUNT
- Total File References: $TOTAL_REFS
- Total URL References: $TOTAL_URLS

EOF

    echo "✅ Verification log created: $LOG_FILE"
fi
```

### Step 10: Update workflow.json

```bash
echo "💾 Updating workflow.json with validation results..."

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")

# Update validation_results.level_0 in workflow.json
WORKFLOW_STATE=$(cat .codex/state/workflow.json)

UPDATED_STATE=$(echo "$WORKFLOW_STATE" | jq \
  --arg timestamp "$TIMESTAMP" \
  --argjson passed "$([ "$OVERALL_SCORE" -ge "$MIN_SCORE" ] && echo 'true' || echo 'false')" \
  --argjson score "$OVERALL_SCORE" \
  '.validation_results.level_0.passed = $passed |
   .validation_results.level_0.last_check = $timestamp |
   .validation_results.level_0.score = $score |
   .validation_results.level_0.violations = []')

echo "$UPDATED_STATE" > .codex/state/workflow.json

echo "✅ workflow.json updated with Phase 0 validation results"
echo ""
```

## Outputs

```yaml
outputs:
  console_output:
    overall_score: "0-100"
    result: "PASSED | FAILED"
    log_file: ".codex/state/validation-logs/prp-validation-{timestamp}.log"

  workflow_state:
    file: ".codex/state/workflow.json"
    updates:
      - validation_results.level_0.passed
      - validation_results.level_0.score
      - validation_results.level_0.last_check

  verification_log:
    file: ".codex/state/validation-logs/prp-validation-{timestamp}.log"
    format: "Markdown"
    content:
      - Timestamp and PRP file
      - Score breakdown
      - Section coverage checklist
      - Validation level coverage
      - Summary statistics

  exit_code:
    0: "Validation passed (score >= min_score)"
    1: "Validation failed (score < min_score)"
```

## Integration Points

### Dev Agent Integration

Dev agent MUST run this validation before beginning implementation:

```yaml
dev_agent_workflow:
  step_0_prp_validation:
    task: "prp-validation-enforcement.md"
    blocking: true
    min_score: 90
    on_failure: "HALT execution, report issues to user"
    on_success: "Proceed with ULTRATHINK planning"
```

### PRP Creator Integration

PRP creator can run this during *validate command:

```yaml
prp_creator_validate:
  command: "*validate"
  invokes: "prp-validation-enforcement.md"
  interactive: true
  display_score: true
  allow_iteration: true
```

## Success Criteria

```yaml
success_indicators:
  - Overall score >= 90 (configurable)
  - All essential sections present
  - Validation levels 1-4 defined
  - Implementation tasks specific and actionable
  - Verification log created
  - workflow.json updated with results
  - Exit code 0 (passing)

failure_indicators:
  - Overall score < 90
  - Missing critical sections
  - No validation commands
  - Vague implementation tasks
  - Exit code 1 (failing)
```

## Anti-Patterns

```yaml
anti_patterns:
  skip_validation:
    bad: "Dev agent starts without running Phase 0"
    good: "Dev agent MUST run Phase 0 before ULTRATHINK"

  ignore_score:
    bad: "Proceed with score of 75/100"
    good: "Improve PRP until score >= 90"

  no_verification_log:
    bad: "Skip creating verification log"
    good: "Always create log for audit trail"

  manual_score_override:
    bad: "User manually sets score to passing"
    good: "Improve PRP quality to pass automated checks"
```
