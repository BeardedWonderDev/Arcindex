#!/bin/bash
# CODEX Test Harness - Enhanced with Branch Testing
# Creates isolated test environment from specified git branch

set -e

# ============================================================================
# 1. REPOSITORY DETECTION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# .../v0.1-implementation/.codex/test-harness/scripts

HARNESS_DIR="$(dirname "$SCRIPT_DIR")"
# .../v0.1-implementation/.codex/test-harness

CODEX_DIR="$(dirname "$HARNESS_DIR")"
# .../v0.1-implementation/.codex

REPO_ROOT="$(dirname "$CODEX_DIR")"
# .../v0.1-implementation (git repo root)

cd "$REPO_ROOT" || {
    echo "❌ Failed to access CODEX repository"
    exit 1
}

# Validate we're in a git repository (handles both .git directory and .git file for worktrees)
if [ ! -d ".git" ] && [ ! -f ".git" ]; then
    echo "❌ Not in a git repository"
    echo "   Expected .git in: $REPO_ROOT"
    exit 1
fi

echo "📂 CODEX Repository: $REPO_ROOT"
echo ""

# ============================================================================
# 2. SOURCE MODE DETECTION (--local or branch)
# ============================================================================

# Detect if running in local mode
if [ "$1" = "--local" ]; then
    SOURCE_MODE="local"
    BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
    echo "🔧 Local mode: Testing uncommitted changes"
    echo "🌿 Current branch: $BRANCH"
    echo ""
else
    SOURCE_MODE="git-archive"
fi

# ============================================================================
# 3. BRANCH SELECTION (Parameter or Interactive) - Git Archive Mode Only
# ============================================================================

if [ "$SOURCE_MODE" = "git-archive" ]; then
  if [ -n "$1" ]; then
    # Branch provided as parameter
    BRANCH="$1"
    echo "🌿 Testing branch: $BRANCH"
  else
    # Interactive branch selection
    echo "📋 Available branches:"
    echo ""

    # Get all branches (local and remote)
    BRANCHES=()
    while IFS= read -r branch; do
        BRANCHES+=("$branch")
    done < <(git branch -a | sed 's/^[* ]*//' | grep -v '^remotes/origin/HEAD' | sed 's|^remotes/origin/||' | sort -u)

    # Display menu
    for i in "${!BRANCHES[@]}"; do
        printf "  %2d) %s\n" "$((i+1))" "${BRANCHES[$i]}"
    done

    echo ""

    # Get current branch as default
    CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
    DEFAULT_SELECTION=""
    for i in "${!BRANCHES[@]}"; do
        if [ "${BRANCHES[$i]}" = "$CURRENT_BRANCH" ]; then
            DEFAULT_SELECTION=$((i+1))
            break
        fi
    done
    DEFAULT_SELECTION=${DEFAULT_SELECTION:-1}

    read -p "Enter branch name or number [$DEFAULT_SELECTION]: " selection
    selection=${selection:-$DEFAULT_SELECTION}

    # Handle numeric selection
    if [[ "$selection" =~ ^[0-9]+$ ]]; then
        idx=$((selection - 1))
        if [ $idx -lt 0 ] || [ $idx -ge ${#BRANCHES[@]} ]; then
            echo "❌ Invalid selection: $selection"
            exit 1
        fi
        BRANCH="${BRANCHES[$idx]}"
    else
        BRANCH="$selection"
    fi

    echo ""
    echo "🌿 Selected branch: $BRANCH"
  fi

  # Clean branch name (remove remotes/origin/ prefix if present)
  BRANCH=$(echo "$BRANCH" | sed 's|^remotes/origin/||')

  echo ""
fi

# ============================================================================
# 4. VALIDATE BRANCH (Git Archive Mode Only)
# ============================================================================

if [ "$SOURCE_MODE" = "git-archive" ]; then
  echo "🔍 Validating branch..."

  if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    echo "❌ Branch '$BRANCH' does not exist"
    echo ""
    echo "Available branches:"
    git branch -a | sed 's/^[* ]*/  /'
    exit 1
  fi

  # Get commit information
  COMMIT_HASH=$(git rev-parse "$BRANCH")
  COMMIT_SHORT=$(git rev-parse --short "$BRANCH")
  COMMIT_MSG=$(git log -1 --pretty=format:"%s" "$BRANCH")

  echo "  ✅ Branch exists"
  echo "  📍 Commit: $COMMIT_SHORT - $COMMIT_MSG"
  echo ""
else
  # Local mode - gather working tree information
  COMMIT_HASH="working-tree"
  COMMIT_SHORT="local"
  COMMIT_MSG="Local uncommitted changes ($(date '+%Y-%m-%d %H:%M'))"

  # Capture git status summary
  GIT_STATUS_SUMMARY=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
  if [ "$GIT_STATUS_SUMMARY" -gt 0 ]; then
    echo "  ⚠️  Working tree has $GIT_STATUS_SUMMARY uncommitted change(s)"
  else
    echo "  ✅ Working tree is clean (testing committed changes in working tree)"
  fi
  echo ""
fi

# ============================================================================
# 5. CREATE TEST DIRECTORY (External to Repo)
# ============================================================================

echo "📁 Creating test directory..."

# Determine parent directory (one level up from repo root)
PARENT_DIR="$(dirname "$REPO_ROOT")"
TEST_BASE="${PARENT_DIR}/codex-tests"

# Validate we're not creating tests in system directories
case "$TEST_BASE" in
    / | /usr | /usr/* | /etc | /etc/* | /bin | /bin/* | /System | /System/*)
        echo "❌ Cannot create tests in system directory: $TEST_BASE"
        exit 1
        ;;
esac

# Verify parent directory is writable
if [ ! -w "$PARENT_DIR" ]; then
    echo "❌ Parent directory not writable: $PARENT_DIR"
    echo "   Cannot create test base at: $TEST_BASE"
    exit 1
fi

# Create test base directory if it doesn't exist
mkdir -p "$TEST_BASE" || {
    echo "❌ Failed to create test base directory: $TEST_BASE"
    echo "   Ensure parent directory is writable"
    exit 1
}

# Sanitize branch name for directory (replace / with -)
BRANCH_SAFE=$(echo "$BRANCH" | tr '/' '-')
if [ "$SOURCE_MODE" = "local" ]; then
    TEST_ID="taskmaster-local-${BRANCH_SAFE}-$(date +%Y%m%d-%H%M)"
else
    TEST_ID="taskmaster-${BRANCH_SAFE}-$(date +%Y%m%d-%H%M)"
fi
TEST_DIR="${TEST_BASE}/${TEST_ID}"

mkdir -p "$TEST_DIR" || {
    echo "❌ Failed to create test directory: $TEST_DIR"
    exit 1
}

echo "  ✅ Created: $TEST_DIR"
echo "  📍 Location: Outside repo (${TEST_BASE})"
echo ""

# ============================================================================
# 6. EXTRACT FILES (Git Archive or Local Copy)
# ============================================================================

if [ "$SOURCE_MODE" = "git-archive" ]; then
  # GIT ARCHIVE MODE: Extract from specific branch/commit

  echo "📦 Extracting .codex/ from branch $BRANCH..."

  if ! git archive "$BRANCH" .codex 2>/dev/null | tar -x -C "$TEST_DIR" 2>/dev/null; then
      echo "❌ Failed to extract .codex/ from branch $BRANCH"
      echo "   This branch may not have a .codex/ directory"
      echo ""
      echo "Cleaning up..."
      rm -rf "$TEST_DIR"
      exit 1
  fi

  echo "  ✅ Extracted .codex/"
  echo ""

  echo "📦 Extracting .claude/commands/codex.md from branch $BRANCH..."

  mkdir -p "$TEST_DIR/.claude/commands"
  if ! git archive "$BRANCH" .claude/commands/codex.md 2>/dev/null | tar -x -C "$TEST_DIR" 2>/dev/null; then
      echo "❌ Failed to extract .claude/commands/codex.md from branch $BRANCH"
      echo "   This branch may not have the /codex command"
      echo ""
      echo "Cleaning up..."
      rm -rf "$TEST_DIR"
      exit 1
  fi

  echo "  ✅ Extracted /codex command"
  echo ""

  echo "📦 Extracting .claude/agents/ from branch $BRANCH..."

  if git archive "$BRANCH" .claude/agents 2>/dev/null | tar -x -C "$TEST_DIR" 2>/dev/null; then
      AGENT_COUNT=$(find "$TEST_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l)
      echo "  ✅ Extracted ${AGENT_COUNT} agent(s)"
  else
      echo "  ⚠️  No .claude/agents/ found (optional)"
  fi

  echo ""

else
  # LOCAL MODE: Copy from working tree

  echo "📦 Copying .codex/ from working tree..."

  if [ ! -d "$REPO_ROOT/.codex" ]; then
      echo "❌ .codex/ directory not found in working tree"
      echo ""
      echo "Cleaning up..."
      rm -rf "$TEST_DIR"
      exit 1
  fi

  cp -r "$REPO_ROOT/.codex" "$TEST_DIR/" || {
      echo "❌ Failed to copy .codex/ from working tree"
      echo ""
      echo "Cleaning up..."
      rm -rf "$TEST_DIR"
      exit 1
  }

  echo "  ✅ Copied .codex/"
  echo ""

  echo "📦 Copying .claude/commands/codex.md from working tree..."

  mkdir -p "$TEST_DIR/.claude/commands"
  if [ -f "$REPO_ROOT/.claude/commands/codex.md" ]; then
      cp "$REPO_ROOT/.claude/commands/codex.md" "$TEST_DIR/.claude/commands/" || {
          echo "❌ Failed to copy .claude/commands/codex.md"
          echo ""
          echo "Cleaning up..."
          rm -rf "$TEST_DIR"
          exit 1
      }
      echo "  ✅ Copied /codex command"
  else
      echo "❌ .claude/commands/codex.md not found in working tree"
      echo ""
      echo "Cleaning up..."
      rm -rf "$TEST_DIR"
      exit 1
  fi

  echo ""

  echo "📦 Copying .claude/agents/ from working tree..."

  if [ -d "$REPO_ROOT/.claude/agents" ]; then
      cp -r "$REPO_ROOT/.claude/agents" "$TEST_DIR/.claude/" || {
          echo "⚠️  Warning: Failed to copy .claude/agents/"
      }
      AGENT_COUNT=$(find "$TEST_DIR/.claude/agents" -name "*.md" 2>/dev/null | wc -l)
      echo "  ✅ Copied ${AGENT_COUNT} agent(s)"
  else
      echo "  ⚠️  No .claude/agents/ found (optional)"
  fi

  echo ""

  # Capture git diff for local tests (optional but helpful)
  if [ "$GIT_STATUS_SUMMARY" -gt 0 ]; then
      echo "📝 Capturing git diff for reproducibility..."
      git diff > "$TEST_DIR/git-diff.patch" 2>/dev/null || true
      git diff --cached >> "$TEST_DIR/git-diff.patch" 2>/dev/null || true
      echo "  ✅ Git diff saved to git-diff.patch"
      echo ""
  fi

fi

# ============================================================================
# 7. COPY DISCOVERY INPUTS
# ============================================================================

echo "📝 Copying discovery inputs..."

cp "${HARNESS_DIR}/templates/discovery-inputs.txt" "$TEST_DIR/" || {
    echo "❌ Failed to copy discovery inputs"
    rm -rf "$TEST_DIR"
    exit 1
}

echo "  ✅ Discovery inputs ready"
echo ""

# ============================================================================
# 8. CREATE TEST METADATA
# ============================================================================

echo "💾 Creating test metadata..."

if [ "$SOURCE_MODE" = "local" ]; then
  # Enhanced metadata for local tests
  cat > "$TEST_DIR/test-metadata.json" <<EOF
{
  "test_id": "${TEST_ID}",
  "source_mode": "local",
  "branch": "${BRANCH}",
  "commit_hash": "${COMMIT_HASH}",
  "commit_short": "${COMMIT_SHORT}",
  "commit_message": "${COMMIT_MSG}",
  "has_uncommitted_changes": $([ "$GIT_STATUS_SUMMARY" -gt 0 ] && echo "true" || echo "false"),
  "uncommitted_changes_count": ${GIT_STATUS_SUMMARY},
  "git_diff_available": $([ -f "$TEST_DIR/git-diff.patch" ] && echo "true" || echo "false"),
  "start_time": "$(date -Iseconds)",
  "repo_root": "${REPO_ROOT}",
  "harness_version": "1.2.0"
}
EOF
else
  # Standard metadata for git archive tests
  cat > "$TEST_DIR/test-metadata.json" <<EOF
{
  "test_id": "${TEST_ID}",
  "source_mode": "git-archive",
  "branch": "${BRANCH}",
  "commit_hash": "${COMMIT_HASH}",
  "commit_short": "${COMMIT_SHORT}",
  "commit_message": "${COMMIT_MSG}",
  "start_time": "$(date -Iseconds)",
  "repo_root": "${REPO_ROOT}",
  "harness_version": "1.2.0"
}
EOF
fi

echo "  ✅ Metadata saved"
echo ""

# ============================================================================
# 9. CREATE TEST README
# ============================================================================

if [ "$SOURCE_MODE" = "local" ]; then
  # README for local tests
  cat > "$TEST_DIR/README-TEST.md" <<EOF
# CODEX Test: ${TEST_ID}

**Source Mode:** Local (uncommitted changes)
**Branch:** ${BRANCH}
**Started:** $(date)

## Test Configuration

This test uses CODEX from:
- **Source:** Working tree (local files)
- **Branch:** ${BRANCH}
- **Uncommitted changes:** $([ "$GIT_STATUS_SUMMARY" -gt 0 ] && echo "$GIT_STATUS_SUMMARY file(s)" || echo "None - testing committed state")
- **Git diff:** $([ -f "$TEST_DIR/git-diff.patch" ] && echo "Captured in git-diff.patch" || echo "Not available")

⚠️  **Note:** This is a local test. It tests uncommitted changes from your working tree.
Reproducibility is limited - the exact state is captured in test-metadata.json and git-diff.patch.

CODEX files copied:
- ✅ .codex/ (complete system)
- ✅ .claude/commands/codex.md (slash command)
- ⚠️  .claude/agents/ (if available)

---

## How to Run This Test

### Step 1: Navigate to test directory
\`\`\`bash
cd ${TEST_DIR}
\`\`\`

### Step 2: Start CODEX workflow
\`\`\`bash
/codex start greenfield-generic "TaskMaster API"
\`\`\`

### Step 3: Provide discovery answers
When prompted, copy-paste answers from:
\`\`\`bash
cat discovery-inputs.txt
\`\`\`

There are 9 questions. Copy each answer line-by-line.

---

## After Workflow Completes

### Analyze results
\`\`\`bash
${HARNESS_DIR}/scripts/analyze-test.sh
\`\`\`

This will:
- Extract epic/story structure
- Pull quality scores
- Calculate pass/fail
- Archive results if passed

---

## Test Metadata

Full metadata available in: \`test-metadata.json\`
EOF
else
  # README for git archive tests
  cat > "$TEST_DIR/README-TEST.md" <<EOF
# CODEX Test: ${TEST_ID}

**Source Mode:** Git Archive (committed code)
**Branch:** ${BRANCH}
**Commit:** ${COMMIT_SHORT}
**Started:** $(date)

## Test Configuration

This test uses CODEX from:
- **Source:** Git archive extraction
- **Branch:** ${BRANCH}
- **Commit:** ${COMMIT_HASH}
- **Message:** ${COMMIT_MSG}

CODEX files extracted:
- ✅ .codex/ (complete system)
- ✅ .claude/commands/codex.md (slash command)
- ⚠️  .claude/agents/ (if available)

---

## How to Run This Test

### Step 1: Navigate to test directory
\`\`\`bash
cd ${TEST_DIR}
\`\`\`

### Step 2: Start CODEX workflow
\`\`\`bash
/codex start greenfield-generic "TaskMaster API"
\`\`\`

### Step 3: Provide discovery answers
When prompted, copy-paste answers from:
\`\`\`bash
cat discovery-inputs.txt
\`\`\`

There are 9 questions. Copy each answer line-by-line.

---

## After Workflow Completes

### Analyze results
\`\`\`bash
${HARNESS_DIR}/scripts/analyze-test.sh
\`\`\`

This will:
- Extract epic/story structure
- Pull quality scores
- Calculate pass/fail
- Archive results if passed

---

## Test Metadata

Full metadata available in: \`test-metadata.json\`
EOF
fi

# ============================================================================
# 11. DISPLAY INSTRUCTIONS
# ============================================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ TEST ENVIRONMENT READY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Test Details"
echo "───────────────────────────────────────────────────────────────────"
echo "  Test ID:  ${TEST_ID}"
echo "  Branch:   ${BRANCH}"
echo "  Commit:   ${COMMIT_SHORT}"
echo "  Message:  ${COMMIT_MSG}"
echo "  Path:     ${TEST_DIR}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Next Steps"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Navigate to test directory:"
echo "   cd $TEST_DIR"
echo ""
echo "2️⃣  Start CODEX workflow:"
echo "   /codex start greenfield-generic \"TaskMaster API\""
echo ""
echo "3️⃣  When prompted, paste answers from:"
echo "   cat discovery-inputs.txt"
echo ""
echo "4️⃣  After workflow completes, analyze results:"
echo "   ${HARNESS_DIR}/scripts/analyze-test.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
