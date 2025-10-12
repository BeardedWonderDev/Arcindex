# Test Plan for AI Artifact Enforcement

**Created:** 2025-10-08
**System:** AI-First Artifact Enforcement (Option 2 Hybrid)
**Status:** Ready for Testing

## Overview

This test plan validates the two-workflow AI artifact enforcement system:
- `ai-artifact-cleanup.yml` - Specialized artifact analysis workflow
- `claude.yml` - General Claude interactions (excludes @claude-artifacts)

## Prerequisites

- [ ] CLAUDE_CODE_OAUTH_TOKEN secret configured in repository
- [ ] Claude Code GitHub App installed on repository
- [ ] All implementation files committed to feature branch
- [ ] Test PR branch created

## Test 1: Automatic PR Analysis

**Objective:** Verify ai-artifact-cleanup.yml runs automatically on PR events

**Steps:**
1. Create a test branch with known AI artifacts:
   ```bash
   git checkout -b test/artifact-enforcement
   echo "# PRP Test" > test-artifact.prp.md
   echo "<codebase></codebase>" > flattened-codebase.xml
   echo "# Real docs" > docs/test-documentation.md
   git add .
   git commit -m "test: add artifacts for validation"
   git push origin test/artifact-enforcement
   ```

2. Create PR from test branch to main
3. Wait for workflow to trigger

**Expected Results:**
- [ ] ai-artifact-cleanup.yml workflow starts automatically
- [ ] Real-time progress checkboxes appear in PR comment
- [ ] Workflow completes within 2 minutes
- [ ] Artifacts (test-artifact.prp.md, flattened-codebase.xml) are removed
- [ ] Legitimate file (docs/test-documentation.md) is kept
- [ ] Commit created with message "chore: remove AI workflow artifacts [bot]"
- [ ] PR comment includes tables: Removed, Kept, Uncertain
- [ ] .claude/artifact-exceptions.txt is updated (if learning occurred)

## Test 2: @claude-artifacts Keyword Trigger

**Objective:** Verify specialized workflow runs when @claude-artifacts is mentioned

**Steps:**
1. On existing PR, add comment:
   ```
   @claude-artifacts re-check
   ```

2. Wait for workflow to trigger

**Expected Results:**
- [ ] ai-artifact-cleanup.yml workflow starts (NOT claude.yml)
- [ ] Complete artifact analysis runs
- [ ] Progress tracked with checkboxes
- [ ] New PR comment posted with analysis results
- [ ] No workflow conflicts (only one workflow runs)

## Test 3: @claude Feedback - Keep File

**Objective:** Verify general workflow handles "keep file" requests

**Steps:**
1. Identify a file marked as "uncertain" in PR comment
2. Add comment:
   ```
   @claude keep docs/planning.md - this is our project roadmap, not AI planning
   ```

3. Wait for workflow response

**Expected Results:**
- [ ] claude.yml workflow runs (NOT ai-artifact-cleanup.yml)
- [ ] File is kept (not removed)
- [ ] .claude/artifact-exceptions.txt is updated with new exception
- [ ] Commit created updating exception file
- [ ] Response confirms file kept and exception added
- [ ] Future PRs won't flag this file

## Test 4: @claude Feedback - Remove File

**Objective:** Verify general workflow handles "remove file" requests

**Steps:**
1. Add a test artifact to PR branch
2. Comment on PR:
   ```
   @claude remove test-notes.md - that's definitely an AI artifact
   ```

3. Wait for workflow response

**Expected Results:**
- [ ] claude.yml workflow runs (NOT ai-artifact-cleanup.yml)
- [ ] File is removed from PR branch
- [ ] Commit created removing the file
- [ ] Response confirms removal
- [ ] Pattern learned for future PRs

## Test 5: No Workflow Conflicts

**Objective:** Verify @claude and @claude-artifacts don't conflict

**Steps:**
1. Comment on PR:
   ```
   @claude help me refactor the authentication module
   ```

2. Wait for workflow

**Expected Results:**
- [ ] claude.yml runs normally
- [ ] No artifact workflows triggered
- [ ] Response is about refactoring (not artifacts)
- [ ] Only one workflow runs

## Test 6: Uncertain Files Handling

**Objective:** Verify workflow correctly identifies and reports uncertain files

**Steps:**
1. Create PR with ambiguous file:
   ```bash
   echo "# Planning notes" > docs/planning.md
   echo "Could be project planning or AI planning" >> docs/planning.md
   ```

2. Create PR

**Expected Results:**
- [ ] ai-artifact-cleanup.yml runs
- [ ] File marked as "uncertain" in PR comment
- [ ] Table shows why file is uncertain
- [ ] Instructions provided for how to respond
- [ ] Instructions mention @claude (not @claude-artifacts)
- [ ] File is NOT removed (conservative approach)

## Test 7: Learning System Integration

**Objective:** Verify exception file is consulted and updated

**Steps:**
1. Add exception to .claude/artifact-exceptions.txt:
   ```
   docs/architecture.md # Real architecture - Test - 2025-10-08
   ```

2. Create PR with docs/architecture.md changes
3. Observe workflow behavior

**Expected Results:**
- [ ] Workflow reads artifact-exceptions.txt
- [ ] docs/architecture.md is NOT flagged as artifact
- [ ] File appears in "Kept" table with reason
- [ ] Exception file reference shown in reasoning

## Test 8: YAML Syntax Validation

**Objective:** Verify workflows are syntactically correct

**Steps:**
1. GitHub Actions parses workflows successfully
2. No YAML syntax errors in logs

**Expected Results:**
- [ ] Both workflows parse without errors
- [ ] No syntax warnings in GitHub Actions
- [ ] Workflows execute successfully

## Test 9: Permissions Validation

**Objective:** Verify workflows have correct permissions

**Steps:**
1. Check workflow execution logs
2. Verify git operations succeed

**Expected Results:**
- [ ] ai-artifact-cleanup.yml can commit and push
- [ ] ai-artifact-cleanup.yml can comment on PRs
- [ ] claude.yml can commit and push
- [ ] claude.yml can comment on PRs
- [ ] No permission errors in logs

## Test 10: Content-Based Analysis

**Objective:** Verify semantic analysis (not just pattern matching)

**Steps:**
1. Create file matching artifact pattern but with legitimate content:
   ```bash
   echo "# Context Manager" > src/context-manager.ts
   echo "export class ContextManager { ... }" >> src/context-manager.ts
   ```

2. Create PR

**Expected Results:**
- [ ] File is analyzed by content (not just filename)
- [ ] File is kept (recognized as production code)
- [ ] Reasoning explains it's legitimate despite "context" in name
- [ ] Pattern may be added to exceptions

## Post-Test Cleanup

After completing all tests:

1. [ ] Delete test branch
2. [ ] Close test PR
3. [ ] Review .claude/artifact-exceptions.txt for test entries
4. [ ] Document any issues found
5. [ ] Update CLAUDE.md if needed based on learnings

## Success Criteria

All tests must pass for deployment to production:
- ✅ Workflows execute without errors
- ✅ Artifacts correctly identified and removed
- ✅ Legitimate files preserved
- ✅ No workflow conflicts
- ✅ Learning system functions correctly
- ✅ Natural language interactions work
- ✅ Content-based analysis works (not just patterns)

## Known Limitations

Document any limitations discovered during testing:
- [To be filled in during testing]

## Next Steps

1. Execute test plan sequentially
2. Document results for each test
3. Fix any issues discovered
4. Re-run failed tests
5. Proceed to deployment when all tests pass

---

**Test Execution Date:** [To be filled in]
**Tester:** [To be filled in]
**Results:** [To be documented during testing]
