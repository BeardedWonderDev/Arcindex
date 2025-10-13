# Workflow Start Protocol Update - Ready to Apply

## File to Update
`/Users/brianpistone/Development/BeardedWonder/CODEX/v0.1-implementation/.codex/tasks/protocols/workflow-start.md`

## Section to Replace

**Current Lines 27-31** (the problematic section):
```markdown
**Step 3: SPAWN Discovery Agent (step: initialize)**
- Use Task tool to spawn discovery agent
- Pass workflow_type and project_name (if provided)
- Discovery agent creates workflow.json and returns formatted questions
- Display returned questions VERBATIM to user         <-- PROBLEM: Vague
- HALT - wait for user to provide comprehensive answers
- DO NOT present your own questions - always use discovery agent's questions
```

## Replace With (Explicit Mechanism Version)

```markdown
**Step 3: SPAWN Discovery Agent (step: initialize)**

Execute the following steps in order:

1. **Spawn Discovery Agent Task**:
   - Use Task tool to spawn discovery agent
   - Pass workflow_type and project_name (if provided)

2. **Wait for Task Completion**:
   - Discovery agent creates workflow.json in sub-context
   - Discovery agent generates formatted question text
   - Discovery agent returns complete question text as Task result

3. **READ the Task Result**:
   - The Task tool returns a result containing formatted questions
   - This result text is NOT automatically visible to user
   - You (orchestrator) must read this result

4. **COPY Result into Your Response**:
   - Take the ENTIRE Task result text
   - Copy it verbatim into your next message
   - Preserve all formatting (markdown, numbering, structure)

5. **Display in YOUR Message**:
   - The questions must appear IN your response to user
   - NOT just in the Task output (user can't see that)
   - User must be able to read questions from your message

6. **Verify Before Halt**:
   - Confirm questions are displayed in YOUR message
   - Ensure user can see the actual question text
   - Do NOT reference "questions above" if you didn't show them

7. **HALT Immediately**:
   - End your response after displaying questions
   - Wait for user to provide comprehensive answers
   - Do NOT proceed to next step automatically

**The Display Mechanism**:
```
Task returns text → You READ text → You COPY text → You ECHO text → User SEES text
NOT: Task returns text → Text magically appears → You reference it
```

**CORRECT Example**:
```
🎯 Discovery phase initialized.

📋 Discovery Questions

Please provide answers to the following:

1. Project Name: What is your project called?
2. Brief Project Concept: What are you building?
[... complete questions displayed ...]

Please provide comprehensive answers to all questions.
```

**VIOLATION INDICATORS**:
- ❌ "I'm awaiting your answers to the discovery questions above" (no questions shown)
- ❌ "Please see the questions I presented" (questions not in this message)
- ❌ "The discovery agent returned questions for you" (describes, doesn't show)
- ❌ Spawning next Task without displaying previous result
- ❌ User cannot see question text in your message
```

## Alternative: Concise Version

If the above is too verbose, use this condensed version:

```markdown
**Step 3: SPAWN Discovery Agent (step: initialize)**

1. Use Task tool to spawn discovery agent
   - Pass: workflow_type, project_name (if provided)

2. Wait for Task completion, then **READ the Task result**

3. **COPY the complete result into your response**:
   - The Task returns formatted questions as text
   - This text is NOT visible to user until you display it
   - You must ECHO the entire result in YOUR message
   - Do NOT just reference "questions above" - SHOW them

4. **Verify and HALT**:
   - Questions must appear IN your response (not just Task output)
   - User must be able to read questions from your message
   - HALT immediately for user to provide answers

**Mechanism**: Task result → READ → COPY → ECHO → User sees

**WRONG**: ❌ "I'm awaiting answers to questions above" (no questions shown)
**RIGHT**: ✅ Display full question text in your message, then halt
```

## Additional Updates Needed

### Update Line 119 (same issue)
**Current**:
```markdown
- Discovery agent creates workflow.json and returns formatted questions
- Display returned questions VERBATIM to user
```

**Replace with**:
```markdown
- Discovery agent creates workflow.json and returns formatted questions
- **READ the Task result and COPY it into your response**
- Questions must appear IN your message for user to see
```

### Update Line 128 (same issue)
**Current**:
```markdown
- Display summary + menu VERBATIM to user
```

**Replace with**:
```markdown
- **READ Task result and COPY into your response**:
  * Complete discovery summary (full text)
  * Full 1-9 elicitation menu
- Content must appear IN your message, not just referenced
```

### Update Line 193 (brownfield section, same issue)
**Current**:
```markdown
- Display returned questions VERBATIM to user
```

**Replace with**:
```markdown
- **READ Task result and COPY into your response**
- Questions must appear IN your message for user to see
```

## Pattern to Apply Throughout File

**Find all instances of**:
- "Display returned X VERBATIM"
- "Display X to user VERBATIM"
- "Present output to user"
- "Show result to user"

**Replace with explicit mechanism**:
- "READ Task result and COPY into your response"
- "Content must appear IN your message"
- "ECHO the complete result verbatim"
- "User must see content in YOUR response, not Task output"

## Testing After Update

### Test 1: Discovery Questions Display
```
Action: /codex start greenfield-swift TestApp
Expected: Orchestrator message contains 8-9 full discovery questions
Fail: "Please answer the questions above" with no questions shown
```

### Test 2: Discovery Summary Display
```
Action: Provide discovery answers
Expected: Orchestrator message contains complete summary text + full 1-9 menu
Fail: Summary as bullets or menu showing only option 1
```

### Test 3: No Invisible References
```
Check: All orchestrator messages
Expected: Any referenced content is SHOWN in that message
Fail: "See above" or "as displayed earlier" with no content
```

## Summary of Changes

**Problem**: "Display VERBATIM" doesn't specify the mechanism in a two-layer architecture

**Solution**: Explicit READ → COPY → ECHO mechanism

**Key Changes**:
1. Add explicit step: "READ the Task result"
2. Add explicit action: "COPY into your response"
3. Add explicit destination: "IN your message" (not Task output)
4. Add verification: "User must see content in YOUR response"
5. Add anti-patterns: Show what NOT to do

**Effect**: Orchestrator knows to read Task results and echo them, not just reference them

---

**Ready to Apply**: Yes
**Files to Update**: workflow-start.md (primary)
**Success Criteria**: Zero instances of invisible content references
