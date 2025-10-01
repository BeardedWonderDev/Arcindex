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

1. **Draft FULL section content**
   - Create the COMPLETE markdown/text for this section
   - This is the actual content that will be saved to the file
   - NOT a summary, NOT a description, the ACTUAL content

2. **Present FULL content to user**
   - Show the ENTIRE drafted section
   - User should see exactly what will be in the file
   - Include all text, formatting, structure

   **EXAMPLE OF CORRECT PRESENTATION**:
   ```
   I've drafted Section 2: User Roles. Here's the complete content:

   ---
   ## User Roles & Permissions

   ### Dealer Admin

   **Responsibilities:**
   - System configuration and settings management
   - User account creation across all locations
   - Role and permission customization
   - Global inventory oversight and reporting

   **System Access:**
   - Full CRUD permissions on all resources
   - Can create custom roles and modify permission matrices
   - Access to all locations and equipment records
   ...

   [COMPLETE SECTION CONTENT - ALL TEXT]
   ---

   **Rationale:** I structured roles hierarchically starting with highest privilege...

   [ELICITATION MENU]
   ```

   **WRONG - VIOLATION EXAMPLES**:
   ❌ "Section 2 includes: Role definitions, Personas, Workflows"
   ❌ "What's Included: 2.1 Dealer Admin role, 2.2 Store Manager role..."
   ❌ "Key Insights: 6 roles defined with CRUD permissions"

3. **Provide detailed rationale** - AFTER showing full content
4. **Add 1-2 sentence context note** - What to review
5. **STOP and present numbered options 1-9:**
   - **MANDATORY**: Use `.codex/tasks/advanced-elicitation.md` to generate the menu
   - **NEVER** create custom elicitation menus
   - **VALIDATION**: Option 1 MUST ALWAYS be "Proceed to next section"
   - **VALIDATION**: Options 2-9 MUST be methods from `.codex/data/elicitation-methods.md`
   - **ENFORCEMENT**: Any menu where option 9 = "Proceed" is a VIOLATION
   - **ENFORCEMENT**: Any menu where option 8 = "Proceed" is a VIOLATION
   - End with: "Select 1-9 or just type your question/feedback:"
6. **WAIT FOR USER RESPONSE** - Do not proceed until user selects option or provides feedback

**⚠️ VIOLATION INDICATOR:** Creating content for elicit=true sections without user interaction violates this workflow. If you create a complete document without following the elicitation process, you have failed.

**NEVER ask yes/no questions or use any other format.**

## Mode-Aware Processing

**CRITICAL: Check operation_mode BEFORE beginning section processing**

1. Read `.codex/state/workflow.json`
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
2. **CRITICAL: Extract output_file path** - Get the SINGLE output file from template
   - Template specifies output_file: "docs/project-brief.md"
   - This is the ONLY file that will be created
   - ALL sections save to this ONE file
3. **Initialize output file** - Create empty file at output_file path
4. **Confirm with user** - "Creating document at: {output_file}"
5. **Detect Operation Mode** - Read workflow.json operation_mode
6. **Select Processing Pattern** - Based on mode (interactive/batch/yolo)
7. **For EACH section**:
   - Draft section content
   - Present content + rationale
   - IF elicit: true → Present 1-9 menu via advanced-elicitation.md
   - **MANDATORY: Append section to output_file** (not a new file!)
   - Verify save succeeded
8. **Continue until complete**
9. **Final verification** - Read output_file to confirm all sections present

## Detailed Rationale Requirements

When presenting section content, ALWAYS include rationale that explains:

- Trade-offs and choices made (what was chosen over alternatives and why)
- Key assumptions made during drafting
- Interesting or questionable decisions that need user attention
- Areas that might need validation

## CRITICAL: Single File Output Enforcement

**RULE**: The template specifies ONE output_file. ALL sections MUST save to this file.

**Process**:
1. **First section**: Use Write tool to CREATE file with section content
2. **All subsequent sections**: Use Edit tool to APPEND to existing file
3. **After EVERY section**:
   - Verify Write/Edit tool reported success
   - Log: "✅ Section '{section_name}' appended to {output_file}"
4. **NEVER**:
   - Create separate files for each section (e.g., section-1.md, section-2.md)
   - Save to different locations than output_file specifies
   - Skip file operations

**VIOLATION INDICATORS**:
- ❌ Creating files like: docs/section-1.md, docs/section-2.md, docs/section-3.md
- ❌ Saying "I'll save this section" without actually using Write/Edit tool
- ✅ CORRECT: All sections in docs/project-brief.md (single file)

**ENFORCEMENT**:
- Before moving to next section, you MUST have used Write or Edit tool
- The tool call must have succeeded
- The content must be in the output_file specified in template

## Elicitation Results Flow

After user selects elicitation method (2-9):

1. Execute method from .codex/data/elicitation-methods.md via advanced-elicitation.md
2. Present results with insights
3. Offer options:
   - **1. Apply changes and update section**
   - **2. Return to elicitation menu**
   - **3. Ask any questions or engage further with this elicitation**

## Section Completion Checkpoint (MANDATORY)

**Before proceeding to next section, verify ALL steps completed:**

**Checklist:**
- [ ] Section content drafted
- [ ] Full content presented to user (not summary)
- [ ] Rationale provided
- [ ] Elicitation menu shown (if elicit: true)
- [ ] User selected option 1 (Proceed) or provided feedback
- [ ] **FILE SAVED**: Used Write or Edit tool to save section
- [ ] **SAVE VERIFIED**: Tool confirmed success
- [ ] **CONTENT IN FILE**: Section now exists in output_file

**MANDATORY QUESTIONS** (answer YES to all):
1. Did I draft the complete section content?
2. Did I present the FULL content to user (not "What's Included" summary)?
3. Did I use Write (first section) or Edit (subsequent) tool?
4. Did the tool report successful save?
5. Is this section now in the output_file?

**IF ANY ANSWER IS NO**: HALT - Complete missing step

**ENFORCEMENT**:
- Cannot say "Moving to Section 2..." without having saved Section 1
- Cannot proceed without file operation completing
- Must use actual Write/Edit tools, not just mention saving

**VIOLATION EXAMPLE**:
❌ "Section 1 complete. Proceeding to Section 2..." (without having called Write/Edit tool)
✅ CORRECT: "Section 1 drafted. [Uses Write tool] ✅ Saved to docs/project-brief.md. Proceeding to Section 2..."

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