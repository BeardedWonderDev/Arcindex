# Task Result Display - Implementation Checklist

**Investigation**: Task Result Display Mechanism Design
**Status**: ✅ Investigation Complete → Ready for Implementation
**Priority**: 🔴 HIGH (Blocking discovery phase UX)

---

## Pre-Implementation

### 1. Review Documentation
- [ ] Read INDEX-task-result-display.md (navigation guide)
- [ ] Read task-display-quick-reference.md (1-page overview)
- [ ] Read workflow-start-protocol-update.md (exact changes)
- [ ] Understand the problem: "Display VERBATIM" is ambiguous in two-layer architecture

### 2. Understand the Pattern
**Mechanism**: Task returns → READ → COPY → ECHO → User sees

**Key Insight**: In CODEX two-layer architecture (orchestrator + sub-agent):
- Sub-agent output is NOT visible to user directly
- Orchestrator must READ Task result and ECHO it
- Instructions must explicitly say "READ → COPY → ECHO"

---

## Implementation Steps

### Phase 1: Primary File (REQUIRED)

#### Update: workflow-start.md

**File**: `.codex/tasks/protocols/workflow-start.md`

**Changes**:

1. **Lines 27-31** (Discovery Initialize - CRITICAL):
   - [ ] Replace "Display returned questions VERBATIM to user"
   - [ ] Add explicit READ → COPY → ECHO mechanism
   - [ ] Add verification: "User must see in YOUR message"
   - [ ] Add anti-pattern examples
   - [ ] See: workflow-start-protocol-update.md §"Section to Replace"

2. **Line 119** (Discovery Initialize - Greenfield):
   - [ ] Replace "Display returned questions VERBATIM to user"
   - [ ] Add "READ Task result and COPY into your response"
   - [ ] See: workflow-start-protocol-update.md §"Update Line 119"

3. **Line 128** (Discovery Process Answers):
   - [ ] Replace "Display summary + menu VERBATIM to user"
   - [ ] Add READ → COPY mechanism for summary + menu
   - [ ] Specify: "Complete summary (full text) + Full 1-9 menu"
   - [ ] See: workflow-start-protocol-update.md §"Update Line 128"

4. **Line 193** (Discovery Initialize - Brownfield):
   - [ ] Replace "Display returned questions VERBATIM to user"
   - [ ] Add "READ Task result and COPY into your response"
   - [ ] See: workflow-start-protocol-update.md §"Update Line 193"

**Verification**:
- [ ] All "Display X VERBATIM" replaced with explicit mechanism
- [ ] All Task outputs have READ → COPY → ECHO instructions
- [ ] All instructions specify "IN your message" (destination)
- [ ] All instructions include verification criteria

---

### Phase 2: Supporting Files (RECOMMENDED)

#### Update: discovery.md

**File**: `.codex/agents/discovery.md`

**Changes**:
- [ ] Add to output-protocol section:
  ```yaml
  critical_output_rules:
    - Your output is NOT automatically visible to user
    - Orchestrator MUST read your result and echo it
    - Return complete formatted text, not meta-descriptions
  ```
- [ ] Update return examples to show plain text format
- [ ] Remove any "display to user" instructions (agent can't do this)

**Verification**:
- [ ] Agent knows output is not directly visible
- [ ] Agent understands orchestrator will echo result
- [ ] No instructions for agent to "display" anything

---

#### Update: output-handling.md

**File**: `.codex/tasks/protocols/output-handling.md`

**Changes**:
- [ ] Add to Step 2 (Interactive Mode):
  ```markdown
  #### Display Verbatim - MECHANISM

  1. READ the Task tool's result/response
  2. COPY entire result into your response
  3. Display in YOUR message (not Task output)
  4. User must see content in YOUR message
  ```
- [ ] Add to Violation Indicators:
  - "Referencing Task result without displaying it"
  - "User cannot see content in orchestrator message"

**Verification**:
- [ ] Task result reading protocol added
- [ ] Echo mechanism specified for all modes
- [ ] Violation indicators include invisible content references

---

#### Update: anti-summarization.md

**File**: `.codex/tasks/protocols/anti-summarization.md`

**Changes**:
- [ ] Add to Discovery Phase section:
  ```markdown
  #### Task Result Echo Requirement

  After ANY Task execution:
  - READ the complete Task result
  - COPY entire result into YOUR response
  - Do NOT reference "above" without showing content
  - User must see content IN your message
  ```
- [ ] Add to Violation Indicators:
  - "Referencing invisible Task results"
  - "Describing content exists without displaying it"

**Verification**:
- [ ] Echo requirement documented
- [ ] Invisible content prevention added
- [ ] Task result violations listed

---

## Testing Protocol

### Test 1: Discovery Questions Display

**Action**: Execute `/codex start greenfield-swift TestApp`

**Expected**:
1. Orchestrator spawns Discovery Task (initialize)
2. Task returns 8-9 formatted questions
3. Orchestrator message contains COMPLETE question text
4. User can read all questions in orchestrator's message
5. Orchestrator halts after displaying questions

**Fail Indicators**:
- ❌ "I'm awaiting your answers to the discovery questions above" (no questions shown)
- ❌ "Please answer the questions" without displaying questions
- ❌ Questions only in Task output, not in orchestrator message

**Pass Criteria**:
- ✅ All 8-9 questions displayed in orchestrator message
- ✅ User can quote back question text from message
- ✅ Orchestrator halts after display
- ✅ No invisible content references

---

### Test 2: Discovery Summary Display

**Action**: Provide discovery answers to questions

**Expected**:
1. Orchestrator spawns Discovery Task (process_answers)
2. Task returns summary + elicitation menu (1-9)
3. Orchestrator message contains:
   - Complete discovery summary (full text, not bullets)
   - Full 1-9 elicitation menu
4. User can read summary and all 9 options
5. Orchestrator halts after displaying

**Fail Indicators**:
- ❌ Summary condensed to "What's Included:" bullet points
- ❌ Menu showing only option 1 (missing 2-9)
- ❌ "Please select from the menu" without showing menu
- ❌ "The discovery summary has been generated" without displaying it

**Pass Criteria**:
- ✅ Complete summary text displayed (not summarized)
- ✅ All 9 elicitation options shown
- ✅ User can read summary and menu in orchestrator message
- ✅ Orchestrator halts after display

---

### Test 3: No Invisible Content References

**Action**: Review all orchestrator messages throughout workflow

**Check Each Message For**:
- References to "above" or "earlier" content
- Verify that referenced content IS displayed in that message
- Ensure no "see questions/menu/content" without showing it

**Fail Indicators**:
- ❌ "As shown above" when content not in message
- ❌ "Review the content earlier" when content not displayed
- ❌ "Select from menu" when menu not visible

**Pass Criteria**:
- ✅ All referenced content is SHOWN in the message
- ✅ No invisible content references
- ✅ User can access all content from orchestrator's messages

---

## Validation Checklist

### Code Review

- [ ] All "Display VERBATIM" instructions replaced
- [ ] All Task executions have explicit echo mechanism
- [ ] All instructions specify destination ("IN your message")
- [ ] All instructions include verification criteria
- [ ] No vague verbs without mechanism specification

### Pattern Compliance

- [ ] Follows READ → COPY → ECHO pattern
- [ ] Uses explicit verbs (READ, COPY, ECHO)
- [ ] Specifies source (Task result)
- [ ] Specifies destination (YOUR message)
- [ ] Includes verification (user must see)

### Documentation

- [ ] Updated instructions are clear and unambiguous
- [ ] Anti-patterns are documented
- [ ] Examples show correct vs incorrect usage
- [ ] Success criteria are measurable

---

## Rollout Plan

### Step 1: Implement Primary Changes
- [ ] Update workflow-start.md (all 4 locations)
- [ ] Test discovery question display
- [ ] Test discovery summary display
- [ ] Verify no invisible references

### Step 2: Implement Supporting Changes
- [ ] Update discovery.md output protocol
- [ ] Update output-handling.md mechanism
- [ ] Update anti-summarization.md requirements
- [ ] Re-test complete discovery flow

### Step 3: Validate and Document
- [ ] Run all test cases
- [ ] Verify success criteria met
- [ ] Document any issues found
- [ ] Mark investigation complete

---

## Success Criteria (Final)

### Zero Instances Of:
- [ ] "Answer questions above" without questions shown
- [ ] "Select from menu" without menu displayed
- [ ] "Review content earlier" without content in message
- [ ] Task results referenced but not echoed

### All Instances Of:
- [ ] Task results properly read and echoed
- [ ] User can see content in orchestrator messages
- [ ] No invisible content references
- [ ] Complete display before halt (interactive mode)

### Verification Method:
**Ask user to quote back content from orchestrator's message**
- If YES: Content was properly displayed ✓
- If NO: Content was referenced but not shown ✗

---

## Post-Implementation

### Monitor For:
- [ ] Any reoccurrence of invisible content references
- [ ] Any new Task execution patterns that need explicit mechanism
- [ ] User feedback on content visibility
- [ ] Related issues in other workflow phases

### Document Results:
- [ ] Test results and findings
- [ ] Any edge cases discovered
- [ ] Lessons learned
- [ ] Pattern improvements for future

---

## Notes and Observations

**Key Takeaway**: In two-layer architecture (orchestrator + sub-agent), explicit mechanism is required:
- Sub-agent can't display directly to user
- Orchestrator is intermediary display layer
- Instructions must say: "READ Task result → COPY to your message → ECHO to user"

**Prevention**: Apply this pattern to ALL Task executions returning user-facing content

---

**Checklist Version**: 1.0
**Last Updated**: 2025-10-09
**Status**: Ready to Execute
**Estimated Time**: 30-45 minutes
