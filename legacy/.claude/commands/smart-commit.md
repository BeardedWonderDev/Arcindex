---
name: commit
description: Create conventional commit (changelog auto-updated on push)
arguments: "Additional instructions for the commit"
---

additional instructions = $ARGUMENTS

type = "feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"

# Smart Git Commit (Automated Changelog)

**Note:** Changelog, statistics, and development history are now automatically updated by GitHub Actions after you push to main.


## Phase 1: Analyze Changes

1. Check the current git status and analyze what changed:

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

```
$type: description

[Optional body explaining what and why]
- Bullet point details
- Technical specifics

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

5. After showing me the suggested commit message, ask if I want to:

- Use it as-is
- Modify it
- Add more details to the body
- Stage different files

## Phase 3: Create Commit

6. Once approved, create the commit:

```bash
git commit -m "$(cat <<'EOF'
{type}: {description}

{optional body with details}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

7. Display commit summary:
   - Commit hash
   - Commit type and description
   - Files changed
   - Lines added/removed

## Phase 4: Sync, Push, and Workflow Trigger

8. After commit, check for unstaged changes and sync/push if clean:

```bash
BRANCH=$(git branch --show-current)
UNSTAGED=$(git status --porcelain | grep -E '^ M|^\?\?' || echo "")

if [ -n "$UNSTAGED" ]; then
  # Working directory still has uncommitted changes
  echo ""
  echo "⚠️  PUSH SKIPPED - Unstaged changes detected"
  echo ""
  echo "Commit created successfully, but not pushed due to uncommitted work:"
  echo ""
  git status -s
  echo ""
  echo "Next steps:"
  echo "  • Review unstaged changes above"
  echo "  • Stage and commit additional work with another /smart-commit"
  echo "  • Or manually push: git push origin $BRANCH"
  echo ""
  echo "✅ Commit saved locally. Push when ready."
else
  # Working directory is clean - safe to sync and push
  echo ""
  echo "✅ Working directory clean - syncing and pushing"
  echo ""

  # Fetch remote to check for workflow commits
  git fetch origin $BRANCH
  BEHIND=$(git rev-list --count HEAD..origin/$BRANCH 2>/dev/null || echo "0")

  if [ "$BEHIND" -gt 0 ]; then
    echo "⬇️  Remote has $BEHIND new commit(s) from previous workflows..."

    # Check if workflows are still running
    CHANGELOG_STATUS=$(gh run list --workflow=changelog-automation.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")
    HISTORY_STATUS=$(gh run list --workflow=development-history.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")
    ROADMAP_STATUS=$(gh run list --workflow=roadmap-update.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")

    # Wait for any in-progress workflows
    if [ "$CHANGELOG_STATUS" != "completed" ] || [ "$HISTORY_STATUS" != "completed" ] || [ "$ROADMAP_STATUS" != "completed" ]; then
      echo "⏳ Waiting for workflows to complete before syncing..."

      while true; do
        CHANGELOG_STATUS=$(gh run list --workflow=changelog-automation.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")
        HISTORY_STATUS=$(gh run list --workflow=development-history.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")
        ROADMAP_STATUS=$(gh run list --workflow=roadmap-update.yml --branch=$BRANCH --limit=1 --json status --jq '.[0].status' 2>/dev/null || echo "completed")

        if [ "$CHANGELOG_STATUS" = "completed" ] && [ "$HISTORY_STATUS" = "completed" ] && [ "$ROADMAP_STATUS" = "completed" ]; then
          echo "✅ All workflows completed"
          break
        fi

        echo "   Changelog: $CHANGELOG_STATUS | History: $HISTORY_STATUS | Roadmap: $ROADMAP_STATUS"
        sleep 10
      done
    fi

    # Pull and rebase workflow commits (safe because working directory is clean)
    git pull --rebase origin $BRANCH
    echo "✅ Synced $BEHIND workflow commit(s)"
  fi

  # Push our commit(s)
  git push origin $BRANCH

  # Trigger workflows
  gh workflow run changelog-automation.yml --ref $BRANCH
  gh workflow run development-history.yml --ref $BRANCH
  gh workflow run roadmap-update.yml --ref $BRANCH

  echo ""
  echo "✅ Commit pushed and workflows triggered on branch: $BRANCH"
  echo "📝 Updates will run asynchronously (1-3 minutes)"
fi
```

**Branch-aware automation:**
- ✅ Feature branches: Workflows update your branch's CHANGELOG.md and ROADMAP.md
- ✅ When creating PR: Conflict resolver automatically merges any conflicts
- ✅ Main branch: Workflows run on merge and daily at midnight PST via schedule
- ✅ No manual conflict resolution needed - intelligent deduplication handles everything

**To skip changelog automation:**
Add `[skip changelog]` to your commit message.