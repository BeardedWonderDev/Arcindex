# AI Artifact Enforcement - Full Implementation Prompt

**Use this prompt in a new Claude Code session to fully implement the AI-first artifact enforcement system.**

---

## Context

Implement a two-workflow system for automatically detecting and removing AI workflow artifacts from pull requests before they merge to main. This uses Claude Code's intelligence to understand file content (not just pattern matching) and provides automatic learning from maintainer feedback.

## Architecture Overview

**Two workflows with zero conflicts:**
1. **ai-artifact-cleanup.yml** - Specialized workflow triggered by PR events and `@claude-artifacts` keyword
2. **claude.yml** (existing, modified) - General workflow triggered by `@claude` (excludes `@claude-artifacts`)

**Key Innovation:** AI semantic analysis instead of brittle regex patterns. Claude reads file content to determine if something is an artifact vs. legitimate code.

## Required Reading (Priority Order)

Read these files to understand the complete plan:

1. **Primary Reference:**
   - `docs/research/ai-first-artifact-enforcement.md` - Complete specification

2. **Current State:**
   - `.github/workflows/claude.yml` - Existing general workflow (already updated to exclude @claude-artifacts)
   - `.github/workflows/claude-code-review.yml` - Example of Claude Code action usage
   - `.github/workflows/changelog-automation.yml` - Example of track_progress and learning
   - `.github/workflows/roadmap-update.yml` - Example of automated updates

3. **Project Context:**
   - `CONTRIBUTING.md` - Existing contributor guidelines (if exists)
   - `.gitignore` - Current ignore patterns
   - `.claude/` directory - Existing Claude configuration

## Implementation Steps

### Phase 1: Create Core Workflows (Parallel - Agent 1)

**Task:** Create the specialized artifact cleanup workflow

**Steps:**
1. Read `docs/research/ai-first-artifact-enforcement.md` section "Complete AI-First Workflow (Option 2 Hybrid)"
2. Create `.github/workflows/ai-artifact-cleanup.yml` with the complete workflow from the research doc
3. Ensure these key features are included:
   - Triggers on `pull_request` events AND `@claude-artifacts` comments
   - Has `track_progress: true` for real-time updates
   - Includes comprehensive prompt with all 7 steps
   - Has proper permissions: `contents: write`, `pull-requests: write`, `id-token: write`
   - Uses model: `claude-sonnet-4-5-20250929`
   - Includes automatic learning (step 7 in prompt)
4. Validate workflow YAML syntax

**Success Criteria:**
- File created at `.github/workflows/ai-artifact-cleanup.yml`
- YAML is valid
- All required sections present

---

### Phase 2: Create Project Documentation (Parallel - Agent 2)

**Task:** Create root CLAUDE.md with artifact guidance for general workflow

**Steps:**
1. Read `docs/research/ai-first-artifact-enforcement.md` section "Add Project-Specific Guidelines"
2. Create `CLAUDE.md` in project root with the complete template
3. Customize the "Project-Specific Decisions" section based on actual project structure:
   - Read existing `docs/` directory structure
   - Identify which docs are legitimate vs. AI artifacts
   - Update the "For this project specifically" section
4. Add any existing project conventions from current documentation
5. Ensure artifact handling guidance is complete and actionable

**Success Criteria:**
- File created at `CLAUDE.md` (project root)
- Artifact policy section complete
- Example interactions included
- Project-specific decisions documented

---

### Phase 3: Initialize Learning System (Parallel - Agent 3)

**Task:** Set up the exception tracking system

**Steps:**
1. Create directory `.claude/` if it doesn't exist
2. Create `.claude/artifact-exceptions.txt` with header:
   ```
   # AI Artifact Exception List
   # Format: pattern # reason - PR #number - date
   # This file is automatically updated by Claude Code
   ```
3. Review existing project files to identify any that might match artifact patterns but are legitimate
4. Add pre-emptive exceptions for known legitimate files
5. Ensure file is tracked by git (not in .gitignore)

**Success Criteria:**
- Directory `.claude/` exists
- File `.claude/artifact-exceptions.txt` created
- Header and format documented
- Any obvious exceptions pre-added

---

### Phase 4: Update Documentation (Parallel - Agent 4)

**Task:** Update CONTRIBUTING.md with artifact policy

**Steps:**
1. Read existing `CONTRIBUTING.md` (create if doesn't exist)
2. Add new section "AI Workflow Artifact Policy" with:
   - Explanation of what artifacts are
   - What contributors can do (commit to branches)
   - What happens at PR time (automatic cleanup)
   - How to respond to uncertain files
   - Reference to CLAUDE.md for details
3. Add Quick Reference table from research doc
4. Ensure it's contributor-friendly and clear

**Success Criteria:**
- CONTRIBUTING.md updated or created
- Artifact policy section added
- Clear instructions for contributors
- Links to relevant documentation

---

### Phase 5: Validation & Testing Setup (Sequential - After Phase 1-4)

**Task:** Validate all components work together

**Steps:**
1. **Validate Workflow Files:**
   ```bash
   # Check YAML syntax
   yamllint .github/workflows/ai-artifact-cleanup.yml
   # Or just ensure GitHub Actions can parse it
   ```

2. **Verify Claude.yml Exclusions:**
   - Read `.github/workflows/claude.yml`
   - Confirm it has `!contains(github.event.comment.body, '@claude-artifacts')` filters
   - Confirm permissions include `contents: write`, `pull-requests: write`
   - Confirm `fetch-depth: 0`

3. **Check File Locations:**
   - `CLAUDE.md` exists in project root (not .claude/)
   - `.claude/artifact-exceptions.txt` exists
   - `.github/workflows/ai-artifact-cleanup.yml` exists

4. **Create Test Plan Document:**
   Create `docs/research/artifact-enforcement-test-plan.md`:
   ```markdown
   # Test Plan for AI Artifact Enforcement

   ## Test 1: Automatic PR Analysis
   - [ ] Create PR with known artifacts (*.prp.md, flattened-codebase.xml)
   - [ ] Verify ai-artifact-cleanup.yml runs automatically
   - [ ] Check for real-time progress updates
   - [ ] Verify artifacts are removed and committed

   ## Test 2: @claude-artifacts Keyword
   - [ ] Comment on PR: "@claude-artifacts re-check"
   - [ ] Verify ai-artifact-cleanup.yml runs (not claude.yml)
   - [ ] Check for complete analysis

   ## Test 3: @claude Feedback (Keep File)
   - [ ] Comment: "@claude keep docs/test.md - legitimate file"
   - [ ] Verify claude.yml runs (not ai-artifact-cleanup.yml)
   - [ ] Check .claude/artifact-exceptions.txt is updated
   - [ ] Verify commit is created

   ## Test 4: @claude Feedback (Remove File)
   - [ ] Comment: "@claude remove test-artifact.md"
   - [ ] Verify claude.yml runs
   - [ ] Check file is removed
   - [ ] Verify commit is created

   ## Test 5: No Conflicts
   - [ ] Comment: "@claude help with feature X"
   - [ ] Verify claude.yml handles normally
   - [ ] No artifact workflows triggered

   ## Test 6: Uncertain Files
   - [ ] Create PR with ambiguous file (docs/planning.md)
   - [ ] Verify ai-artifact-cleanup marks as uncertain
   - [ ] Check PR comment has proper instructions
   - [ ] Verify instructions mention @claude (not @claude-artifacts)
   ```

5. **Document Next Steps:**
   Create `docs/research/deployment-checklist.md`:
   ```markdown
   # Deployment Checklist

   ## Prerequisites
   - [ ] CLAUDE_CODE_OAUTH_TOKEN secret configured in repository
   - [ ] Repository has Claude Code GitHub App installed

   ## Deployment Steps
   1. [ ] Commit all new files to a feature branch
   2. [ ] Create PR to test the system
   3. [ ] Verify ai-artifact-cleanup.yml runs on the PR
   4. [ ] Test @claude and @claude-artifacts interactions
   5. [ ] Merge to main once validated

   ## Post-Deployment
   - [ ] Monitor first few PRs closely
   - [ ] Build up exception list
   - [ ] Adjust CLAUDE.md based on learnings
   - [ ] Document any issues or improvements needed
   ```

**Success Criteria:**
- All files validated
- Test plan created
- Deployment checklist created
- No syntax errors

---

### Phase 6: Create Summary Report (Sequential - After Phase 5)

**Task:** Generate implementation summary for review

**Steps:**
1. Create `docs/research/implementation-summary.md` with:
   - What was implemented
   - File locations and purposes
   - How to test the system
   - Quick reference for using both workflows
   - Link to all relevant documentation

2. Include verification checklist:
   ```markdown
   ## Verification Checklist

   ### Files Created
   - [ ] .github/workflows/ai-artifact-cleanup.yml
   - [ ] CLAUDE.md (project root)
   - [ ] .claude/artifact-exceptions.txt
   - [ ] docs/research/artifact-enforcement-test-plan.md
   - [ ] docs/research/deployment-checklist.md
   - [ ] docs/research/implementation-summary.md

   ### Files Updated
   - [ ] .github/workflows/claude.yml (already done)
   - [ ] CONTRIBUTING.md

   ### Validations Passed
   - [ ] YAML syntax valid
   - [ ] CLAUDE.md complete
   - [ ] Exception system initialized
   - [ ] Documentation updated
   - [ ] Test plan created
   ```

3. Add "What Happens Next" section with:
   - How to test before deploying
   - Expected behavior on first PR
   - How system improves over time
   - Where to find help

**Success Criteria:**
- Implementation summary created
- All files accounted for
- Clear next steps documented

---

## Execution Strategy

**Run these phases in parallel where possible:**

```
Phase 1 (Agent 1) ─┐
Phase 2 (Agent 2) ─┼─→ Phase 5 (Validation) ─→ Phase 6 (Summary)
Phase 3 (Agent 3) ─┤
Phase 4 (Agent 4) ─┘
```

**Agent Assignments:**
- **Agent 1 (Workflow Specialist):** Phase 1 - Create ai-artifact-cleanup.yml
- **Agent 2 (Documentation Specialist):** Phase 2 - Create root CLAUDE.md
- **Agent 3 (System Setup):** Phase 3 - Initialize learning system
- **Agent 4 (Contributor Experience):** Phase 4 - Update CONTRIBUTING.md
- **Main/Coordinator:** Phases 5-6 - Validation and summary

## Success Criteria (Overall)

✅ **Workflows Created:**
- ai-artifact-cleanup.yml exists and is valid
- claude.yml properly excludes @claude-artifacts

✅ **Documentation Complete:**
- Root CLAUDE.md with artifact guidance
- CONTRIBUTING.md updated
- Test plan created
- Deployment checklist created

✅ **System Initialized:**
- Exception file created
- Pre-existing exceptions added
- All files committed

✅ **Validation Passed:**
- YAML syntax valid
- File locations correct
- No conflicts between workflows
- Test plan comprehensive

✅ **Ready to Deploy:**
- Implementation summary created
- Clear testing instructions
- Next steps documented

## Important Notes

1. **DO NOT** modify the existing claude.yml beyond what's already done (it's been updated to exclude @claude-artifacts)

2. **DO** use the exact templates from `docs/research/ai-first-artifact-enforcement.md`

3. **DO** ensure CLAUDE.md is in project root, not .claude/

4. **DO** make .claude/artifact-exceptions.txt tracked by git

5. **DO** validate all YAML syntax before considering complete

6. **DO** create comprehensive test plans for post-implementation validation

## Expected Output

At the end of execution, you should have:

1. **New Files Created (6):**
   - .github/workflows/ai-artifact-cleanup.yml
   - CLAUDE.md
   - .claude/artifact-exceptions.txt
   - docs/research/artifact-enforcement-test-plan.md
   - docs/research/deployment-checklist.md
   - docs/research/implementation-summary.md

2. **Updated Files (1):**
   - CONTRIBUTING.md

3. **Validation:**
   - All YAML valid
   - All documentation complete
   - System ready to test

4. **Next Steps Documented:**
   - Test plan ready
   - Deployment checklist ready
   - Clear instructions for first use

## Questions to Answer Before Starting

1. Does CLAUDE_CODE_OAUTH_TOKEN secret exist in repository?
   - If NO: Document this as prerequisite in deployment checklist
   - If YES: Proceed with implementation

2. Does CONTRIBUTING.md exist?
   - If NO: Create new file
   - If YES: Add artifact policy section

3. Are there obvious files that match artifact patterns but are legitimate?
   - Add to .claude/artifact-exceptions.txt pre-emptively

## Post-Implementation Commands

After all agents complete, run these validation commands:

```bash
# Verify file structure
ls -la .github/workflows/ai-artifact-cleanup.yml
ls -la CLAUDE.md
ls -la .claude/artifact-exceptions.txt
ls -la CONTRIBUTING.md

# Validate YAML
cat .github/workflows/ai-artifact-cleanup.yml | grep -E "track_progress|@claude-artifacts"

# Check claude.yml exclusions
cat .github/workflows/claude.yml | grep -E "@claude-artifacts"

# Verify documentation
head -20 CLAUDE.md | grep -i "artifact"

# Check test plan exists
ls -la docs/research/artifact-enforcement-test-plan.md
```

---

## Ready to Execute

This prompt provides everything needed to fully implement the Option 2 Hybrid AI artifact enforcement system. Use with Claude Code's parallel agent execution for fastest results.

**Estimated Time:** 20-30 minutes with parallel agents
**Complexity:** Medium (well-specified, clear templates)
**Risk:** Low (doesn't modify existing code, only adds workflows)

---

**Command to start:**
```
/codex implement the AI artifact enforcement system using the plan in docs/research/ai-first-artifact-enforcement.md
```

Or paste this entire file as context and ask Claude Code to execute the phases in parallel.
