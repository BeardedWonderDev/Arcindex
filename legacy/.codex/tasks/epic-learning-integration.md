# Epic Learning Integration Task

## Purpose

Apply learnings from Epic N execution to improve Epic N+1 PRP creation through systematic analysis of execution reports and pattern extraction.

## Inputs

```yaml
inputs:
  required:
    completed_epic:
      type: integer
      description: "Epic number that was just completed"
      example: 1

    next_epic:
      type: integer
      description: "Epic number to create PRPs for"
      example: 2

  optional:
    focus_areas:
      type: array
      description: "Specific areas to focus learning extraction"
      example: ["validation_patterns", "prp_quality", "time_estimates"]
```

## Prerequisites

```yaml
prerequisites:
  - Epic N implementation complete
  - Execution reports exist for Epic N (.codex/state/execution-reports/epic-{N}-*.json)
  - Epic N+1 requirements defined in PRD
  - PRP creator ready to create Epic N+1 PRPs
```

## Workflow Steps

### Step 1: Collect Epic N Execution Reports

```bash
echo "📊 Collecting execution reports for Epic $COMPLETED_EPIC..."

# Find all execution reports for the completed epic
REPORT_FILES=(.codex/state/execution-reports/epic-${COMPLETED_EPIC}-story-*.json)

if [ ${#REPORT_FILES[@]} -eq 0 ]; then
    echo "❌ ERROR: No execution reports found for Epic $COMPLETED_EPIC"
    echo "   Expected location: .codex/state/execution-reports/epic-${COMPLETED_EPIC}-story-*.json"
    exit 1
fi

echo "✅ Found ${#REPORT_FILES[@]} execution reports for Epic $COMPLETED_EPIC"
```

### Step 2: Extract Common Patterns

```bash
echo ""
echo "🔍 Analyzing patterns across Epic $COMPLETED_EPIC..."

# Initialize pattern collections
SUCCESSFUL_PATTERNS=()
FAILED_PATTERNS=()
PRP_GAPS=()
VALIDATION_ISSUES=()
TIME_VARIANCES=()

# Analyze each report
for REPORT_FILE in "${REPORT_FILES[@]}"; do
    # Extract successful patterns
    PATTERNS=$(jq -r '.patterns_that_worked[]?.pattern // empty' "$REPORT_FILE")
    if [ -n "$PATTERNS" ]; then
        while IFS= read -r pattern; do
            SUCCESSFUL_PATTERNS+=("$pattern")
        done <<< "$PATTERNS"
    fi
    
    # Extract PRP quality issues
    PRP_ISSUES=$(jq -r '.prp_quality_issues[]?.issue // empty' "$REPORT_FILE")
    if [ -n "$PRP_ISSUES" ]; then
        while IFS= read -r issue; do
            PRP_GAPS+=("$issue")
        done <<< "$PRP_ISSUES"
    fi
    
    # Extract validation issues
    for LEVEL in 0 1 2 3 4; do
        LEVEL_ISSUES=$(jq -r ".validation_results.level_${LEVEL}.issues[]? // empty" "$REPORT_FILE")
        if [ -n "$LEVEL_ISSUES" ]; then
            while IFS= read -r issue; do
                VALIDATION_ISSUES+=("Level $LEVEL: $issue")
            done <<< "$LEVEL_ISSUES"
        fi
    done
    
    # Calculate time variance
    ESTIMATED=$(jq -r '.estimated_duration_hours // 0' "$REPORT_FILE")
    ACTUAL=$(jq -r '.actual_duration_hours // 0' "$REPORT_FILE")
    if [ "$ESTIMATED" != "0" ] && [ "$ACTUAL" != "0" ]; then
        VARIANCE=$(echo "scale=2; ($ACTUAL - $ESTIMATED) / $ESTIMATED * 100" | bc)
        TIME_VARIANCES+=("${VARIANCE}%")
    fi
done

echo "✅ Pattern extraction complete"
echo "   Successful patterns: ${#SUCCESSFUL_PATTERNS[@]}"
echo "   PRP gaps identified: ${#PRP_GAPS[@]}"
echo "   Validation issues: ${#VALIDATION_ISSUES[@]}"
```

### Step 3: Identify Common Issues

```bash
echo ""
echo "🎯 Identifying common issues..."

# Find most common PRP gaps (frequency analysis)
COMMON_GAPS=$(printf '%s\n' "${PRP_GAPS[@]}" | sort | uniq -c | sort -rn | head -5)

echo ""
echo "Top 5 Common PRP Gaps:"
echo "$COMMON_GAPS"

# Find most common validation issues
COMMON_VALIDATION=$(printf '%s\n' "${VALIDATION_ISSUES[@]}" | sort | uniq -c | sort -rn | head -5)

echo ""
echo "Top 5 Common Validation Issues:"
echo "$COMMON_VALIDATION"
```

### Step 4: Calculate Average Time Variance

```bash
echo ""
echo "⏱️  Time Estimate Analysis..."

if [ ${#TIME_VARIANCES[@]} -gt 0 ]; then
    # Calculate average time variance
    TOTAL_VARIANCE=0
    for VARIANCE in "${TIME_VARIANCES[@]}"; do
        # Remove % sign and add to total
        VARIANCE_NUM=$(echo "$VARIANCE" | sed 's/%//')
        TOTAL_VARIANCE=$(echo "$TOTAL_VARIANCE + $VARIANCE_NUM" | bc)
    done
    AVG_VARIANCE=$(echo "scale=2; $TOTAL_VARIANCE / ${#TIME_VARIANCES[@]}" | bc)
    
    echo "Average time estimate variance: ${AVG_VARIANCE}%"
    
    if (( $(echo "$AVG_VARIANCE > 20" | bc -l) )); then
        echo "⚠️  Time estimates consistently off by more than 20%"
        echo "   Recommendation: Adjust Epic $NEXT_EPIC estimates upward"
    fi
else
    echo "No time variance data available"
fi
```

### Step 5: Generate Learning Summary

```bash
echo ""
echo "📝 Generating learning summary for Epic $NEXT_EPIC..."

LEARNING_FILE=".codex/state/epic-learnings/epic-${COMPLETED_EPIC}-learning-summary.md"
mkdir -p .codex/state/epic-learnings

cat > "$LEARNING_FILE" <<EOF
# Epic $COMPLETED_EPIC Learning Summary

**Generated:** $(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")  
**For Use In:** Epic $NEXT_EPIC PRP Creation

---

## Executive Summary

Epic $COMPLETED_EPIC implementation complete with ${#REPORT_FILES[@]} stories executed.

**Key Metrics:**
- Average PRP Quality Score: TBD
- Average Time Variance: ${AVG_VARIANCE}%
- Successful Patterns Discovered: ${#SUCCESSFUL_PATTERNS[@]}
- PRP Gaps Identified: ${#PRP_GAPS[@]}

---

## Successful Patterns to Reuse

$(if [ ${#SUCCESSFUL_PATTERNS[@]} -gt 0 ]; then
    for i in "${!SUCCESSFUL_PATTERNS[@]}"; do
        echo "$((i+1)). ${SUCCESSFUL_PATTERNS[$i]}"
    done
else
    echo "No patterns captured"
fi)

---

## PRP Quality Issues to Address

$(if [ ${#PRP_GAPS[@]} -gt 0 ]; then
    printf '%s\n' "${PRP_GAPS[@]}" | sort | uniq | nl
else
    echo "No PRP quality issues identified"
fi)

---

## Validation Issues Encountered

$(if [ ${#VALIDATION_ISSUES[@]} -gt 0 ]; then
    printf '%s\n' "${VALIDATION_ISSUES[@]}" | sort | uniq | nl
else
    echo "No validation issues encountered"
fi)

---

## Recommendations for Epic $NEXT_EPIC PRPs

### File References
- Verify all file paths exist before including in PRPs
- Use absolute paths from project root
- Include line number ranges for context

### Validation Commands
- Test all validation commands in PRP verification log
- Include expected output examples
- Document command prerequisites

### Time Estimates
$(if [ -n "$AVG_VARIANCE" ] && (( $(echo "$AVG_VARIANCE > 10" | bc -l) )); then
    echo "- Adjust time estimates by ${AVG_VARIANCE}% based on Epic $COMPLETED_EPIC actuals"
else
    echo "- Time estimates were accurate, maintain current estimation approach"
fi)

### Patterns to Apply
$(if [ ${#SUCCESSFUL_PATTERNS[@]} -gt 0 ]; then
    for pattern in "${SUCCESSFUL_PATTERNS[@]:0:3}"; do
        echo "- $pattern"
    done
else
    echo "- No specific patterns to apply"
fi)

---

## Epic $NEXT_EPIC PRP Creation Checklist

Apply these learnings during Epic $NEXT_EPIC PRP creation:

- [ ] Review successful patterns from Epic $COMPLETED_EPIC
- [ ] Address all identified PRP gaps
- [ ] Verify file references exist
- [ ] Test validation commands
- [ ] Adjust time estimates based on variance
- [ ] Include gotchas from Epic $COMPLETED_EPIC in "Known Gotchas" section
- [ ] Reference working patterns in "Implementation Patterns" section
- [ ] Add anti-patterns discovered to "Anti-Patterns to Avoid" section

---

## Execution Report References

$(for REPORT_FILE in "${REPORT_FILES[@]}"; do
    STORY=$(basename "$REPORT_FILE" | sed 's/epic-[0-9]*-story-\([0-9]*\)\.json/Story \1/')
    QUALITY=$(jq -r '.prp_quality_assessment' "$REPORT_FILE")
    echo "- $STORY: PRP Quality Score ${QUALITY}/100 - $REPORT_FILE"
done)

EOF

echo "✅ Learning summary generated: $LEARNING_FILE"
```

### Step 6: Create Learning Integration Checklist

```bash
echo ""
echo "📋 Creating integration checklist for PRP Creator..."

CHECKLIST_FILE=".codex/state/epic-learnings/epic-${NEXT_EPIC}-integration-checklist.md"

cat > "$CHECKLIST_FILE" <<EOF
# Epic $NEXT_EPIC Learning Integration Checklist

**Source:** Epic $COMPLETED_EPIC Execution Learnings  
**Created:** $(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")

Use this checklist when creating Epic $NEXT_EPIC PRPs to ensure Epic $COMPLETED_EPIC learnings are applied.

---

## Pre-PRP Creation Review

- [ ] Read Epic $COMPLETED_EPIC learning summary: $LEARNING_FILE
- [ ] Review top 3 successful patterns
- [ ] Note all PRP gaps to avoid
- [ ] Check time estimate variance guidance

---

## During PRP Creation

### Context Section
- [ ] Include successful patterns from Epic $COMPLETED_EPIC in "Implementation Patterns"
- [ ] Add gotchas from Epic $COMPLETED_EPIC to "Known Gotchas of our codebase"
- [ ] Reference Epic $COMPLETED_EPIC execution reports for similar stories

### File References
$(if [ ${#PRP_GAPS[@]} -gt 0 ] && echo "${PRP_GAPS[@]}" | grep -q "file\|path\|reference"; then
    echo "- [ ] Verify every file reference exists (Issue identified in Epic $COMPLETED_EPIC)"
    echo "- [ ] Use absolute paths from project root"
    echo "- [ ] Test file accessibility with Read tool"
else
    echo "- [ ] Verify file references (standard check)"
fi)

### Validation Commands
$(if [ ${#VALIDATION_ISSUES[@]} -gt 0 ]; then
    echo "- [ ] Test all validation commands (Issues found in Epic $COMPLETED_EPIC)"
    echo "- [ ] Include verification log section"
    echo "- [ ] Document command prerequisites"
else
    echo "- [ ] Verify validation commands work"
fi)

### Time Estimates
$(if [ -n "$AVG_VARIANCE" ]; then
    if (( $(echo "$AVG_VARIANCE > 20" | bc -l) )); then
        echo "- [ ] Adjust estimates upward by ${AVG_VARIANCE}% (Epic $COMPLETED_EPIC ran over)"
    elif (( $(echo "$AVG_VARIANCE < -20" | bc -l) )); then
        echo "- [ ] Review estimates, Epic $COMPLETED_EPIC ran under by ${AVG_VARIANCE}%"
    else
        echo "- [ ] Time estimates were accurate in Epic $COMPLETED_EPIC"
    fi
fi)

---

## Post-PRP Creation Validation

- [ ] Cross-reference with Epic $COMPLETED_EPIC learning summary
- [ ] Confirm all PRP gaps addressed
- [ ] Verify patterns integrated
- [ ] Run PRP quality gate (target: ≥90)

---

## Notes

Add notes during PRP creation on how Epic $COMPLETED_EPIC learnings were applied:

EOF

echo "✅ Integration checklist created: $CHECKLIST_FILE"
```

### Step 7: Update workflow.json

```bash
echo ""
echo "📝 Updating workflow.json with learning summary..."

# Update workflow.json epic_learnings
LEARNING_ENTRY=$(cat <<EOF
{
  "epic_id": $COMPLETED_EPIC,
  "epic_name": "Epic $COMPLETED_EPIC",
  "learning_summary_file": "$LEARNING_FILE",
  "integration_checklist_file": "$CHECKLIST_FILE",
  "patterns_count": ${#SUCCESSFUL_PATTERNS[@]},
  "gaps_count": ${#PRP_GAPS[@]},
  "avg_time_variance_percent": ${AVG_VARIANCE},
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"
}
EOF
)

WORKFLOW=$(cat .codex/state/workflow.json)
UPDATED_WORKFLOW=$(echo "$WORKFLOW" | jq \
    --argjson entry "$LEARNING_ENTRY" \
    '.epic_learnings.learnings += [$entry] |
     .epic_learnings.current_epic = "Epic '"$NEXT_EPIC"'"')
echo "$UPDATED_WORKFLOW" > .codex/state/workflow.json

echo "✅ workflow.json updated with Epic $COMPLETED_EPIC learnings"
```

### Step 8: Present Summary to User

```bash
echo ""
echo "═══════════════════════════════════════════════════════"
echo "📚 Epic $COMPLETED_EPIC Learning Integration Complete"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Learning Summary: $LEARNING_FILE"
echo "Integration Checklist: $CHECKLIST_FILE"
echo ""
echo "Key Insights:"
echo "  • Successful Patterns: ${#SUCCESSFUL_PATTERNS[@]}"
echo "  • PRP Gaps Identified: ${#PRP_GAPS[@]}"
echo "  • Avg Time Variance: ${AVG_VARIANCE}%"
echo ""
echo "Next Steps:"
echo "  1. Review learning summary before creating Epic $NEXT_EPIC PRPs"
echo "  2. Use integration checklist during PRP creation"
echo "  3. Apply successful patterns from Epic $COMPLETED_EPIC"
echo "  4. Avoid identified PRP gaps"
echo ""
echo "═══════════════════════════════════════════════════════"
```

## Outputs

```yaml
outputs:
  learning_summary:
    file: .codex/state/epic-learnings/epic-{N}-learning-summary.md
    contains:
      - Successful patterns to reuse
      - PRP gaps to address
      - Validation issues encountered
      - Time estimate recommendations
      - Epic N+1 PRP creation checklist

  integration_checklist:
    file: .codex/state/epic-learnings/epic-{N+1}-integration-checklist.md
    contains:
      - Pre-creation review items
      - During-creation application points
      - Post-creation validation checks

  workflow_update:
    file: .codex/state/workflow.json
    changes:
      - epic_learnings.learnings array updated
      - epic_learnings.current_epic updated
```

## Integration with PRP Creator

PRP Creator should invoke this task before creating Epic N+1 PRPs:

```yaml
prp_creator_workflow:
  1_check_epic:
    condition: "Creating PRPs for Epic N where N > 1"
    action: "Check if Epic N-1 complete"

  2_integrate_learnings:
    condition: "Epic N-1 complete"
    action: "Execute epic-learning-integration.md"
    inputs:
      completed_epic: "N-1"
      next_epic: "N"

  3_review_summary:
    action: "Read learning summary file"
    checklist: "Review integration checklist"

  4_create_prps:
    action: "Create Epic N PRPs with learnings applied"
    validation: "Verify learnings integrated via checklist"
```

## Success Criteria

```yaml
success_indicators:
  - Learning summary generated for Epic N
  - Integration checklist created for Epic N+1
  - Patterns extracted and documented
  - PRP gaps identified and remediation provided
  - Time variance calculated and recommendations made
  - workflow.json updated with learnings
  - Files accessible to PRP Creator
```

## Anti-Patterns

```yaml
anti_patterns:
  skip_learning_review:
    bad: "Start Epic N+1 PRPs immediately without reviewing Epic N learnings"
    good: "Always review learning summary before creating next epic's PRPs"

  ignore_patterns:
    bad: "Successful patterns noted but not applied"
    good: "Explicitly integrate successful patterns into Epic N+1 PRPs"

  repeat_mistakes:
    bad: "PRP gaps from Epic N repeated in Epic N+1"
    good: "Use integration checklist to verify all gaps addressed"
```
