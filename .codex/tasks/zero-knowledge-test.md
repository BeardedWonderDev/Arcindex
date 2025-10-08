# Zero-Knowledge Test Task

## Purpose

Validate architecture document completeness from an external perspective to ensure someone with no prior project knowledge can successfully implement from the documentation.

## Inputs

```yaml
inputs:
  required:
    architecture_file:
      type: string
      description: "Path to architecture document to validate"
      example: "docs/architecture.md"

    checklist_file:
      type: string
      description: "Checklist to validate against"
      default: ".codex/checklists/architect-quality-gate.md"

  optional:
    output_file:
      type: string
      description: "Where to save gap report"
      default: ".codex/state/zero-knowledge-test-results.md"
```

## Prerequisites

```yaml
prerequisites:
  - Architecture document exists and is complete
  - Architect quality gate checklist available
  - Sufficient context to evaluate completeness
```

## Workflow Steps

### Step 1: Load Architecture Document

```bash
echo "📖 Loading architecture document: $ARCHITECTURE_FILE..."

if [ ! -f "$ARCHITECTURE_FILE" ]; then
    echo "❌ ERROR: Architecture file not found: $ARCHITECTURE_FILE"
    exit 1
fi

# Read architecture content
ARCH_CONTENT=$(cat "$ARCHITECTURE_FILE")
ARCH_LINE_COUNT=$(wc -l < "$ARCHITECTURE_FILE")

echo "✅ Loaded architecture document (${ARCH_LINE_COUNT} lines)"
```

### Step 2: Load Quality Gate Checklist

```bash
echo "📋 Loading quality gate checklist: $CHECKLIST_FILE..."

if [ ! -f "$CHECKLIST_FILE" ]; then
    echo "❌ ERROR: Checklist file not found: $CHECKLIST_FILE"
    exit 1
fi

# Extract checklist items
CHECKLIST_ITEMS=$(grep -E "^- \[[ x]\]" "$CHECKLIST_FILE" | wc -l)

echo "✅ Loaded checklist (${CHECKLIST_ITEMS} items)"
```

### Step 3: Simulate Zero-Knowledge Perspective

```bash
echo ""
echo "🎭 Simulating zero-knowledge developer perspective..."
echo "   Perspective: Developer who knows nothing about this project"
echo "   Task: Can they implement successfully from this architecture?"
echo ""
```

### Step 4: Validate Each Checklist Item

```bash
echo "🔍 Validating architecture completeness..."

# Initialize gap tracking
GAPS_FOUND=0
MISSING_INFO=()
VAGUE_GUIDANCE=()
UNDOCUMENTED_ASSUMPTIONS=()

# Parse checklist and validate
while IFS= read -r line; do
    # Extract checklist item
    if [[ "$line" =~ ^\-\ \[([ x])\]\ (.+) ]]; then
        ITEM="${BASH_REMATCH[2]}"
        
        # For each item, check if architecture provides specific info
        # This is a simplified validation - real implementation would be more sophisticated
        
        # Check if key terms from checklist item appear in architecture
        # Extract key terms (simplified approach)
        KEY_TERMS=$(echo "$ITEM" | tr '[:upper:]' '[:lower:]' | grep -oE '\w{4,}' | head -3)
        
        FOUND=false
        for TERM in $KEY_TERMS; do
            if echo "$ARCH_CONTENT" | grep -iq "$TERM"; then
                FOUND=true
                break
            fi
        done
        
        if ! $FOUND; then
            MISSING_INFO+=("$ITEM")
            ((GAPS_FOUND++))
        fi
    fi
done < "$CHECKLIST_FILE"

echo "✅ Validation complete: ${GAPS_FOUND} gaps found"
```

### Step 5: Check for Vague Language

```bash
echo ""
echo "🔍 Checking for vague language..."

# Look for vague terms that indicate incomplete specification
VAGUE_TERMS=("TODO" "TBD" "will be" "should be" "to be determined" "best practices" "as needed" "appropriate")

for TERM in "${VAGUE_TERMS[@]}"; do
    if grep -iq "$TERM" "$ARCHITECTURE_FILE"; then
        INSTANCES=$(grep -ic "$TERM" "$ARCHITECTURE_FILE")
        VAGUE_GUIDANCE+=("Found $INSTANCES instances of '$TERM'")
    fi
done

if [ ${#VAGUE_GUIDANCE[@]} -gt 0 ]; then
    echo "⚠️  Found ${#VAGUE_GUIDANCE[@]} types of vague language"
else
    echo "✅ No vague language detected"
fi
```

### Step 6: Check for Undocumented Assumptions

```bash
echo ""
echo "🔍 Checking for undocumented assumptions..."

# Look for common assumption indicators
ASSUMPTION_PATTERNS=(
    "obviously"
    "clearly"
    "simply"
    "just use"
    "standard approach"
    "well-known"
    "typical"
)

for PATTERN in "${ASSUMPTION_PATTERNS[@]}"; do
    if grep -iq "$PATTERN" "$ARCHITECTURE_FILE"; then
        INSTANCES=$(grep -ic "$PATTERN" "$ARCHITECTURE_FILE")
        UNDOCUMENTED_ASSUMPTIONS+=("Found $INSTANCES instances of '$PATTERN' (may indicate assumption)")
    fi
done

if [ ${#UNDOCUMENTED_ASSUMPTIONS[@]} -gt 0 ]; then
    echo "⚠️  Found ${#UNDOCUMENTED_ASSUMPTIONS[@]} potential undocumented assumptions"
else
    echo "✅ No assumption indicators detected"
fi
```

### Step 7: Generate Gap Report

```bash
echo ""
echo "📝 Generating zero-knowledge test gap report..."

mkdir -p "$(dirname "$OUTPUT_FILE")"

cat > "$OUTPUT_FILE" <<EOF
# Zero-Knowledge Test Results

**Architecture File:** $ARCHITECTURE_FILE  
**Test Date:** $(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")  
**Checklist:** $CHECKLIST_FILE  
**Perspective:** Developer with no prior project knowledge

---

## Test Summary

- **Total Checklist Items:** ${CHECKLIST_ITEMS}
- **Gaps Found:** ${GAPS_FOUND}
- **Vague Language Instances:** ${#VAGUE_GUIDANCE[@]}
- **Potential Assumptions:** ${#UNDOCUMENTED_ASSUMPTIONS[@]}

**Overall Completeness:** $(( (CHECKLIST_ITEMS - GAPS_FOUND) * 100 / CHECKLIST_ITEMS ))%

$(if [ $GAPS_FOUND -eq 0 ] && [ ${#VAGUE_GUIDANCE[@]} -eq 0 ] && [ ${#UNDOCUMENTED_ASSUMPTIONS[@]} -eq 0 ]; then
    echo "**Status:** ✅ PASSED - Architecture is complete and actionable"
else
    echo "**Status:** ⚠️  NEEDS IMPROVEMENT - Gaps identified"
fi)

---

## Missing Information

$(if [ ${#MISSING_INFO[@]} -gt 0 ]; then
    echo "The following checklist items could not be verified in the architecture:"
    echo ""
    for i in "${!MISSING_INFO[@]}"; do
        echo "$((i+1)). ${MISSING_INFO[$i]}"
    done
else
    echo "✅ All checklist items have corresponding information in architecture"
fi)

---

## Vague Language Detected

$(if [ ${#VAGUE_GUIDANCE[@]} -gt 0 ]; then
    echo "Vague language that should be made more specific:"
    echo ""
    for item in "${VAGUE_GUIDANCE[@]}"; do
        echo "- $item"
    done
    echo ""
    echo "**Remediation:** Replace vague terms with specific, actionable guidance."
else
    echo "✅ No vague language detected"
fi)

---

## Potential Undocumented Assumptions

$(if [ ${#UNDOCUMENTED_ASSUMPTIONS[@]} -gt 0 ]; then
    echo "Language that may indicate undocumented assumptions:"
    echo ""
    for item in "${UNDOCUMENTED_ASSUMPTIONS[@]}"; do
        echo "- $item"
    done
    echo ""
    echo "**Remediation:** Explain concepts fully rather than assuming knowledge."
else
    echo "✅ No assumption indicators detected"
fi)

---

## Remediation Guidance

### For Missing Information
Each gap should be addressed by adding specific, actionable content:
- **What**: Clear description of the component/pattern/decision
- **Why**: Rationale for the approach
- **How**: Step-by-step implementation guidance
- **Examples**: Concrete code or configuration examples

### For Vague Language
Replace generic terms with specifics:
- "Best practices" → List specific practices to follow
- "Appropriate approach" → Define what makes an approach appropriate
- "As needed" → Specify when and how to determine need
- "TODO/TBD" → Complete the specification or remove if not relevant

### For Undocumented Assumptions
Document assumed knowledge:
- "Obviously" → Explain why it's the right choice
- "Simply use X" → Explain what X is and how to use it
- "Standard approach" → Document the standard and why it applies
- "Well-known pattern" → Describe the pattern for those unfamiliar

---

## Zero-Knowledge Test Criteria

An architecture passes the zero-knowledge test when:

1. **Information Present:** All checklist items have corresponding content
2. **Specific and Actionable:** Guidance is concrete, not generic
3. **Self-Contained:** No assumed prior knowledge
4. **Complete Context:** All decisions, rationale, and tradeoffs documented
5. **Implementation-Ready:** Developer can begin coding immediately

---

## Next Steps

$(if [ $GAPS_FOUND -gt 0 ] || [ ${#VAGUE_GUIDANCE[@]} -gt 0 ] || [ ${#UNDOCUMENTED_ASSUMPTIONS[@]} -gt 0 ]; then
    echo "1. Review gap report with architect"
    echo "2. Address each identified gap"
    echo "3. Replace vague language with specifics"
    echo "4. Document all assumptions"
    echo "5. Re-run zero-knowledge test"
    echo "6. Target: ≥95% completeness before PRP creation"
else
    echo "✅ Architecture passed zero-knowledge test"
    echo "Ready for PRP creation phase"
fi)

EOF

echo "✅ Gap report generated: $OUTPUT_FILE"
```

### Step 8: Display Summary

```bash
echo ""
echo "═══════════════════════════════════════════════════════"
echo "📊 Zero-Knowledge Test Results"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Architecture: $ARCHITECTURE_FILE"
echo "Completeness: $(( (CHECKLIST_ITEMS - GAPS_FOUND) * 100 / CHECKLIST_ITEMS ))%"
echo ""
echo "Gaps Found: $GAPS_FOUND"
echo "Vague Language: ${#VAGUE_GUIDANCE[@]} types"
echo "Assumptions: ${#UNDOCUMENTED_ASSUMPTIONS[@]} indicators"
echo ""
if [ $GAPS_FOUND -eq 0 ] && [ ${#VAGUE_GUIDANCE[@]} -eq 0 ] && [ ${#UNDOCUMENTED_ASSUMPTIONS[@]} -eq 0 ]; then
    echo "Status: ✅ PASSED"
else
    echo "Status: ⚠️  NEEDS IMPROVEMENT"
fi
echo ""
echo "Full Report: $OUTPUT_FILE"
echo "═══════════════════════════════════════════════════════"
```

## Outputs

```yaml
outputs:
  gap_report:
    file: .codex/state/zero-knowledge-test-results.md
    contains:
      - Missing information gaps
      - Vague language instances
      - Undocumented assumptions
      - Remediation guidance
      - Completeness percentage

  console_output:
    summary: Completeness score and gap count
    status: PASSED or NEEDS IMPROVEMENT
```

## Integration with Architect Agent

Architect should run this test before completing architecture phase:

```yaml
architect_workflow:
  1_create_architecture:
    action: "Draft architecture document"

  2_run_zero_knowledge_test:
    action: "Execute zero-knowledge-test.md"
    validation: "Check completeness ≥95%"

  3_remediate_gaps:
    condition: "Gaps found"
    action: "Address each gap in architecture"

  4_retest:
    action: "Re-run zero-knowledge-test.md"
    target: "100% completeness"

  5_handoff:
    condition: "Test passed"
    action: "Handoff to PRP Creator"
```

## Success Criteria

```yaml
success_indicators:
  - Zero-knowledge test executed against architecture
  - Gap report generated with specific remediation
  - Completeness percentage calculated
  - Missing information identified
  - Vague language flagged
  - Assumptions documented
  - Status determined (PASSED or NEEDS IMPROVEMENT)

  pass_threshold:
    completeness: "≥95%"
    gaps: "≤5% of checklist items"
    vague_language: "0 instances"
    assumptions: "0 undocumented"
```

## Anti-Patterns

```yaml
anti_patterns:
  skip_test:
    bad: "Architecture looks good, skip zero-knowledge test"
    good: "Always run test - external perspective catches gaps"

  ignore_vague_language:
    bad: "'Best practices' is clear enough"
    good: "Replace with specific practices to follow"

  assume_knowledge:
    bad: "'Obviously use X' - everyone knows X"
    good: "Explain X and why it's the right choice"

  low_bar:
    bad: "60% completeness is acceptable"
    good: "Target ≥95% completeness before handoff"
```
