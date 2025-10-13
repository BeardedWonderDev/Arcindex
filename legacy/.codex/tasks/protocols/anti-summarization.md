# Anti-Summarization Protocol

## Purpose
Prevent output summarization bugs through strict enforcement of verbatim display requirements

## Core Rules

### Context Pressure Does Not Excuse Summarization

**CRITICAL**: Regardless of:
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

### Self-Check Questions Before Next Task

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

## Progressive Failure Prevention

**WARNING**: The summarization bug typically occurs PROGRESSIVELY

**Pattern of failure**:
- Sections 1-3: Work correctly (full display + halt)
- Section 4+: Start summarizing/skipping
- Later phases: Complete content suppression

**Root cause**: As context grows, you optimize by summarizing

**Prevention**: These rules apply FOREVER, not just at start

**AT EVERY SECTION** (not just early ones):
- Read operation_mode from workflow.json
- Apply full VERBATIM display rules
- Enforce BLOCKING HALT after elicitation menu
- NEVER assume "user knows the pattern now"

## Mode-Specific Enforcement

### Interactive Mode
- **Display**: VERBATIM every section
- **Halt**: MANDATORY after every elicitation menu
- **Violation**: Any summarization or auto-progression

### Batch Mode
- **Display**: ACCUMULATE without showing (until phase end)
- **Halt**: ONLY at phase completion
- **Violation**: Showing individual sections OR skipping phase-end display

### YOLO Mode
- **Display**: VERBATIM as sections complete (optional accumulation)
- **Halt**: NONE (continuous progression)
- **Violation**: Summarizing content (still show full sections)

## Discovery Phase Special Handling

**DISCOVERY PHASE HAS DIFFERENT PATTERN THAN SECTION-BASED PHASES**

Discovery uses multi-step agent pattern (initialize → process_answers → process_elicitation → finalize).
The orchestrator MUST handle Task outputs correctly for each step.

### After Task(Discovery - Initialize) completes:
- MUST display ENTIRE Task output (formatted discovery questions)
- Questions should be 8-9 comprehensive questions for greenfield
- HALT and wait for user to provide comprehensive answers

### After Task(Discovery - Process answers) completes:
- MUST display ENTIRE Task output
- This includes:
  * Complete discovery summary (full text, not "What's Included" bullets)
  * Full 1-9 elicitation menu
- Do NOT just say "I'm waiting for your selection from the menu above"
- The menu must actually BE above (you must display it first)
- HALT and wait for user selection

### Self-Check After Discovery Task:

1. **"Did I display the discovery summary text that the agent generated?"**
   - If NO: VIOLATION - display it now

2. **"Did I display all 9 elicitation options (not simplified menu)?"**
   - If NO: VIOLATION - display full menu now

3. **"Can the user see options 1-9 in my previous message?"**
   - If NO: You referenced invisible content - VIOLATION

4. **"Or did I just say 'waiting for selection from menu above' without showing the menu?"**
   - If YES: CRITICAL VIOLATION - display the actual menu

### Discovery Multi-Step Auto-Progression:
- After user provides discovery answers → Auto-spawn process_answers step (NOT user-initiated)
- After process_answers output displayed → HALT for user elicitation selection
- After user selects option 2-9 → Auto-spawn process_elicitation step
- After user selects option 1 → Auto-spawn finalize step
- Different from section-based work where every progression waits for user input

## Section-to-Section Halt Enforcement

**MANDATORY HALT BETWEEN SECTIONS**

In interactive mode during analyst/pm/architect phases:

### After ANY section Task completes and returns output:
- Orchestrator MUST display output + elicitation menu
- Orchestrator MUST HALT immediately
- DO NOT spawn next section Task automatically
- DO NOT interpret "continue" as "auto-progress to next section"
- WAIT for user to provide explicit input (option 1-9 or feedback)

### User response triggers next action:
- User types "1" → Spawn next section Task
- User types "2-9" → Spawn same section Task with elicitation method
- User provides feedback → Spawn same section Task with revision request

### VIOLATION INDICATORS:
- ❌ Task(Section 3) completes → Task(Section 4) spawns immediately
- ❌ Saying "Perfect! Proceeding to Section 4" without showing Section 3 content
- ❌ Showing "Section N complete" without displaying Section N content
- ❌ Displaying Section 4 content before user responded to Section 3 menu
- ❌ Processing multiple sections in one Task execution (should be separate)
- ❌ "Batch processing" multiple sections in interactive mode
- ❌ Creating simplified menu instead of showing agent's full 1-9 menu
- ❌ User never sees section content or elicitation menu before next section spawns
- ❌ Condensing multi-paragraph content to "What's Included:" bullet lists
- ❌ Multiple "Done" messages with no content displayed between them

### CORRECT PATTERN:
- ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User "1" → Task(Section 4)
- ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User "7" → Task(Section 3 elicitation)
- ✓ Task(Section 3) → Display FULL content → Display FULL menu → HALT → User feedback → Task(Section 3 revision)
- ✓ User can quote back section content they saw in orchestrator's display
- ✓ User sees actual 1-9 menu with all elicitation methods listed
- ✓ No progression until user provides explicit response

### AUTO-PROGRESSION ONLY ALLOWED IN:
- operation_mode == "batch" AND at phase completion boundary
- operation_mode == "yolo" (no elicitation required)
- Discovery phase multi-step completion (different pattern)
- Phase-to-phase transitions (after validation)

### NEVER auto-progress in:
- ❌ Interactive mode section-by-section work
- ❌ After elicitation menu presentation
- ❌ Between sections with elicit: true
- ❌ During document creation phases (analyst, pm, architect)

---

**Protocol Version**: 1.0
**Last Updated**: 2025-10-09
**Source**: orchestrator.md lines 671-854, 1047-1097
