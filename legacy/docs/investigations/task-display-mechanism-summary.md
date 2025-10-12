# Task Result Display Mechanism - Investigation Summary

**Date**: 2025-10-09
**Investigation**: Design explicit instructions for displaying Task tool results
**Status**: ✅ Complete - Ready for implementation

---

## Problem Statement

**Current Issue**:
Orchestrator references Task results without displaying them to user, leading to phrases like:
- "I'm awaiting your answers to the discovery questions above" ← NO QUESTIONS SHOWN
- "Please review the menu I presented" ← NO MENU VISIBLE
- "Based on the content displayed earlier" ← NOTHING WAS DISPLAYED

**Root Cause**:
Instructions say "Display VERBATIM" but don't specify the mechanism in a two-layer architecture where:
1. Sub-agent runs in Task tool (isolated context)
2. Sub-agent returns result text
3. Orchestrator must READ and ECHO that result
4. User only sees orchestrator's messages

---

## Key Findings

### 1. Architecture Difference: BMAD vs CODEX

**BMAD (Single Layer)**:
```
Agent → User (direct)
"Display content" = "Output in my message" ✓
```

**CODEX (Two Layers)**:
```
Sub-Agent → Orchestrator → User
"Display content" = ??? (ambiguous)
Must be: "Read Task result → Echo in your message" ✓
```

**Why BMAD's Instructions Don't Translate**:
- BMAD agents display their own output directly
- CODEX orchestrator displays sub-agent output by proxy
- BMAD can use vague verbs (display, present, show)
- CODEX needs explicit mechanism (read, copy, echo)

### 2. The Ambiguity of "VERBATIM"

**Current instruction**:
```
"Display returned questions VERBATIM to user"
```

**What's ambiguous**:
- ❌ Source: "returned" by what? Task? Where is this text?
- ❌ Action: "display" how? Reference? Echo? Copy?
- ❌ Destination: "to user" via what? Task output? Orchestrator message?
- ❌ Verification: How to confirm user can see it?

**Result**: Orchestrator assumes questions exist "somewhere" and references them

### 3. Explicit Mechanism Required

**What works**:
```markdown
1. READ the Task tool's result text
2. COPY the entire result into your response
3. ECHO it in YOUR message (not Task output)
4. User must see content IN your message
5. HALT after displaying
```

**Why it works**:
- ✓ Source: "Task tool's result text"
- ✓ Action: "COPY" (unambiguous)
- ✓ Destination: "YOUR message"
- ✓ Verification: "User must see in your message"

---

## Solution Design

### Instruction Pattern Template

```markdown
**Step X: SPAWN [Agent] Task**

1. Use Task tool to spawn [agent]
   - Pass: [parameters]

2. Wait for Task completion

3. **READ the Task result**:
   - Task returns [description] as text
   - This is NOT visible to user yet

4. **COPY result into YOUR response**:
   - Take ENTIRE result text
   - Preserve all formatting
   - Do NOT summarize or condense

5. **Display in YOUR message**:
   - Content must appear in your response
   - User must see it in YOUR message
   - NOT just in Task output

6. **Verify before HALT**:
   - Content is IN your message
   - User can read it
   - Not just referenced

7. **HALT immediately**:
   - Wait for user input
   - Do NOT auto-progress

**Mechanism**: Task returns → READ → COPY → ECHO → User sees

**WRONG**: ❌ "Awaiting response to content above" (no content shown)
**RIGHT**: ✅ Show complete content, then halt
```

### Verb Hierarchy (Most to Least Explicit)

Use in order of preference:

1. **READ** - "Read the Task result" (clearest source)
2. **COPY** - "Copy into your response" (clearest action)
3. **ECHO** - "Echo the result verbatim" (clear duplication)
4. **DISPLAY** - "Display in YOUR message" (acceptable with "in YOUR message")
5. **SHOW** - "Show in your response" (acceptable with destination)

**Avoid**:
- ❌ "Present" - too vague
- ❌ "Output" - unclear destination
- ❌ "Return" - could mean pass-through
- ❌ "Display" alone - no destination specified

---

## Implementation Updates

### Primary File: workflow-start.md

**Lines to update**: 27-31, 119, 128, 193

**Pattern**: Replace all "Display X VERBATIM" with explicit mechanism

**See**: `/docs/investigations/workflow-start-protocol-update.md` for exact replacement text

### Supporting Files

**discovery.md**:
- Add output protocol: "Your result is NOT visible to user directly"
- Clarify: "Orchestrator will echo your result"
- Remove: Any "display to user" instructions (agent can't do this)

**output-handling.md**:
- Add: Task result reading protocol
- Specify: Echo mechanism for all modes
- Enforce: Verbatim display = echo complete result

**anti-summarization.md**:
- Add: Task result display rules
- Prevent: Referencing invisible content
- Require: Complete echo before halt

---

## Testing Protocol

### Test Case Matrix

| Test | Input | Expected | Violation |
|------|-------|----------|-----------|
| Discovery Init | `/codex start greenfield-swift` | 8-9 questions in orchestrator message | "Answer questions above" with no questions |
| Discovery Process | User answers | Complete summary + 1-9 menu in message | "Select from menu" with no menu shown |
| Section Display | User selects "1" | Full section content + menu in message | "Section N complete" without content |
| No References | Any step | All content shown, not referenced | "See above" without content |

### Success Criteria

**For each Task execution**:
- [ ] Task completes and returns result
- [ ] Orchestrator reads result text
- [ ] Orchestrator copies complete result into response
- [ ] User can see content in orchestrator's message
- [ ] No references to invisible content
- [ ] HALT occurs after display (if interactive mode)

---

## Anti-Pattern Examples

### ❌ WRONG: Referencing Invisible Content
```
Orchestrator: "I'm awaiting your answers to the discovery questions above"
User: "What questions? I don't see any questions"
```

**Problem**: Questions exist in Task result but never echoed to user

### ❌ WRONG: Meta-Description Instead of Content
```
Orchestrator: "The discovery agent returned 9 comprehensive questions for you to answer"
User: "Where are the questions?"
```

**Problem**: Describes that questions exist but doesn't show them

### ❌ WRONG: Assuming Task Output is Visible
```
Task(Discovery) returns: "1. Project Name...\n2. Concept..."
Orchestrator: "Please provide your answers"
User: [sees no questions]
```

**Problem**: Task output is not visible to user, only to orchestrator

### ✅ CORRECT: Explicit Echo Pattern
```
Task(Discovery) returns: "📋 Discovery Questions\n\n1. Project Name..."
Orchestrator: "📋 Discovery Questions\n\n1. Project Name..." [exact copy]
User: [sees questions and can answer]
```

**Solution**: Orchestrator reads and echoes complete Task result

---

## Comparison: Before vs After

### BEFORE (Vague)
```markdown
**Step 3: SPAWN Discovery Agent**
- Use Task tool to spawn discovery agent
- Pass workflow_type and project_name
- Display returned questions VERBATIM to user
- HALT for answers
```

**Result**: Orchestrator says "answer questions above" (no questions shown)

### AFTER (Explicit)
```markdown
**Step 3: SPAWN Discovery Agent**
1. Use Task tool to spawn discovery agent
2. Wait for Task completion
3. READ the Task result text
4. COPY entire result into YOUR response
5. User must see questions IN your message
6. HALT after displaying

**Mechanism**: Task returns → READ → COPY → ECHO → User sees
```

**Result**: Orchestrator displays complete questions, then halts

---

## Key Insights

### 1. Two-Layer Architecture Requires Explicit Mechanism
- Sub-agent can't display directly to user
- Orchestrator is display intermediary
- Must explicitly read and echo results

### 2. "VERBATIM" is Not Enough
- Needs source: "Task result"
- Needs action: "READ and COPY"
- Needs destination: "YOUR message"
- Needs verification: "User must see"

### 3. Verb Choice Matters
- Vague: display, present, show (ambiguous)
- Explicit: READ, COPY, ECHO (clear mechanism)

### 4. BMAD Patterns Don't Translate Directly
- BMAD: single-layer, direct display
- CODEX: two-layer, proxy display
- CODEX needs more explicit instructions

---

## Recommendations

### Immediate Actions
1. ✅ Update workflow-start.md with explicit mechanism (lines 27-31, 119, 128, 193)
2. ✅ Update discovery.md output protocol
3. ✅ Update output-handling.md with Task result protocol
4. ✅ Add to anti-summarization.md

### Pattern to Apply Universally
**Whenever Task tool returns user-facing content**:
```
1. READ Task result
2. COPY into your response
3. Display in YOUR message
4. Verify user can see it
5. HALT if needed
```

### Long-Term Guidelines
- Always specify mechanism for two-layer patterns
- Use explicit verbs (READ, COPY, ECHO)
- Include destination (YOUR message, not Task output)
- Add verification (user must see in your message)
- Document anti-patterns (what NOT to do)

---

## Files Created

1. **task-result-display-mechanism-design.md**
   - Complete analysis and solution design
   - Anti-pattern documentation
   - Testing protocol

2. **workflow-start-protocol-update.md**
   - Ready-to-apply replacement text
   - Exact updates for workflow-start.md
   - Before/after examples

3. **task-display-mechanism-summary.md** (this file)
   - Executive summary
   - Key findings and insights
   - Implementation checklist

---

## Success Metrics

**Goal**: Zero instances of invisible content references

**Measure**:
- No "answer questions above" without questions shown
- No "select from menu" without menu displayed
- No "review content earlier" without content in message
- All Task results properly echoed to user

**Verification**:
- User can quote back content from orchestrator's message
- No references to content that isn't visible
- Complete display before halt in interactive mode

---

## Conclusion

**Problem**: Vague "display VERBATIM" instruction fails in two-layer architecture

**Solution**: Explicit READ → COPY → ECHO mechanism with verification

**Impact**: Ensures all Task results are properly displayed to users through orchestrator's message channel

**Next Step**: Apply updates to workflow-start.md and supporting files

---

**Investigation Status**: ✅ Complete
**Design Status**: ✅ Ready for Implementation
**Documentation**: ✅ Complete
**Testing Protocol**: ✅ Defined
