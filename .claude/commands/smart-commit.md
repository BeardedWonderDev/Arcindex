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

## Phase 4: Auto-push and Workflow Trigger

8. Automatically push to remote:

```bash
BRANCH=$(git branch --show-current)
git push origin $BRANCH
```

9. Trigger changelog/roadmap automation workflows on current branch:

```bash
gh workflow run changelog-automation.yml --ref $BRANCH
gh workflow run development-history.yml --ref $BRANCH
gh workflow run roadmap-update.yml --ref $BRANCH
```

10. Confirm completion:
   - Show commit hash and branch
   - Confirm push succeeded
   - Confirm workflows triggered (show command output)
   - Display message: "✅ Workflows running on branch: $BRANCH. CHANGELOG.md and ROADMAP.md will be updated shortly."

**Branch-aware automation:**
- ✅ Feature branches: Workflows update your branch's CHANGELOG.md and ROADMAP.md
- ✅ When creating PR: Conflict resolver automatically merges any conflicts
- ✅ Main branch: Workflows run on merge and daily at midnight PST via schedule
- ✅ No manual conflict resolution needed - intelligent deduplication handles everything

**To skip changelog automation:**
Add `[skip changelog]` to your commit message.