# Confidence Scoring Task

## Purpose

Calculate architect's confidence score for architecture document to identify weak areas requiring additional validation or review before PRP creation.

## Inputs

```yaml
inputs:
  required:
    architecture_file:
      type: string
      description: "Path to architecture document"
      example: "docs/architecture.md"

  optional:
    output_file:
      type: string
      description: "Where to save confidence report"
      default: ".codex/state/confidence-scoring-results.md"

    scoring_method:
      type: string
      values: [comprehensive, quick]
      default: "comprehensive"
      description: "Scoring method to use"
```

## Prerequisites

```yaml
prerequisites:
  - Architecture document exists
  - Architect has completed architecture
  - Zero-knowledge test completed (recommended)
```

## Workflow Steps

### Step 1: Load Architecture Document

```bash
echo "📖 Loading architecture document: $ARCHITECTURE_FILE..."

if [ ! -f "$ARCHITECTURE_FILE" ]; then
    echo "❌ ERROR: Architecture file not found: $ARCHITECTURE_FILE"
    exit 1
fi

ARCH_CONTENT=$(cat "$ARCHITECTURE_FILE")

echo "✅ Architecture document loaded"
```

### Step 2: Define Confidence Scoring Dimensions

```bash
echo ""
echo "📊 Defining confidence scoring dimensions..."

# Scoring dimensions (0-10 scale for each)
DIMENSIONS=(
    "technology_selection"
    "scalability_approach"
    "security_design"
    "api_design"
    "data_model"
    "deployment_strategy"
    "testing_approach"
    "error_handling"
    "performance_optimization"
    "integration_points"
)

declare -A CONFIDENCE_SCORES
declare -A REASONING

echo "✅ ${#DIMENSIONS[@]} dimensions defined"
```

### Step 3: Prompt Architect for Confidence Scores

```bash
echo ""
echo "═══════════════════════════════════════════════════════"
echo "Architect Confidence Self-Assessment"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Rate your confidence (0-10) for each dimension:"
echo "  0-3: Low confidence, significant uncertainty"
echo "  4-6: Medium confidence, some aspects unclear"
echo "  7-8: High confidence, minor uncertainties"
echo "  9-10: Very high confidence, fully validated"
echo ""

for DIMENSION in "${DIMENSIONS[@]}"; do
    # Format dimension name for display
    DISPLAY_NAME=$(echo "$DIMENSION" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
    
    echo "─────────────────────────────────────────────────────"
    echo "$DISPLAY_NAME"
    echo ""
    
    # Prompt for confidence score
    read -p "Confidence (0-10): " SCORE
    
    # Validate input
    if ! [[ "$SCORE" =~ ^[0-9]$|^10$ ]]; then
        echo "Invalid input. Using default: 5"
        SCORE=5
    fi
    
    CONFIDENCE_SCORES[$DIMENSION]=$SCORE
    
    # If low confidence, ask for reasoning
    if [ "$SCORE" -lt 7 ]; then
        echo ""
        read -p "Why low confidence? (optional): " REASON
        REASONING[$DIMENSION]="$REASON"
    fi
    
    echo ""
done

echo "═══════════════════════════════════════════════════════"
```

### Step 4: Calculate Overall Confidence Score

```bash
echo ""
echo "🔢 Calculating overall confidence score..."

TOTAL_SCORE=0
DIMENSION_COUNT=${#DIMENSIONS[@]}

for DIMENSION in "${DIMENSIONS[@]}"; do
    SCORE=${CONFIDENCE_SCORES[$DIMENSION]}
    TOTAL_SCORE=$((TOTAL_SCORE + SCORE))
done

OVERALL_CONFIDENCE=$((TOTAL_SCORE * 10 / DIMENSION_COUNT))

echo "✅ Overall confidence: ${OVERALL_CONFIDENCE}/100"
```

### Step 5: Identify Weak Areas

```bash
echo ""
echo "🔍 Identifying weak areas (confidence < 7)..."

WEAK_AREAS=()

for DIMENSION in "${DIMENSIONS[@]}"; do
    SCORE=${CONFIDENCE_SCORES[$DIMENSION]}
    if [ "$SCORE" -lt 7 ]; then
        WEAK_AREAS+=("$DIMENSION")
    fi
done

if [ ${#WEAK_AREAS[@]} -gt 0 ]; then
    echo "⚠️  Found ${#WEAK_AREAS[@]} weak areas requiring attention"
else
    echo "✅ No weak areas identified"
fi
```

### Step 6: Generate Confidence Report

```bash
echo ""
echo "📝 Generating confidence report..."

mkdir -p "$(dirname "$OUTPUT_FILE")"

cat > "$OUTPUT_FILE" <<EOF
# Architecture Confidence Scoring Report

**Architecture File:** $ARCHITECTURE_FILE  
**Assessed By:** Architect  
**Assessment Date:** $(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")  
**Scoring Method:** ${SCORING_METHOD:-comprehensive}

---

## Executive Summary

**Overall Confidence Score:** ${OVERALL_CONFIDENCE}/100

$(if [ "$OVERALL_CONFIDENCE" -ge 85 ]; then
    echo "**Status:** ✅ HIGH CONFIDENCE - Architecture is well-validated and ready for PRP creation"
elif [ "$OVERALL_CONFIDENCE" -ge 70 ]; then
    echo "**Status:** ⚠️  MEDIUM CONFIDENCE - Some areas need additional validation before PRP creation"
else
    echo "**Status:** ❌ LOW CONFIDENCE - Significant gaps, additional research and validation required"
fi)

**Weak Areas (< 7/10):** ${#WEAK_AREAS[@]}

---

## Confidence Scores by Dimension

| Dimension | Score | Status | Notes |
|-----------|-------|--------|-------|
EOF

# Add each dimension to table
for DIMENSION in "${DIMENSIONS[@]}"; do
    SCORE=${CONFIDENCE_SCORES[$DIMENSION]}
    DISPLAY_NAME=$(echo "$DIMENSION" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
    
    if [ "$SCORE" -ge 9 ]; then
        STATUS="✅ Very High"
    elif [ "$SCORE" -ge 7 ]; then
        STATUS="✅ High"
    elif [ "$SCORE" -ge 4 ]; then
        STATUS="⚠️ Medium"
    else
        STATUS="❌ Low"
    fi
    
    REASON="${REASONING[$DIMENSION]:-N/A}"
    
    echo "| $DISPLAY_NAME | $SCORE/10 | $STATUS | $REASON |" >> "$OUTPUT_FILE"
done

cat >> "$OUTPUT_FILE" <<EOF

---

## Weak Areas Requiring Attention

$(if [ ${#WEAK_AREAS[@]} -gt 0 ]; then
    echo "The following areas have low confidence and should be addressed:"
    echo ""
    for AREA in "${WEAK_AREAS[@]}"; do
        SCORE=${CONFIDENCE_SCORES[$AREA]}
        DISPLAY_NAME=$(echo "$AREA" | tr '_' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
        REASON="${REASONING[$AREA]:-No reason provided}"
        echo "### $DISPLAY_NAME (Score: $SCORE/10)"
        echo ""
        echo "**Reason:** $REASON"
        echo ""
        echo "**Recommended Actions:**"
        
        case "$AREA" in
            "technology_selection")
                echo "- Research alternative technologies and document trade-offs"
                echo "- Validate technology choices against requirements"
                echo "- Get team consensus on technology stack"
                ;;
            "scalability_approach")
                echo "- Define scalability metrics and targets"
                echo "- Document scaling strategy (vertical/horizontal)"
                echo "- Identify bottlenecks and mitigation strategies"
                ;;
            "security_design")
                echo "- Conduct threat modeling session"
                echo "- Document security controls for each threat"
                echo "- Review with security expert if available"
                ;;
            "api_design")
                echo "- Create detailed API specifications"
                echo "- Document request/response schemas"
                echo "- Define error handling and status codes"
                ;;
            "data_model")
                echo "- Complete entity-relationship diagram"
                echo "- Document data validation rules"
                echo "- Define migration strategy"
                ;;
            "deployment_strategy")
                echo "- Document deployment pipeline steps"
                echo "- Define environment configurations"
                echo "- Document rollback procedures"
                ;;
            "testing_approach")
                echo "- Define testing strategy (unit/integration/e2e)"
                echo "- Specify coverage targets"
                echo "- Document test data strategy"
                ;;
            "error_handling")
                echo "- Document error classification scheme"
                echo "- Define retry and fallback strategies"
                echo "- Specify logging and monitoring approach"
                ;;
            "performance_optimization")
                echo "- Define performance metrics and targets"
                echo "- Document caching strategy"
                echo "- Identify optimization opportunities"
                ;;
            "integration_points")
                echo "- Document all external dependencies"
                echo "- Define integration patterns"
                echo "- Specify failure handling for external services"
                ;;
        esac
        echo ""
    done
else
    echo "✅ No weak areas identified. All dimensions have high confidence (≥7/10)."
fi)

---

## Recommended Next Steps

$(if [ "$OVERALL_CONFIDENCE" -ge 85 ]; then
    echo "✅ Architecture confidence is high. Proceed with PRP creation."
    echo ""
    echo "**Optional Enhancements:**"
    echo "1. Review architecture with technical lead for validation"
    echo "2. Run zero-knowledge test for external perspective"
    echo "3. Document any remaining minor uncertainties in PRPs"
elif [ "$OVERALL_CONFIDENCE" -ge 70 ]; then
    echo "⚠️ Architecture confidence is medium. Address weak areas before PRP creation."
    echo ""
    echo "**Required Actions:**"
    echo "1. Address all weak areas (< 7/10 confidence)"
    echo "2. Conduct additional research for low-confidence dimensions"
    echo "3. Review with technical expert if available"
    echo "4. Re-run confidence scoring after addressing gaps"
    echo "5. Target: ≥85/100 before PRP creation"
else
    echo "❌ Architecture confidence is low. Significant work required before PRP creation."
    echo ""
    echo "**Required Actions:**"
    echo "1. Address all weak areas immediately"
    echo "2. Conduct thorough research on uncertain dimensions"
    echo "3. Consider technical spike or proof-of-concept for high-risk areas"
    echo "4. Review with technical lead and subject matter experts"
    echo "5. Re-run confidence scoring after each remediation"
    echo "6. Do NOT proceed to PRP creation until confidence ≥85/100"
fi)

---

## Confidence Scoring Methodology

### Scoring Scale (0-10)

- **0-3 (Low):** Significant uncertainty, major gaps in understanding
- **4-6 (Medium):** Some clarity but important aspects unclear
- **7-8 (High):** Good understanding, minor uncertainties only
- **9-10 (Very High):** Complete confidence, fully validated

### Overall Score Calculation

Overall Score = (Sum of all dimension scores × 10) / Number of dimensions

### Status Thresholds

- **HIGH CONFIDENCE:** ≥85/100 → Ready for PRP creation
- **MEDIUM CONFIDENCE:** 70-84/100 → Address weak areas first
- **LOW CONFIDENCE:** <70/100 → Significant work required

---

## Integration with Workflow

This confidence assessment should be completed:

1. **After** architecture document is complete
2. **Before** handing off to PRP Creator
3. **Target:** ≥85/100 overall confidence

If confidence is < 85, iterate on architecture until threshold met.

EOF

echo "✅ Confidence report generated: $OUTPUT_FILE"
```

### Step 7: Display Summary

```bash
echo ""
echo "═══════════════════════════════════════════════════════"
echo "📊 Confidence Scoring Results"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Overall Confidence: ${OVERALL_CONFIDENCE}/100"
echo ""
if [ "$OVERALL_CONFIDENCE" -ge 85 ]; then
    echo "Status: ✅ HIGH CONFIDENCE"
    echo "Action: Proceed with PRP creation"
elif [ "$OVERALL_CONFIDENCE" -ge 70 ]; then
    echo "Status: ⚠️  MEDIUM CONFIDENCE"
    echo "Action: Address ${#WEAK_AREAS[@]} weak areas before PRP creation"
else
    echo "Status: ❌ LOW CONFIDENCE"
    echo "Action: Significant remediation required"
fi
echo ""
echo "Weak Areas: ${#WEAK_AREAS[@]}"
echo "Report: $OUTPUT_FILE"
echo "═══════════════════════════════════════════════════════"
```

### Step 8: Update workflow.json

```bash
# Add confidence assessment to workflow.json
CONFIDENCE_ENTRY=$(cat <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "overall_confidence": $OVERALL_CONFIDENCE,
  "weak_areas_count": ${#WEAK_AREAS[@]},
  "weak_areas": [$(printf '"%s",' "${WEAK_AREAS[@]}" | sed 's/,$//')]
}
EOF
)

if [ -f ".codex/state/workflow.json" ]; then
    WORKFLOW=$(cat .codex/state/workflow.json)
    UPDATED_WORKFLOW=$(echo "$WORKFLOW" | jq \
        --argjson entry "$CONFIDENCE_ENTRY" \
        '.validation_evidence.architect += [$entry]')
    echo "$UPDATED_WORKFLOW" > .codex/state/workflow.json
    echo "✅ workflow.json updated with confidence assessment"
fi
```

## Outputs

```yaml
outputs:
  confidence_report:
    file: .codex/state/confidence-scoring-results.md
    contains:
      - Overall confidence score (0-100)
      - Scores by dimension (0-10 each)
      - Weak areas requiring attention
      - Recommended actions per weak area
      - Next steps based on overall score

  workflow_update:
    file: .codex/state/workflow.json
    changes:
      - validation_evidence.architect updated with confidence data
```

## Integration with Architect Agent

Architect should run this scoring before handoff:

```yaml
architect_workflow:
  1_complete_architecture:
    action: "Draft complete architecture document"

  2_run_zero_knowledge_test:
    action: "Execute zero-knowledge-test.md"

  3_run_confidence_scoring:
    action: "Execute confidence-scoring.md"
    validation: "Check overall confidence ≥85/100"

  4_remediate_if_needed:
    condition: "Confidence < 85"
    action: "Address weak areas"
    loop: "Re-run scoring until ≥85"

  5_handoff_to_prp_creator:
    condition: "Confidence ≥85"
    action: "Export architecture for PRP creation"
```

## Success Criteria

```yaml
success_indicators:
  - Confidence scores collected for all dimensions
  - Overall confidence calculated (0-100 scale)
  - Weak areas identified (< 7/10)
  - Recommended actions provided for each weak area
  - Confidence report generated
  - workflow.json updated with assessment

  quality_threshold:
    minimum_for_handoff: "≥85/100"
    target: "≥90/100"
    weak_areas_max: "≤2 dimensions < 7/10"
```

## Anti-Patterns

```yaml
anti_patterns:
  skip_assessment:
    bad: "Architecture looks complete, skip confidence scoring"
    good: "Always run confidence scoring - it catches blind spots"

  overconfidence:
    bad: "Rate everything 9-10 without critical review"
    good: "Be honest about uncertainties - low scores drive improvement"

  ignore_weak_areas:
    bad: "70/100 is good enough, proceed anyway"
    good: "Address weak areas before handoff - prevents PRP rework"

  single_assessment:
    bad: "Score once, don't reassess after remediation"
    good: "Re-run after addressing gaps to verify improvement"
```
