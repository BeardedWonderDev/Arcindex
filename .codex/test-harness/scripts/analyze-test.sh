#!/bin/bash
# CODEX Test Analysis Script

echo "🔍 Analyzing CODEX test results..."
echo ""

# Find most recent test directory
if [ -z "$1" ]; then
    # Detect harness directory from script location
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    HARNESS_DIR="$(dirname "$SCRIPT_DIR")"

    # Determine external test directory location
    CODEX_DIR="$(dirname "$HARNESS_DIR")"
    REPO_ROOT="$(dirname "$CODEX_DIR")"
    PARENT_DIR="$(dirname "$REPO_ROOT")"
    TEST_BASE="${PARENT_DIR}/codex-tests"

    TEST_DIR=$(ls -td "${TEST_BASE}"/taskmaster-* 2>/dev/null | head -1)
    if [ -z "$TEST_DIR" ]; then
        echo "❌ No test results found in $TEST_BASE"
        echo "   Run a test first: ${HARNESS_DIR}/scripts/run-test.sh"
        exit 1
    fi
    echo "📁 Analyzing most recent test: $(basename $TEST_DIR)"
else
    TEST_DIR="$1"
fi

cd "$TEST_DIR" || exit 1

# Create results file
RESULTS_FILE="analysis-results.txt"
echo "=== CODEX TEST ANALYSIS ===" > "$RESULTS_FILE"
echo "Test: $(basename $TEST_DIR)" >> "$RESULTS_FILE"
echo "Date: $(date)" >> "$RESULTS_FILE"

# Read test metadata if available
if [ -f "test-metadata.json" ]; then
    SOURCE_MODE=$(jq -r '.source_mode // "git-archive"' test-metadata.json 2>/dev/null)
    BRANCH=$(jq -r '.branch // "unknown"' test-metadata.json 2>/dev/null)
    COMMIT=$(jq -r '.commit_short // "unknown"' test-metadata.json 2>/dev/null)
    COMMIT_MSG=$(jq -r '.commit_message // "unknown"' test-metadata.json 2>/dev/null)
    echo "Source Mode: $SOURCE_MODE" >> "$RESULTS_FILE"
    echo "Branch: $BRANCH" >> "$RESULTS_FILE"
    echo "Commit: $COMMIT" >> "$RESULTS_FILE"
    echo "Message: $COMMIT_MSG" >> "$RESULTS_FILE"

    # Warn if local test
    if [ "$SOURCE_MODE" = "local" ]; then
        HAS_UNCOMMITTED=$(jq -r '.has_uncommitted_changes // false' test-metadata.json 2>/dev/null)
        CHANGES_COUNT=$(jq -r '.uncommitted_changes_count // 0' test-metadata.json 2>/dev/null)
        echo "" >> "$RESULTS_FILE"
        echo "⚠️  LOCAL TEST WARNING:" >> "$RESULTS_FILE"
        echo "   This test used uncommitted changes from working tree" >> "$RESULTS_FILE"
        if [ "$HAS_UNCOMMITTED" = "true" ]; then
            echo "   $CHANGES_COUNT file(s) had uncommitted changes" >> "$RESULTS_FILE"
        else
            echo "   Working tree was clean (testing committed state)" >> "$RESULTS_FILE"
        fi
        echo "   Reproducibility is limited - see git-diff.patch if available" >> "$RESULTS_FILE"
    fi
fi

echo "" >> "$RESULTS_FILE"

# 1. Extract Epic/Story Structure
echo "=== STRUCTURE ANALYSIS ===" >> "$RESULTS_FILE"
if [ -f "docs/prd.md" ]; then
    EPIC_COUNT=$(grep -c "^## Epic" docs/prd.md 2>/dev/null || echo 0)
    STORY_COUNT=$(grep -c "^### US-" docs/prd.md 2>/dev/null || echo 0)
    echo "Epics: $EPIC_COUNT" >> "$RESULTS_FILE"
    echo "Stories: $STORY_COUNT" >> "$RESULTS_FILE"
    echo "" >> "$RESULTS_FILE"
    echo "Epic Titles:" >> "$RESULTS_FILE"
    grep "^## Epic" docs/prd.md >> "$RESULTS_FILE" 2>/dev/null || echo "  (none found)" >> "$RESULTS_FILE"
else
    echo "❌ PRD not found" >> "$RESULTS_FILE"
fi
echo "" >> "$RESULTS_FILE"

# 2. Extract Quality Scores
echo "=== QUALITY SCORES ===" >> "$RESULTS_FILE"
if [ -f ".codex/state/workflow.json" ]; then
    PM_SCORE=$(jq -r '.quality_gate_results.pm.score // "N/A"' .codex/state/workflow.json 2>/dev/null)
    ARCH_SCORE=$(jq -r '.quality_gate_results.architect.score // "N/A"' .codex/state/workflow.json 2>/dev/null)
    
    echo "PM: ${PM_SCORE}/100" >> "$RESULTS_FILE"
    echo "Architect: ${ARCH_SCORE}/100" >> "$RESULTS_FILE"
    
    # Get PRP scores (may be multiple)
    PRP_SCORES=$(jq -r '[.quality_gate_results | to_entries[] | select(.key | startswith("prp")) | .value.score] | @json' .codex/state/workflow.json 2>/dev/null)
    if [ "$PRP_SCORES" != "null" ] && [ -n "$PRP_SCORES" ]; then
        PRP_AVG=$(echo "$PRP_SCORES" | jq 'add / length' 2>/dev/null || echo "N/A")
        echo "PRP Average: ${PRP_AVG}/100" >> "$RESULTS_FILE"
    else
        echo "PRP Average: N/A" >> "$RESULTS_FILE"
    fi
else
    echo "❌ workflow.json not found" >> "$RESULTS_FILE"
    PM_SCORE="N/A"
    ARCH_SCORE="N/A"
    PRP_AVG="N/A"
fi
echo "" >> "$RESULTS_FILE"

# 3. Check Epic Learning
echo "=== EPIC LEARNING ===" >> "$RESULTS_FILE"
if [ -d ".codex/state/execution-reports" ]; then
    REPORT_COUNT=$(ls .codex/state/execution-reports/*.json 2>/dev/null | wc -l)
    echo "Execution reports: $REPORT_COUNT" >> "$RESULTS_FILE"
    
    # Check for epic learning summary
    if [ -f ".codex/state/epic-learnings/epic-1-learning-summary.md" ]; then
        echo "✅ Epic learning summary exists" >> "$RESULTS_FILE"
    else
        echo "❌ Epic learning summary missing" >> "$RESULTS_FILE"
    fi
else
    echo "No execution reports found" >> "$RESULTS_FILE"
fi
echo "" >> "$RESULTS_FILE"

# 4. Calculate Pass/Fail
echo "=== PASS/FAIL EVALUATION ===" >> "$RESULTS_FILE"
PASS_COUNT=0
FAIL_COUNT=0

# Check PM score
if [ "$PM_SCORE" != "N/A" ] && [ "$PM_SCORE" -ge 80 ] 2>/dev/null; then
    echo "✅ PM Quality: PASS ($PM_SCORE ≥ 80)" >> "$RESULTS_FILE"
    ((PASS_COUNT++))
else
    echo "❌ PM Quality: FAIL ($PM_SCORE < 80)" >> "$RESULTS_FILE"
    ((FAIL_COUNT++))
fi

# Check Architect score
if [ "$ARCH_SCORE" != "N/A" ] && [ "$ARCH_SCORE" -ge 85 ] 2>/dev/null; then
    echo "✅ Architect Quality: PASS ($ARCH_SCORE ≥ 85)" >> "$RESULTS_FILE"
    ((PASS_COUNT++))
else
    echo "❌ Architect Quality: FAIL ($ARCH_SCORE < 85)" >> "$RESULTS_FILE"
    ((FAIL_COUNT++))
fi

# Overall result
echo "" >> "$RESULTS_FILE"
echo "Passed: $PASS_COUNT checks" >> "$RESULTS_FILE"
echo "Failed: $FAIL_COUNT checks" >> "$RESULTS_FILE"

if [ "$FAIL_COUNT" -eq 0 ]; then
    RESULT="✅ PASS"
elif [ "$FAIL_COUNT" -le 1 ]; then
    RESULT="⚠️  CONDITIONAL"
else
    RESULT="❌ FAIL"
fi

echo "" >> "$RESULTS_FILE"
echo "RESULT: $RESULT" >> "$RESULTS_FILE"

# Display results
cat "$RESULTS_FILE"

# Create simple summary
cat > TEST-RESULT.txt << EOF
Test: $(basename $TEST_DIR)
Branch: ${BRANCH:-unknown}
Commit: ${COMMIT:-unknown}
Result: $RESULT
PM Score: $PM_SCORE
Architect Score: $ARCH_SCORE
Epics: $EPIC_COUNT
Stories: $STORY_COUNT

See analysis-results.txt for full details
EOF

echo ""
echo "📊 Full results: ${TEST_DIR}/analysis-results.txt"
echo "📄 Summary: ${TEST_DIR}/TEST-RESULT.txt"

# Archive if passed
if [ "$FAIL_COUNT" -eq 0 ]; then
    # Determine test base directory from test directory path
    TEST_BASE="$(dirname "$TEST_DIR")"

    # Archive local tests separately
    if [ "$SOURCE_MODE" = "local" ]; then
        ARCHIVE_DIR="${TEST_BASE}/archive/local/$(basename $TEST_DIR)"
        echo ""
        echo "⚠️  Local test - archiving to separate location:"
    else
        ARCHIVE_DIR="${TEST_BASE}/archive/$(basename $TEST_DIR)"
    fi

    mkdir -p "$ARCHIVE_DIR"
    cp -r docs PRPs .codex/state analysis-results.txt TEST-RESULT.txt test-metadata.json "$ARCHIVE_DIR/" 2>/dev/null || true

    # Copy git diff if available (local tests only)
    if [ -f "git-diff.patch" ]; then
        cp git-diff.patch "$ARCHIVE_DIR/" 2>/dev/null || true
    fi

    echo "📦 Archived to: $ARCHIVE_DIR"

    if [ "$SOURCE_MODE" = "local" ]; then
        echo "   Note: Local tests are archived separately from branch tests"
    fi
fi

