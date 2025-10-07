---
name: commit
description: Analyze changes and create a smart git commit with automatic changelog updates
arguments: "Additional instructions for the commit"
---

additional instructions = $ARGUMENTS

type = "feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"

# Smart Git Commit with Changelog Integration

Please help me create a git commit by:

## Phase 1: Analyze Changes

1. First, check the current git status and analyze what changed:

```bash
git status
git diff --staged
```

2. If no files are staged, show me the changes and help me decide what to stage:

```bash
git diff
git status -s
```

## Phase 2: Suggest Commit Message

3. Based on the changes, suggest:

- The appropriate commit type (feat/fix/docs/style/refactor/perf/test/chore)
- A concise, descriptive commit message following conventional commits
- If the changes are complex, suggest breaking into multiple commits

4. The commit format should be:

$type: description for simple commits
For complex changes, include a body explaining what and why

5. After showing me the suggested commit message, ask if I want to:

- Use it as-is
- Modify it
- Add more details to the body
- Stage different files

## Phase 3: Update CHANGELOG.md

6. Determine if changelog update is needed:

**Auto-include for:** feat, fix, refactor, perf
**Ask user for:** docs (prompt: "Include changelog entry for documentation changes? (y/n)")
**Skip for:** style, test, chore

7. If changelog update needed, perform the following updates to CHANGELOG.md:

   a. **Add entry to [Unreleased] section:**
      - Map commit type to category:
        - `feat` → `### Added`
        - `fix` → `### Fixed`
        - `refactor` → `### Changed`
        - `perf` → `### Changed`
        - `docs` → `### Changed` (or Added if new documentation)
      - Prompt user: "Changelog entry (press Enter to use commit description): "
      - Insert entry: `- {entry_text}` under appropriate category
      - Preserve all existing entries
      - Create category section if it doesn't exist (order: Added, Changed, Fixed, Removed)

   b. **Update Total Commits count:**
      - Run: `git rev-list --count HEAD`
      - Increment by 1 (for the commit about to be made)
      - Update line: `- **Total Commits**: {new_count}`

   c. **Update Date Range:**
      - Extract existing start date from `- **Date Range**: YYYY-MM-DD to YYYY-MM-DD`
      - Get current date: `date +%Y-%m-%d`
      - Update line: `- **Date Range**: {start_date} to {current_date}`

   d. **Update Commit Type Distribution:**
      - Count all commits by type:
        ```bash
        feat_count=$(git log --oneline --all | grep -c "^[a-f0-9]\+ feat:" || echo 0)
        fix_count=$(git log --oneline --all | grep -c "^[a-f0-9]\+ fix:" || echo 0)
        refactor_count=$(git log --oneline --all | grep -c "^[a-f0-9]\+ refactor:" || echo 0)
        docs_count=$(git log --oneline --all | grep -c "^[a-f0-9]\+ docs:" || echo 0)
        # ... etc for perf, test, chore, style
        ```
      - Increment the count for current commit type by 1
      - Calculate total commits
      - Calculate percentages: `{count} * 100 / {total}` (one decimal place)
      - Update Commit Type Distribution section with new counts and percentages

   e. **Handle edge cases:**
      - If CHANGELOG.md doesn't exist: Create from Keep a Changelog template
      - If [Unreleased] section missing: Insert template section
      - If category subsection missing: Create in standard order
      - If statistics section malformed: Validate and recreate if needed

   f. **Stage the updated changelog:**
      ```bash
      git add CHANGELOG.md
      ```

   g. **Development History - DEFERRED TO COMMIT 2:**
      - DO NOT update Development History in this phase
      - Development History will be updated in Commit 2 (see Phase 4)
      - This two-commit approach prevents amend loops by allowing us to reference the actual hash from Commit 1

## Phase 4: Create Commits (Two-Commit Workflow)

8. **Create Commit 1 - Main Changes:**

   Once approved and changelog updated, create the first commit:

   ```bash
   git commit -m "$(cat <<'EOF'
   {type}: {description}

   {optional body with details}

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

   This commit includes:
   - Your code changes
   - Updated CHANGELOG.md [Unreleased] section
   - Updated CHANGELOG.md Statistics section
   - NO Development History changes (yet)

   Capture the commit hash: `git log -1 --format=%h`

9. **Create Commit 2 - Development History Update:**

   a. **Update Development History section in CHANGELOG.md:**
      - Determine the week of Commit 1 (ISO week, Monday-Sunday)
      - Get Monday date of current week: `date -v-Mon +%Y-%m-%d` (or equivalent)
      - Check if "Week of {monday_date}" section exists in Development History
      - Insert commit entry using ACTUAL hash from Commit 1
      - Format: `- {hash}: {type}: {description} ({YYYY-MM-DD})`

      - If week section exists:
        * Insert new commit at TOP of that week's commit list (reverse chronological)
        * Update week count (count all commits in that week)
        * Regenerate focus line for that week
      - If week section doesn't exist:
        * Create new week section at TOP of Development History
        * Add commit entry with count: `### Week of YYYY-MM-DD (1 commit)`
        * Generate initial focus line

      **Focus Line Generation Algorithm:**
      1. Get all commits for the week: `git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --pretty=format:"%s"`
      2. Extract keywords from commit messages (text after "type:" prefix)
      3. Weight by commit type:
         - feat: 3 points
         - fix: 2 points
         - refactor: 2 points
         - docs: 1 point
         - others: 1 point
      4. Count weighted keyword frequency across all week's commits
      5. Select top 2-3 themes (most frequent weighted keywords)
      6. Format themes as gerunds/noun phrases: "Orchestrator enhancements", "validation improvements"
      7. Combine: "**Focus:** theme1, theme2, theme3"

      **Week Section Format:**
      ```
      ### Week of YYYY-MM-DD (X commits)
      **Focus:** [auto-generated themes]

      - hash: type: description (YYYY-MM-DD)
      - hash: type: description (YYYY-MM-DD)
      ```

      **Implementation Notes:**
      - Week count updates automatically (count commits in that week section)
      - Commits within week are reverse chronological (newest first)
      - Week sections themselves are reverse chronological (newest week first)
      - Regenerate focus line each time a commit is added to ensure accuracy

   b. **Create Commit 2:**
      ```bash
      git add CHANGELOG.md
      git commit -m "$(cat <<'EOF'
      chore: update changelog development history

      🤖 Generated with [Claude Code](https://claude.com/claude-code)

      Co-Authored-By: Claude <noreply@anthropic.com>
      EOF
      )"
      ```

10. **Display commit summary showing:**
    - Commit 1 hash, type, description, files changed
    - Commit 2 hash (development history update)
    - Total: 2 commits created
    - Changelog sections updated

## Phase 5: Next Steps

11. Finally, ask if I want to push or create a PR.