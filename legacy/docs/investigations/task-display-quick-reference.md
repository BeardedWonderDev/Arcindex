# Task Result Display - Quick Reference Card

## The Problem (One-Liner)
**"Display VERBATIM" doesn't specify mechanism in two-layer architecture → orchestrator references instead of echoing**

---

## The Solution (One-Liner)
**Explicit: READ Task result → COPY into your response → ECHO to user → Verify visible**

---

## Pattern to Use Everywhere

```markdown
1. Spawn Task(agent, params)
2. Wait for Task completion
3. READ the Task result text
4. COPY entire result into YOUR response
5. User must see content IN your message
6. HALT (if interactive mode)
```

---

## Wrong vs Right

### ❌ WRONG
```
"I'm awaiting your answers to the discovery questions above"
"Please select from the menu I presented"
"Review the content displayed earlier"
```
**Problem**: References invisible content

### ✅ RIGHT
```
[Complete question text displayed in orchestrator's message]
"Please provide comprehensive answers to these questions"
```
**Solution**: Echo complete Task result, then halt

---

## Explicit Verb Hierarchy

Use these verbs (most explicit first):

1. **READ** - "Read the Task result"
2. **COPY** - "Copy into your response"
3. **ECHO** - "Echo the result verbatim"
4. **DISPLAY** - "Display in YOUR message" (needs "in YOUR message")

**Avoid**: present, output, return, show (too vague)

---

## Mechanism Visualization

```
❌ WRONG:
Task returns text → [magical display] → Reference it
Orchestrator: "Answer the questions above" (no questions shown)

✅ RIGHT:
Task returns text → READ → COPY → ECHO → User sees
Orchestrator: [displays full questions] "Please answer these questions"
```

---

## Self-Check Before HALT

Before halting after Task execution:

- [ ] Did I READ the Task result?
- [ ] Did I COPY the complete result into MY response?
- [ ] Can user SEE content in MY message (not just Task output)?
- [ ] Did I avoid referencing "above/earlier" without showing content?
- [ ] Is content displayed, not described?

**If ANY is NO**: Display the content now before halting

---

## Quick Fix Template

**Replace this pattern**:
```
- Display X to user VERBATIM
```

**With this pattern**:
```
- READ Task result and COPY into your response
- X must appear IN your message for user to see
- Do NOT reference invisible content
```

---

## Files to Update

| File | Lines | Pattern |
|------|-------|---------|
| workflow-start.md | 27-31, 119, 128, 193 | "Display VERBATIM" → READ/COPY/ECHO |
| discovery.md | Output protocol | Add "not visible until echoed" |
| output-handling.md | Step 2 | Add Task result reading protocol |
| anti-summarization.md | Discovery section | Add echo requirement |

---

## Key Insight

**BMAD (one-layer)**: "Display" = "output in my message" ✓

**CODEX (two-layer)**: "Display" = ??? (ambiguous)
- Must specify: "READ Task result, COPY to your message"

**Why**: Sub-agent runs in isolated Task context, can't display directly to user

---

## Success Criteria

**Zero instances of invisible content references**

Test: Can user quote back content from orchestrator's message?
- YES ✓ = Content was properly displayed
- NO ✗ = Content was referenced but not shown

---

## Implementation Checklist

- [ ] Update workflow-start.md with explicit mechanism
- [ ] Update discovery.md output protocol
- [ ] Update output-handling.md Task result protocol
- [ ] Update anti-summarization.md echo requirement
- [ ] Test: Discovery questions display correctly
- [ ] Test: Discovery summary + menu display correctly
- [ ] Test: No invisible content references

---

**Printed**: 2025-10-09
**Status**: Ready to implement
**Source**: task-result-display-mechanism-design.md
