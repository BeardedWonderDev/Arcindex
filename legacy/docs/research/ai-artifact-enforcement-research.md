# AI Workflow Artifact Enforcement Research
**Comprehensive Strategy for Preventing AI-Assisted Development Artifacts from Contaminating Main Branches**

**Research Completed:** January 2025
**Focus:** Merge-time enforcement for multi-contributor AI-assisted projects
**Scope:** GitHub Actions, GitLab CI, multi-methodology support (BMAD, PRP, Claude Code, Cursor, Aider)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Enforcement Architecture](#enforcement-architecture)
3. [Enforcement Layer Catalog](#enforcement-layer-catalog)
4. [Artifact Detection Patterns](#artifact-detection-patterns)
5. [Implementation Playbook](#implementation-playbook)
6. [Real-World Analysis](#real-world-analysis)
7. [Contributor Guidelines Template](#contributor-guidelines-template)
8. [Troubleshooting & Edge Cases](#troubleshooting--edge-cases)
9. [Decision Framework](#decision-framework)
10. [Appendices](#appendices)

---

## Executive Summary

### Key Finding: Multi-Layer Defense-in-Depth Strategy

The most effective approach to preventing AI workflow artifacts from entering main branches is a **multi-layer enforcement strategy** that combines:

1. **Branch Protection Rules** (Layer 1) - Native platform controls
2. **CI/CD Validation Workflows** (Layer 2) - Automated file pattern detection
3. **Bot Automation** (Layer 3) - Contributor feedback and guidance
4. **Review Enforcement** (Layer 4) - CODEOWNERS and manual checkpoints

### Critical Insight: Merge-Time Focus

**All enforcement occurs at PR/merge time, NOT during local development.** Contributors maintain complete freedom to work with AI artifacts in their own branches and forks. The enforcement boundary is crossed only when attempting to merge into protected branches (main, develop, etc.).

### Quick Wins (Immediate Implementation, Day 1)

1. **Basic File Pattern Validation Workflow** (~30 minutes)
   - GitHub Action using `xalvarez/prevent-file-change-action`
   - Blocks common AI artifact patterns: `.prp.md`, `flattened-codebase.xml`, `INITIAL.md`
   - Fails PR check if artifacts detected
   - **ROI:** Immediate prevention of most common artifacts

2. **Branch Protection Rule** (~5 minutes)
   - Enable "Require status checks to pass before merging"
   - Select validation workflow as required check
   - **ROI:** Prevents any PR from merging without passing validation

3. **Basic .gitignore Extension** (~10 minutes)
   - Add common AI artifact patterns
   - Reduces accidental commits (defense-in-depth)
   - **ROI:** Prevents artifacts from entering git tracking

### Common Pitfalls to Avoid

1. **❌ Using .gitignore as Only Defense**
   - Reason: Contributors can override with `git add -f`
   - Solution: Must combine with CI/CD validation

2. **❌ Relying on CODEOWNERS Alone**
   - Reason: Only enforces manual review, doesn't block specific files
   - Solution: Use as Layer 4, not Layer 1-2

3. **❌ Overly Broad Path Filtering**
   - Reason: Can create false positives, block legitimate files
   - Solution: Use precise regex patterns with exclusion rules

4. **❌ Missing Status Check Configuration**
   - Reason: Workflow may run but not block merge
   - Solution: Configure branch protection to require check passage

5. **❌ Skipped Workflows Remain "Pending"**
   - Reason: Path-filtered workflows stay pending, blocking merges
   - Solution: Use inverse path filtering for "always pass" dummy workflows

### Recommended Architecture for BMAD/CODEX Projects

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Branch Protection                                  │
│  ✓ Require status checks (validation-workflow)              │
│  ✓ Require pull request reviews (1 reviewer minimum)        │
│  ✓ Dismiss stale reviews on new commits                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: CI/CD Validation Workflow                          │
│  ✓ Detect changed files in PR                               │
│  ✓ Match against artifact patterns                          │
│  ✓ Fail check if artifacts found                            │
│  ✓ Generate detailed error output                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Bot Automation                                     │
│  ✓ Post PR comment with violation details                   │
│  ✓ List specific files to remove                            │
│  ✓ Provide cleanup commands                                 │
│  ✓ Link to contributor guidelines                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: CODEOWNERS Review (Optional)                       │
│  ✓ Require review for sensitive paths                       │
│  ✓ Documentation maintainer approval                        │
│  ✓ Configuration file review                                │
└─────────────────────────────────────────────────────────────┘
```

### Success Metrics

- **Zero** AI artifacts merged to main branch
- **< 5 minutes** contributor time to fix validation failures
- **< 10%** false positive rate on legitimate files
- **100%** of validation failures include actionable guidance

---

## Enforcement Architecture

### Overview: Defense-in-Depth Approach

The enforcement architecture uses multiple layers to ensure comprehensive protection while maintaining developer productivity. Each layer provides different benefits and addresses different failure modes.

### Layer Comparison Matrix

| Layer | Enforcement Point | Automation Level | Developer Friction | Effectiveness | Setup Time |
|-------|-------------------|------------------|-------------------|---------------|------------|
| **1. Branch Protection** | Pre-merge | High | Low | High | 5 min |
| **2. CI/CD Validation** | PR submission | Full | Low | Very High | 30 min |
| **3. Bot Feedback** | PR submission | Full | Very Low | Medium | 2 hours |
| **4. CODEOWNERS** | PR review | Manual | Medium | Medium | 15 min |

### Layer 1: Branch Protection Rules

**Purpose:** Native platform controls that enforce policies at the branch level.

**Capabilities:**
- Require status checks before merging
- Require PR reviews
- Restrict who can push to protected branches
- Require signed commits
- Require linear history

**Limitations:**
- Cannot directly prevent specific file patterns
- Requires Layer 2 (CI/CD) for file-level validation
- Configuration is branch-specific

**Best For:**
- Enforcing that validation workflows run and pass
- Preventing direct pushes to main/protected branches
- Requiring human review as additional checkpoint

### Layer 2: CI/CD Validation Workflows

**Purpose:** Automated file pattern detection and validation.

**Capabilities:**
- Detect changed files in PRs
- Match against regex/glob patterns
- Fail CI check to block merge
- Generate detailed error messages
- Support complex validation logic

**Limitations:**
- Requires initial configuration
- Patterns must be maintained
- Can have false positives if poorly configured

**Best For:**
- Primary enforcement mechanism for file-level restrictions
- Detecting AI artifact patterns
- Providing immediate feedback to contributors
- Supporting multiple methodologies (BMAD, PRP, etc.)

### Layer 3: Bot Automation

**Purpose:** Provide contributor-friendly feedback and guidance.

**Capabilities:**
- Post PR comments automatically
- List specific files that violate rules
- Provide cleanup commands
- Link to documentation
- Update comments on new commits

**Limitations:**
- Requires bot configuration and permissions
- Doesn't block merge (requires Layer 1+2)
- Additional complexity

**Best For:**
- Improving contributor experience
- Reducing time to fix validation failures
- Educating contributors about policies
- Providing context-specific guidance

### Layer 4: CODEOWNERS Review

**Purpose:** Manual review checkpoint for sensitive paths.

**Capabilities:**
- Require approval from specific users/teams
- Path-based ownership assignment
- Integration with branch protection

**Limitations:**
- Manual process, not automated
- Doesn't prevent file changes, only requires review
- Can't block specific file patterns directly

**Best For:**
- Documentation review
- Configuration file changes
- Sensitive code areas
- Final human checkpoint

---

## Enforcement Layer Catalog

### GitHub Actions Solutions

#### Option 1: xalvarez/prevent-file-change-action (Recommended for Simplicity)

**Description:** Purpose-built action that fails PR workflow if specified file patterns are changed.

**Pros:**
- Simple, declarative configuration
- Regex pattern matching
- Trusted authors whitelist
- Mature, well-maintained
- Used by major projects (Prettier)

**Cons:**
- Only supports `pull_request_target` events
- Less flexible than custom scripts
- Limited to pattern matching

**Example Workflow:**

```yaml
name: Prevent AI Artifact Merge

on:
  pull_request_target:
    types: [opened, synchronize, reopened]

jobs:
  validate-no-artifacts:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read

    steps:
      - name: Prevent AI workflow artifacts from merging
        uses: xalvarez/prevent-file-change-action@v2
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          # Regex pattern matching AI artifact files
          pattern: |
            .*\.prp\.md$|
            ^PRPs/.*\.md$|
            ^flattened-codebase\.xml$|
            ^INITIAL\.md$|
            ^\.bmad-flattenignore$|
            ^docs/stories/story-.*\.md$|
            ^\.aiderignore$|
            ^\.cursorignore$
          # Optional: Allow specific trusted users to merge artifacts
          # trustedAuthors: admin-user,ci-bot
          allowNewFiles: false
```

**Setup Time:** 15 minutes
**Maintenance:** Low (update pattern as needed)

#### Option 2: dorny/paths-filter + Custom Validation (Recommended for Flexibility)

**Description:** Detect changed files with paths-filter, then run custom validation logic.

**Pros:**
- Extremely flexible
- Can implement complex validation logic
- Provides outputs for conditional steps
- Good for monorepos
- Active maintenance, widely used

**Cons:**
- Requires more configuration
- More complex than Option 1
- Need to write custom validation logic

**Example Workflow:**

```yaml
name: PR Artifact Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  check-artifacts:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect changed files
        uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            artifacts:
              - '**/*.prp.md'
              - 'PRPs/**'
              - 'flattened-codebase.xml'
              - 'INITIAL.md'
              - '.bmad-flattenignore'
              - 'docs/stories/story-*.md'
              - 'docs/qa/assessments/**'
              - '.aiderignore'
              - '.cursorignore'
              - '.cursorindexingignore'
              - '**/.claude/**'
              - '**/context-*.md'
              - '**/planning-*.md'

      - name: Get list of artifact files
        if: steps.filter.outputs.artifacts == 'true'
        id: artifact-list
        run: |
          echo "Finding artifact files..."
          FILES=$(git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }} | \
            grep -E '\.(prp\.md|PRPs/|flattened-codebase\.xml|INITIAL\.md)' || true)
          echo "files<<EOF" >> $GITHUB_OUTPUT
          echo "$FILES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Fail if artifacts detected
        if: steps.filter.outputs.artifacts == 'true'
        run: |
          echo "❌ AI workflow artifacts detected in PR"
          echo ""
          echo "The following files should not be merged to main:"
          echo "${{ steps.artifact-list.outputs.files }}"
          echo ""
          echo "Please remove these files from your PR."
          echo "See CONTRIBUTING.md for guidelines on working with AI artifacts."
          exit 1

      - name: Post PR comment with guidance
        if: failure() && steps.filter.outputs.artifacts == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const files = `${{ steps.artifact-list.outputs.files }}`.split('\n').filter(f => f);
            const body = `## ❌ AI Workflow Artifacts Detected

            This PR contains AI workflow artifacts that should not be merged to the main branch.

            ### Files to Remove:
            ${files.map(f => `- \`${f}\``).join('\n')}

            ### How to Fix:

            1. Remove these files from your branch:
               \`\`\`bash
               git rm ${files.join(' ')}
               git commit -m "Remove AI workflow artifacts"
               git push
               \`\`\`

            2. Or, if you've already committed them, you can amend:
               \`\`\`bash
               git rm ${files.join(' ')}
               git commit --amend --no-edit
               git push --force-with-lease
               \`\`\`

            ### Why This Matters:
            AI workflow artifacts are valuable for individual development but can clutter the main branch and confuse other contributors. Keep them in your fork/branch for context, but don't merge them upstream.

            📖 See [CONTRIBUTING.md](../CONTRIBUTING.md) for more details.`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

**Setup Time:** 30-45 minutes
**Maintenance:** Medium (update filters and validation logic)

#### Option 3: tj-actions/changed-files (Alternative)

**Description:** Comprehensive action to retrieve all types of changed files.

**Pros:**
- Very feature-rich
- Outputs for all change types (added, modified, deleted, renamed)
- JSON output option
- Can filter by file type

**Cons:**
- More complex than needed for simple use cases
- Requires custom validation script

**Example Workflow:**

```yaml
name: Validate Changed Files

on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v45
        with:
          files: |
            **/*.prp.md
            PRPs/**
            flattened-codebase.xml
            INITIAL.md
            .bmad-flattenignore
            docs/stories/story-*.md

      - name: Check for artifacts
        if: steps.changed-files.outputs.any_changed == 'true'
        run: |
          echo "Artifact files changed:"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"
          exit 1
```

**Setup Time:** 20-30 minutes
**Maintenance:** Low-Medium

### GitLab CI Solutions

#### GitLab CI with rules:changes

**Description:** Native GitLab CI feature using `rules:changes` with glob patterns.

**Pros:**
- Native to GitLab, no external dependencies
- Simple, declarative syntax
- Integrates with merge request pipelines
- No additional actions needed

**Cons:**
- GitLab-specific, not portable
- Less flexible than GitHub Actions ecosystem
- Requires understanding of GitLab CI syntax

**Example Pipeline:**

```yaml
# .gitlab-ci.yml

stages:
  - validate

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH

validate-no-artifacts:
  stage: validate
  image: alpine:latest
  script:
    - |
      echo "Checking for AI workflow artifacts..."

      # Get changed files
      CHANGED_FILES=$(git diff --name-only $CI_MERGE_REQUEST_DIFF_BASE_SHA $CI_COMMIT_SHA)

      # Define artifact patterns
      ARTIFACT_PATTERNS=(
        "\.prp\.md$"
        "^PRPs/"
        "^flattened-codebase\.xml$"
        "^INITIAL\.md$"
        "^\.bmad-flattenignore$"
        "^docs/stories/story-.*\.md$"
        "^\.aiderignore$"
        "^\.cursorignore$"
      )

      # Check for matches
      FOUND_ARTIFACTS=""
      for file in $CHANGED_FILES; do
        for pattern in "${ARTIFACT_PATTERNS[@]}"; do
          if echo "$file" | grep -qE "$pattern"; then
            FOUND_ARTIFACTS="$FOUND_ARTIFACTS\n  - $file"
          fi
        done
      done

      if [ -n "$FOUND_ARTIFACTS" ]; then
        echo "❌ AI workflow artifacts detected:"
        echo -e "$FOUND_ARTIFACTS"
        echo ""
        echo "Please remove these files before merging."
        exit 1
      fi

      echo "✅ No AI workflow artifacts detected"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.prp.md"
        - "PRPs/**"
        - "flattened-codebase.xml"
        - "INITIAL.md"
        - ".bmad-flattenignore"
        - "docs/stories/story-*.md"
        - ".aiderignore"
        - ".cursorignore"
  allow_failure: false
```

**Setup Time:** 20-30 minutes
**Maintenance:** Low-Medium

---

## Artifact Detection Patterns

### Pattern Library Structure

Patterns are organized by methodology and tool to support extensibility. Each pattern includes:
- **Pattern Type:** Regex, glob, or exact match
- **Methodology:** BMAD, PRP, general AI workflow
- **Risk Level:** High (always block), Medium (context-dependent), Low (warn only)
- **Description:** What the pattern matches and why

### BMAD (Breakthrough Method for Agile AI-Driven Development) Artifacts

#### High-Risk Patterns (Always Block)

| Pattern | Type | Description |
|---------|------|-------------|
| `flattened-codebase.xml` | Exact | BMAD codebase flattener output |
| `.bmad-flattenignore` | Exact | BMAD custom ignore patterns |
| `docs/stories/story-*.md` | Glob | BMAD story files generated by SM agent |
| `docs/qa/assessments/*.md` | Glob | BMAD QA assessment documents |

**Regex Pattern:**
```regex
^(flattened-codebase\.xml|\.bmad-flattenignore|docs/stories/story-.*\.md|docs/qa/assessments/.*\.md)$
```

#### Medium-Risk Patterns (Context-Dependent)

| Pattern | Type | Description | Legitimate Use Case |
|---------|------|-------------|-------------------|
| `docs/prd.md` | Exact | Product requirements doc | May be legitimate documentation |
| `docs/architecture.md` | Exact | Architecture documentation | May be legitimate if project uses this structure |

**Decision Logic:**
- If `docs/` is project documentation directory → **Allow**
- If `docs/` is BMAD artifact directory → **Block**
- Recommended: Use subdirectory like `docs/planning/` for project docs

### PRP (Product Requirement Prompt) Artifacts

#### High-Risk Patterns (Always Block)

| Pattern | Type | Description |
|---------|------|-------------|
| `**/*.prp.md` | Glob | PRP prompt files |
| `PRPs/**` | Glob | PRP directory and all contents |
| `INITIAL.md` | Exact | Initial feature request file |
| `**/context-*.md` | Glob | Context engineering files |
| `**/planning-*.md` | Glob | AI planning documents |

**Regex Pattern:**
```regex
^(.*\.prp\.md|PRPs/.*|INITIAL\.md|.*/context-.*\.md|.*/planning-.*\.md)$
```

### Tool-Specific Patterns

#### Claude Code

| Pattern | Type | Description |
|---------|------|-------------|
| `.claude/**` | Glob | Claude configuration and context (Note: `.claude/CLAUDE.md` may be legitimate) |
| `**/.claude/conversation-*.json` | Glob | Conversation logs |

**Note:** `.claude/CLAUDE.md` and `.claude/commands/` may contain legitimate project configuration. Consider allowing these with explicit rules.

#### Cursor

| Pattern | Type | Description |
|---------|------|-------------|
| `.cursorignore` | Exact | Cursor-specific ignore file (generally should be in .gitignore) |
| `.cursorindexingignore` | Exact | Cursor indexing ignore file |
| `.cursor/**` | Glob | Cursor configuration directory |

#### Aider

| Pattern | Type | Description |
|---------|------|-------------|
| `.aiderignore` | Exact | Aider-specific ignore file |
| `.aider/**` | Glob | Aider working directory |
| `.aider.input.history` | Exact | Aider command history |
| `.aider.chat.history.md` | Exact | Aider conversation history |

### Generic AI Workflow Patterns

#### Conversation and Context Files

| Pattern | Type | Risk Level | Description |
|---------|------|------------|-------------|
| `**/ai-context-*.md` | Glob | High | AI context documents |
| `**/conversation-*.md` | Glob | High | AI conversation logs |
| `**/*-prompt.md` | Glob | Medium | Prompt engineering files |
| `**/*-instructions.md` | Glob | Medium | AI instruction files |

#### Generated Planning Documents

| Pattern | Type | Risk Level | Description |
|---------|------|------------|-------------|
| `**/tasks-*.md` | Glob | Medium | Task lists (may be legitimate) |
| `**/todo-ai-*.md` | Glob | High | AI-generated todo lists |
| `**/implementation-plan-*.md` | Glob | Medium | Implementation plans (context-dependent) |

### Exclusion Patterns (Do NOT Block)

Important: These patterns should NOT be blocked as they represent legitimate files.

| Pattern | Type | Reason |
|---------|------|--------|
| `README.md` | Exact | Project documentation |
| `CONTRIBUTING.md` | Exact | Project documentation |
| `docs/**/*.md` | Glob | Legitimate documentation (unless using docs/ for BMAD) |
| `.github/**` | Glob | GitHub configuration and workflows |
| `.gitignore` | Exact | Git configuration |

### Combined Pattern Library (JSON Format)

```json
{
  "artifact_patterns": {
    "bmad": {
      "high_risk": [
        "flattened-codebase.xml",
        ".bmad-flattenignore",
        "docs/stories/story-*.md",
        "docs/qa/assessments/*.md"
      ],
      "medium_risk": [
        "docs/prd.md",
        "docs/architecture.md"
      ]
    },
    "prp": {
      "high_risk": [
        "**/*.prp.md",
        "PRPs/**",
        "INITIAL.md",
        "**/context-*.md",
        "**/planning-*.md"
      ]
    },
    "tools": {
      "claude": {
        "high_risk": [
          "**/.claude/conversation-*.json",
          "**/.claude/history/**"
        ],
        "medium_risk": [
          ".claude/CLAUDE.md"
        ]
      },
      "cursor": {
        "high_risk": [
          ".cursorignore",
          ".cursorindexingignore",
          ".cursor/**"
        ]
      },
      "aider": {
        "high_risk": [
          ".aiderignore",
          ".aider/**",
          ".aider.input.history",
          ".aider.chat.history.md"
        ]
      }
    },
    "generic": {
      "high_risk": [
        "**/ai-context-*.md",
        "**/conversation-*.md",
        "**/*-ai-prompt.md",
        "**/todo-ai-*.md"
      ],
      "medium_risk": [
        "**/*-prompt.md",
        "**/*-instructions.md",
        "**/tasks-*.md",
        "**/implementation-plan-*.md"
      ]
    }
  },
  "exclusions": [
    "README.md",
    "CONTRIBUTING.md",
    "docs/**/*.md",
    ".github/**",
    ".gitignore",
    "LICENSE"
  ]
}
```

### Pattern Configuration (YAML Format for GitHub Actions)

```yaml
# artifact-patterns.yml
patterns:
  # BMAD Artifacts
  bmad_high:
    - 'flattened-codebase.xml'
    - '.bmad-flattenignore'
    - 'docs/stories/story-*.md'
    - 'docs/qa/assessments/*.md'

  # PRP Artifacts
  prp_high:
    - '**/*.prp.md'
    - 'PRPs/**'
    - 'INITIAL.md'
    - '**/context-*.md'
    - '**/planning-*.md'

  # Tool-Specific
  claude_high:
    - '**/.claude/conversation-*.json'
    - '**/.claude/history/**'

  cursor_high:
    - '.cursorignore'
    - '.cursorindexingignore'
    - '.cursor/**'

  aider_high:
    - '.aiderignore'
    - '.aider/**'
    - '.aider.input.history'
    - '.aider.chat.history.md'

  # Generic AI Workflow
  generic_high:
    - '**/ai-context-*.md'
    - '**/conversation-*.md'
    - '**/*-ai-prompt.md'
    - '**/todo-ai-*.md'

# Files to never block
exclusions:
  - 'README.md'
  - 'CONTRIBUTING.md'
  - 'docs/**/*.md'
  - '.github/**'
  - '.gitignore'
  - 'LICENSE'
```

### Pattern Maintenance Strategy

1. **Regular Review:** Quarterly review of patterns based on false positives/negatives
2. **Community Contributions:** Accept PR to add new patterns for emerging AI tools
3. **Versioning:** Tag pattern library versions for reproducibility
4. **Testing:** Maintain test cases with sample files to validate patterns
5. **Documentation:** Each pattern should document its purpose and examples

---

## Implementation Playbook

### Phase 1: Immediate Protection (Day 1, ~1 hour)

**Goal:** Block most common AI artifacts from entering main branch with minimal setup.

#### Step 1.1: Create Basic Validation Workflow (30 minutes)

1. **Create workflow file:**

```bash
mkdir -p .github/workflows
touch .github/workflows/pr-artifact-validation.yml
```

2. **Add basic validation workflow:**

**File:** `.github/workflows/pr-artifact-validation.yml`

```yaml
name: PR Artifact Validation

on:
  pull_request_target:
    types: [opened, synchronize, reopened]

jobs:
  prevent-artifacts:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read

    steps:
      - name: Prevent AI artifacts from merging
        uses: xalvarez/prevent-file-change-action@v2
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          pattern: .*\.prp\.md$|^PRPs/.*|^flattened-codebase\.xml$|^INITIAL\.md$|^\.bmad-flattenignore$|^docs/stories/story-.*\.md$|^\.aiderignore$|^\.cursorignore$
          allowNewFiles: false
```

3. **Commit and push:**

```bash
git add .github/workflows/pr-artifact-validation.yml
git commit -m "Add PR artifact validation workflow"
git push origin main
```

#### Step 1.2: Enable Branch Protection (5 minutes)

1. Navigate to repository **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Configure:
   - **Branch name pattern:** `main`
   - ✅ **Require status checks to pass before merging**
   - Search for and select: `prevent-artifacts`
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Do not allow bypassing the above settings**
4. Click **Create** or **Save changes**

#### Step 1.3: Update .gitignore (10 minutes)

Add common AI artifact patterns to `.gitignore` as defense-in-depth:

**File:** `.gitignore`

```gitignore
# AI Workflow Artifacts - Keep in forks/branches, don't merge to main
*.prp.md
PRPs/
flattened-codebase.xml
INITIAL.md
.bmad-flattenignore
docs/stories/story-*.md
docs/qa/assessments/

# Tool-Specific
.aiderignore
.aider/
.cursorignore
.cursorindexingignore
.cursor/
.claude/conversation-*.json
.claude/history/

# Generic AI Context Files
**/ai-context-*.md
**/conversation-*.md
**/*-ai-prompt.md
**/todo-ai-*.md
```

Commit changes:

```bash
git add .gitignore
git commit -m "Update .gitignore for AI workflow artifacts"
git push origin main
```

#### Step 1.4: Test the Validation (15 minutes)

1. **Create test branch:**

```bash
git checkout -b test-artifact-validation
```

2. **Create test artifact:**

```bash
echo "# Test PRP" > test-feature.prp.md
git add test-feature.prp.md
git commit -m "Test: Add PRP artifact"
git push origin test-artifact-validation
```

3. **Open PR** and verify:
   - Workflow runs automatically
   - `prevent-artifacts` check **fails**
   - PR is blocked from merging

4. **Clean up:**

```bash
git checkout main
git branch -D test-artifact-validation
git push origin --delete test-artifact-validation
```

#### Phase 1 Success Criteria

- ✅ Workflow file exists and runs on PRs
- ✅ Branch protection requires workflow to pass
- ✅ Test PR with artifact is blocked
- ✅ .gitignore updated with common patterns

**Time Investment:** ~1 hour
**Protection Level:** 70-80% of common artifacts blocked

---

### Phase 2: Enhanced Validation (Week 1, ~4 hours)

**Goal:** Add comprehensive pattern detection, better error messages, and contributor feedback.

#### Step 2.1: Enhanced Validation Workflow (2 hours)

Replace basic workflow with enhanced version that provides detailed feedback.

**File:** `.github/workflows/pr-artifact-validation.yml`

```yaml
name: PR Artifact Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate-artifacts:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect changed files
        uses: dorny/paths-filter@v3
        id: filter
        with:
          list-files: 'json'
          filters: |
            artifacts:
              - '**/*.prp.md'
              - 'PRPs/**'
              - 'flattened-codebase.xml'
              - 'INITIAL.md'
              - '.bmad-flattenignore'
              - 'docs/stories/story-*.md'
              - 'docs/qa/assessments/**'
              - '.aiderignore'
              - '.aider/**'
              - '.cursorignore'
              - '.cursorindexingignore'
              - '.cursor/**'
              - '**/.claude/conversation-*.json'
              - '**/.claude/history/**'
              - '**/ai-context-*.md'
              - '**/conversation-*.md'
              - '**/*-ai-prompt.md'
              - '**/todo-ai-*.md'

      - name: Parse artifact files
        if: steps.filter.outputs.artifacts == 'true'
        id: artifacts
        run: |
          echo "Artifact files detected:"
          echo '${{ steps.filter.outputs.artifacts_files }}' | jq -r '.[]'

          FILES=$(echo '${{ steps.filter.outputs.artifacts_files }}' | jq -r '.[]' | tr '\n' '|')
          echo "files=$FILES" >> $GITHUB_OUTPUT

      - name: Categorize artifacts
        if: steps.filter.outputs.artifacts == 'true'
        id: categorize
        run: |
          FILES='${{ steps.filter.outputs.artifacts_files }}'

          BMAD=$(echo "$FILES" | jq -r '.[] | select(test("flattened-codebase\\.xml|bmad|docs/stories"))')
          PRP=$(echo "$FILES" | jq -r '.[] | select(test("\\.prp\\.md|PRPs/|INITIAL\\.md"))')
          CLAUDE=$(echo "$FILES" | jq -r '.[] | select(test("\\.claude/"))')
          CURSOR=$(echo "$FILES" | jq -r '.[] | select(test("\\.cursor"))')
          AIDER=$(echo "$FILES" | jq -r '.[] | select(test("\\.aider"))')
          GENERIC=$(echo "$FILES" | jq -r '.[] | select(test("ai-context|conversation|prompt|todo-ai"))')

          echo "bmad<<EOF" >> $GITHUB_OUTPUT
          echo "$BMAD" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "prp<<EOF" >> $GITHUB_OUTPUT
          echo "$PRP" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "claude<<EOF" >> $GITHUB_OUTPUT
          echo "$CLAUDE" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "cursor<<EOF" >> $GITHUB_OUTPUT
          echo "$CURSOR" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "aider<<EOF" >> $GITHUB_OUTPUT
          echo "$AIDER" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "generic<<EOF" >> $GITHUB_OUTPUT
          echo "$GENERIC" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post detailed PR comment
        if: steps.filter.outputs.artifacts == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const bmad = `${{ steps.categorize.outputs.bmad }}`.trim();
            const prp = `${{ steps.categorize.outputs.prp }}`.trim();
            const claude = `${{ steps.categorize.outputs.claude }}`.trim();
            const cursor = `${{ steps.categorize.outputs.cursor }}`.trim();
            const aider = `${{ steps.categorize.outputs.aider }}`.trim();
            const generic = `${{ steps.categorize.outputs.generic }}`.trim();

            let body = `## ❌ AI Workflow Artifacts Detected\n\n`;
            body += `This PR contains AI workflow artifacts that should not be merged to the main branch.\n\n`;
            body += `These artifacts are valuable for your individual development workflow but should remain in your fork or feature branch.\n\n`;

            if (bmad) {
              body += `### 🔧 BMAD Artifacts\n`;
              bmad.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            if (prp) {
              body += `### 📝 PRP (Product Requirement Prompt) Artifacts\n`;
              prp.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            if (claude) {
              body += `### 🤖 Claude Code Artifacts\n`;
              claude.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            if (cursor) {
              body += `### 🖱️ Cursor Artifacts\n`;
              cursor.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            if (aider) {
              body += `### 🤝 Aider Artifacts\n`;
              aider.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            if (generic) {
              body += `### 📋 Generic AI Workflow Artifacts\n`;
              generic.split('\n').filter(f => f).forEach(f => body += `- \`${f}\`\n`);
              body += `\n`;
            }

            body += `### 🔧 How to Fix\n\n`;
            body += `**Option 1: Remove files (recommended)**\n\`\`\`bash\n`;
            body += `git rm <files>\n`;
            body += `git commit -m "Remove AI workflow artifacts"\n`;
            body += `git push\n\`\`\`\n\n`;

            body += `**Option 2: Amend your last commit**\n\`\`\`bash\n`;
            body += `git rm <files>\n`;
            body += `git commit --amend --no-edit\n`;
            body += `git push --force-with-lease\n\`\`\`\n\n`;

            body += `### 💡 Why This Matters\n\n`;
            body += `AI workflow artifacts serve important purposes for individual development:\n`;
            body += `- They provide context for AI assistants\n`;
            body += `- They track your development workflow\n`;
            body += `- They help you iterate on features\n\n`;

            body += `However, they should **NOT** be merged to the main branch because:\n`;
            body += `- They clutter the codebase with files not relevant to all contributors\n`;
            body += `- They may contain personal workflow preferences\n`;
            body += `- They can confuse contributors using different AI tools\n`;
            body += `- They don't provide value in the final product\n\n`;

            body += `### 📚 Resources\n\n`;
            body += `- [Contributing Guidelines](../blob/main/CONTRIBUTING.md)\n`;
            body += `- [Working with AI Assistants Guide](../blob/main/docs/ai-workflow-guide.md)\n`;

            // Find existing comment
            const comments = await github.rest.issues.listComments({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
            });

            const botComment = comments.data.find(comment =>
              comment.user.type === 'Bot' &&
              comment.body.includes('AI Workflow Artifacts Detected')
            );

            // Update or create comment
            if (botComment) {
              await github.rest.issues.updateComment({
                comment_id: botComment.id,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: body
              });
            } else {
              await github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: body
              });
            }

      - name: Fail if artifacts detected
        if: steps.filter.outputs.artifacts == 'true'
        run: |
          echo "❌ AI workflow artifacts detected in PR"
          echo "See PR comment for details and instructions"
          exit 1
```

#### Step 2.2: Create Contributor Documentation (1 hour)

**File:** `CONTRIBUTING.md` (or append to existing)

```markdown
# Working with AI Assistants

This project welcomes contributors using AI-assisted development tools (Claude Code, Cursor, Aider, etc.) and methodologies (BMAD, PRP, etc.).

## AI Artifacts Policy

### ✅ Allowed in Your Fork/Branch

You may use any AI workflow artifacts in your personal fork or feature branches, including:
- PRP files (`*.prp.md`)
- BMAD artifacts (`flattened-codebase.xml`, story files)
- Context engineering files
- AI conversation logs
- Tool-specific configuration (`.cursor`, `.aider`, `.claude`)
- Planning and prompt documents

### ❌ Not Allowed in Main Branch

The following should **NOT** be included in pull requests:
- `**/*.prp.md` - PRP prompt files
- `PRPs/**` - PRP directories
- `flattened-codebase.xml` - BMAD codebase flattener output
- `INITIAL.md` - Initial feature request files
- Tool-specific artifacts (`.cursorignore`, `.aiderignore`, `.claude/conversation-*.json`)
- AI context and planning files

### Why This Policy?

**Benefits for Your Workflow:**
- Keep artifacts in your fork for AI context continuity
- Maintain your preferred development methodology
- Personal AI tool configurations remain private

**Benefits for the Project:**
- Clean main branch focused on production code
- Reduces confusion for contributors using different tools
- Maintains repository clarity and purpose

## Pull Request Validation

Our automated PR validation will check for AI artifacts and:
1. **Detect** any artifact files in your PR
2. **Comment** with specific files and removal instructions
3. **Block** the PR from merging until artifacts are removed

### How to Handle Validation Failures

If your PR fails artifact validation:

1. **Review the PR comment** - it lists specific files to remove

2. **Remove the artifacts:**
   ```bash
   git rm file1.prp.md file2.xml
   git commit -m "Remove AI workflow artifacts"
   git push
   ```

3. **If you've already committed multiple times:**
   ```bash
   # Remove files
   git rm <artifact-files>

   # Amend your last commit
   git commit --amend --no-edit

   # Force push (safe because it's your branch)
   git push --force-with-lease
   ```

4. **For artifacts buried in history:**
   ```bash
   # Use interactive rebase to remove from specific commits
   git rebase -i HEAD~N  # where N is number of commits back

   # Or start fresh if easier
   git checkout main
   git pull
   git checkout -b clean-feature-branch
   # Cherry-pick clean commits or re-implement
   ```

### Best Practices

1. **Use .gitignore**: Add your AI artifacts to `.gitignore` to prevent accidental commits
2. **Review before commit**: Check `git status` before committing
3. **Keep artifacts in separate directory**: Use a local directory outside the repo for AI context files
4. **Commit frequently**: Small, focused commits make it easier to remove artifacts if needed

## Questions?

If you have questions about this policy or encounter issues with validation:
- Open an issue with the `ai-workflow` label
- Ask in our [Discord/Slack/Forum]
- Review the [AI Workflow Guide](docs/ai-workflow-guide.md)
```

#### Step 2.3: Create AI Workflow Guide (1 hour)

**File:** `docs/ai-workflow-guide.md`

```markdown
# AI-Assisted Development Workflow Guide

This guide helps you use AI assistants effectively while keeping the main branch clean.

## Recommended Workflow Structure

### Option 1: Separate Context Directory (Recommended)

Keep AI artifacts outside your project directory:

```
~/projects/
├── myproject/              # Your actual project (clean)
└── myproject-ai-context/   # AI artifacts (not tracked in main repo)
    ├── PRPs/
    ├── context/
    ├── conversations/
    └── planning/
```

**Pros:**
- Impossible to accidentally commit artifacts
- Clean separation of concerns
- Can version control separately if desired

**Cons:**
- AI assistants may have trouble finding context
- Requires manual context management

### Option 2: Gitignored Directory

Keep AI artifacts in a gitignored directory:

```
myproject/
├── .git/
├── .gitignore              # Contains ai-context/
├── src/
├── docs/
└── ai-context/             # Not tracked by git
    ├── PRPs/
    ├── context/
    └── planning/
```

**Pros:**
- Artifacts close to code
- AI assistants can easily access
- Part of project structure

**Cons:**
- Must remember to gitignore
- Can accidentally force-add

### Option 3: Fork with Artifacts

Maintain a personal fork with all your AI artifacts:

```
upstream/repo (clean)    →    your-fork/repo (with artifacts)
main branch                   main branch + ai-workflow branch
```

**Workflow:**
1. Work in `ai-workflow` branch with all artifacts
2. Merge clean commits to `main`
3. PR from your fork's `main` to upstream

**Pros:**
- Complete freedom in your fork
- Easy to sync clean code upstream
- Artifacts versioned if desired

**Cons:**
- More complex git workflow
- Must maintain two branches

## Tool-Specific Configuration

### Claude Code

Add to `.gitignore`:
```gitignore
.claude/conversation-*.json
.claude/history/
```

Keep `.claude/CLAUDE.md` and `.claude/commands/` if they contain project-specific configuration.

### Cursor

Add to `.gitignore`:
```gitignore
.cursorignore
.cursorindexingignore
.cursor/
```

Use Cursor's ignore feature to exclude your project from indexing while keeping context.

### Aider

Add to `.gitignore`:
```gitignore
.aiderignore
.aider/
.aider.input.history
.aider.chat.history.md
```

Aider respects `.aiderignore` - use it to exclude artifacts from Aider's awareness.

### BMAD Method

If using BMAD:
```gitignore
flattened-codebase.xml
.bmad-flattenignore
docs/stories/story-*.md
docs/qa/assessments/
```

**Alternative:** Keep BMAD artifacts in `bmad/` directory outside repo.

### PRP (Product Requirement Prompts)

If using PRP:
```gitignore
PRPs/
*.prp.md
INITIAL.md
context-*.md
planning-*.md
```

**Alternative:** Maintain PRPs in a separate repository linked as documentation.

## Troubleshooting

### "I accidentally committed artifacts"

**If not yet pushed:**
```bash
git reset HEAD~1  # Undo last commit
git rm <artifacts>  # Remove artifacts
git commit -am "Your original commit message"
```

**If already pushed to your branch:**
```bash
git rm <artifacts>
git commit -m "Remove AI artifacts"
git push
```

**If merged to main (rare):**
Contact maintainers immediately. We'll need to:
1. Use `git-filter-repo` to rewrite history
2. Force push to main (requires coordination)
3. All contributors must re-clone

### "Validation is blocking legitimate files"

If validation incorrectly flags legitimate files:

1. **Check the pattern** - does your file match an artifact pattern?
2. **Rename if possible** - choose a name that doesn't match patterns
3. **Open an issue** - we'll adjust patterns if too broad
4. **Request exception** - some files may warrant explicit exceptions

### "I need artifacts for AI context"

Use one of these strategies:
1. **Separate directory** - keep context outside repo
2. **Personal fork** - maintain artifacts in your fork
3. **Local branch** - keep local branch with artifacts, don't push
4. **Documentation** - convert essential context to proper documentation

## Examples

### Example 1: BMAD Workflow

```bash
# Setup
cd ~/projects
git clone git@github.com:org/myproject.git
mkdir myproject-bmad-context

cd myproject
# ... work on code ...

cd ../myproject-bmad-context
# ... generate PRD, stories, etc. ...

# When ready to commit
cd ../myproject
git add src/  # Only add actual code
git commit -m "Implement feature X"
git push origin feature-x
# Open PR - passes validation ✅
```

### Example 2: PRP with Claude Code

```bash
# Create PRP outside repo
cd ~/ai-context
mkdir myproject-prps
cd myproject-prps
echo "# Feature X PRP" > feature-x.prp.md

# Work on feature
cd ~/projects/myproject
# Use Claude Code with PRP context
# Implement feature

# Commit only code
git add src/feature-x/
git commit -m "Add feature X"
git push origin feature-x
# Open PR - passes validation ✅
```

### Example 3: Cursor with Context Files

```bash
# In your project
cd ~/projects/myproject

# Create context directory (gitignored)
mkdir cursor-context
echo "cursor-context/" >> .gitignore

# Store context there
echo "# Project context" > cursor-context/context.md

# Work normally
git add src/
git commit -m "Implement feature"
# cursor-context/ is ignored automatically ✅
```

## Getting Help

- **Validation issues:** Open issue with `validation` label
- **Workflow questions:** Open discussion in GitHub Discussions
- **Pattern exceptions:** Open issue with `artifact-pattern` label

## Contributing to This Guide

Help us improve this guide:
- Add your successful workflow patterns
- Report validation false positives
- Suggest new AI tool integrations
- Share troubleshooting tips
```

#### Phase 2 Success Criteria

- ✅ Enhanced workflow with detailed categorization
- ✅ Automated PR comments with guidance
- ✅ Contributor documentation complete
- ✅ AI workflow guide published
- ✅ Pattern coverage > 90%

**Time Investment:** ~4 hours
**Protection Level:** 90-95% of artifacts blocked
**Contributor Experience:** Significantly improved with clear guidance

---

### Phase 3: Advanced Automation (Month 1, ~6 hours)

**Goal:** Add metrics, monitoring, automated remediation suggestions, and continuous improvement.

#### Step 3.1: Metrics and Monitoring (2 hours)

Track validation effectiveness and false positive rates.

**File:** `.github/workflows/pr-artifact-metrics.yml`

```yaml
name: PR Artifact Metrics

on:
  pull_request:
    types: [opened, closed]

jobs:
  track-metrics:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == true

    steps:
      - name: Record validation metrics
        uses: actions/github-script@v7
        with:
          script: |
            const pr = context.payload.pull_request;
            const checks = await github.rest.checks.listForRef({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: pr.head.sha
            });

            const validationCheck = checks.data.check_runs.find(
              check => check.name === 'validate-artifacts'
            );

            if (validationCheck) {
              console.log(`PR #${pr.number} validation status: ${validationCheck.conclusion}`);
              console.log(`Validation run time: ${validationCheck.completed_at - validationCheck.started_at}ms`);

              // In production, send to monitoring system
              // await sendToDatadog/Prometheus/etc.
            }
```

#### Step 3.2: Auto-Remediation Suggestions (2 hours)

Provide automated suggestions for cleaning up artifacts.

**File:** `.github/workflows/pr-artifact-remediation.yml`

```yaml
name: PR Artifact Remediation

on:
  issue_comment:
    types: [created]

jobs:
  suggest-remediation:
    runs-on: ubuntu-latest
    if: |
      github.event.issue.pull_request &&
      contains(github.event.comment.body, '/fix-artifacts')
    permissions:
      pull-requests: write
      contents: read

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.issue.pull_request.head.ref }}
          fetch-depth: 0

      - name: Generate remediation script
        id: remediation
        run: |
          # Detect artifact files
          ARTIFACTS=$(git diff --name-only origin/main...HEAD | \
            grep -E '\.(prp\.md|bmad|\.cursor|\.aider|\.claude)' || true)

          if [ -z "$ARTIFACTS" ]; then
            echo "No artifacts found"
            exit 0
          fi

          # Generate script
          echo '#!/bin/bash' > remediate.sh
          echo 'set -e' >> remediate.sh
          echo '' >> remediate.sh
          echo '# Remove artifact files' >> remediate.sh
          echo "$ARTIFACTS" | while read file; do
            echo "git rm '$file'" >> remediate.sh
          done
          echo '' >> remediate.sh
          echo 'git commit -m "Remove AI workflow artifacts"' >> remediate.sh
          echo 'git push' >> remediate.sh

          # Save script
          cat remediate.sh
          echo "script<<EOF" >> $GITHUB_OUTPUT
          cat remediate.sh >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post remediation script
        uses: actions/github-script@v7
        with:
          script: |
            const script = `${{ steps.remediation.outputs.script }}`;
            const body = `## 🔧 Automated Remediation Script

            Run this script in your local repository to remove detected artifacts:

            \`\`\`bash
            ${script}
            \`\`\`

            Or copy-paste line by line to review each change.

            **After running:**
            1. Review the changes: \`git status\`
            2. Push to update your PR: \`git push\`
            3. Validation will re-run automatically`;

            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

#### Step 3.3: Pattern Library Versioning (1 hour)

Create versioned pattern library for reproducibility.

**File:** `.github/artifact-patterns/v1.0.0.json`

```json
{
  "version": "1.0.0",
  "updated": "2025-01-08",
  "description": "AI workflow artifact patterns for validation",
  "patterns": {
    "bmad": {
      "high_risk": [
        {
          "pattern": "flattened-codebase\\.xml",
          "type": "regex",
          "description": "BMAD codebase flattener output"
        },
        {
          "pattern": "\\.bmad-flattenignore",
          "type": "regex",
          "description": "BMAD custom ignore patterns"
        },
        {
          "pattern": "docs/stories/story-.*\\.md",
          "type": "regex",
          "description": "BMAD story files"
        }
      ]
    },
    "prp": {
      "high_risk": [
        {
          "pattern": ".*\\.prp\\.md",
          "type": "regex",
          "description": "PRP prompt files"
        },
        {
          "pattern": "PRPs/",
          "type": "path_prefix",
          "description": "PRP directory"
        },
        {
          "pattern": "INITIAL\\.md",
          "type": "regex",
          "description": "Initial feature request"
        }
      ]
    }
  },
  "exclusions": [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE"
  ],
  "changelog": [
    {
      "version": "1.0.0",
      "date": "2025-01-08",
      "changes": ["Initial pattern library"]
    }
  ]
}
```

#### Step 3.4: Continuous Improvement Workflow (1 hour)

Create process for community pattern contributions.

**File:** `.github/ISSUE_TEMPLATE/artifact-pattern.md`

```markdown
---
name: Artifact Pattern Submission
about: Submit a new AI artifact pattern or request pattern adjustment
title: '[PATTERN] '
labels: artifact-pattern
assignees: ''
---

## Pattern Type

- [ ] New pattern to add
- [ ] False positive (legitimate file blocked)
- [ ] False negative (artifact not blocked)
- [ ] Pattern adjustment

## Pattern Details

**File pattern:**
```
# Example: docs/my-ai-context-*.md
```

**Pattern type:**
- [ ] Regex
- [ ] Glob
- [ ] Exact match

**Risk level:**
- [ ] High (always block)
- [ ] Medium (context-dependent)
- [ ] Low (warn only)

## Justification

**Why should this pattern be added/changed?**

**Which AI tool or methodology does this relate to?**
- [ ] BMAD
- [ ] PRP
- [ ] Claude Code
- [ ] Cursor
- [ ] Aider
- [ ] Other: ___________

**Examples of files that match this pattern:**
```
# List example filenames
```

## Testing

**Have you tested this pattern?**
- [ ] Yes, validated with sample files
- [ ] No, proposing for discussion

**Test cases:**
```
# Files that should match:
file1.txt
file2.txt

# Files that should NOT match:
file3.txt
file4.txt
```

## Additional Context

Add any other context about the pattern submission here.
```

#### Phase 3 Success Criteria

- ✅ Metrics collection implemented
- ✅ Auto-remediation available via bot command
- ✅ Pattern library versioned
- ✅ Community contribution process established
- ✅ Monitoring dashboard (optional)

**Time Investment:** ~6 hours
**Protection Level:** 95%+ with continuous improvement
**Contributor Experience:** Excellent with auto-remediation

---

## Real-World Analysis

### Projects Examined

1. **Archon** (github.com/coleam00/Archon)
   - Multi-contributor AI task management system
   - Uses GitHub Actions: `ci.yml`, `claude-fix.yml`, `claude-review.yml`
   - **Artifact Handling:** Not explicitly addressed, opportunity for improvement
   - **Key Insight:** Even AI-focused projects need artifact enforcement

2. **BMAD Method Repositories** (github.com/bmad-code-org/BMAD-METHOD)
   - Official BMAD framework repository
   - Documents artifact structure (flattened-codebase.xml, docs/stories/)
   - **Artifact Handling:** Gitignore patterns documented
   - **Key Insight:** Frameworks document artifacts but don't enforce exclusion

3. **Context Engineering Intro** (github.com/coleam00/context-engineering-intro)
   - PRP methodology examples and templates
   - Contains PRPs/, INITIAL.md examples
   - **Artifact Handling:** Examples present in repo (acceptable for template repo)
   - **Key Insight:** Template repos need different rules than project repos

### Patterns Observed

| Project Type | Artifact Handling | Effectiveness | Notes |
|-------------|-------------------|---------------|-------|
| **AI Framework Repos** | Allow artifacts (by design) | N/A | Artifacts are the product |
| **Multi-contributor Projects** | Mixed or none | Low | Artifacts often slip through |
| **Enterprise Projects** | Strict validation | High | Use CODEOWNERS + CI/CD |
| **Open Source** | Gitignore only | Medium | Relies on contributor diligence |

### Common Gaps Identified

1. **No Merge-Time Enforcement**
   - Most projects rely on .gitignore alone
   - Contributors can bypass with `git add -f`
   - **Solution:** CI/CD validation + branch protection

2. **Lack of Contributor Guidance**
   - Validation failures don't explain why or how to fix
   - New contributors confused by errors
   - **Solution:** Detailed PR comments with commands

3. **Tool-Specific Patterns Missing**
   - Most .gitignore files miss .cursor, .aider, .claude patterns
   - Gaps allow tool-specific artifacts through
   - **Solution:** Comprehensive pattern library

4. **No Pattern Versioning**
   - Patterns added ad-hoc without tracking
   - Can't reproduce validation behavior over time
   - **Solution:** Versioned pattern library

### Success Patterns

1. **Prettier Project** (uses xalvarez/prevent-file-change-action)
   - Prevents changes to `.github/FUNDING.yml`
   - Simple, effective, well-maintained
   - **Lesson:** Purpose-built actions work well for simple cases

2. **Enterprise Monorepos** (use dorny/paths-filter)
   - Conditional validation based on changed paths
   - Scales to large codebases
   - **Lesson:** Flexible actions needed for complex scenarios

3. **Major OSS Projects** (use branch protection + CODEOWNERS)
   - Layered approach: multiple checkpoints
   - Human review for sensitive changes
   - **Lesson:** Defense-in-depth provides best protection

### Recommendations Based on Analysis

1. **For Small Projects (< 5 contributors):**
   - Phase 1 implementation sufficient
   - xalvarez/prevent-file-change-action
   - Basic branch protection

2. **For Medium Projects (5-20 contributors):**
   - Phase 2 implementation recommended
   - dorny/paths-filter with detailed feedback
   - Contributor documentation
   - PR comment bot

3. **For Large Projects (20+ contributors):**
   - Phase 3 full implementation
   - Metrics and monitoring
   - Auto-remediation
   - Pattern library versioning
   - CODEOWNERS for sensitive paths

---

## Contributor Guidelines Template

Use this template to create contributor guidelines for your project. Customize based on your needs.

```markdown
# Contributing to [Project Name]

## AI-Assisted Development Policy

We welcome contributors using AI coding assistants and methodologies like BMAD, PRP, Claude Code, Cursor, and Aider.

### Workflow Artifact Guidelines

#### ✅ Use AI Artifacts in Your Workflow

You're encouraged to use AI artifacts in your personal development workflow:
- Keep them in your fork or feature branches
- Use them for AI context and continuity
- Maintain them however works best for you

#### ❌ Don't Merge Artifacts to Main

These files should NOT be included in pull requests to main:

**BMAD Artifacts:**
- `flattened-codebase.xml`
- `.bmad-flattenignore`
- `docs/stories/story-*.md`
- `docs/qa/assessments/**`

**PRP Artifacts:**
- `**/*.prp.md`
- `PRPs/**`
- `INITIAL.md`

**Tool-Specific:**
- `.cursorignore`, `.cursor/**`
- `.aiderignore`, `.aider/**`
- `.claude/conversation-*.json`

**Generic AI Files:**
- `**/ai-context-*.md`
- `**/conversation-*.md`
- `**/*-ai-prompt.md`

### Automated Validation

Our CI/CD pipeline automatically:
1. Detects AI artifacts in your PR
2. Posts a comment listing specific files
3. Provides removal commands
4. Blocks PR merge until artifacts removed

### How to Handle Validation Failures

When your PR fails artifact validation:

1. **Check the PR comment** for the list of files to remove

2. **Remove artifacts:**
   ```bash
   git rm <artifact-files>
   git commit -m "Remove AI workflow artifacts"
   git push
   ```

3. **Or amend your last commit:**
   ```bash
   git rm <artifact-files>
   git commit --amend --no-edit
   git push --force-with-lease
   ```

### Preventing Validation Failures

Add these patterns to your `.gitignore`:

```gitignore
# AI Workflow Artifacts
*.prp.md
PRPs/
flattened-codebase.xml
INITIAL.md
.bmad-flattenignore
docs/stories/story-*.md
.aiderignore
.aider/
.cursorignore
.cursor/
.claude/conversation-*.json
**/ai-context-*.md
**/conversation-*.md
```

### Recommended Workflow

**Option 1: Separate Context Directory**
```
~/projects/
├── myproject/          # Your repo (clean)
└── myproject-ai/       # AI artifacts (separate)
```

**Option 2: Gitignored Directory**
```
myproject/
├── src/
└── ai-context/         # Gitignored
```

**Option 3: Personal Fork with Artifacts**
- Maintain artifacts in your fork
- PR clean commits to upstream

See our [AI Workflow Guide](docs/ai-workflow-guide.md) for detailed instructions.

### Questions?

- **Validation issues:** Open an issue with `validation` label
- **Pattern exceptions:** Open an issue with `artifact-pattern` label
- **Workflow questions:** Ask in Discussions

### False Positives

If validation incorrectly flags a legitimate file:
1. Verify it doesn't match artifact patterns
2. Rename if possible to avoid pattern match
3. Open an issue requesting pattern adjustment
4. Maintainers will review and update patterns

## Additional Contributing Guidelines

[Your existing contributing guidelines...]
```

---

## Troubleshooting & Edge Cases

### Common Issues and Solutions

#### Issue 1: Workflow Runs But Doesn't Block Merge

**Symptom:** Validation workflow executes but PR can still be merged despite failures.

**Cause:** Branch protection not configured to require status check.

**Solution:**
1. Go to repository Settings → Branches
2. Edit protection rule for main branch
3. Enable "Require status checks to pass before merging"
4. Search for and select your validation job name
5. Save changes

**Verification:**
```bash
# Test by creating PR with artifact
echo "test" > test.prp.md
git add test.prp.md
git commit -m "Test validation"
git push origin test-branch
# Open PR - should be blocked ✅
```

#### Issue 2: Skipped Workflows Show as "Pending"

**Symptom:** Workflow skipped due to path filtering stays in "Pending" state, blocking PR merge.

**Cause:** GitHub treats skipped required checks as pending.

**Solution:** Create inverse "always pass" workflow:

```yaml
# .github/workflows/validation-dummy.yml
name: validation-dummy

on:
  pull_request:
    paths-ignore:
      - '**/*.prp.md'
      - 'PRPs/**'
      # ... other artifact patterns

jobs:
  dummy-validation:
    runs-on: ubuntu-latest
    steps:
      - name: Pass
        run: echo "No artifacts changed, passing"
```

**Alternative:** Use `if: always()` in validation workflow instead of path filtering.

#### Issue 3: False Positive - Legitimate File Blocked

**Symptom:** Validation blocks a file that should be allowed (e.g., `docs/architecture.md`).

**Cause:** Pattern too broad or file matches artifact pattern.

**Solutions:**

**Option A: Add Exclusion to Workflow**
```yaml
# In paths-filter step
filters: |
  artifacts:
    - '**/*.prp.md'
    - '!docs/architecture.md'  # Explicit exclusion
```

**Option B: Rename File**
```bash
# If docs/architecture.md conflicts with BMAD pattern
git mv docs/architecture.md docs/system-architecture.md
```

**Option C: Adjust Pattern**
```yaml
# Change from broad pattern
- 'docs/**'
# To specific pattern
- 'docs/stories/**'
- 'docs/qa/**'
```

**Option D: Request Pattern Adjustment**
- Open issue with `artifact-pattern` label
- Provide examples of legitimate vs. artifact files
- Maintainers will refine pattern

#### Issue 4: Artifacts Buried in History

**Symptom:** Validation passes on new commits, but artifacts exist in PR history.

**Cause:** Validation only checks changed files in latest commit, not entire PR diff.

**Solution:** Ensure validation compares against base branch:

```yaml
# In validation workflow
- name: Checkout with full history
  uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Important: get full history

- name: Get all changed files in PR
  run: |
    # Compare entire PR diff, not just latest commit
    git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }}
```

**Manual cleanup if needed:**
```bash
# Use interactive rebase to remove from history
git rebase -i HEAD~N  # N = number of commits

# Or use git-filter-repo
git filter-repo --path-glob '*.prp.md' --invert-paths
```

#### Issue 5: Artifacts Already in Main Branch

**Symptom:** Artifacts somehow made it into main branch despite validation.

**Cause:** Validation was added after artifacts were merged, or validation was bypassed.

**Solution:** Clean up main branch history:

⚠️ **WARNING:** This rewrites history and requires coordination with all contributors.

**Step 1: Backup**
```bash
git clone --mirror git@github.com:org/repo.git repo-backup
```

**Step 2: Clean with git-filter-repo**
```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove artifact files from all history
git filter-repo --invert-paths \
  --path-glob '*.prp.md' \
  --path-glob 'PRPs/*' \
  --path-glob 'flattened-codebase.xml' \
  --path-glob '.bmad-flattenignore' \
  --path-glob 'docs/stories/story-*.md'

# Verify changes
git log --all --oneline -- '*.prp.md'  # Should return nothing

# Force push (requires admin permissions and coordination)
git push origin --force --all
git push origin --force --tags
```

**Step 3: Notify Contributors**
```
⚠️ HISTORY REWRITE COMPLETED

We've cleaned up AI artifacts from the main branch history.

ACTION REQUIRED for all contributors:

1. Backup your local work:
   git stash
   git branch backup-$(date +%Y%m%d)

2. Re-clone the repository:
   cd ..
   rm -rf old-repo-name
   git clone git@github.com:org/repo.git

3. Restore your local work:
   git cherry-pick <commits> # or manually re-apply changes

4. Resume normal development

Questions? Ask in #dev-support channel.
```

#### Issue 6: Tool-Specific Configuration Needed

**Symptom:** `.claude/CLAUDE.md` or `.cursor/settings.json` are project-specific but flagged as artifacts.

**Cause:** Pattern blocks entire tool directory.

**Solution:** Allow specific project configuration files:

```yaml
# In paths-filter
filters: |
  artifacts:
    - '.claude/**'
    - '!.claude/CLAUDE.md'        # Allow project instructions
    - '!.claude/commands/**'       # Allow custom commands
    - '!.cursor/settings.json'     # Allow cursor settings
```

**Best Practice:**
- Allow configuration files that benefit all contributors
- Block conversation logs and histories
- Document which tool files are project-standard

#### Issue 7: Multiple AI Tools Used in Project

**Symptom:** Some contributors use Claude, others use Cursor, patterns conflict.

**Cause:** Different tools generate different artifact structures.

**Solution:** Support all tools with comprehensive patterns:

```yaml
# .github/artifact-patterns.yml
patterns:
  claude:
    - '**/.claude/conversation-*.json'
    - '**/.claude/history/**'

  cursor:
    - '.cursorignore'
    - '.cursor/history/**'

  aider:
    - '.aiderignore'
    - '.aider/**'

  # Add more as needed
```

**Documentation:** Update CONTRIBUTING.md with guidance for all supported tools.

### Edge Cases

#### Edge Case 1: Monorepo with Multiple Subprojects

**Challenge:** Different subprojects may have different artifact policies.

**Solution:** Use path-scoped validation:

```yaml
# .github/workflows/pr-artifact-validation.yml
jobs:
  validate-artifacts:
    strategy:
      matrix:
        subproject: [projectA, projectB, projectC]
    steps:
      - name: Validate ${{ matrix.subproject }}
        uses: dorny/paths-filter@v3
        with:
          filters: |
            artifacts:
              - '${{ matrix.subproject }}/**/*.prp.md'
              - '${{ matrix.subproject }}/PRPs/**'
```

#### Edge Case 2: Template/Starter Repository

**Challenge:** Starter repos may need example artifacts.

**Solution:** Separate example and template directories:

```
starter-repo/
├── template/          # Clean template, validated
├── examples/          # Examples with artifacts, excluded from validation
└── README.md
```

```yaml
# Exclude examples/ from validation
- name: Detect artifacts
  uses: dorny/paths-filter@v3
  with:
    filters: |
      artifacts:
        - '**/*.prp.md'
        - '!examples/**'  # Exclude examples directory
```

#### Edge Case 3: Documentation Repository

**Challenge:** Docs repo may document AI workflows and need artifact examples.

**Solution:** Use metadata markers:

```markdown
<!-- artifact-example -->
# Example PRP file
<!-- /artifact-example -->
```

```yaml
# Validation script
- name: Check for unmarked artifacts
  run: |
    # Allow artifacts between markers
    # Block artifacts without markers
```

#### Edge Case 4: Migration from Contaminated Repository

**Challenge:** Existing repo has extensive artifact contamination.

**Approach 1: Clean Slate**
1. Create new clean repository
2. Migrate only production code
3. Archive old repo
4. Point contributors to new repo

**Approach 2: Gradual Cleanup**
1. Implement validation (blocks new artifacts)
2. Create cleanup issues for existing artifacts
3. Remove artifacts over time
4. Eventually clean history once all removed

**Approach 3: Hard Break**
1. Use git-filter-repo to clean all history
2. Force push clean history
3. All contributors re-clone
4. Requires coordination and downtime

**Recommendation:** Approach 2 (gradual) for active projects, Approach 3 (hard break) for smaller teams.

### Testing Validation Rules

Before deploying validation, test thoroughly:

**Test Script:**
```bash
#!/bin/bash
# test-validation.sh

# Setup
git checkout -b test-validation
echo "Test PRP" > test.prp.md
echo "Test BMAD" > flattened-codebase.xml
mkdir -p PRPs
echo "Test" > PRPs/test.md

# Commit artifacts
git add .
git commit -m "Test: Add artifacts"

# Push and create PR
git push origin test-validation

echo "Check PR for validation failure"
echo "Expected: ❌ Validation fails"
echo "Expected: PR comment lists 3 files"

# Cleanup
read -p "Press enter to cleanup..."
git checkout main
git branch -D test-validation
git push origin --delete test-validation
```

**Validation Checklist:**
- [ ] Workflow runs on PR open/sync
- [ ] Correctly detects artifacts
- [ ] Fails workflow (exit 1)
- [ ] Posts PR comment
- [ ] Lists specific files
- [ ] Provides removal commands
- [ ] Blocks merge via branch protection
- [ ] Passes when artifacts removed

---

## Decision Framework

### Choosing Enforcement Layers

Use this decision tree to determine which enforcement layers your project needs:

```
START
  ↓
[How many active contributors?]
  ├─ 1-3: → Basic enforcement (Layer 1 + 2)
  ├─ 4-10: → Standard enforcement (Layer 1 + 2 + 3)
  └─ 10+: → Full enforcement (All layers)

[How critical is main branch cleanliness?]
  ├─ Critical (production/enterprise): → Add Layer 4 (CODEOWNERS)
  ├─ Important (OSS/team projects): → Layer 1 + 2 + 3
  └─ Low (personal/experimental): → Layer 1 + 2 only

[How diverse are AI tools used?]
  ├─ Single tool (e.g., only Claude): → Basic patterns
  ├─ 2-3 tools: → Standard patterns + tool-specific
  └─ Many tools: → Comprehensive pattern library + versioning

[What's your tolerance for false positives?]
  ├─ Zero tolerance: → Strict patterns + manual review (Layer 4)
  ├─ Low (< 5%): → Balanced patterns + exclusions
  └─ Medium (< 10%): → Broad patterns + override process
```

### Implementation Phase Selection

| Project Size | Recommended Phase | Time Investment | Protection Level |
|--------------|------------------|----------------|------------------|
| **Solo/Small** (1-3 contributors) | Phase 1 | 1 hour | 70-80% |
| **Small Team** (4-10 contributors) | Phase 2 | 5 hours | 90-95% |
| **Medium Team** (11-25 contributors) | Phase 2 + metrics | 7 hours | 90-95% |
| **Large Team** (25+ contributors) | Phase 3 full | 11 hours | 95%+ |

### Pattern Strictness Levels

**Level 1: Permissive (Recommended for starting out)**
- Block only obvious artifacts (*.prp.md, flattened-codebase.xml)
- Allow context-dependent files
- False positive rate: < 2%
- **Use when:** New to validation, diverse workflows

**Level 2: Balanced (Recommended for most projects)**
- Block common artifacts across methodologies
- Some context-dependent decisions
- False positive rate: < 5%
- **Use when:** Established project, some AI usage patterns known

**Level 3: Strict (Recommended for production/enterprise)**
- Block all artifact patterns including generic
- Minimal context-dependent allowances
- False positive rate: < 10% (but requires manual review)
- **Use when:** Critical cleanliness needed, can afford manual review overhead

### Tradeoff Analysis

| Factor | Layer 1 Only | Layers 1+2 | Layers 1+2+3 | All Layers |
|--------|-------------|-----------|-------------|------------|
| **Setup Time** | 5 min | 30 min | 5 hours | 12 hours |
| **Maintenance** | Low | Medium | Medium-High | High |
| **Protection Level** | 20% | 80% | 95% | 98% |
| **Contributor Friction** | None | Low | Very Low | Low-Medium |
| **False Positives** | N/A | 5-10% | 2-5% | < 2% |
| **Automation** | None | High | Very High | Full |
| **Extensibility** | N/A | Medium | High | Very High |

### Choosing a GitHub Action

| Action | Best For | Pros | Cons | Complexity |
|--------|---------|------|------|-----------|
| **xalvarez/prevent-file-change-action** | Simple patterns, single methodology | Easy setup, reliable | Less flexible | Low |
| **dorny/paths-filter** | Multiple methodologies, complex logic | Very flexible, powerful | Requires custom scripts | Medium |
| **tj-actions/changed-files** | Advanced filtering, comprehensive data | Feature-rich | Overkill for simple cases | Medium-High |
| **Custom Script** | Highly specific needs | Full control | Must maintain | High |

**Recommendation:**
- Start with **xalvarez/prevent-file-change-action** (Phase 1)
- Upgrade to **dorny/paths-filter** (Phase 2) when you need:
  - Better error messages
  - Categorized feedback
  - PR comments
  - More flexible patterns

### When to Use GitLab vs GitHub

| Criterion | GitHub Actions | GitLab CI |
|----------|---------------|-----------|
| **Platform** | GitHub | GitLab |
| **Ease of Use** | High (marketplace) | Medium (native) |
| **Flexibility** | Very High (actions) | High (rules) |
| **Community** | Large ecosystem | Smaller ecosystem |
| **Setup Time** | Fast (use actions) | Moderate (write rules) |

**Recommendation:**
- **GitHub:** Use Actions-based approach (more examples, easier setup)
- **GitLab:** Use native rules:changes (integrated, no external dependencies)

---

## Appendices

### Appendix A: Ready-to-Deploy Workflows

#### A.1: Basic Validation (GitHub Actions)

**File:** `.github/workflows/basic-artifact-validation.yml`

```yaml
name: Basic Artifact Validation

on:
  pull_request_target:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read
    steps:
      - name: Block AI artifacts
        uses: xalvarez/prevent-file-change-action@v2
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          pattern: .*\.prp\.md$|^PRPs/|^flattened-codebase\.xml$|^INITIAL\.md$
          allowNewFiles: false
```

**Setup:**
```bash
mkdir -p .github/workflows
curl -o .github/workflows/basic-artifact-validation.yml \
  https://raw.githubusercontent.com/[your-repo]/main/.github/workflows/basic-artifact-validation.yml
git add .github/workflows/basic-artifact-validation.yml
git commit -m "Add basic artifact validation"
git push origin main
```

#### A.2: Comprehensive Validation with Feedback (GitHub Actions)

See [Phase 2 Implementation](#step-21-enhanced-validation-workflow-2-hours) for complete workflow.

#### A.3: GitLab CI Validation

**File:** `.gitlab-ci.yml`

```yaml
stages:
  - validate

validate-artifacts:
  stage: validate
  image: alpine:latest
  script:
    - apk add --no-cache git
    - |
      ARTIFACTS=$(git diff --name-only $CI_MERGE_REQUEST_DIFF_BASE_SHA $CI_COMMIT_SHA | \
        grep -E '\.(prp\.md|bmad|\.cursor|\.aider)' || true)
      if [ -n "$ARTIFACTS" ]; then
        echo "❌ AI artifacts detected:"
        echo "$ARTIFACTS"
        exit 1
      fi
      echo "✅ No artifacts detected"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.prp.md"
        - "PRPs/**"
        - "flattened-codebase.xml"
  allow_failure: false
```

### Appendix B: Pattern Library

#### B.1: JSON Format

See [Artifact Detection Patterns - Combined Pattern Library](#combined-pattern-library-json-format) for complete JSON.

#### B.2: YAML Format

See [Artifact Detection Patterns - Pattern Configuration](#pattern-configuration-yaml-format-for-github-actions) for complete YAML.

#### B.3: Regex Patterns

**All BMAD Artifacts:**
```regex
^(flattened-codebase\.xml|\.bmad-flattenignore|docs/stories/story-.*\.md|docs/qa/assessments/.*\.md)$
```

**All PRP Artifacts:**
```regex
^(.*\.prp\.md|PRPs/.*|INITIAL\.md|.*/context-.*\.md|.*/planning-.*\.md)$
```

**All Tool-Specific:**
```regex
^(\.cursorignore|\.cursor/.*|\.aiderignore|\.aider/.*|\.claude/conversation-.*\.json|\.claude/history/.*)$
```

**All Generic AI:**
```regex
^(.*/ai-context-.*\.md|.*/conversation-.*\.md|.*-ai-prompt\.md|.*/todo-ai-.*\.md)$
```

**Combined (all artifacts):**
```regex
^(.*\.prp\.md|PRPs/.*|flattened-codebase\.xml|INITIAL\.md|\.bmad-flattenignore|docs/stories/story-.*\.md|docs/qa/assessments/.*|\.cursorignore|\.cursor/.*|\.aiderignore|\.aider/.*|\.claude/conversation-.*\.json|\.claude/history/.*|.*/ai-context-.*\.md|.*/conversation-.*\.md|.*-ai-prompt\.md|.*/todo-ai-.*\.md)$
```

### Appendix C: Cleanup Scripts

#### C.1: Remove Artifacts from Current Branch

**File:** `scripts/remove-artifacts.sh`

```bash
#!/bin/bash
set -e

echo "🔍 Scanning for AI workflow artifacts..."

# Define patterns
PATTERNS=(
  "*.prp.md"
  "PRPs/"
  "flattened-codebase.xml"
  "INITIAL.md"
  ".bmad-flattenignore"
  "docs/stories/story-*.md"
  ".aiderignore"
  ".aider/"
  ".cursorignore"
  ".cursor/"
)

# Find matching files
FOUND_FILES=()
for pattern in "${PATTERNS[@]}"; do
  while IFS= read -r file; do
    if [ -f "$file" ] || [ -d "$file" ]; then
      FOUND_FILES+=("$file")
    fi
  done < <(find . -path "./.git" -prune -o -name "$pattern" -print 2>/dev/null)
done

# Check if any files found
if [ ${#FOUND_FILES[@]} -eq 0 ]; then
  echo "✅ No artifacts found"
  exit 0
fi

# Display found files
echo "Found ${#FOUND_FILES[@]} artifact(s):"
for file in "${FOUND_FILES[@]}"; do
  echo "  - $file"
done

# Confirm removal
read -p "Remove these files? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled"
  exit 0
fi

# Remove files
for file in "${FOUND_FILES[@]}"; do
  git rm -r "$file"
  echo "Removed: $file"
done

# Commit
git commit -m "Remove AI workflow artifacts"

echo "✅ Artifacts removed and committed"
echo "Run 'git push' to update your PR"
```

**Usage:**
```bash
chmod +x scripts/remove-artifacts.sh
./scripts/remove-artifacts.sh
```

#### C.2: Clean History with git-filter-repo

**File:** `scripts/clean-history.sh`

```bash
#!/bin/bash
set -e

echo "⚠️  WARNING: This will rewrite Git history"
echo "Make sure all team members are notified"
read -p "Continue? (yes/NO) " -r
if [ "$REPLY" != "yes" ]; then
  echo "Cancelled"
  exit 0
fi

# Backup
echo "Creating backup..."
git clone --mirror . ../$(basename $(pwd))-backup.git

# Install git-filter-repo if needed
if ! command -v git-filter-repo &> /dev/null; then
  echo "Installing git-filter-repo..."
  pip install git-filter-repo
fi

# Define patterns to remove
PATTERNS=(
  "*.prp.md"
  "PRPs/*"
  "flattened-codebase.xml"
  "INITIAL.md"
  ".bmad-flattenignore"
  "docs/stories/story-*.md"
  ".aiderignore"
  ".aider/*"
  ".cursorignore"
  ".cursor/*"
  ".claude/conversation-*.json"
  ".claude/history/*"
)

# Build filter-repo command
FILTER_ARGS=""
for pattern in "${PATTERNS[@]}"; do
  FILTER_ARGS="$FILTER_ARGS --path-glob '$pattern'"
done

# Run filter-repo
echo "Cleaning history..."
eval "git filter-repo --invert-paths $FILTER_ARGS --force"

# Cleanup
echo "Running garbage collection..."
git gc --prune=now --aggressive

echo "✅ History cleaned"
echo ""
echo "Next steps:"
echo "1. Review changes: git log --all --oneline"
echo "2. Force push: git push origin --force --all"
echo "3. Force push tags: git push origin --force --tags"
echo "4. Notify team to re-clone repository"
```

**Usage:**
```bash
chmod +x scripts/clean-history.sh
./scripts/clean-history.sh
```

### Appendix D: Additional Resources

#### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [git-filter-repo Manual](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)

#### Tools and Actions

- [xalvarez/prevent-file-change-action](https://github.com/xalvarez/prevent-file-change-action)
- [dorny/paths-filter](https://github.com/dorny/paths-filter)
- [tj-actions/changed-files](https://github.com/tj-actions/changed-files)
- [actions/github-script](https://github.com/actions/github-script)
- [git-filter-repo](https://github.com/newren/git-filter-repo)

#### AI Workflow Methodologies

- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)
- [Context Engineering Intro (PRP)](https://github.com/coleam00/context-engineering-intro)
- [Archon AI Task Management](https://github.com/coleam00/Archon)

#### Example Repositories

- [Prettier (uses prevent-file-change-action)](https://github.com/prettier/prettier)
- [Archon](https://github.com/coleam00/Archon)

#### Community

- [GitHub Community Discussions](https://github.com/orgs/community/discussions)
- [GitLab Forum](https://forum.gitlab.com/)

---

## Conclusion

This research provides a comprehensive strategy for preventing AI workflow artifacts from contaminating main branches while allowing contributors full freedom in their personal workflows.

### Key Takeaways

1. **Multi-Layer Defense-in-Depth** is the most effective approach
2. **Merge-time enforcement** is the critical boundary
3. **Contributor experience** matters - provide clear guidance
4. **Pattern libraries** need maintenance and versioning
5. **Start simple** (Phase 1) and evolve as needed

### Quick Start Checklist

- [ ] Create basic validation workflow (30 min)
- [ ] Enable branch protection (5 min)
- [ ] Update .gitignore (10 min)
- [ ] Test with sample PR (15 min)
- [ ] Document in CONTRIBUTING.md (1 hour)
- [ ] Monitor and refine patterns (ongoing)

### Success Metrics

Track these metrics to measure effectiveness:
- **Artifact Detection Rate:** % of PRs with artifacts detected
- **False Positive Rate:** % of legitimate files blocked
- **Time to Fix:** Average time for contributors to fix validation failures
- **Zero Contamination:** Days since last artifact merged to main

### Future Enhancements

Consider these enhancements as your project matures:
1. **AI-powered pattern detection** using ML to identify new artifact types
2. **Auto-update pattern library** from community contributions
3. **Integration with project management** (link validation to tasks)
4. **Artifact analytics dashboard** for maintainers
5. **Contributor reputation system** based on clean PR history

---

**Document Version:** 1.0.0
**Last Updated:** January 2025
**Maintained By:** [Your Team/Name]
**Contributions Welcome:** Open issues or PRs to improve this research

