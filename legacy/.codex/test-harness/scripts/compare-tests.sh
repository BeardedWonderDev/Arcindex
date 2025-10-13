#!/bin/bash
# Compare multiple test runs

echo "📊 CODEX Test Comparison"
echo ""

# Find harness directory and external test location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(dirname "$SCRIPT_DIR")"

# Determine external test directory location
CODEX_DIR="$(dirname "$HARNESS_DIR")"
REPO_ROOT="$(dirname "$CODEX_DIR")"
PARENT_DIR="$(dirname "$REPO_ROOT")"
TEST_BASE="${PARENT_DIR}/codex-tests"
ARCHIVE_DIR="${TEST_BASE}/archive"

if [ ! -d "$ARCHIVE_DIR" ] || [ -z "$(ls -A $ARCHIVE_DIR 2>/dev/null)" ]; then
    echo "No archived tests found. Run and analyze tests first."
    exit 1
fi

echo "| Test ID | Branch | Commit | PM | Arch | PRP | Epics | Stories | Result |"
echo "|---------|--------|--------|----|----- |-----|-------|---------|--------|"

for test in $(ls -d $ARCHIVE_DIR/taskmaster-* 2>/dev/null | sort); do
    test_id=$(basename "$test")

    if [ -f "$test/TEST-RESULT.txt" ]; then
        # Extract branch and commit if available
        if [ -f "$test/test-metadata.json" ]; then
            branch=$(jq -r '.branch // "unknown"' "$test/test-metadata.json" 2>/dev/null | cut -c1-12)
            commit=$(jq -r '.commit_short // "unknown"' "$test/test-metadata.json" 2>/dev/null)
        else
            branch=$(grep "Branch:" "$test/TEST-RESULT.txt" | awk '{print $2}' | cut -c1-12)
            commit=$(grep "Commit:" "$test/TEST-RESULT.txt" | awk '{print $2}')
        fi

        # Extract scores
        pm=$(grep "PM Score:" "$test/TEST-RESULT.txt" | awk '{print $3}')
        arch=$(grep "Architect Score:" "$test/TEST-RESULT.txt" | awk '{print $3}')

        # Get PRP score from analysis-results.txt if available
        if [ -f "$test/analysis-results.txt" ]; then
            prp=$(grep "PRP Average:" "$test/analysis-results.txt" | awk '{print $3}' | cut -d'/' -f1)
        else
            prp="N/A"
        fi

        epics=$(grep "Epics:" "$test/TEST-RESULT.txt" | awk '{print $2}')
        stories=$(grep "Stories:" "$test/TEST-RESULT.txt" | awk '{print $2}')
        result=$(grep "Result:" "$test/TEST-RESULT.txt" | cut -d' ' -f2-)

        # Truncate test_id for readability
        test_id_short=$(echo "$test_id" | cut -c1-30)

        echo "| $test_id_short | $branch | $commit | $pm | $arch | $prp | $epics | $stories | $result |"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 Summary Statistics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Calculate statistics
TOTAL_TESTS=$(ls -d $ARCHIVE_DIR/taskmaster-* 2>/dev/null | wc -l)
PASSED=$(grep -l "✅ PASS" $ARCHIVE_DIR/*/TEST-RESULT.txt 2>/dev/null | wc -l)
FAILED=$(grep -l "❌ FAIL" $ARCHIVE_DIR/*/TEST-RESULT.txt 2>/dev/null | wc -l)
CONDITIONAL=$(grep -l "⚠️  CONDITIONAL" $ARCHIVE_DIR/*/TEST-RESULT.txt 2>/dev/null | wc -l)

echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Conditional: $CONDITIONAL"

if [ "$TOTAL_TESTS" -gt 0 ]; then
    PASS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED / $TOTAL_TESTS) * 100}")
    echo "Pass Rate: ${PASS_RATE}%"
fi

echo ""
