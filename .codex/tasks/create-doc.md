<!-- Powered by CODEX™ Core -->

# Create Document from Template (YAML Driven)

## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

When this task is invoked:

1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
2. **MANDATORY STEP-BY-STEP EXECUTION** - Each section must be processed sequentially with user feedback
3. **ELICITATION IS REQUIRED** - When `elicit: true`, you MUST use the 1-9 format and wait for user response
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without following this workflow

**VIOLATION INDICATOR:** If you create a complete document without user interaction, you have violated this workflow.

## Critical: Template Discovery

If a YAML Template has not been provided, list all templates from .codex/templates or ask the user to provide another.

## CRITICAL: Mandatory Elicitation Format

**When `elicit: true`, this is a HARD STOP requiring user interaction:**

**⚠️ NO SHORTCUTS ALLOWED ⚠️**

**YOU MUST:**

1. Present section content
2. Provide detailed rationale (explain trade-offs, assumptions, decisions made)
3. **STOP and present numbered options 1-9 using advanced-elicitation.md:**
   - **Option 1:** Always "Proceed to next section"
   - **Options 2-9:** Select 8 methods from .codex/data/elicitation-methods.md
   - Use .codex/tasks/advanced-elicitation.md for intelligent method selection
   - End with: "Select 1-9 or just type your question/feedback:"
4. **WAIT FOR USER RESPONSE** - Do not proceed until user selects option or provides feedback

**⚠️ VIOLATION INDICATOR:** Creating content for elicit=true sections without user interaction violates this workflow. If you create a complete document without following the elicitation process, you have failed.

**NEVER ask yes/no questions or use any other format.**

## Mode-Aware Processing

**CRITICAL: Check operation_mode BEFORE beginning section processing**

1. Read `.codex/state/runtime/workflow.json`
2. Extract `operation_mode` value
3. Select processing pattern based on mode:

### Interactive Mode (operation_mode == "interactive")
**REQUIRED PATTERN: Section-by-section with elicitation after EACH section**

For each section with elicit: true:
  1. Draft ONLY this section (not future sections)
  2. Present content + detailed rationale
  3. HALT and present 1-9 numbered elicitation options
  4. WAIT for user response
  5. Process user selection
  6. If user selects 1: Save section, move to next
  7. If user selects 2-9: Execute method, return to step 3

**VIOLATION**: Drafting multiple sections before presenting elicitation in interactive mode

### Batch Mode (operation_mode == "batch")
**ALLOWED PATTERN: Draft all sections, elicit at phase boundary**

Process all sections:
  1. Draft ALL sections (no intermediate elicitation)
  2. Save complete document
  3. At phase completion, present comprehensive review elicitation
  4. User reviews entire document and provides feedback
  5. Apply changes if needed

**Note**: Batch mode elicitation happens at phase boundaries, not section boundaries

### YOLO Mode (operation_mode == "yolo")
**ALLOWED PATTERN: Skip all elicitation**

Process all sections:
  1. Draft ALL sections without elicitation
  2. Save complete document immediately
  3. No user interaction required
  4. Log decisions for audit trail

**Note**: YOLO mode bypasses all elicitation requirements

## Processing Flow

1. **Parse YAML template** - Load template metadata and sections
2. **Set preferences** - Show current mode, confirm output file
3. **Detect Operation Mode** - Read workflow.json operation_mode
4. **Select Processing Pattern**:
   - If interactive: Use section-by-section pattern
   - If batch: Use complete-document-then-review pattern
   - If yolo: Use no-elicitation pattern
5. **Execute Selected Pattern** - Follow mode-specific instructions above
6. **Continue until complete**

## Detailed Rationale Requirements

When presenting section content, ALWAYS include rationale that explains:

- Trade-offs and choices made (what was chosen over alternatives and why)
- Key assumptions made during drafting
- Interesting or questionable decisions that need user attention
- Areas that might need validation

## Elicitation Results Flow

After user selects elicitation method (2-9):

1. Execute method from .codex/data/elicitation-methods.md via advanced-elicitation.md
2. Present results with insights
3. Offer options:
   - **1. Apply changes and update section**
   - **2. Return to elicitation menu**
   - **3. Ask any questions or engage further with this elicitation**

## Agent Permissions

When processing sections with agent permission fields:

- **owner**: Note which agent role initially creates/populates the section
- **editors**: List agent roles allowed to modify the section
- **readonly**: Mark sections that cannot be modified after creation

**For sections with restricted access:**

- Include a note in the generated document indicating the responsible agent
- Example: "_(This section is owned by dev-agent and can only be modified by dev-agent)_"

## YOLO Mode

User can type `#yolo` to toggle to YOLO mode (process all sections at once).

## CRITICAL REMINDERS

**❌ NEVER:**

- Ask yes/no questions for elicitation
- Use any format other than 1-9 numbered options
- Create new elicitation methods

**✅ ALWAYS:**

- Use exact 1-9 format when elicit: true
- Select options 2-9 from .codex/data/elicitation-methods.md only (8 methods total)
- Use .codex/tasks/advanced-elicitation.md for intelligent method selection
- Provide detailed rationale explaining decisions
- End with "Select 1-9 or just type your question/feedback:"

## CODEX Integration Notes

- Templates located in .codex/templates/
- Elicitation methods in .codex/data/elicitation-methods.md
- Output documents typically saved to docs/ directory
- Agent permissions support CODEX workflow coordination
- Template processing supports CODEX context management