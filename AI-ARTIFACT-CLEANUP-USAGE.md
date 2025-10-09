# AI Artifact Cleanup Workflow - Usage Guide

## Overview

The AI Artifact Cleanup workflow now supports **manual triggering** in addition to automatic PR-based cleanup. This provides flexibility for different cleanup scenarios while maintaining safety through configurable strategies.

## Trigger Methods

### 1. Automatic (Existing Behavior)

**PR Events:**
- Automatically runs on PR `opened`, `synchronize`, `reopened`
- Cleans artifacts from PR branch
- Posts analysis comment to PR

**Comment Trigger:**
- Use `@claude-artifacts` in PR comment
- Re-runs full artifact analysis
- Updates PR with new findings

### 2. Manual Trigger (NEW)

**Command:**
```bash
gh workflow run ai-artifact-cleanup.yml [options]
```

**Available Strategies:**
- `create-pr` (default, safe): Creates PR for review
- `push-direct` (fast): Pushes directly to target branch

---

## Usage Examples

### 🧪 Test Run (Recommended First Step)

Analyze without making any changes:

```bash
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=main \
  -f dry_run=true
```

**What happens:**
- ✅ Analyzes all files in main branch
- ✅ Shows what would be removed (with evidence)
- ✅ Shows what would be kept (with rationale)
- ❌ Makes NO changes to repository
- 📊 Outputs detailed report to workflow logs

**View results:**
```bash
gh run list --workflow=ai-artifact-cleanup.yml --limit 1
gh run view <run-id> --log
```

---

### 📝 Safe Cleanup (Default - Recommended)

Create a PR for artifact cleanup:

```bash
# Use defaults (main branch, create-pr strategy)
gh workflow run ai-artifact-cleanup.yml

# Or explicitly specify
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=main \
  -f strategy=create-pr
```

**What happens:**
- ✅ Analyzes main branch for artifacts
- ✅ Creates new branch: `artifact-cleanup-YYYYMMDD-HHMMSS`
- ✅ Commits artifact removals to new branch
- ✅ Creates pull request with detailed analysis
- ✅ You review PR before merging
- ✅ Safe - allows human verification

**After running:**
1. Check your PRs: `gh pr list`
2. Review the created PR
3. Merge if satisfied with artifact removal

---

### ⚡ Fast Cleanup (Direct Push)

Push cleanup directly to target branch (bypasses review):

```bash
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=main \
  -f strategy=push-direct
```

**⚠️ WARNING:**
- Changes are immediate
- No code review step
- AI determines what to remove
- Use only when confident in artifact detection

**What happens:**
- ✅ Analyzes target branch
- ✅ Removes artifacts immediately
- ✅ Commits with `[skip ci]` to prevent loops
- ✅ Pushes directly to specified branch
- ⚠️ Bypasses pull request review

**When to use:**
- Emergency cleanup after accidental merge
- Trusted artifact patterns (obvious files in `docs/`, `PRPs/`)
- Periodic maintenance on main branch
- You've already validated with dry-run

---

### 🌿 Clean Feature Branch

Clean a specific feature branch:

```bash
# Safe approach - create PR
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=feature/my-branch \
  -f strategy=create-pr

# Fast approach - direct push
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=feature/my-branch \
  -f strategy=push-direct
```

---

## Execution Modes Comparison

| Mode | Safety | Speed | Review | Use Case |
|------|--------|-------|--------|----------|
| **Dry Run** | 🟢 Highest | 🟢 Fast | N/A | Testing, validation |
| **Create PR** | 🟢 High | 🟡 Medium | ✅ Yes | Initial cleanup, uncertain artifacts |
| **Push Direct** | 🟡 Medium | 🟢 Fast | ❌ No | Emergency, obvious artifacts |
| **PR Event** | 🟢 High | 🟢 Fast | ✅ Yes | Standard PR workflow |

---

## Workflow Inputs

### `target_branch`
- **Type:** String
- **Required:** No
- **Default:** `main`
- **Description:** Branch to analyze and clean

### `strategy`
- **Type:** Choice
- **Required:** Yes
- **Default:** `create-pr`
- **Options:**
  - `create-pr`: Create pull request (safe)
  - `push-direct`: Push directly to branch (fast)
- **Description:** How to handle cleanup changes

### `dry_run`
- **Type:** Boolean
- **Required:** No
- **Default:** `false`
- **Description:** Analyze only, make no changes

---

## Safety Features

### 1. Dry Run Mode
- Test artifact detection without risk
- See exactly what would be removed
- Validate logic before committing

### 2. Default to PR Creation
- Human review before changes merged
- Transparent decision making
- Evidence-based artifact classification

### 3. Skip CI Prevention
- `[skip ci]` in direct push commits
- Prevents infinite workflow loops
- Follows project automation patterns

### 4. Semantic Analysis
- AI reads file content, not just patterns
- Evidence-based classification
- Uncertainty flagged for review

### 5. Loop Prevention
- PRs from `artifact-cleanup-*` branches are automatically skipped
- Prevents workflow from re-checking its own cleanup PRs
- No infinite loops when using `create-pr` strategy

---

## Reserved Branch Prefix

**⚠️ Important:** The branch prefix `artifact-cleanup-*` is reserved for automated cleanup PRs.

**Used by:** Manual trigger with `create-pr` strategy

**Behavior:**
- Workflow automatically skips PRs from branches starting with `artifact-cleanup-`
- These PRs contain cleaned artifacts by definition and don't need re-checking
- Prevents infinite workflow loops

**Branch naming pattern:** `artifact-cleanup-YYYYMMDD-HHMMSS`

**Example:** `artifact-cleanup-20251008-162345`

**Note:** Avoid using this prefix for manual branches. If you need to manually trigger the workflow on a cleanup PR, use the `@claude-artifacts` comment trigger.

---

## Common Workflows

### Initial Repository Cleanup

When you first add this workflow to clean existing artifacts:

```bash
# Step 1: Test what would be removed
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=main \
  -f dry_run=true

# Step 2: Review dry-run output
gh run list --workflow=ai-artifact-cleanup.yml --limit 1
gh run view <run-id> --log

# Step 3: Create PR for safe review
gh workflow run ai-artifact-cleanup.yml \
  -f target_branch=main \
  -f strategy=create-pr

# Step 4: Review and merge PR
gh pr list
gh pr view <pr-number>
gh pr merge <pr-number>
```

### Periodic Maintenance

Monthly cleanup of any artifacts that slipped through:

```bash
# Direct approach (trusted patterns)
gh workflow run ai-artifact-cleanup.yml \
  -f strategy=push-direct

# Or safe approach (create PR)
gh workflow run ai-artifact-cleanup.yml
```

### Emergency Cleanup

Artifacts accidentally merged to main:

```bash
# Fast removal
gh workflow run ai-artifact-cleanup.yml \
  -f strategy=push-direct
```

---

## Troubleshooting

### Workflow Not Showing in GitHub UI

**Problem:** "Run workflow" button not visible in Actions tab

**Cause:** Workflow must exist on default branch (main)

**Solution:**
```bash
# Commit and push workflow to main
git add .github/workflows/ai-artifact-cleanup.yml
git commit -m "feat: add manual trigger to artifact cleanup workflow"
git push origin main
```

### Protected Branch Issues

**Problem:** Direct push fails due to branch protection

**Cause:** `GITHUB_TOKEN` lacks permission to push to protected branch

**Solution:**
- Use `create-pr` strategy instead (works with protected branches)
- Or configure branch protection to allow GitHub Actions bot
- Or use PAT with proper permissions (advanced)

### Infinite Loop Detection

**Problem:** Workflow triggers itself

**Prevention:**
- Workflow includes `[skip ci]` in commit messages
- Job condition checks prevent workflow_dispatch from triggering on bot commits

---

## Best Practices

### ✅ Do:
- **Always test with dry-run first** when using manual triggers
- **Use create-pr strategy** for uncertain artifact classifications
- **Review workflow logs** after dry-run to verify detection logic
- **Use push-direct** only for obvious artifacts (docs/, PRPs/, .bmad-core/)

### ❌ Don't:
- **Don't use push-direct** without dry-run validation
- **Don't ignore uncertain files** in analysis reports
- **Don't skip reviewing** created PRs before merging

---

## Integration with Project Workflow

This workflow integrates with CODEX development workflow:

- **Development:** Contributors use artifacts (PRPs, docs/) in feature branches
- **PR Review:** Automatic cleanup runs on PR events
- **Merge:** Only production code (`.codex/`) merged to main
- **Maintenance:** Periodic manual cleanup for safety

---

## Monitoring and Logs

### Check Recent Runs
```bash
gh run list --workflow=ai-artifact-cleanup.yml --limit 10
```

### View Specific Run
```bash
gh run view <run-id>
gh run view <run-id> --log
```

### Watch Live Execution
```bash
gh run watch <run-id>
```

---

## Advanced Usage

### Clean Multiple Branches

```bash
# Clean several feature branches
for branch in feature/auth feature/api feature/ui; do
  gh workflow run ai-artifact-cleanup.yml \
    -f target_branch=$branch \
    -f strategy=push-direct
  sleep 10  # Rate limiting
done
```

### Scheduled Cleanup (Future Enhancement)

Add to workflow triggers:
```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

---

## Support and Feedback

- **Issues:** Report bugs or unexpected behavior
- **Improvements:** Suggest enhancements to artifact detection
- **Questions:** Ask about artifact classification decisions

---

**Last Updated:** 2025-10-08
**Version:** 1.1.0 (Manual trigger support added)
