# Task Result Display Mechanism Design

## Investigation Summary

**Date**: 2025-10-09
**Objective**: Design explicit, unambiguous instructions for displaying Task tool results to prevent misinterpretation

**Current Problem**:
- Instruction "Display returned questions VERBATIM" is too vague
- Doesn't specify the mechanism (read from where, output how)
- Orchestrator misinterprets as "questions are already displayed somewhere"
- Results in referencing invisible content instead of showing it

## Root Cause Analysis

### Why Current Instructions Fail

The instruction in `workflow-start.md` line 30:
```
- Display questions to user VERBATIM
```

**Fails because:**
1. No explicit source: "Display WHAT?" → Assumes questions already exist visibly
2. No explicit mechanism: "HOW to display?" → Could mean reference, echo, copy, show
3. No explicit destination: "WHERE to display?" → In Task output? In orchestrator response?
4. No explicit format: "In what structure?" → Plain text? Formatted? Embedded?

### Comparison with BMAD System

**BMAD approach** (from `.bmad-core/tasks/create-doc.md`):
```yaml
2. Present results with insights
```

**Analysis**: BMAD also uses vague verbs ("Present"), BUT:
- BMAD operates with single agent (no Task tool spawning pattern)
- BMAD agent directly displays its own output
- No orchestrator → sub-agent → output chain

**CODEX difference**:
- Orchestrator spawns Discovery agent via Task tool
- Discovery returns output as Task result
- Orchestrator MUST extract and display that result
- Two-step process requires explicit mechanism

## The Display Mechanism Problem

### Current Ambiguous Pattern
```
Step 3: SPAWN Discovery Agent (step: initialize)
- Use Task tool to spawn discovery agent
- Pass workflow_type and project_name (if provided)
- Discovery agent creates workflow.json and returns questions
- Display questions to user VERBATIM     <-- AMBIGUOUS
- HALT - wait for user to provide answers
```

**What orchestrator interprets:**
- "Discovery agent returns questions" = questions exist somewhere
- "Display VERBATIM" = reference what already exists
- Result: "I'm awaiting your answers to the discovery questions above" ← NO QUESTIONS SHOWN

### What Actually Happens

**Task tool execution flow:**
1. Orchestrator invokes: `Task(agent: discovery, step: initialize, ...)`
2. Discovery agent executes in sub-context
3. Discovery agent generates formatted question text
4. Discovery agent returns: `result = "📋 Discovery Questions\n\n1. Project Name...\n2. Brief Concept..."`
5. Task tool completes, result available to orchestrator
6. **PROBLEM**: Orchestrator doesn't know to read `result` and echo it

## Solution: Explicit Mechanism Instructions

### Design Requirements

Instructions must specify:
1. **Source**: Read the Task tool's result/response
2. **Action**: Copy/echo the entire text
3. **Destination**: Into your (orchestrator's) next message
4. **Format**: As plain text, preserving all formatting
5. **Verification**: Questions must appear IN your response, not referenced

### Revised Instruction Format

**BEFORE (vague):**
```
- Display questions to user VERBATIM
```

**AFTER (explicit):**
```
- **READ** the Task tool's result/response text
- **COPY** the entire response into your next message as plain text
- The questions must appear **IN YOUR RESPONSE**, not just in the Task result
- Do NOT reference "questions above" - SHOW them in full
- HALT - wait for user to provide comprehensive answers
```

### Complete Step Protocol

```markdown
### Step b: SPAWN Discovery Agent (step: initialize)

1. Use Task tool to spawn discovery agent
2. Pass workflow_type and project_name (if provided)
3. **WAIT** for Task tool to complete execution
4. **READ** the Task tool's returned result text
5. **COPY** the entire result into your next message verbatim
6. Ensure questions appear as plain text in YOUR response
7. Do NOT just reference the questions - DISPLAY them in full
8. The user must be able to read the questions in your message
9. HALT - wait for user to provide comprehensive answers

**CRITICAL**: The mechanism is:
- Task returns text → You read that text → You echo that text → User sees text
- NOT: Task returns text → Text magically appears → You reference it
```

## Anti-Pattern Documentation

### ❌ WRONG Patterns to Prevent

**Anti-Pattern 1: Referencing Invisible Content**
```
❌ "I'm awaiting your answers to the discovery questions above"
❌ "Please see the questions I presented earlier"
❌ "The questions have been displayed for you"
```
**Why wrong**: Questions never displayed, user cannot see them

**Anti-Pattern 2: Meta-Description Instead of Content**
```
❌ "I've spawned the discovery agent which returned 9 questions"
❌ "The Task completed successfully with discovery questions"
❌ "Here are the discovery questions: [Task tool output]"
```
**Why wrong**: Describes questions exist but doesn't show them

**Anti-Pattern 3: Assuming Task Output is Visible**
```
❌ Task completes → Orchestrator says "Please answer the questions"
❌ Task completes → Orchestrator spawns next Task immediately
❌ Task completes → Orchestrator references result without displaying
```
**Why wrong**: Task results are NOT automatically visible to user

### ✅ CORRECT Patterns to Follow

**Correct Pattern 1: Explicit Echo**
```
✅ Task(Discovery - initialize) completes
✅ Orchestrator reads: result = "📋 Discovery Questions\n\n1. ..."
✅ Orchestrator responds: "📋 Discovery Questions\n\n1. ..." [exact copy]
✅ User sees questions in orchestrator's message
```

**Correct Pattern 2: Verbatim Display with Context**
```
✅ "🎯 Discovery phase initialized. Here are your discovery questions:

📋 Discovery Questions

1. Project Name: What is your project called?
2. Brief Concept: What are you building?
...

Please provide comprehensive answers to all questions."
```

**Correct Pattern 3: Verification Before Halt**
```
✅ Display complete Task result
✅ Verify result text is in YOUR message (not just Task output)
✅ Then HALT for user input
```

## Implementation Specifications

### Task Result Handling Protocol

**For ALL Task tool executions that return user-facing content:**

```yaml
task_result_handling:
  step_1_execute:
    action: "Invoke Task tool with agent and parameters"

  step_2_wait:
    action: "Wait for Task execution to complete"
    note: "Task runs in sub-context, not visible to user"

  step_3_read:
    action: "Read the Task tool's result/response property"
    source: "task.result or task.output or returned text"

  step_4_echo:
    action: "Copy the ENTIRE result text into your response"
    format: "Plain text, preserve all formatting"
    destination: "Your (orchestrator's) next message to user"

  step_5_verify:
    check: "Result text appears IN your message"
    not: "Result only in Task output"
    not: "Referenced but not shown"

  step_6_halt:
    condition: "If result contains questions or menu"
    action: "HALT immediately for user response"
    no_auto_progress: true
```

### Explicit Verb Hierarchy

**Use these verbs in descending order of explicitness:**

1. **READ** - "Read the Task tool's result text"
2. **COPY** - "Copy the entire result into your response"
3. **ECHO** - "Echo the Task output verbatim"
4. **DISPLAY** - "Display the result in your message" (acceptable if context clear)
5. **SHOW** - "Show the questions in your response" (acceptable if context clear)

**AVOID these vague verbs:**
- ❌ "Present" - too ambiguous
- ❌ "Return" - could mean pass through
- ❌ "Provide" - doesn't specify how
- ❌ "Output" - doesn't specify destination
- ❌ "Display" without "in your message" - ambiguous destination

### Success Criteria Checklist

Before HALT after Task execution, verify:

- [ ] Task tool has completed execution
- [ ] Result text has been read from Task output
- [ ] Entire result appears in YOUR message (not just Task output)
- [ ] User can read the content in your response
- [ ] No references to "above" or "earlier" without showing content
- [ ] Content is shown, not described
- [ ] Format is preserved (markdown, lists, structure)
- [ ] HALT occurs AFTER display, not before

## Revised Protocol Text

### For workflow-start.md

Replace lines 27-31 with:

```markdown
**Step 3: SPAWN Discovery Agent (step: initialize)**

1. Use Task tool to spawn discovery agent:
   - Pass: workflow_type, project_name (if provided)

2. Wait for Task tool to complete execution

3. **READ the Task result text**:
   - The Task returns formatted discovery questions
   - This text exists in the Task result, NOT visible to user yet

4. **COPY the complete result into your response**:
   - Do NOT reference "questions above"
   - Do NOT describe that questions exist
   - SHOW the actual question text in YOUR message
   - Preserve all formatting (markdown, numbers, structure)

5. Verify questions appear IN your response:
   - User must be able to read questions from your message
   - Questions should be visible as plain text
   - NOT just referenced or described

6. **HALT immediately**:
   - Wait for user to provide comprehensive answers
   - Do NOT proceed to next step
   - Do NOT spawn another Task

**Example of CORRECT execution:**
```
🎯 Discovery phase initialized.

📋 Discovery Questions

Please provide answers to the following:

1. Project Name: What is your project called?
2. Brief Project Concept: What are you building?
[... full questions displayed ...]

Please provide comprehensive answers to all questions.
```

**VIOLATION INDICATORS:**
- ❌ "I'm awaiting your answers to the discovery questions above" (no questions shown)
- ❌ "Please see the questions displayed earlier" (questions not in this message)
- ❌ "The Task returned 9 questions for you" (describes but doesn't show)
- ❌ Spawning next Task without displaying previous result
```

### For discovery.md Output Protocol

Add to discovery agent's return documentation:

```yaml
critical_output_rules:
  - Your output is NOT automatically visible to user
  - Orchestrator MUST read your result and echo it
  - Return complete formatted text, not meta-descriptions
  - Orchestrator will copy your result into their response
  - User sees content via orchestrator's echo, not your Task output

output_format:
  - Return plain text with markdown formatting
  - Include all content user needs to see
  - Do NOT say "display this to user" - just return the content
  - Orchestrator will handle the display mechanism

example_return:
  correct: |
    📋 Discovery Questions

    Please provide answers to the following:

    1. Project Name...
    2. Brief Concept...
    [complete questions]

  incorrect: |
    "Display these 9 questions to the user:
    [questions]

    Wait for answers."
```

## BMAD vs CODEX Pattern Comparison

### BMAD Pattern (Single Agent)
```
Agent: "Here is Section 1 content: [content]"
↓
User sees: Section 1 content (agent displays directly)
```

**Characteristics:**
- Agent has direct message channel to user
- "Display" means "output in my response"
- No intermediary needed
- Works with vague verbs (display, present, show)

### CODEX Pattern (Orchestrator + Sub-Agent)
```
Sub-Agent: Returns "Section 1 content: [content]"
↓ (via Task tool)
Orchestrator: Must READ result and ECHO to user
↓
User sees: Section 1 content (via orchestrator's echo)
```

**Characteristics:**
- Sub-agent runs in isolated Task context
- Sub-agent output is NOT visible to user
- Orchestrator is intermediary display layer
- Requires explicit mechanism (read → echo)
- Vague verbs FAIL without explicit instructions

### Why CODEX Needs More Explicit Instructions

**BMAD can say:**
- "Display the content" ✓ (agent displays own output)

**CODEX must say:**
- "Read Task result, copy into your response, show to user" ✓
- NOT just "Display the content" ✗ (which Task's content?)

**Root difference**:
- BMAD = 1-layer (agent → user)
- CODEX = 2-layer (sub-agent → orchestrator → user)

## Testing Protocol

### Test Case 1: Discovery Initialize
```
Input: /codex start greenfield-swift MyApp
Expected:
  1. Orchestrator spawns Task(Discovery - initialize)
  2. Task returns 8-9 formatted questions
  3. Orchestrator response contains full question text
  4. User can read questions in orchestrator's message
  5. Orchestrator halts for answers

Violation:
  - Orchestrator says "answer the questions" but shows no questions
  - Orchestrator references questions without displaying
```

### Test Case 2: Discovery Process Answers
```
Input: User provides discovery answers
Expected:
  1. Orchestrator spawns Task(Discovery - process_answers)
  2. Task returns summary + elicitation menu (1-9)
  3. Orchestrator response contains FULL summary text
  4. Orchestrator response contains complete 1-9 menu
  5. Orchestrator halts for menu selection

Violation:
  - Summary condensed to "What's Included:" bullets
  - Menu shown as "1. Proceed" only (missing 2-9)
  - Orchestrator references "menu above" but didn't show it
```

### Test Case 3: Section Elicitation
```
Input: User selects option 1 after section display
Expected:
  1. Orchestrator spawns next section Task
  2. Task returns section content + menu
  3. Orchestrator displays COMPLETE section text
  4. Orchestrator displays FULL 1-9 menu
  5. Orchestrator halts for selection

Violation:
  - "Section 3 complete, proceeding..." (no content shown)
  - Condensed multi-paragraph to single line
  - Shows simplified menu instead of agent's 1-9
  - Auto-spawns Section 4 without waiting
```

## Recommended Instruction Patterns

### Pattern 1: Step-by-Step Mechanism
```markdown
1. Spawn Task(agent, params)
2. Wait for Task completion
3. **READ** Task result text
4. **COPY** result into your response
5. Display to user in YOUR message
6. HALT for user input
```

### Pattern 2: Explicit Echo Instruction
```markdown
**CRITICAL**: After Task completes:
- Read the Task tool's returned result text
- Echo the ENTIRE result in your next message
- User must see content in YOUR response
- Do NOT reference invisible content
- HALT after displaying
```

### Pattern 3: Anti-Pattern Prevention
```markdown
**DO**:
- ✓ Copy Task result into your message
- ✓ Show complete content verbatim
- ✓ User sees content in your response

**DO NOT**:
- ✗ Reference "questions above" without showing them
- ✗ Describe content exists without displaying it
- ✗ Assume Task output is visible to user
- ✗ Auto-progress without displaying result
```

## Implementation Checklist

### For workflow-start.md
- [ ] Replace vague "Display VERBATIM" with explicit mechanism
- [ ] Add READ → COPY → ECHO steps
- [ ] Include anti-pattern examples
- [ ] Add verification criteria
- [ ] Specify HALT enforcement after display

### For discovery.md
- [ ] Document that output is NOT visible to user directly
- [ ] Clarify orchestrator must echo the result
- [ ] Specify return format (plain text with markdown)
- [ ] Remove any "display to user" instructions (agent can't)

### For output-handling.md
- [ ] Add Task result reading protocol
- [ ] Specify echo mechanism for all modes
- [ ] Include verbatim display requirements
- [ ] Document verification before halt

### For anti-summarization.md
- [ ] Add Task result display rules
- [ ] Prevent referencing invisible content
- [ ] Enforce complete echo requirement
- [ ] Add self-check questions for Task outputs

## Conclusion

**Key Insight**: The verb "DISPLAY" is ambiguous in a two-layer architecture (orchestrator + sub-agent). The mechanism must be explicit:

**Explicit Mechanism**:
1. Task returns result → 2. Orchestrator reads result → 3. Orchestrator echoes result → 4. User sees content

**Instructions must say**:
- "READ the Task result"
- "COPY into your response"
- "ECHO to user in YOUR message"
- "Show in YOUR response, not Task output"

**NOT just**:
- "Display VERBATIM" ← ambiguous destination
- "Show to user" ← ambiguous mechanism
- "Present questions" ← ambiguous source

This design provides unambiguous, executable instructions that prevent misinterpretation and ensure Task outputs are properly displayed to users through the orchestrator's message mechanism.

---

**Document Status**: Design Complete
**Next Step**: Implement changes to workflow-start.md, discovery.md, output-handling.md
**Success Metric**: Zero instances of "awaiting answers to questions above" without questions shown
