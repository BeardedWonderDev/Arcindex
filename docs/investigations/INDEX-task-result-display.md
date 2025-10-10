# Task Result Display Investigation - Index

**Investigation Date**: 2025-10-09
**Objective**: Design explicit instructions for displaying Task tool results
**Status**: ✅ Complete - Ready for Implementation

---

## Document Structure

This investigation produced 4 comprehensive documents:

### 1. Design Document (Complete Analysis)
**File**: `task-result-display-mechanism-design.md`

**Purpose**: Complete investigation, analysis, and solution design

**Contents**:
- Root cause analysis (why current instructions fail)
- BMAD vs CODEX architecture comparison
- Explicit mechanism specification (READ → COPY → ECHO)
- Anti-pattern documentation with examples
- Testing protocol and success criteria
- Implementation specifications

**Use when**: Need complete understanding of problem and solution

---

### 2. Protocol Update (Ready-to-Apply Text)
**File**: `workflow-start-protocol-update.md`

**Purpose**: Exact replacement text for workflow-start.md

**Contents**:
- Current problematic text (lines to replace)
- NEW explicit mechanism instructions
- Before/after comparison
- All line numbers and exact replacements
- Testing checklist

**Use when**: Ready to implement changes to workflow-start.md

---

### 3. Executive Summary (Key Insights)
**File**: `task-display-mechanism-summary.md`

**Purpose**: High-level overview and implementation guide

**Contents**:
- Problem statement (one-paragraph summary)
- Key findings (architecture difference, ambiguity analysis)
- Solution design (instruction template)
- Implementation checklist (files to update)
- Success metrics and verification

**Use when**: Need quick overview or presenting to others

---

### 4. Quick Reference (Cheat Sheet)
**File**: `task-display-quick-reference.md`

**Purpose**: One-page quick lookup for developers

**Contents**:
- Problem and solution (one-liners)
- Pattern to use everywhere
- Wrong vs Right examples
- Self-check before HALT
- Files to update (table)

**Use when**: Need quick reminder of correct pattern

---

## Problem Statement (Executive Summary)

**Current Issue**:
Orchestrator references Task results without displaying them, saying:
- "I'm awaiting your answers to the discovery questions above" ← NO QUESTIONS SHOWN
- "Please select from the menu I presented" ← NO MENU VISIBLE

**Root Cause**:
Instruction "Display VERBATIM" doesn't specify mechanism in two-layer architecture:
- Sub-agent returns result to Task tool (isolated context)
- Orchestrator receives result but doesn't know to echo it
- User only sees orchestrator's messages, not Task output
- "Display" is ambiguous: Reference? Echo? Copy?

**Solution**:
Explicit READ → COPY → ECHO mechanism:
```
1. READ the Task tool's result text
2. COPY entire result into YOUR response
3. ECHO to user IN your message
4. Verify content visible in YOUR message
5. HALT after displaying
```

---

## Key Findings

### 1. Architecture Matters
**BMAD (one-layer)**:
- Agent displays own output directly
- "Display" = "output in my message" ✓
- Vague verbs work fine

**CODEX (two-layer)**:
- Sub-agent → Orchestrator → User
- "Display" = ??? (ambiguous)
- Needs explicit: "READ Task result → ECHO in your message"

### 2. The Ambiguity Problem
"Display returned questions VERBATIM to user" lacks:
- Source specification (Task result? Where?)
- Action specification (Reference? Copy? Echo?)
- Destination specification (Task output? Orchestrator message?)
- Verification criteria (How to confirm visible?)

### 3. Explicit Mechanism Required
Instructions must say:
- "READ the Task tool's result text" (source)
- "COPY into your response" (action)
- "IN your message" (destination)
- "User must see in YOUR message" (verification)

---

## Solution Pattern

### Universal Template (Use Everywhere)
```markdown
**Step X: SPAWN [Agent] Task**

1. Use Task tool to spawn [agent]
2. Wait for Task completion
3. **READ the Task result text**
4. **COPY entire result into YOUR response**
5. **User must see content IN your message**
6. **HALT after displaying** (if interactive mode)

Mechanism: Task returns → READ → COPY → ECHO → User sees

❌ WRONG: Reference invisible content
✅ RIGHT: Display complete content, then halt
```

### Verb Hierarchy
1. **READ** (clearest source)
2. **COPY** (clearest action)
3. **ECHO** (clear duplication)
4. **DISPLAY in YOUR message** (acceptable with destination)

Avoid: present, output, return (too vague)

---

## Implementation Guide

### Files to Update

| Priority | File | Changes | See Document |
|----------|------|---------|--------------|
| 🔴 HIGH | workflow-start.md | Lines 27-31, 119, 128, 193 | protocol-update.md |
| 🟡 MED | discovery.md | Output protocol | design.md §"For discovery.md" |
| 🟡 MED | output-handling.md | Task result protocol | design.md §"Implementation" |
| 🟢 LOW | anti-summarization.md | Echo requirement | summary.md §"Supporting Files" |

### Update Pattern
**Find**: "Display X VERBATIM to user"
**Replace with**:
```
- READ Task result and COPY into your response
- X must appear IN your message for user to see
- Do NOT reference invisible content
```

---

## Testing Protocol

### Test Cases

| Test | Input | Expected | Violation |
|------|-------|----------|-----------|
| Discovery Init | `/codex start greenfield-swift` | 8-9 questions in orchestrator message | "Answer questions above" (no questions) |
| Discovery Process | User provides answers | Complete summary + 1-9 menu | "Select from menu" (no menu shown) |
| Section Display | User selects option 1 | Full section content + menu | "Section N complete" (no content) |

### Success Criteria
**For each Task execution**:
- [ ] Orchestrator reads Task result
- [ ] Orchestrator copies complete result into response
- [ ] User sees content in orchestrator's message
- [ ] No references to invisible content
- [ ] HALT after display (interactive mode)

---

## Quick Reference

### The Problem (One-Liner)
"Display VERBATIM" doesn't specify mechanism → orchestrator references instead of echoing

### The Solution (One-Liner)
Explicit: READ Task result → COPY to response → ECHO to user → Verify visible

### Wrong vs Right
❌ "I'm awaiting answers to questions above" (invisible content)
✅ [displays full questions] "Please answer these questions"

---

## Document Navigation

### Start Here
→ **task-display-quick-reference.md** (1-page overview)

### Deep Dive
→ **task-result-display-mechanism-design.md** (complete analysis)

### Implementation
→ **workflow-start-protocol-update.md** (exact replacement text)

### Summary
→ **task-display-mechanism-summary.md** (executive overview)

---

## Next Steps

1. **Review**: Read quick-reference.md for pattern understanding
2. **Implement**: Use protocol-update.md to update workflow-start.md
3. **Test**: Verify discovery questions display correctly
4. **Validate**: Ensure no invisible content references
5. **Document**: Mark investigation complete

---

## Success Metrics

**Goal**: Zero instances of invisible content references

**Measure**:
- ✓ All Task results properly echoed to user
- ✓ No "see above" without content shown
- ✓ User can quote back content from orchestrator message

---

## Related Issues

**Root Issue**: Two-layer architecture (orchestrator + sub-agent) requires explicit display mechanism

**Similar Issues to Watch**:
- Any "display agent output" instruction
- Any "present results to user" pattern
- Any Task tool execution with user-facing content

**Prevention**: Always specify READ → COPY → ECHO mechanism for Task results

---

**Investigation Lead**: Claude (Sonnet 4.5)
**Date Completed**: 2025-10-09
**Status**: ✅ Ready for Implementation
**Priority**: 🔴 HIGH (blocking discovery phase UX)
