# AI Artifact Policy - Detailed Reference

**For:** Claude Code GitHub Actions
**Project:** CODEX - AI Agent Workflow System
**Last Updated:** 2025-10-08

## Purpose

This document provides detailed artifact identification guidance for the AI artifact enforcement workflows. Claude Code should read this document when analyzing PRs for artifacts or responding to artifact-related questions.

## When to Read This Document

Read this detailed reference when:
1. Analyzing a PR for artifacts (@claude-artifacts trigger or PR events)
2. User asks: "is X an artifact?"
3. Uncertain about whether a file is an artifact
4. Need detailed reasoning for artifact classification

## CODEX Project Structure

### Product Code (ALWAYS KEEP)

**`.codex/` - The ONLY product code directory**

This is the entire CODEX framework implementation:

```
.codex/
├── agents/           # 9 workflow agents (analyst, architect, pm, etc.)
├── workflows/        # 4 workflow definitions (greenfield, brownfield, etc.)
├── templates/        # Document templates (project-brief, prd, architecture, prp)
├── tasks/            # 40+ task definitions (create-doc, validation, etc.)
├── state/            # State management (workflow tracking, checkpoints, feedback)
├── checklists/       # 5 quality gate checklists
├── config/           # Configuration files
└── data/             # Shared knowledge (elicitation methods, patterns)
```

**All files in `.codex/` are production code - NEVER remove.**

### AI Workflow Artifacts (ALWAYS REMOVE)

**1. `docs/` - Entire directory is AI artifacts**

Exception: These two files were moved to project root (no longer in docs/):
- `CODEX-User-Guide.md` (now in root)
- `CODEX-Workflow-Guide.md` (now in root)

All other files in `docs/` are AI-generated planning, research, or testing artifacts:
- `docs/research/` - Research documents
- `docs/testing/` - Test plans
- `docs/planning/` - Planning documents
- `docs/validation/` - Validation docs
- `docs/pre-v0.1-Plan/` - Pre-release planning
- `docs/v0.1-Plan/` - Version planning
- Any other files in `docs/`

**Rule:** If it's in `docs/`, it's an artifact (remove from main branch).

**2. `PRPs/` - PRP workflow artifacts**

All files in this directory are workflow artifacts:
- `PRPs/*.prp.md` - Individual PRP files
- `PRPs/templates/` - PRP templates
- `PRPs/ai_docs/` - AI documentation for PRPs
- `PRPs/prp-readme.md` - PRP documentation

**Rule:** Entire `PRPs/` directory is artifacts (remove from main branch).

**3. `.bmad-core/` - BMAD reference files**

These are reference files only, not needed in main branch:
- All files in `.bmad-core/` directory

**Rule:** Remove `.bmad-core/` directory and all contents from main branch.

**4. Standard AI Artifacts**

- `*.prp.md` - PRP files anywhere in repo
- `flattened-codebase.xml` - BMAD codebase flattener output
- `.bmad-flattenignore` - BMAD configuration
- `.cursorignore`, `.cursor/` - Cursor tool artifacts
- `.aiderignore`, `.aider/` - Aider tool artifacts
- `.claude/conversation-*.json` - Claude conversation logs
- `.claude/history/` - Claude history files

### Project Documentation (ALWAYS KEEP)

**Root-level documentation:**
- `README.md` - Project overview
- `ROADMAP.md` - Development roadmap
- `CHANGELOG.md` - Change history
- `LICENSE` - License file
- `CONTRIBUTING.md` - Contributor guidelines
- `CLAUDE.md` - This project's Claude guidelines (you're following it now!)
- `CODEX-User-Guide.md` - User documentation (moved from docs/)
- `CODEX-Workflow-Guide.md` - Workflow guide (moved from docs/)

### Claude Configuration (CONTEXT-DEPENDENT)

**`.claude/` directory - Analyze each file:**

**ALWAYS KEEP:**
- `.claude/commands/*.md` - Project-level slash commands
- `.claude/settings.json` - Project Claude configuration
- `.claude/artifact-exceptions.txt` - Exception learning system
- `.claude/artifact-policy-reference.md` - This file!

**ALWAYS REMOVE:**
- `.claude/conversation-*.json` - Conversation logs
- `.claude/history/` - History files
- Any other personal workflow artifacts

**Rule:** Claude project configuration = KEEP, Claude conversation history = REMOVE

## Detailed Classification Rules

### Rule 1: Location-Based Classification

```
.codex/**           → KEEP (product code)
docs/**             → REMOVE (all AI artifacts)
PRPs/**             → REMOVE (workflow artifacts)
.bmad-core/**       → REMOVE (reference only)
*.prp.md            → REMOVE (anywhere in repo)
```

### Rule 2: Content-Based Override

Even if filename matches artifact pattern, KEEP if:
- File is in `.codex/` (product code directory)
- File is root-level documentation
- File is `.claude/commands/` or `.claude/settings.json`

### Rule 3: Semantic Analysis for Edge Cases

For files not covered by rules 1-2:

**Artifact Indicators:**
- Contains "PRP Template", "BMAD-generated", or AI tool headers
- Has AI conversation structure ("User:", "Assistant:", prompts/responses)
- References AI workflows, prompts, or planning sessions
- Matches tool-specific patterns (Cursor, Aider, Windsurf, etc.)

**Legitimate Indicators:**
- Part of `.codex/` framework
- Referenced by production code
- Serves core project functionality
- Contains actual implementation, not planning

## Common Patterns

### Legitimate Files That Look Like Artifacts

**Pattern:** `context-*.ts` or `context-*.md`

**Analysis:**
- In `.codex/`? → Production code (KEEP)
- In `docs/`? → AI artifact (REMOVE)
- Contains TypeScript class? → Production code (KEEP)
- Contains AI conversation? → Artifact (REMOVE)

**Example:**
```
.codex/agents/context-manager.ts  → KEEP (product code)
docs/context-notes.md             → REMOVE (AI artifact)
```

### Artifacts That Look Legitimate

**Pattern:** `architecture.md`, `planning.md`, `roadmap.md`

**Analysis:**
- In root? → Check specific file (README.md refs it? → KEEP)
- In `docs/`? → REMOVE (entire docs/ is artifacts)
- In `PRPs/`? → REMOVE (workflow artifacts)

**Specific to this project:**
```
ROADMAP.md                → KEEP (root documentation)
docs/architecture.md      → REMOVE (docs/ is artifacts)
docs/planning/roadmap.md  → REMOVE (docs/ is artifacts)
```

## Decision Tree

```
Is file in .codex/?
├─ YES → KEEP (product code)
└─ NO → Continue

Is file in docs/, PRPs/, or .bmad-core/?
├─ YES → REMOVE (artifact directories)
└─ NO → Continue

Is file root-level documentation?
├─ YES → KEEP (README, ROADMAP, LICENSE, etc.)
└─ NO → Continue

Is file .claude/commands/ or .claude/settings.json?
├─ YES → KEEP (project configuration)
└─ NO → Continue

Does filename match artifact pattern?
├─ YES → Analyze content (semantic check)
└─ NO → Analyze content (semantic check)

Content has AI workflow indicators?
├─ YES → REMOVE (artifact)
└─ NO → UNCERTAIN (ask maintainer)
```

## Current Project Status

**Version:** Pre-v0.1.0 (Phase 2 Week 4 Complete)
**Completion:** 85% Infrastructure Complete

**Critical Blockers:**
1. Archon MCP integration (0%)
2. Quality gate wiring (30%)
3. End-to-end testing (20%)

**Active Development:**
- `.codex/` framework complete
- Workflows implemented but need testing
- Quality gates defined but not fully wired
- State management structure in place

**What this means for artifact detection:**
- Empty directories in `.codex/state/` are EXPECTED (template repo)
- Files in `.codex/` are production code even if they look like artifacts
- `docs/` is pure AI artifacts - entire directory can be removed from main

## Example Scenarios

### Scenario 1: New PR with Standard Artifacts

**Files changed:**
- `feature.prp.md`
- `docs/research/analysis.md`
- `flattened-codebase.xml`
- `.codex/agents/analyst.md`

**Classification:**
- `feature.prp.md` → REMOVE (*.prp.md pattern)
- `docs/research/analysis.md` → REMOVE (docs/ is artifacts)
- `flattened-codebase.xml` → REMOVE (BMAD artifact)
- `.codex/agents/analyst.md` → KEEP (product code)

**Action:** Remove first 3 files, keep last file

### Scenario 2: Ambiguous Filenames

**Files changed:**
- `docs/context-api.md`
- `.codex/context-manager.ts`
- `context-notes.md` (in root)

**Classification:**
- `docs/context-api.md` → REMOVE (docs/ is artifacts)
- `.codex/context-manager.ts` → KEEP (.codex/ is product code)
- `context-notes.md` → UNCERTAIN (not in standard location, check content)

**Content check for context-notes.md:**
- Contains API documentation? → UNCERTAIN, ask: "Is this API docs or AI notes?"
- Contains "Asked Claude..." → REMOVE (AI conversation log)

### Scenario 3: Moved Documentation

**File changed:**
- `CODEX-User-Guide.md` (in root)

**Analysis:**
- Previously in `docs/` (would be artifact)
- Now in root (project documentation)
- Referenced by README.md
- Real user documentation

**Classification:** KEEP (legitimate root documentation)

### Scenario 4: BMAD Reference

**File changed:**
- `.bmad-core/reference-implementation.md`

**Old assumption:** Keep for reference
**Correct classification:** REMOVE (reference only, not needed in main)

## Uncertainty Handling

When uncertain about a file:

**1. Check exception list:**
```bash
cat .claude/artifact-exceptions.txt
```

**2. If file is in exception list:**
→ KEEP and note the reason from exception list

**3. If not in exception list:**
→ Mark as UNCERTAIN in PR comment
→ Provide reasoning for uncertainty
→ Ask maintainer for decision

**4. Maintainer responds:**
→ Learn from response (update exceptions automatically)
→ Follow maintainer guidance

## Response Format

When posting PR analysis comment:

```markdown
## 🤖 AI Artifact Analysis Complete

### ✅ Removed (High Confidence)

| File | Reason | Location Rule |
|------|--------|---------------|
| docs/research/notes.md | In docs/ directory | docs/** → REMOVE |
| feature.prp.md | PRP artifact | *.prp.md → REMOVE |
| .bmad-core/ref.md | BMAD reference | .bmad-core/** → REMOVE |

### 🟢 Kept (Legitimate Files)

| File | Reason |
|------|--------|
| .codex/agents/analyst.md | Product code in .codex/ |
| ROADMAP.md | Root documentation |

### ❓ Uncertain - Maintainer Review Needed

| File | Question | Why Uncertain |
|------|----------|---------------|
| notes.md | Is this AI notes or project notes? | Not in standard location, content ambiguous |

**For specific decisions:** Use `@claude keep/remove filename - reason`
**For re-analysis:** Use `@claude-artifacts re-check`
```

## Learning and Improvement

After each PR analysis:

**1. Update exceptions file:**
```
# Add patterns discovered
echo "filename.md # reason - PR #123 - 2025-10-08" >> .claude/artifact-exceptions.txt
```

**2. Commit learnings:**
```bash
git add .claude/artifact-exceptions.txt
git commit -m "chore: update artifact exceptions from PR #123"
```

**3. Track patterns:**
- Frequently uncertain files → Document in this reference
- New AI tools → Add patterns
- Project-specific conventions → Update rules

## Summary: Quick Reference

**ALWAYS KEEP:**
- `.codex/**` (product code)
- Root documentation (README, ROADMAP, etc.)
- `.claude/commands/`, `.claude/settings.json`
- `CODEX-User-Guide.md`, `CODEX-Workflow-Guide.md` (in root)

**ALWAYS REMOVE:**
- `docs/**` (entire directory)
- `PRPs/**` (entire directory)
- `.bmad-core/**` (entire directory)
- `*.prp.md` (anywhere)
- `flattened-codebase.xml`
- AI tool artifacts (.cursor/, .aider/, etc.)
- Conversation logs (.claude/conversation-*.json, .claude/history/)

**ANALYZE CONTENT:**
- Files not matching above patterns
- Ambiguous filenames (context-*, planning, etc.)
- New/unknown file types

---

**Remember:** When in doubt, mark as UNCERTAIN and ask the maintainer. Conservative approach prevents false positives.
