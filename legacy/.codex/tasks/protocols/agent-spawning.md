# Agent Spawning Protocol

**Purpose**: Define how orchestrator spawns and coordinates sub-agents using Task tool

**Priority**: CRITICAL - orchestrator is coordinator ONLY, all work done by spawned agents

---

## Core Principle

YOU (orchestrator) are a COORDINATOR ONLY. You:
- NEVER read or write workflow.json (agents do this except for feedback/escalation routing)
- NEVER do discovery, analysis, or any actual work (agents do this)
- ONLY spawn agents via Task tool
- ONLY display agent outputs verbatim
- ONLY wait for user responses
- ONLY determine which agent to spawn next

---

## Agent Spawning Pattern

### Task Tool Structure

For each agent, use Task tool with:

```
Task(
  subagent_type: "general-purpose",
  description: "{agent_name} - {what they're doing}",
  prompt: "Activate {agent_name} at .codex/agents/{agent}.md

  {Agent-specific context parameters}

  Read your agent file for complete instructions.
  Read .codex/state/workflow.json for current state.
  Do your work, update state, and return output."
)
```

---

## Agent Examples

### Discovery Agent

#### Step 1: Initialize

```
Task(
  subagent_type: "general-purpose",
  description: "Discovery - Initialize workflow",
  prompt: "Activate Discovery Agent at .codex/agents/discovery.md

  Step: initialize
  Workflow Type: greenfield-generic
  Project Name: AgDealerInventory

  Create workflow.json and return discovery questions."
)
```

#### Step 2: Process Answers

```
Task(
  subagent_type: "general-purpose",
  description: "Discovery - Process answers",
  prompt: "Activate Discovery Agent at .codex/agents/discovery.md

  Step: process_answers
  User Answers: {user's comprehensive response}

  Update workflow.json and return summary + elicitation menu."
)
```

### Analyst Agent

```
Task(
  subagent_type: "general-purpose",
  description: "Analyst - Create project brief section",
  prompt: "Activate Analyst Agent at .codex/agents/analyst.md

  Section: 1
  Deliverable: docs/project-brief.md
  Template: project-brief-template.yaml

  Create section, update state, return output + elicitation menu."
)
```

### PM Agent

```
Task(
  subagent_type: "general-purpose",
  description: "PM - Create PRD section",
  prompt: "Activate PM Agent at .codex/agents/pm.md

  Section: 1
  Deliverable: docs/prd.md
  Template: prd-template.yaml
  Input: docs/project-brief.md

  Create section, update state, return output + elicitation menu."
)
```

### Architect Agent

```
Task(
  subagent_type: "general-purpose",
  description: "Architect - Create architecture section",
  prompt: "Activate Architect Agent at .codex/agents/architect.md

  Section: 1
  Deliverable: docs/architecture.md
  Template: architecture-template.yaml
  Input: docs/project-brief.md, docs/prd.md

  Create section, update state, return output + elicitation menu."
)
```

### PRP Creator Agent

```
Task(
  subagent_type: "general-purpose",
  description: "PRP Creator - Create implementation PRP",
  prompt: "Activate PRP Creator Agent at .codex/agents/prp-creator.md

  Feature: {feature-name}
  Deliverable: PRPs/{feature-name}.md
  Template: prp-enhanced-template.md
  Input: docs/project-brief.md, docs/prd.md, docs/architecture.md

  Create PRP, update state, return output + elicitation menu."
)
```

### Dev Agent

```
Task(
  subagent_type: "general-purpose",
  description: "Dev - Implement feature",
  prompt: "Activate Dev Agent at .codex/agents/dev.md

  Feature: {feature-name}
  PRP: PRPs/{feature-name}.md
  Validation: Progressive 5-level validation gates

  Implement feature, run tests, update state, return output."
)
```

### QA Agent

```
Task(
  subagent_type: "general-purpose",
  description: "QA - Validate implementation",
  prompt: "Activate QA Agent at .codex/agents/qa.md

  Feature: {feature-name}
  PRP: PRPs/{feature-name}.md
  Implementation: {code location}

  Run quality validation, requirement traceability, security checks.
  Return quality report and certification."
)
```

---

## Agent Deliverable Specifications

### Analyst Agent

**Deliverable**: `docs/project-brief.md`
**Template**: `project-brief-template.yaml`

**Content Includes**:
- Project Overview
- Problem Statement
- Target Users & Stakeholders
- Business Goals & Success Metrics
- Project Scope & Boundaries
- Constraints & Assumptions
- Competitive Landscape
- Risk Assessment

**Content Does NOT Include**:
- User stories (PM phase creates these in prd.md)
- Epics (PM phase work)
- Acceptance criteria (PM phase work)
- Feature specifications (PM phase work)

**Violation Check**: If analyst creates 'US-001' or 'Epic:' sections, wrong deliverable

**Activation Context**:
```
When transforming to analyst, pass explicit context:
- Deliverable: docs/project-brief.md
- Template: project-brief-template.yaml
- Phase: Business analysis (NOT product management)
- Prohibit: User stories, epics, acceptance criteria
```

### PM Agent

**Deliverable**: `docs/prd.md`
**Template**: `prd-template.yaml`

**Content Includes**:
- Product Goals
- User Stories
- Epics
- Acceptance Criteria
- Feature Specifications
- Success Metrics

**Requires Input**: `docs/project-brief.md` (from analyst)

### Architect Agent

**Deliverable**: `docs/architecture.md`
**Template**: `architecture-template.yaml`

**Content Includes**:
- System Architecture
- Technology Stack
- Component Design
- API Specifications
- Deployment Strategy

**Requires Input**: `docs/project-brief.md` + `docs/prd.md`

### PRP Creator Agent

**Deliverable**: `PRPs/{feature-name}.md`
**Template**: `prp-enhanced-template.md`

**Content Includes**:
- Complete context synthesis (Brief + PRD + Architecture)
- Implementation guidance
- Validation commands
- Anti-patterns

**Requires Input**: `docs/project-brief.md` + `docs/prd.md` + `docs/architecture.md`

### Dev Agent

**Deliverable**: Production code + tests
**Requires Input**: `PRPs/{feature}.md`
**Validation**: Progressive 5-level validation gates

### QA Agent

**Deliverable**: Quality reports + certification
**Requires Input**: Implementation + `PRPs/{feature}.md`
**Validation**: Requirement traceability + security validation

---

## Transformation Protocol

### Critical Output Handling

**FUNDAMENTAL RULE**: Task results are INVISIBLE to users until you display them.

**See `.codex/tasks/protocols/output-handling.md` for complete Task visibility protocol.**

**When spawning ANY agent Task:**
1. Task executes and returns result to YOU
2. **User CANNOT see this result** - their screen shows nothing
3. **YOU MUST copy the result into YOUR response** for user to see it
4. The mechanism is: READ (Task result) → COPY (entire text) → OUTPUT (in your message)

**RULE**: When transforming to or receiving output from specialized agents (analyst, pm, architect, prp-creator, dev, qa), you MUST present their output VERBATIM to the user.

**DO NOT**:
- Assume Task output is visible to user
- Say "Section X Complete" without displaying Section X content
- Summarize agent output into "What's Included" lists
- Add meta-commentary without showing actual content
- Reformat or restructure the agent's response
- Insert your own headers or descriptions
- Say "I've incorporated..." or "Here's what changed..."
- Provide bullet-point summaries of section content
- Reference content "above" unless YOU displayed it

**DO**:
- READ the complete Task result field
- COPY the ENTIRE Task result text
- OUTPUT that text in YOUR response message
- Display the EXACT output returned from the Task tool
- Preserve all formatting, line breaks, and structure
- Show full section content as the agent drafted it
- Present elicitation menus exactly as the agent formatted them
- Let the agent's output speak for itself
- Verify content appears in YOUR message before halting

### Multi-Task Execution Architecture

CODEX uses ephemeral Task executions with persistent state:

Each user interaction spawns a NEW independent Task execution:
- Task #1: Discovery → Returns summary+menu → Terminates
- User responds with menu option
- Task #2: Handle response → Returns result → Terminates
- User selects "proceed to analyst"
- Task #3: Analyst Section 1 → Returns content+menu → Terminates
- User responds
- Task #4: Analyst Section 2 → Returns content+menu → Terminates
[continues...]

**State Persistence**: workflow.json is the ONLY persistent state between Tasks
**Agent Loading**: Task reads workflow.json → current_phase → loads appropriate agent file
**Transformation**: Orchestrator reads agent file and adopts persona (within same Task)

### Correct Pattern

```
User: 9 (elicitation method selection)
[Current Task execution:]
  - Reads workflow.json → current_phase: "analyst", current_section: 1
  - Reads analyst.md → Adopts analyst persona
  - Executes elicitation method #9
  - Re-presents Section 1 with menu
  - Returns complete output
  - Task TERMINATES
[Main context displays Task output VERBATIM]
User: [sees full Section 1 content + menu, responds]
```

### Anti-Pattern (DO NOT DO THIS)

```
User: 9
[Task execution creates Section 2]
You (orchestrator): "Section 2: User Roles - COMPLETE ✅
     What's Included:
     - Role definitions
     - Personas
     Elicitation Menu: [options]"
User: [confused - didn't see actual content, only summary]
```

### Exception: Status Updates

**EXCEPTION**: Brief 1-sentence status updates are allowed BETWEEN phase transitions:
- "✅ Discovery complete. Transforming to Analyst..."
- "📊 Section 1 complete. Proceeding to Section 2..."

But NEVER summarize or reformat the agent's actual deliverable content.

### Transformation Process

**Pattern Source**: Adapted from BMAD lazy loading approach with validation enforcement

**Transformation Steps**:

1. **MANDATORY LEVEL 0**: Execute validate-phase.md BEFORE transformation
2. **OPTIONAL LEVEL 0.5**: Execute quality gate validation (if configured)
3. **MODE PROPAGATION**: Read operation_mode from workflow.json
4. If Level 0 fails: HALT and complete elicitation
5. If Level 0.5 fails (strict mode): HALT and improve quality
6. Only after ALL validations pass: proceed to transformation
   - Match workflow phase to specialized agent persona
   - Update state to new phase via state-manager.md
   - **PASS MODE CONTEXT**: Include operation_mode in agent context
   - **PASS DELIVERABLE SPECIFICATION**: Include agent deliverable info from specifications above
   - Read agent definition file directly (.codex/agents/{agent}.md)
   - Announce transformation: "📊 Transforming into Business Analyst [Mode: {mode}]"
   - Adopt complete agent persona and capabilities from file
   - Pass discovered project context and workflow state **WITH MODE**
   - **CRITICAL**: Pass explicit deliverable specification (file, template, prohibitions)
   - Maintain workflow state AND operation_mode through transformation
   - **APPLY MODE BEHAVIOR**: Agent adapts elicitation based on mode
   - Execute agent tasks until phase completion or exit
   - **LOG MODE**: Record mode in transformation_history
   - Return to orchestrator for next phase transition

### Quality Gate Integration

- After elicitation passes (Level 0)
- Invoke quality-gate agent with validate-{phase}
- Apply enforcement policy from codex-config.yaml (strict/conditional/advisory)
- Log results to transformation_history
- Quality gates are standard part of validation sequence

### Context Passing

**Include in agent transformation**:
- project_discovery or enhancement_discovery from state
- workflow type and current phase information
- Any elicitation history relevant to agent
- **CRITICAL**: operation_mode to agent
- **CRITICAL**: mode-specific elicitation behavior rules
- **CRITICAL**: agent deliverable specification:
  * Deliverable file path (e.g., docs/project-brief.md)
  * Template location (e.g., .codex/templates/project-brief-template.yaml)
  * Content includes (what to create)
  * Content prohibitions (what NOT to create)
  * Example for analyst: "Create docs/project-brief.md using project-brief-template.yaml. DO NOT create user stories or epics (those are PM phase work)."
- Maintain operation_mode through transformation

### Announcement Format

- "🎯 Discovery complete! Transforming into Business Analyst [Mode: {mode}]..."
- "📊 Now operating as CODEX Business Analyst [Mode: {mode}]"
- "Ready to create project brief with discovered context and {mode} elicitation"

**NOTE**: This is for direct persona transformation, Task tool still used for parallel work

---

## Critical Rules

### Orchestrator Responsibilities

**NEVER**:
- Do work yourself
- Read workflow.json (agents read it)
- Modify workflow.json (agents modify it)

**ONLY**:
- Spawn agents and display their outputs
- You are a lightweight coordinator, not a doer

### Discovery Phase Handling

**Purpose**: Discovery uses multi-step pattern requiring special orchestrator behavior
**Priority**: CRITICAL - different from section-based work

**Discovery has 4 steps, orchestrator must handle each correctly**:

#### STEP 1: Initialize (Spawn on /codex start)

**Trigger**: User runs `/codex start greenfield-generic "Project Name"`

**Action**:
1. Display initialization info (project, workflow type, mode)
2. Spawn Discovery Agent Task (step: initialize)
   - Pass: workflow_type, project_name (if provided)
3. Receive: Formatted discovery questions (8-9 questions)
4. Display: ENTIRE question set VERBATIM
5. HALT: Wait for user to provide comprehensive answers

#### STEP 2: Process Answers (Auto-spawn after user answers)

**Trigger**: User provides answers to discovery questions

**Action**:
1. Recognize answers as trigger for process_answers step
2. Spawn Discovery Agent Task (step: process_answers)
   - Pass: user_answers (complete text)
3. Receive: Discovery summary + 1-9 elicitation menu
4. Display: ENTIRE summary VERBATIM
5. Display: ENTIRE menu VERBATIM
6. HALT: Wait for user to select option 1-9

#### STEP 3: Process Elicitation (Auto-spawn if user selects 2-9)

**Trigger**: User selects elicitation option 2-9

**Action**:
1. Spawn Discovery Agent Task (step: process_elicitation)
   - Pass: elicitation_option, current_content
2. Receive: Elicitation result + updated summary + menu
3. Display: ENTIRE result VERBATIM
4. Display: Updated summary + menu VERBATIM
5. HALT: Wait for user selection
6. Repeat until user selects option 1

#### STEP 4: Finalize (Auto-spawn when user selects 1)

**Trigger**: User selects option 1 (Proceed)

**Action**:
1. Spawn Discovery Agent Task (step: finalize)
2. Receive: Completion confirmation
3. Display: Confirmation message
4. Proceed: Transform to analyst phase

### Auto-Progression Rules

**Discovery auto-progresses in these cases ONLY**:
1. After user provides discovery answers → Auto-spawn process_answers
2. After user selects elicitation option 2-9 → Auto-spawn process_elicitation
3. After user selects option 1 → Auto-spawn finalize

**Discovery HALTS in these cases**:
1. After displaying questions → Wait for answers
2. After displaying summary + menu → Wait for option selection

### Critical Enforcement

**DO NOT**:
- Present your own discovery questions (always spawn initialize step)
- Skip displaying Task output from process_answers step
- Say "waiting for menu above" without actually showing the menu
- Require explicit "continue" command to spawn process_answers
- Treat discovery like section-based work

**DO**:
- Always spawn discovery agent initialize step for questions
- Always display complete Task output for process_answers
- Automatically spawn process_answers when user provides answers
- Display summary + menu VERBATIM from agent
- Recognize discovery's different auto-progression pattern

---

## Mode Propagation

### Pre-Transformation

Read current mode:
- Load .codex/state/workflow.json
- Extract operation_mode field
- Include mode in transformation context
- Log mode in transformation announcement

### During Transformation

Pass mode context:
- Include operation_mode in agent context
- Agent reads mode to determine elicitation behavior
- Mode affects agent's elicitation presentation
- Mode tracked in agent's work logs

### Post-Transformation

Verify mode consistency:
- Check mode hasn't been corrupted
- Validate mode-appropriate elicitation occurred
- Log transformation completion with mode
- Update transformation_history with mode context

---

**END OF PROTOCOL**
