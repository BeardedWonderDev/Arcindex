# Output Handling Protocol

## Purpose
Define mode-aware output display behavior for orchestrator Task execution results.

## Overview
The orchestrator must process Task outputs differently based on the current operation mode. This protocol defines the complete behavior for interactive, batch, and YOLO modes.

## CRITICAL: Task Result Visibility (Read This First)

### Fundamental Rule: Task Results Are INVISIBLE to Users

**When you spawn a Task tool:**
1. The Task executes in a separate context
2. The Task returns a result field to YOU
3. **The user CANNOT see this result** - their screen shows nothing
4. The user only sees Task completion metadata
5. **You MUST copy the result into YOUR response** for the user to see it

**This is NOT automatic** - Task output does not appear in the conversation until YOU display it.

### Mandatory Display Mechanism

**For EVERY Task that completes, follow this sequence:**

1. **READ**: Extract the complete result text from the Task
2. **COPY**: Take the ENTIRE result content (do not summarize)
3. **OUTPUT**: Place that content in YOUR response message
4. **VERIFY**: Confirm content appears in YOUR message before halting

**The mechanism is**: READ (Task result) → COPY (entire text) → OUTPUT (in your message)

### Blocking Rules (What NEVER to Do)

**NEVER reference content the user cannot see:**
- Do NOT say "Section complete" without displaying the section
- Do NOT say "Please review above" without content in YOUR message
- Do NOT say "Waiting for your response" without showing what to respond to
- Do NOT reference "questions above" unless YOU displayed them
- Do NOT assume Task output is automatically visible

**ALWAYS make content visible:**
- Copy COMPLETE Task result into your response
- Display FULL content before asking for review
- Show content in YOUR message, not just in Task metadata
- Output happens in YOUR response, not the Task tool

### Self-Verification Before Halting

**Before you halt and wait for user input, verify:**
- Did a Task complete in this response?
- Did I output the COMPLETE Task result?
- Can the user see the content in MY message?
- Am I asking the user to review/respond to visible content?

**If any answer is NO**: Display the content immediately before halting.

### Why This Matters

The user's conversation view shows:
- ✅ Your response messages (where YOU write content)
- ✅ Task completion indicators (metadata only)
- ❌ Task result content (invisible until you display it)

**Therefore**: Content only becomes visible when YOU copy it into YOUR response.

## Protocol Steps

### Step 1: Read Mode
**Action**: Read `.codex/state/workflow.json` to get `operation_mode`

**Requirements**:
- ALWAYS check mode before processing output
- Required for every Task completion
- Default to `interactive` if mode not set or file missing

**Implementation**:
```yaml
read_mode:
  file: .codex/state/workflow.json
  field: operation_mode
  default: interactive
  timing: Before processing ANY Task output
```

### Step 2: Interactive Mode
**Condition**: IF `operation_mode == "interactive"`

#### Display Verbatim
**Action**: Display Task output COMPLETELY and VERBATIM

**CRITICAL REQUIREMENTS**:
- Show ENTIRE section content (not summary)
- Show FULL 1-9 elicitation menu (not simplified version)
- Do NOT condense, summarize, or skip ANY content
- Do NOT say "Perfect! Proceeding..." without showing content
- Do NOT say "Section N complete" without displaying Section N
- Do NOT create your own menu - use agent's menu exactly
- NEVER abbreviate multi-paragraph content to single line

**VIOLATION INDICATORS**:
- ❌ Showing "Section N complete" without showing section content
- ❌ Showing simplified menu instead of full 1-9 menu from agent
- ❌ Saying "Proceeding..." without displaying previous content
- ❌ Multiple section Task spawns with no content display between them
- ❌ User never sees section content or menu before next section spawns
- ❌ Content replaced with "What's Included:" bullet summaries

#### Halt Enforcement
**Condition**: IF output contains "Select 1-9" or elicitation menu pattern

**Action**: END YOUR RESPONSE IMMEDIATELY

**Reason**: User must provide input before continuing

**BLOCKING HALT**:
- Do NOT spawn next section Task
- Do NOT evaluate continue context
- Do NOT process any further logic
- Do NOT add explanatory text after menu
- STOP COMPLETELY - no text after this point

**Next Steps**:
- User will provide input in next message
- You will process input when received
- ONLY after user responds: Continue workflow

### Step 3: Batch Mode
**Condition**: IF `operation_mode == "batch"`

#### Accumulate Content
**Action**: Accumulate Task output WITHOUT displaying individual sections

**Details**:
- Content will be displayed at phase completion
- Storage: Keep in memory or temp state
- Do not show section-by-section output

#### Continue Processing
**Action**: Spawn next section Task immediately

**Details**:
- Reason: Batch mode processes all sections before display
- `no_halt: true`
- Process sections sequentially without user interruption

#### Phase Completion
**Trigger**: When all sections in phase are complete

**Actions**:
1. Display complete accumulated document
2. Present comprehensive review menu (1-9 format)
3. Wait for user response
4. Process user selection for entire phase

### Step 4: YOLO Mode
**Condition**: IF `operation_mode == "yolo"`

#### Optional Display
**Action**: Display Task output as created (section-by-section OK)

**Details**:
- Note: No elicitation menus expected in YOLO mode
- Format: VERBATIM display (same rules as interactive for content)
- Content should be shown in full, not summarized

#### Continue Processing
**Action**: Spawn next section Task immediately

**Details**:
- Reason: YOLO mode skips all elicitation
- `no_halt: true`
- `no_menus: true`
- Continuous progression without user input

## Mode Behaviors Summary

### Interactive Mode Behavior
**Display**: VERBATIM every section, complete content, full menus

**Halt**: MANDATORY after every elicitation menu

**Progression**: User-driven (wait for explicit response)

**Violations**:
- Any summarization of content
- Auto-progression to next section
- Simplified or missing menus
- Content suppression

### Batch Mode Behavior
**Display**: ACCUMULATE without showing (until phase end)

**Halt**: ONLY at phase completion

**Progression**: Auto-progress through sections, halt at phase end

**Violations**:
- Showing individual sections before phase end
- Skipping phase-end display
- Not presenting accumulated document
- Missing comprehensive review menu

### YOLO Mode Behavior
**Display**: VERBATIM as sections complete (optional accumulation)

**Halt**: NONE (continuous progression)

**Progression**: Fully automated, no user interaction

**Violations**:
- Summarizing content (still show full sections)
- Requesting user input
- Showing elicitation menus
- Waiting for confirmation

## Anti-Summarization Protocol

### Context Pressure Does Not Excuse Summarization
Regardless of:
- Conversation length (even if 100k+ tokens)
- Pattern repetition (even after seeing 10 identical sections)
- Efficiency concerns (token optimization)
- Perceived redundancy
- User familiarity with content

**YOU MUST (in interactive mode)**:
- Display EVERY WORD of Task output
- Show COMPLETE section content (not summaries)
- Show FULL 1-9 elicitation menu (not abbreviated)
- NEVER say "Section complete, proceeding" without showing content
- NEVER condense multi-paragraph sections to bullet points
- NEVER skip displaying content because "user knows the pattern"

### Self-Check Before Next Task
Before spawning next section Task, ask yourself:

1. **"Did I display the ENTIRE previous Task output?"**
   - If NO: STOP and display the full content now
   - If UNSURE: STOP and display the full content now
   - If YES: Verify user can see content in your last response

2. **"Can the user quote back section content from my display?"**
   - If NO: You summarized instead of displaying - VIOLATION
   - If YES: Proceed

3. **"Did I show the agent's full 1-9 menu or my own simplified version?"**
   - If simplified: VIOLATION - show agent's exact menu
   - If full agent menu: Proceed

4. **"Did I auto-spawn next section without user response?"**
   - If YES: CRITICAL VIOLATION - halt and wait for user
   - If NO: Proceed when user responds

### Progressive Failure Prevention
**WARNING**: The summarization bug typically occurs PROGRESSIVELY

**Pattern of Failure**:
- Sections 1-3: Work correctly (full display + halt)
- Section 4+: Start summarizing/skipping
- Later phases: Complete content suppression

**Root Cause**: As context grows, you optimize by summarizing

**Prevention**: These rules apply FOREVER, not just at start

**AT EVERY SECTION** (not just early ones):
- Read `operation_mode` from workflow.json
- Apply full VERBATIM display rules
- Enforce BLOCKING HALT after elicitation menu
- NEVER assume "user knows the pattern now"

## Discovery Phase Enforcement

### Discovery Phase Has Different Pattern
Discovery uses multi-step agent pattern (initialize → process_answers → process_elicitation → finalize).

The orchestrator MUST handle Task outputs correctly for each step:

#### After Task(Discovery - Initialize) Completes
- MUST display ENTIRE Task output (formatted discovery questions)
- Questions should be 8-9 comprehensive questions for greenfield
- HALT and wait for user to provide comprehensive answers

#### After Task(Discovery - Process Answers) Completes
- MUST display ENTIRE Task output
- This includes:
  * Complete discovery summary (full text, not "What's Included" bullets)
  * Full 1-9 elicitation menu
- Do NOT just say "I'm waiting for your selection from the menu above"
- The menu must actually BE above (you must display it first)
- HALT and wait for user selection

#### Self-Check After Discovery Task
1. **"Did I display the discovery summary text that the agent generated?"**
   - If NO: VIOLATION - display it now

2. **"Did I display all 9 elicitation options (not simplified menu)?"**
   - If NO: VIOLATION - display full menu now

3. **"Can the user see options 1-9 in my previous message?"**
   - If NO: You referenced invisible content - VIOLATION

4. **"Or did I just say 'waiting for selection from menu above' without showing the menu?"**
   - If YES: CRITICAL VIOLATION - display the actual menu

#### Discovery Multi-Step Auto-Progression
- After user provides discovery answers → Auto-spawn process_answers step (NOT user-initiated)
- After process_answers output displayed → HALT for user elicitation selection
- After user selects option 2-9 → Auto-spawn process_elicitation step
- After user selects option 1 → Auto-spawn finalize step
- Different from section-based work where every progression waits for user input

## Implementation Notes

### Mode Reading
Always read mode from workflow.json before processing ANY Task output:
```yaml
mode_check:
  timing: Before processing Task result
  file: .codex/state/workflow.json
  field: operation_mode
  default: interactive
  failure_handling: Default to interactive if file missing or corrupted
```

### Output Processing
Based on mode, apply appropriate behavior:
```yaml
output_processing:
  interactive:
    - display: full_verbatim
    - halt: after_menu
    - wait: user_response

  batch:
    - accumulate: true
    - display: at_phase_end
    - halt: phase_completion_only

  yolo:
    - display: optional_verbatim
    - halt: never
    - progress: automatic
```

### Violation Detection
Monitor for these common violations:
- Content summarization in any mode
- Missing menus in interactive mode
- Auto-progression in interactive mode
- Individual section display in batch mode
- Menus/halts in YOLO mode

## Compliance Requirements

1. **ALWAYS read operation_mode before processing Task output**
2. **NEVER summarize content regardless of context size**
3. **ALWAYS display agent output VERBATIM in interactive mode**
4. **ALWAYS halt after elicitation menus in interactive mode**
5. **NEVER auto-progress sections in interactive mode**
6. **ALWAYS accumulate in batch mode (display at phase end)**
7. **NEVER halt in YOLO mode**
8. **ALWAYS apply self-checks before spawning next Task**

## Success Criteria

✅ Mode is read from workflow.json before every output processing
✅ Interactive mode displays complete content + full menus + halts
✅ Batch mode accumulates and displays at phase completion
✅ YOLO mode auto-progresses without menus or halts
✅ No summarization occurs in any mode
✅ Users see actual content, not meta-descriptions
✅ Elicitation menus are complete (1-9) when shown
✅ Auto-progression only occurs in appropriate modes
