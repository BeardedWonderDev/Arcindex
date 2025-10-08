# CODEX Development Reference - For Claude Code

**Audience:** Claude Code, AI assistants, automation workflows
**For Human Contributors:** See `CONTRIBUTING.md` instead

This document provides detailed guidance for Claude Code when working on CODEX development tasks.

---

## When to Read This Document

Read this reference when:
- Implementing new CODEX workflows
- Creating or modifying agents
- Working with the `.codex/` framework
- Adding quality gates or validation
- Managing state or checkpoints
- Need architectural guidance
- Unsure about CODEX conventions

---

## CODEX Architecture Overview

### Product Code Structure

**`.codex/` - The ONLY product code directory**

```
.codex/
├── agents/           # 9 workflow agents
│   ├── analyst.md
│   ├── architect.md
│   ├── pm.md
│   ├── prp-creator.md
│   ├── dev.md
│   ├── qa.md
│   ├── orchestrator.md
│   └── [specialized agents]
│
├── workflows/        # 4 workflow definitions (YAML)
│   ├── greenfield-swift.yaml
│   ├── greenfield-generic.yaml
│   ├── brownfield-enhancement.yaml
│   └── health-check.yaml
│
├── templates/        # Document templates
│   ├── project-brief.md
│   ├── prd.md
│   ├── architecture.md
│   └── prp-enhanced.md
│
├── tasks/            # 40+ task definitions
│   ├── create-doc.md
│   ├── validation-gate.md
│   ├── elicit-requirements.md
│   ├── git-operations.md
│   └── [many more tasks]
│
├── state/            # State management
│   ├── workflow/         # Workflow progress tracking
│   ├── checkpoints/      # Context checkpoints
│   ├── feedback/         # PM↔Architect, PRP↔Execution
│   ├── learnings/        # Epic learnings
│   ├── escalations/      # Issues requiring attention
│   └── validation-logs/  # Quality gate results
│
├── checklists/       # 5 quality gate checklists
│   ├── discovery-quality-gate.md      # 15 items
│   ├── analyst-quality-gate.md        # 169 items
│   ├── pm-quality-gate.md             # 130 items
│   ├── architect-quality-gate.md      # 89 items
│   └── prp-quality-gate.md            # 48 items
│
├── config/           # Configuration
│   └── codex-config.yaml
│
└── data/             # Shared knowledge
    ├── elicitation-methods.md
    ├── quality-scoring-rubric.md
    ├── codex-kb.md
    └── prp-patterns.md
```

### Current Project Status

**Version:** Pre-v0.1.0 (Phase 2 Week 4 Complete)
**Completion:** 85% Infrastructure Complete

**Critical Blockers:**
1. Archon MCP integration (0%)
2. Quality gate wiring (30%)
3. End-to-end testing (20%)

**What this means:**
- Infrastructure exists but needs testing
- Empty directories in `.codex/state/` are EXPECTED
- Quality gates defined but not fully wired
- Focus on wiring and testing, not new features

---

## Core Development Principles

Apply these principles to all CODEX development work:

### 1. Fix-Forward Approach

**Never maintain backwards compatibility in Pre-v0.1.0**

```yaml
# BAD: Keeping deprecated code
workflow:
  - old-task: legacy-validation  # Deprecated
  - new-task: quality-gate-validation

# GOOD: Remove immediately
workflow:
  - quality-gate-validation
```

**When you find deprecated code:** Remove it immediately, don't comment it out.

### 2. KISS - Keep It Simple

**Workflows should be readable by humans AND AI**

```yaml
# BAD: Over-engineered
- task: validate-with-complex-conditional-logic
  conditions:
    - if: ${previous.status} == "success" AND ${config.strict_mode}
      then: full-validation
      else:
        if: ${config.lenient_mode}
          then: basic-validation

# GOOD: Simple and clear
- task: validate-output
  validation-level: ${config.validation_level}
```

### 3. DRY - Don't Repeat Yourself (When Appropriate)

**Extract common patterns, but not prematurely**

```yaml
# GOOD: Reusable task definition
# In .codex/tasks/validate-quality.md
- Use this task in multiple workflows
- Parameterize the validation level
- Keep task focused on one responsibility

# ACCEPTABLE: Slight duplication for clarity
# If two workflows have similar but different needs,
# it's OK to have separate tasks if it improves clarity
```

**When to DRY:**
- Same logic in 3+ places → Extract
- Clear abstraction exists → Extract
- Improves maintainability → Extract

**When NOT to DRY:**
- Only 2 uses and might diverge → Wait
- Abstraction is unclear → Wait
- Makes code harder to understand → Don't

### 4. YAGNI - You Aren't Gonna Need It

**Don't add workflow steps or features speculatively**

```yaml
# BAD: Speculative features
- task: setup-advanced-caching  # Not needed yet
- task: implement-retry-logic   # No failures observed
- task: add-telemetry          # No monitoring requirements

# GOOD: Add only what's needed NOW
- task: create-project-brief
- task: elicit-requirements
- task: validate-against-checklist
```

**Questions to ask:**
- Is this needed for the current task? → Add it
- Might we need this later? → Don't add it yet
- This would be nice to have? → Don't add it

### 5. Clear Over Clever

**CODEX workflows should be obvious, not optimized for brevity**

```yaml
# BAD: Clever but cryptic
- task: validate
  params: {l: 4, s: true, f: ["a", "b"]}

# GOOD: Clear and explicit
- task: validate-architecture
  params:
    validation-level: 4
    strict-mode: true
    focus-areas:
      - consistency
      - completeness
```

### 6. Validate Early

**Use quality gates to catch issues fast**

```yaml
# GOOD: Validate at each phase boundary
greenfield-workflow:
  phases:
    - discovery:
        tasks: [...]
        quality-gate: discovery-quality-gate

    - analysis:
        tasks: [...]
        quality-gate: analyst-quality-gate

    - design:
        tasks: [...]
        quality-gate: architect-quality-gate
```

**Don't wait until the end to validate - catch issues early.**

### 7. Document Decisions

**Track architectural choices in ROADMAP.md**

When you make a significant decision:
1. Document WHY in commit message
2. Update ROADMAP.md with context
3. Add to epic learnings if applicable

### 8. One Source of Truth

**`.codex/` is product code. Everything else is artifacts.**

```
.codex/              → Product code (commit to main)
docs/                → AI artifacts (remove from main)
PRPs/                → Workflow artifacts (remove from main)
.bmad-core/          → Reference only (remove from main)
```

Never put production logic outside `.codex/`.

---

## Workflow Development Guide

### Creating New Workflows

**1. Start with YAML structure:**

```yaml
name: workflow-name
version: "1.0"
description: Clear one-line description

phases:
  - phase-name:
      description: What this phase accomplishes

      tasks:
        - task: task-name
          agent: responsible-agent
          inputs: [previous-outputs]
          outputs: [what-this-produces]

      quality-gate:
        checklist: path/to/checklist.md
        required-score: 85
```

**2. Define tasks in `.codex/tasks/`:**

Each task should:
- Have ONE clear responsibility
- Specify inputs and outputs
- Include validation criteria
- Reference the responsible agent

**3. Reference quality gates:**

Every phase should end with a quality gate from `.codex/checklists/`.

### Agent Development

**Agent Structure:**

```markdown
# Agent Name

## Purpose
One-line description of agent responsibility

## Inputs
- What this agent needs to receive

## Outputs
- What this agent produces

## Responsibilities
- Clear list of what agent does
- Each responsibility should be testable

## Quality Criteria
- How to validate agent output
- Reference to quality gate if applicable

## Handoff
- What agent passes to next phase
- Format and structure requirements
```

**Agent Principles:**
- One primary responsibility
- Clear input/output contracts
- Quality criteria built-in
- Handles its own validation

### State Management

**Use `.codex/state/` for:**

1. **Workflow Progress** (`state/workflow/`)
   - Current phase
   - Completed tasks
   - Next task

2. **Checkpoints** (`state/checkpoints/`)
   - Context snapshots
   - Resume points
   - Rollback capability

3. **Feedback Loops** (`state/feedback/`)
   - PM ↔ Architect communication
   - PRP ↔ Execution learning
   - Escalation tracking

4. **Learnings** (`state/learnings/`)
   - Epic-level patterns
   - What worked / didn't work
   - Improvement recommendations

**State File Format:**

```json
{
  "workflow": "greenfield-swift",
  "phase": "analysis",
  "current_task": "elicit-requirements",
  "progress": {
    "discovery": "completed",
    "analysis": "in-progress"
  },
  "context": {
    "project_id": "...",
    "previous_outputs": {...}
  }
}
```

### Quality Gates

**Using Quality Gates:**

1. **Read checklist** from `.codex/checklists/`
2. **Validate output** against each item
3. **Score** (0-100, need 85+ to pass)
4. **Log results** to `.codex/state/validation-logs/`
5. **Block progress** if fails

**Quality Gate Format:**

```markdown
# Phase Quality Gate

## Category 1: Completeness
- [ ] Item 1 (Critical)
- [ ] Item 2 (Important)
- [ ] Item 3 (Nice-to-have)

## Category 2: Consistency
- [ ] Item 4 (Critical)
- [ ] Item 5 (Important)

Scoring:
- Critical failed: Block
- Important failed: Score -20
- Nice-to-have failed: Score -5

Pass threshold: 85/100
```

---

## Common Patterns

### Pattern: Elicitation

```yaml
- task: elicit-requirements
  agent: analyst
  method: structured-conversation
  focus: [goals, constraints, success-criteria]
  output: requirements.md
```

**Use when:** Gathering information from user
**Reference:** `.codex/data/elicitation-methods.md`

### Pattern: Validation

```yaml
- task: validate-output
  agent: qa
  checklist: phase-quality-gate.md
  min-score: 85
  on-fail: escalate
```

**Use when:** Ending a phase
**Reference:** `.codex/checklists/`

### Pattern: Handoff

```yaml
- task: create-handoff
  agent: current-phase-agent
  format: structured-document
  contents: [summary, outputs, next-steps]
  deliver-to: next-phase-agent
```

**Use when:** Transitioning between phases
**Reference:** Agent templates

### Pattern: Feedback Loop

```yaml
- task: request-feedback
  from: architect
  to: pm
  question: "Does this design meet requirements?"
  wait-for: response

- task: incorporate-feedback
  if: feedback.requires_changes
  then: iterate-design
  else: proceed
```

**Use when:** Cross-agent validation needed
**Reference:** `.codex/state/feedback/`

---

## Error Handling Philosophy

### Fail Fast for Critical Issues

**When to fail immediately:**
- Quality gate score < 85
- Missing required inputs
- Invalid workflow configuration
- Agent cannot complete task
- State corruption detected

```yaml
- task: validate
  on-fail: STOP  # Don't continue
  reason: "Cannot proceed without valid architecture"
```

### Log and Continue for Non-Critical

**When to log but continue:**
- Optional quality improvements
- Nice-to-have checklist items
- Non-blocking warnings
- Performance optimization opportunities

```yaml
- task: optimize
  on-fail: LOG  # Continue workflow
  reason: "Optimization failed but not blocking"
```

### Never Accept Corrupted Data

**Always validate:**
- Quality gate results
- Agent outputs
- State transitions
- Handoff documents

If data is corrupted or invalid → FAIL FAST.

---

## Testing Approach

### Current Status

**Infrastructure:** 85% complete
**Testing:** 20% complete (critical blocker)

**Priority:** Write end-to-end tests for existing workflows

### Test Structure

```
tests/
├── unit/              # Task-level tests
├── integration/       # Agent-level tests
└── e2e/               # Full workflow tests
```

### What to Test

1. **Each workflow** (greenfield, brownfield, health-check)
2. **Each agent** (analyst, architect, pm, etc.)
3. **Quality gates** (scoring, blocking, escalation)
4. **State management** (save, load, resume)
5. **Feedback loops** (PM↔Architect, PRP↔Execution)

### Test Quality Gate Integration

Reference: `docs/testing/quality-gate-integration-test-plan.md`

This test plan validates:
- Quality gate execution
- Scoring algorithms
- Pass/fail thresholds
- Escalation triggers
- State logging

---

## Archon MCP Integration (0% - Critical Blocker)

**Status:** Not yet integrated
**Priority:** Critical

### Planned Integration

When Archon MCP is integrated:
- Task management → Archon tasks
- Knowledge base → Archon RAG
- Project tracking → Archon projects
- Document storage → Archon documents

**Until then:** Use local state management

### What This Means

- `.codex/state/` manages everything locally
- No external dependencies yet
- Design for Archon integration (interface ready)
- Don't build duplicate features Archon will provide

---

## Common Mistakes to Avoid

### 1. Don't Put Logic Outside `.codex/`

```
# BAD
scripts/validate.sh    # External script
utils/helper.py        # External utility

# GOOD
.codex/tasks/validate.md          # Task definition
.codex/agents/qa.md                # Agent with logic
```

### 2. Don't Create PRPs for `.codex/` Development

PRPs are workflow artifacts. Use them for feature planning, not framework development.

```
# BAD
PRPs/implement-new-agent.prp.md

# GOOD
Direct implementation in .codex/agents/new-agent.md
Document in ROADMAP.md
```

### 3. Don't Over-Engineer State Management

State is simple: JSON files in `.codex/state/`. Don't build a database.

```
# BAD: Complex state management
state-manager.py with SQL database

# GOOD: Simple JSON files
.codex/state/workflow/current.json
```

### 4. Don't Skip Quality Gates

Every phase MUST end with quality gate validation.

```yaml
# BAD: Skipping validation
phases:
  - analysis:
      tasks: [...]
      # No quality gate!
  - design:
      tasks: [...]

# GOOD: Always validate
phases:
  - analysis:
      tasks: [...]
      quality-gate: analyst-quality-gate
  - design:
      tasks: [...]
      quality-gate: architect-quality-gate
```

### 5. Don't Duplicate Quality Checklists

Quality checklists are defined ONCE in `.codex/checklists/`. Reference them, don't copy.

---

## Quick Reference

### File Locations

```
.codex/agents/          → Agent definitions
.codex/workflows/       → Workflow YAML
.codex/tasks/           → Task definitions
.codex/checklists/      → Quality gates
.codex/state/           → Runtime state
.codex/templates/       → Document templates
.codex/config/          → Configuration
.codex/data/            → Shared knowledge
```

### Key Files

```
.codex/config/codex-config.yaml          → Main configuration
.codex/workflows/greenfield-swift.yaml   → Swift project workflow
.codex/workflows/greenfield-generic.yaml → Generic project workflow
.codex/checklists/analyst-quality-gate.md → Analysis validation (169 items)
.codex/data/elicitation-methods.md       → Requirement gathering patterns
```

### Quality Gate Thresholds

- **Discovery:** 85/100 required
- **Analysis:** 85/100 required (169 items)
- **PM:** 85/100 required (130 items)
- **Architecture:** 85/100 required (89 items)
- **PRP:** 85/100 required (48 items)

### Current Priorities

1. **Wire quality gates** (30% complete)
2. **Integrate Archon MCP** (0% complete)
3. **Write e2e tests** (20% complete)
4. **Test existing workflows** (health-check, greenfield)

---

## Getting Help

**For Claude Code development questions:**
- This document (development guidance)
- `.claude/artifact-policy-reference.md` (artifact classification)
- `CODEX-Workflow-Guide.md` (workflow conceptual guide)

**For architectural questions:**
- ROADMAP.md (current status, decisions)
- .codex/data/codex-kb.md (knowledge base)

**Don't create new documentation files** - update existing ones or ask maintainer.

---

**Remember:** Fix-forward, KISS, DRY when appropriate, YAGNI. Build what's needed now, not what might be needed later.
