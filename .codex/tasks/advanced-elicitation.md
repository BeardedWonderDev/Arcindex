<!-- Powered by CODEX™ Core -->

# Advanced Elicitation Task

## Purpose

- Provide optional reflective and brainstorming actions to enhance content quality
- Enable deeper exploration of ideas through structured elicitation techniques
- Support iterative refinement through multiple analytical perspectives
- Usable during template-driven document creation or any chat conversation
- Enforce mandatory elicitation at workflow phase transitions when configured

## Usage Scenarios

### Scenario 1: Template Document Creation

After outputting a section during document creation:

1. **Section Review**: Ask user to review the drafted section
2. **Offer Elicitation**: Present 9 carefully selected elicitation methods
3. **Simple Selection**: User types a number (1-9) to engage method, where 1 is to proceed
4. **Execute & Loop**: Apply selected method, then re-offer choices until user proceeds

### Scenario 2: General Chat Elicitation

User can request advanced elicitation on any agent output:

- User says "do advanced elicitation" or similar
- Agent selects 9 relevant methods for the context
- Same simple 1-9 selection process

### Scenario 3: Workflow Phase Transition (CODEX Mandatory)

When workflow state shows elicitation_required for current phase:

- **HARD STOP**: Cannot proceed without elicitation completion
- Present elicitation options with phase-specific context
- Record selection in workflow.json elicitation_history
- Update elicitation_completed[phase] = true

### Mode-Based Elicitation Behavior

**Before Presenting Elicitation:**

1. **Read Operation Mode**: Check `.codex/state/workflow.json` operation_mode
2. **Mode-Specific Behavior**:

   **Interactive Mode**:
   - Present 1-9 elicitation menu after EACH section
   - Wait for user response before continuing
   - This is the DEFAULT and RECOMMENDED mode

   **Batch Mode**:
   - Skip section-level elicitation
   - Accumulate for end-of-phase review
   - Present comprehensive review at phase completion

   **YOLO Mode**:
   - Skip ALL elicitation
   - Log decisions for audit trail
   - Continue processing without user interaction

3. **Mode Validation**: Ensure elicitation timing matches operation_mode

## Task Instructions

### 1. Intelligent Method Selection

**Context Analysis**: Before presenting options, analyze:

- **Content Type**: Technical specs, user stories, architecture, requirements, PRPs
- **Complexity Level**: Simple, moderate, or complex content
- **Stakeholder Needs**: Who will use this information
- **Risk Level**: High-impact decisions vs routine items
- **Creative Potential**: Opportunities for innovation or alternatives
- **Workflow Phase**: Current CODEX workflow phase if active

**Method Selection Strategy**:

1. **Always Include Core Methods** (choose 3-4):
   - Expand or Contract for Audience
   - Critique and Refine
   - Identify Potential Risks
   - Assess Alignment with Goals

2. **Context-Specific Methods** (choose 4-5):
   - **Technical Content**: Tree of Thoughts, ReWOO, Meta-Prompting
   - **User-Facing Content**: Agile Team Perspective, Stakeholder Roundtable
   - **Creative Content**: Innovation Tournament, Escape Room Challenge
   - **Strategic Content**: Red Team vs Blue Team, Hindsight Reflection
   - **PRP/Workflow Content**: Self-Consistency, Chain of Verification, Multi-Agent Debate

3. **Always Include**: "Proceed / No Further Actions" as option 1

### 2. Section Context and Review

When invoked after outputting a section:

1. **Provide Context Summary**: Give a brief 1-2 sentence summary of what the user should look for in the section just presented

2. **Explain Visual Elements**: If the section contains diagrams, explain them briefly before offering elicitation options

3. **Clarify Scope Options**: If the section contains multiple distinct items, inform the user they can apply elicitation actions to:
   - The entire section as a whole
   - Individual items within the section (specify which item when selecting an action)

### 3. Present Elicitation Options

**Review Request Process:**

- Ask the user to review the drafted section
- In the SAME message, inform them they can suggest direct changes OR select an elicitation method
- Present 9 intelligently selected methods (1-9) where "Proceed" is option 1
- Keep descriptions short - just the method name
- Await simple numeric selection

**Action List Presentation Format:**

```text
**Advanced Elicitation Options**
Select 1-9 or type your feedback:

1. Proceed to next section
2. [Method Name]
3. [Method Name]
4. [Method Name]
5. [Method Name]
6. [Method Name]
7. [Method Name]
8. [Method Name]
9. [Method Name]
```

**Response Handling:**

- **Numbers 2-9**: Execute the selected method, then re-offer the choice
- **Number 1**: Proceed to next section or continue conversation
- **Direct Feedback**: Apply user's suggested changes and continue

### 4. Method Execution Framework

**Execution Process:**

1. **Retrieve Method**: Access the specific elicitation method from .codex/data/elicitation-methods.md
2. **Apply Context**: Execute the method from your current role's perspective
3. **Provide Results**: Deliver insights, critiques, or alternatives relevant to the content
4. **Re-offer Choice**: Present the same 9 options again until user selects 9 or gives direct feedback

**Execution Guidelines:**

- **Be Concise**: Focus on actionable insights, not lengthy explanations
- **Stay Relevant**: Tie all elicitation back to the specific content being analyzed
- **Identify Personas**: For multi-persona methods, clearly identify which viewpoint is speaking
- **Maintain Flow**: Keep the process moving efficiently

### 5. CODEX Workflow Integration

**Workflow State Tracking:**

When operating within a CODEX workflow:

1. **Check State**: Read .codex/state/workflow.json for elicitation_required
2. **Enforce Gates**: Block progression if elicitation_completed[phase] = false
3. **Record History**: Log all selections to elicitation_history array
4. **Update Status**: Set elicitation_completed[phase] = true when done

**Violation Detection:**

- If attempting to skip elicitation when required, show:
  "⚠️ VIOLATION INDICATOR: Elicitation required for [phase] phase before proceeding"
- Log violation to .codex/debug-log.md
- HALT workflow until elicitation completed

## CRITICAL ENFORCEMENT

**❌ NEVER:**
- Skip elicitation when workflow state requires it
- Allow phase progression without elicitation completion
- Create new elicitation methods not in .codex/data/elicitation-methods.md

**✅ ALWAYS:**
- Use exact 1-9 format when presenting options
- Record all elicitation interactions in workflow state
- Enforce HARD STOPS at phase boundaries when configured
- Reference methods from .codex/data/elicitation-methods.md only