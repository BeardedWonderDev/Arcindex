# AI Artifact Enforcement Deployment Checklist

**System:** Option 2 Hybrid (AI-First Artifact Enforcement)
**Created:** 2025-10-08
**Status:** Pre-Deployment

## Prerequisites

### 1. Repository Configuration

- [ ] **CLAUDE_CODE_OAUTH_TOKEN Secret Configured**
  - Location: Repository Settings → Secrets and variables → Actions
  - How to obtain:
    ```bash
    claude
    /install-github-app
    # Follow prompts to authenticate and grant permissions
    ```
  - Verify: Check Settings → Secrets → Actions for CLAUDE_CODE_OAUTH_TOKEN

- [ ] **Claude Code GitHub App Installed**
  - Install at: https://github.com/apps/claude-code-action
  - Grant permissions to repository
  - Verify: Settings → GitHub Apps shows claude-code-action

- [ ] **Repository Permissions**
  - Workflows have write access to repository
  - Actions enabled in repository settings
  - No branch protection rules blocking bot commits (or bot is allowlisted)

### 2. File Verification

- [ ] **All required files exist:**
  ```bash
  ls -l .github/workflows/ai-artifact-cleanup.yml
  ls -l .github/workflows/claude.yml
  ls -l CLAUDE.md
  ls -l CONTRIBUTING.md
  ls -l .claude/artifact-exceptions.txt
  ```

- [ ] **Files are in correct locations:**
  - CLAUDE.md in project root (NOT .claude/)
  - artifact-exceptions.txt in .claude/ directory
  - Both workflows in .github/workflows/

- [ ] **Files are committed to git:**
  ```bash
  git add .github/workflows/ai-artifact-cleanup.yml
  git add CLAUDE.md
  git add CONTRIBUTING.md
  git add .claude/artifact-exceptions.txt
  git status
  ```

### 3. Workflow Validation

- [ ] **YAML Syntax Valid**
  - GitHub Actions can parse both workflows
  - No syntax errors when viewing in GitHub UI
  - Optional: Validate locally with yamllint or GitHub CLI

- [ ] **Key Features Present in ai-artifact-cleanup.yml:**
  - [ ] `track_progress: true`
  - [ ] Model: `claude-sonnet-4-5-20250929`
  - [ ] Triggers on pull_request and @claude-artifacts
  - [ ] Complete 7-step prompt
  - [ ] Permissions: contents, pull-requests, id-token

- [ ] **Key Features Present in claude.yml:**
  - [ ] Excludes @claude-artifacts mentions
  - [ ] Permissions: contents, pull-requests, issues
  - [ ] Full git history (`fetch-depth: 0`)

## Deployment Steps

### Phase 1: Pre-Deployment Testing (Recommended)

- [ ] **Create test branch:**
  ```bash
  git checkout -b test/artifact-enforcement-system
  ```

- [ ] **Commit all implementation files:**
  ```bash
  git add .github/workflows/ai-artifact-cleanup.yml
  git add CLAUDE.md
  git add CONTRIBUTING.md
  git add .claude/artifact-exceptions.txt
  git commit -m "feat: implement AI-first artifact enforcement system"
  ```

- [ ] **Create test PR:**
  ```bash
  git push origin test/artifact-enforcement-system
  # Create PR via GitHub UI or gh CLI
  gh pr create --title "Test: AI Artifact Enforcement System" \
               --body "Testing automated artifact cleanup workflows"
  ```

- [ ] **Add test artifacts to PR:**
  ```bash
  # Add known artifacts for testing
  echo "# Test PRP" > test.prp.md
  echo "<codebase></codebase>" > flattened-codebase.xml
  git add . && git commit -m "test: add artifacts for validation"
  git push
  ```

- [ ] **Verify ai-artifact-cleanup.yml runs automatically:**
  - Check GitHub Actions tab
  - Workflow should trigger on PR sync
  - Wait for completion

- [ ] **Test @claude-artifacts trigger:**
  ```
  Comment on PR: @claude-artifacts re-check
  ```
  - Verify workflow runs
  - Check for progress updates

- [ ] **Test @claude interactions:**
  ```
  Comment on PR: @claude keep test.prp.md - this is for testing
  ```
  - Verify general workflow handles it
  - Check exception file updated

- [ ] **Execute full test plan:**
  - Follow: docs/research/artifact-enforcement-test-plan.md
  - Document all results
  - Fix any issues found

### Phase 2: Production Deployment

- [ ] **Review test results:**
  - All tests passed
  - No unexpected behaviors
  - Performance acceptable (< 2 min per PR)

- [ ] **Merge to main:**
  ```bash
  # If tests passed, merge test PR
  gh pr merge test/artifact-enforcement-system --squash
  ```

- [ ] **Verify workflows active:**
  - Check .github/workflows/ in main branch
  - Workflows should appear in Actions tab

- [ ] **Monitor first production PR:**
  - Watch workflow execution closely
  - Check PR comments for accuracy
  - Verify artifacts removed correctly

### Phase 3: Post-Deployment Validation

- [ ] **First PR Monitoring (Critical):**
  - Manually review first 3-5 PRs with artifacts
  - Verify removals are correct
  - Check for false positives
  - Ensure no legitimate files removed

- [ ] **Exception List Building:**
  - Review .claude/artifact-exceptions.txt regularly
  - Add project-specific patterns as discovered
  - Update CLAUDE.md with learnings

- [ ] **Performance Monitoring:**
  - Workflow execution time (should be < 2 min)
  - Token usage (should be reasonable)
  - No workflow conflicts

- [ ] **Contributor Feedback:**
  - Ask contributors about their experience
  - Are instructions clear?
  - Any confusion about artifact handling?
  - Update CONTRIBUTING.md if needed

## Post-Deployment Tasks

### Week 1: Active Monitoring

- [ ] **Daily checks:**
  - Review all artifact cleanup actions
  - Monitor for false positives/negatives
  - Check exception file growth
  - Watch for workflow errors

- [ ] **Update documentation:**
  - Add any missing patterns to CLAUDE.md
  - Update CONTRIBUTING.md with FAQ
  - Document edge cases discovered

- [ ] **Tune prompts if needed:**
  - Adjust confidence thresholds
  - Clarify uncertain file handling
  - Improve PR comment formatting

### Month 1: System Refinement

- [ ] **Metrics Collection:**
  - PRs analyzed: _____
  - Artifacts removed: _____
  - False positives: _____
  - False negatives: _____
  - Uncertain files requiring review: _____

- [ ] **System Improvements:**
  - Review exception list effectiveness
  - Optimize prompt based on patterns
  - Adjust project-specific guidelines
  - Consider confidence scoring adjustments

- [ ] **Team Training:**
  - Share Quick Reference with team
  - Demonstrate @claude vs @claude-artifacts
  - Review example interactions
  - Address questions/concerns

### Ongoing: Maintenance

- [ ] **Monthly Review:**
  - Check exception file for outdated entries
  - Review accuracy metrics
  - Update CLAUDE.md with new patterns
  - Prune unnecessary exceptions

- [ ] **Quarterly Assessment:**
  - Evaluate system effectiveness
  - Compare to goals (accuracy, time saved)
  - Document ROI
  - Share learnings with team

## Rollback Plan

If issues arise during deployment:

### Immediate Rollback

```bash
# Option 1: Disable workflows temporarily
# Rename files to prevent execution
mv .github/workflows/ai-artifact-cleanup.yml \
   .github/workflows/ai-artifact-cleanup.yml.disabled
git commit -m "temp: disable artifact enforcement"
git push
```

### Partial Rollback

```bash
# Option 2: Keep learning system but disable auto-removal
# Edit ai-artifact-cleanup.yml and add to step 5:
# "Do NOT remove files automatically. Only analyze and report."
```

### Full Rollback

```bash
# Option 3: Revert implementation commit
git revert <commit-hash>
git push
```

## Success Criteria

System is considered successfully deployed when:

- ✅ **Accuracy:** > 95% correct artifact identification
- ✅ **False Positives:** < 2% of flagged files
- ✅ **Performance:** < 2 minutes per PR analysis
- ✅ **Adoption:** Contributors comfortable with system
- ✅ **Automation:** < 5% of PRs require manual intervention
- ✅ **Learning:** Exception list grows appropriately
- ✅ **Stability:** No workflow conflicts or errors

## Documentation Updates

After successful deployment:

- [ ] Update README.md with artifact policy overview
- [ ] Add badge showing artifact enforcement active
- [ ] Link to CONTRIBUTING.md in PR template
- [ ] Update team onboarding documentation
- [ ] Share deployment summary with stakeholders

## Contact & Support

**Issues:** https://github.com/anthropics/claude-code/issues
**Documentation:** https://docs.claude.com/claude-code
**Community:** [Project-specific contact info]

---

**Deployment Date:** [To be filled in]
**Deployed By:** [To be filled in]
**Status:** [To be updated during deployment]
