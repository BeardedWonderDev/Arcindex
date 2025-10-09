#!/bin/bash
# CODEX Test Cleanup Utility

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="$(dirname "$SCRIPT_DIR")"

# Determine external test directory location
CODEX_DIR="$(dirname "$HARNESS_DIR")"
REPO_ROOT="$(dirname "$CODEX_DIR")"
PARENT_DIR="$(dirname "$REPO_ROOT")"
TEST_BASE="${PARENT_DIR}/codex-tests"

echo "🧹 CODEX Test Cleanup Utility"
echo ""

if [ ! -d "$TEST_BASE" ]; then
    echo "No test directory found at: $TEST_BASE"
    exit 0
fi

# Count tests
ACTIVE_COUNT=$(find "$TEST_BASE" -maxdepth 1 -name "taskmaster-*" -type d 2>/dev/null | wc -l | xargs)
ARCHIVE_COUNT=0
if [ -d "${TEST_BASE}/archive" ]; then
    ARCHIVE_COUNT=$(find "${TEST_BASE}/archive" -maxdepth 1 -name "taskmaster-*" -type d 2>/dev/null | wc -l | xargs)
fi

echo "📊 Current State:"
echo "  Active tests: $ACTIVE_COUNT"
echo "  Archived tests: $ARCHIVE_COUNT"
echo "  Location: $TEST_BASE"
echo ""

# Menu
echo "What would you like to do?"
echo "  1) Remove all active tests (keep archive)"
echo "  2) Remove all tests (active + archive)"
echo "  3) Remove tests older than 7 days"
echo "  4) List all tests"
echo "  5) Cancel"
echo ""

read -p "Select option [1-5]: " choice

case $choice in
    1)
        read -p "Remove $ACTIVE_COUNT active tests? [y/N]: " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            find "$TEST_BASE" -maxdepth 1 -name "taskmaster-*" -type d -exec rm -rf {} \; 2>/dev/null
            echo "✅ Removed active tests"
        else
            echo "Cancelled"
        fi
        ;;
    2)
        TOTAL=$((ACTIVE_COUNT + ARCHIVE_COUNT))
        read -p "Remove ALL tests ($ACTIVE_COUNT active + $ARCHIVE_COUNT archived = $TOTAL total)? [y/N]: " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            rm -rf "$TEST_BASE"
            echo "✅ Removed all tests and test directory"
        else
            echo "Cancelled"
        fi
        ;;
    3)
        echo "Removing tests older than 7 days..."
        REMOVED_COUNT=0

        # Remove old active tests
        while IFS= read -r -d '' dir; do
            rm -rf "$dir"
            ((REMOVED_COUNT++))
        done < <(find "$TEST_BASE" -maxdepth 1 -name "taskmaster-*" -type d -mtime +7 -print0 2>/dev/null)

        # Remove old archived tests
        if [ -d "${TEST_BASE}/archive" ]; then
            while IFS= read -r -d '' dir; do
                rm -rf "$dir"
                ((REMOVED_COUNT++))
            done < <(find "${TEST_BASE}/archive" -maxdepth 1 -name "taskmaster-*" -type d -mtime +7 -print0 2>/dev/null)
        fi

        echo "✅ Removed $REMOVED_COUNT tests older than 7 days"
        ;;
    4)
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Active Tests:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        FOUND_ACTIVE=false
        while IFS= read -r dir; do
            FOUND_ACTIVE=true
            TEST_NAME=$(basename "$dir")
            TEST_SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
            TEST_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$dir" 2>/dev/null || stat -c "%y" "$dir" 2>/dev/null | cut -d'.' -f1)
            echo "  📁 $TEST_NAME"
            echo "     Size: $TEST_SIZE | Created: $TEST_DATE"
        done < <(find "$TEST_BASE" -maxdepth 1 -name "taskmaster-*" -type d 2>/dev/null | sort -r)

        if [ "$FOUND_ACTIVE" = false ]; then
            echo "  (none)"
        fi

        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Archived Tests:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        if [ -d "${TEST_BASE}/archive" ]; then
            FOUND_ARCHIVE=false
            while IFS= read -r dir; do
                FOUND_ARCHIVE=true
                TEST_NAME=$(basename "$dir")
                TEST_SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
                TEST_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$dir" 2>/dev/null || stat -c "%y" "$dir" 2>/dev/null | cut -d'.' -f1)

                # Try to get result from TEST-RESULT.txt
                if [ -f "$dir/TEST-RESULT.txt" ]; then
                    RESULT=$(grep "Result:" "$dir/TEST-RESULT.txt" | cut -d' ' -f2-)
                    echo "  📦 $TEST_NAME [$RESULT]"
                else
                    echo "  📦 $TEST_NAME"
                fi
                echo "     Size: $TEST_SIZE | Archived: $TEST_DATE"
            done < <(find "${TEST_BASE}/archive" -maxdepth 1 -name "taskmaster-*" -type d 2>/dev/null | sort -r)

            if [ "$FOUND_ARCHIVE" = false ]; then
                echo "  (none)"
            fi
        else
            echo "  (none)"
        fi
        echo ""
        ;;
    5)
        echo "Cancelled"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
