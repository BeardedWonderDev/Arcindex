# CODEX Workflow Guide

## 🚀 Quick Start

CODEX orchestrates complete development workflows with mandatory user interaction at strategic decision points. This guide explains how to use CODEX effectively with its elicitation enforcement system.

### Starting a New Project

```bash
/codex start greenfield-swift "MyAwesomeApp"
```

Or without a project name (you'll be prompted):
```bash
/codex start greenfield-swift
```

### Available Workflows

- **greenfield-swift**: New Swift/iOS application from scratch
- **greenfield-generic**: Language-agnostic workflow for any programming language
- **brownfield-enhancement**: Add features to existing projects
- **health-check**: Validate project health and quality

## 📋 The CODEX Workflow Process

### Phase 1: Discovery

When you start a new workflow, CODEX begins with discovery:

1. **Questions Asked**:
   - Project name/working title
   - Brief project concept (what you're building)
   - Existing inputs (research, brainstorming, or starting fresh)

2. **Discovery Elicitation** (NEW):
   After answering questions, you'll see:
   - A summary of your answers
   - A 1-9 menu of elicitation options
   - You MUST select an option before proceeding

   Example:
   ```
   Discovery Summary:
   - Project: MyAwesomeApp
   - Concept: A todo list app with AI suggestions
   - Starting: Fresh project

   Select 1-9 or type your feedback:
   1. Proceed to next section
   2. Expand or Contract for Audience
   3. Critique and Refine
   4. Identify Potential Risks
   5. Challenge from Critical Perspective
   6. Tree of Thoughts Deep Dive
   7. Stakeholder Round Table
   8. Innovation Tournament
   9. Red Team vs Blue Team
   ```

### Phase 2: Business Analysis

After discovery validation, CODEX transforms into the Business Analyst:

1. **Automatic Transformation**:
   - "📊 Transforming into Business Analyst..."
   - Uses discovery context from Phase 1
   - Creates project brief document

2. **Section-by-Section Elicitation**:
   For each section marked with `elicit: true`:
   - Section content is presented
   - Detailed rationale provided
   - 1-9 elicitation menu appears
   - You must interact before continuing

### Phase 3: Product Management

The PM phase creates detailed requirements:

1. **PRD Creation**:
   - Based on approved project brief
   - User stories and acceptance criteria
   - Technical requirements

2. **Elicitation Points**:
   - Feature prioritization
   - User story refinement
   - Acceptance criteria validation

### Phase 4: Architecture

The Architect designs the technical solution:

1. **Architecture Document**:
   - System design and patterns
   - Technology stack decisions
   - Integration points

2. **Elicitation Focus**:
   - Technology choices
   - Scalability considerations
   - Security architecture

### Phase 5: PRP Creation

Enhanced PRP for implementation readiness:

1. **PRP Generation**:
   - Zero-knowledge validation
   - Implementation blueprint
   - Validation commands

## 🎯 Operation Modes

CODEX supports three operation modes that control elicitation behavior:

### Interactive Mode (Default)
```bash
/codex interactive
```
- Full elicitation at every marked point
- Maximum user control and quality
- Best for critical projects

### Batch Mode
```bash
/codex batch
```
- Collects elicitation at phase boundaries
- Reduces interruptions
- Good for experienced users

### YOLO Mode
```bash
/codex yolo
```
- Skips all elicitation prompts
- Still logs decisions
- Use with caution - reduced quality assurance

### Check Current Mode
```bash
/codex mode
```

## 🛡️ Elicitation Enforcement System

### What is Elicitation?

Elicitation ensures human expertise guides AI at critical decision points. When you see a 1-9 menu, the system is requesting your input to:

- Validate AI-generated content
- Provide domain expertise
- Make strategic decisions
- Catch potential issues early

### The 1-9 Menu Format

Every elicitation menu follows this pattern:

1. **Option 1**: Always "Proceed to next section"
2. **Options 2-9**: Context-specific elicitation methods

Example methods:
- **Expand or Contract**: Adjust detail level for your audience
- **Critique and Refine**: Review for improvements
- **Identify Risks**: Spot potential problems
- **Tree of Thoughts**: Deep exploration of alternatives

### Responding to Elicitation

You have three ways to respond:

1. **Type a number (1-9)**: Select a specific elicitation method
2. **Type feedback**: Provide direct changes or questions
3. **Type #yolo**: Switch to YOLO mode (bypass all future elicitation)

### Why Can't I Skip Elicitation?

In Interactive mode, elicitation is mandatory because:

- **Quality Assurance**: Human validation improves output quality
- **Strategic Alignment**: Your decisions guide the project direction
- **Error Prevention**: Catches issues before they compound
- **Context Preservation**: Ensures AI understands your specific needs

## 📊 Workflow State Management

CODEX maintains persistent state throughout your workflow:

### State Location
```
.codex/state/runtime/workflow.json
```

### View Current State
```bash
/codex state
```

### State Tracking Includes
- Current phase and progress
- Elicitation completion status
- Document creation history
- Validation results
- Operation mode

## 🔧 Common Commands

### Workflow Management
```bash
/codex start [workflow]     # Start new workflow
/codex continue            # Resume from checkpoint
/codex status             # Show current progress
/codex validate           # Run validation gates
/codex rollback           # Revert to previous checkpoint
```

### System Commands
```bash
/codex help               # Show all commands
/codex workflows          # List available workflows
/codex agents            # Show specialized agents
/codex config            # View configuration
/codex exit              # Exit CODEX
```

## ⚠️ Validation Gates

CODEX uses a 5-level validation system:

### Level 0: Elicitation Validation (Highest Priority)
- Ensures required elicitation is complete
- Blocks all progression until satisfied
- Cannot be bypassed in Interactive mode

### Level 1-4: Technical Validation
- Syntax and style checks
- Unit testing
- Integration testing
- Domain-specific validation

## 🚨 Troubleshooting

### "Elicitation required for [phase] before proceeding"

**Cause**: You haven't completed elicitation for the current phase.

**Solution**:
1. Review the presented content
2. Select from the 1-9 menu
3. Or type `#yolo` to switch to YOLO mode

### "No active workflow found"

**Cause**: No workflow has been started or state was lost.

**Solution**:
```bash
/codex start [workflow-type] [project-name]
```

### Multiple Greeting Messages

**Cause**: Workflow not properly initialized.

**Solution**:
- Ensure you use the correct command format
- Include project name in initial command when possible

### Documents Not Saved

**Cause**: Workflow interrupted before completion.

**Solution**:
```bash
/codex continue  # Resume workflow
/codex validate  # Check validation status
```

## 💡 Best Practices

### 1. Start with Clear Intent
Provide comprehensive answers during discovery to get better results.

### 2. Use Elicitation Thoughtfully
- Option 1 (Proceed) when content looks good
- Options 2-9 when you want refinement
- Direct feedback for specific changes

### 3. Choose the Right Mode
- **Interactive**: New projects, critical features
- **Batch**: Routine enhancements, familiar patterns
- **YOLO**: Prototypes, experiments

### 4. Save Progress Regularly
CODEX auto-saves state, but you can create git commits:
```bash
git add .
git commit -m "CODEX checkpoint: [phase] complete"
```

### 5. Review Generated Documents
Documents are saved to `docs/` directory:
- `project-brief.md`
- `prd.md`
- `architecture.md`
- `prp.md`

## 🎓 Example Workflow Walkthroughs

### Starting a New iOS App (greenfield-swift)

1. **Initiate Workflow**:
   ```bash
   /codex start greenfield-swift "WeatherApp"
   ```

2. **Answer Discovery Questions**:
   - Concept: "A weather app with AI predictions"
   - Inputs: "Starting fresh"

3. **Complete Discovery Elicitation**:
   - Review summary
   - Select "4. Identify Potential Risks"
   - Discuss API limitations
   - Select "1. Proceed to next section"

4. **Business Analysis Phase**:
   - System transforms to analyst
   - Creates project brief
   - Each section requires elicitation

5. **Continue Through Phases**:
   - Complete each phase with elicitation
   - Documents created automatically
   - State tracked throughout

6. **Implementation Ready**:
   - PRP document contains complete blueprint
   - All decisions documented
   - Ready for development

### Starting a Generic Language Project (greenfield-generic)

The greenfield-generic workflow supports any programming language (JavaScript, Python, Go, Rust, etc.).

1. **Initiate Workflow**:
   ```bash
   /codex start greenfield-generic "MyPythonAPI"
   ```

2. **Language Configuration**:
   During discovery, you'll specify:
   - Primary language (e.g., "python")
   - Framework (e.g., "django", "flask")
   - Build commands for your toolchain
   - Test commands for your environment

3. **Custom Validation**:
   The workflow adapts to your language:
   - JavaScript: `npm test`, `eslint`, `prettier`
   - Python: `pytest`, `flake8`, `black`
   - Go: `go test`, `golangci-lint`, `gofmt`
   - Rust: `cargo test`, `cargo clippy`, `rustfmt`

4. **Same Phases, Different Tools**:
   - Discovery → Business Analysis → PM → Architecture → PRP
   - Each phase works identically to greenfield-swift
   - Validation commands adapt to your language

5. **Example Language Configurations**:
   - **Python/Django**: pytest, flake8, black, mypy
   - **JavaScript/React**: jest, eslint, prettier, npm build
   - **Go/Gin**: go test, golangci-lint, go build
   - **Rust/Actix**: cargo test, clippy, rustfmt

## 🔄 Resuming Work

If your session is interrupted:

1. **Check Status**:
   ```bash
   /codex status
   ```

2. **Continue Workflow**:
   ```bash
   /codex continue
   ```

3. **Validation Ensures Completeness**:
   - System checks elicitation status
   - Resumes from last checkpoint
   - No work is lost

## 📚 Advanced Features

### Parallel Agent Execution
CODEX can coordinate multiple specialized agents for complex tasks.

### Context Breakpoints
Manages token limits by creating strategic checkpoints.

### Git Integration
Can create commits at phase boundaries (if configured).

### Custom Workflows
Extensible system allows custom workflow definitions.

## 🤝 Getting Help

### In-Session Help
```bash
/codex help
```

### Report Issues
Create an issue at your project repository with:
- Workflow type used
- Phase where issue occurred
- Error messages
- Current state (`/codex state`)

## 🎯 Summary

CODEX transforms AI-assisted development through:

1. **Structured Workflows**: Systematic progression through phases
2. **Mandatory Elicitation**: Human expertise at critical points
3. **State Management**: Persistent tracking and recovery
4. **Quality Gates**: Multi-level validation system
5. **Flexible Modes**: Balance between control and efficiency

The elicitation enforcement ensures your expertise guides the AI, resulting in higher quality outputs that match your specific needs.

---

*Remember: Elicitation isn't a barrier—it's your opportunity to ensure the AI understands and implements your vision correctly.*