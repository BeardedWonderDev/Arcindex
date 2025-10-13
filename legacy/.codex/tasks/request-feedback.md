# Request Feedback Task

## Purpose

Enable bi-directional feedback between CODEX workflow agents to resolve ambiguities, clarify requirements, and improve document quality through iterative refinement.

## Inputs

```yaml
inputs:
  required:
    from_agent:
      type: string
      description: "Agent initiating the feedback request"
      values: [orchestrator, discovery, analyst, pm, architect, prp-creator, dev, qa]
      example: "architect"

    to_agent:
      type: string
      description: "Agent that should resolve the feedback"
      values: [orchestrator, discovery, analyst, pm, architect, prp-creator, dev, qa]
      example: "pm"
      validation: "from_agent != to_agent"

    issue:
      type: string
      description: "Clear description of ambiguity, question, or issue"
      min_length: 10
      example: "Story 1.3 acceptance criteria unclear - 'real-time' undefined. Need specific latency requirement."

    context:
      type: object
      description: "Context information for locating and understanding the issue"
      fields:
        document:
          type: string
          required: true
          example: "docs/prd.md"
        section:
          type: string
          required: false
          example: "User Stories → Epic 1 → Story 1.3"
        line_refs:
          type: array
          required: false
          example: [42, 43, 44]
        quote:
          type: string
          required: false
          example: "The system shall provide real-time updates"

  optional:
    priority:
      type: string
      default: "medium"
      values: [high, medium, low]
      description: "Priority level for resolution"
```

## Prerequisites

```yaml
prerequisites:
  - Workflow state exists (.codex/state/workflow.json)
  - Referenced document exists and is accessible
  - Issue is specific and actionable (not vague)
  - Agent has genuine need for clarification
```

## Workflow Steps

### Step 1: Validate Feedback Request

```bash
# Verify required fields are present
echo "🔍 Validating feedback request..."

# Check from_agent and to_agent are different
if [ "$FROM_AGENT" == "$TO_AGENT" ]; then
    echo "❌ ERROR: Cannot request feedback from yourself"
    exit 1
fi

# Check document exists
if [ ! -f "$CONTEXT_DOCUMENT" ]; then
    echo "❌ ERROR: Referenced document not found: $CONTEXT_DOCUMENT"
    exit 1
fi

# Check issue is not empty or too vague
ISSUE_LENGTH=${#ISSUE}
if [ $ISSUE_LENGTH -lt 10 ]; then
    echo "❌ ERROR: Issue description too vague (must be at least 10 characters)"
    exit 1
fi

echo "✅ Feedback request validation passed"
```

### Step 2: Generate Feedback ID

```bash
# Generate unique feedback ID using timestamp
FEEDBACK_ID="fb-$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"

echo "📝 Generated feedback ID: $FEEDBACK_ID"
```

### Step 3: Create Feedback Object

```bash
# Load feedback request template
TEMPLATE=$(cat .codex/data/feedback-request-template.yaml)

# Create feedback object (JSON for workflow.json)
FEEDBACK_OBJECT=$(cat <<EOF
{
  "id": "$FEEDBACK_ID",
  "from_agent": "$FROM_AGENT",
  "to_agent": "$TO_AGENT",
  "issue": "$ISSUE",
  "context": {
    "document": "$CONTEXT_DOCUMENT",
    "section": "${CONTEXT_SECTION:-null}",
    "line_refs": ${CONTEXT_LINE_REFS:-null},
    "quote": "${CONTEXT_QUOTE:-null}"
  },
  "status": "pending",
  "priority": "${PRIORITY:-medium}",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")",
  "resolved_at": null,
  "resolution": null,
  "iteration_count": 1,
  "related_feedback": []
}
EOF
)

echo "✅ Feedback object created"
```

### Step 4: Update workflow.json

```bash
# Read current workflow.json
WORKFLOW_STATE=$(cat .codex/state/workflow.json)

# Add feedback request to feedback_requests array using jq
UPDATED_STATE=$(echo "$WORKFLOW_STATE" | jq \
  --argjson feedback "$FEEDBACK_OBJECT" \
  '.feedback_requests += [$feedback]')

# Write updated state back to file
echo "$UPDATED_STATE" > .codex/state/workflow.json

echo "✅ Updated workflow.json with feedback request"
```

### Step 5: Log Transformation History

```bash
# Add entry to transformation_history
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")

HISTORY_ENTRY=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "type": "feedback_requested",
  "from": "$FROM_AGENT",
  "to": "$TO_AGENT",
  "feedback_id": "$FEEDBACK_ID",
  "context": {
    "document": "$CONTEXT_DOCUMENT",
    "issue_preview": "${ISSUE:0:50}..."
  }
}
EOF
)

# Update transformation_history in workflow.json
UPDATED_STATE=$(cat .codex/state/workflow.json | jq \
  --argjson entry "$HISTORY_ENTRY" \
  '.agent_context.transformation_history += [$entry]')

echo "$UPDATED_STATE" > .codex/state/workflow.json

echo "✅ Logged feedback request to transformation history"
```

### Step 6: Create Feedback Context Package

```bash
# Create temporary feedback context file for target agent
CONTEXT_FILE=".codex/state/feedback/${FEEDBACK_ID}-context.md"
mkdir -p .codex/state/feedback

cat > "$CONTEXT_FILE" <<EOF
# Feedback Request: $FEEDBACK_ID

## From: $FROM_AGENT → To: $TO_AGENT

**Priority:** ${PRIORITY:-medium}

**Created:** $(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")

---

## Issue

$ISSUE

---

## Context

**Document:** $CONTEXT_DOCUMENT

EOF

# Add section if provided
if [ -n "$CONTEXT_SECTION" ]; then
    echo "**Section:** $CONTEXT_SECTION" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
fi

# Add line references if provided
if [ -n "$CONTEXT_LINE_REFS" ]; then
    echo "**Line References:** $CONTEXT_LINE_REFS" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
fi

# Add quote if provided
if [ -n "$CONTEXT_QUOTE" ]; then
    echo "**Quote:**" >> "$CONTEXT_FILE"
    echo "> $CONTEXT_QUOTE" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
fi

# Add relevant document section
echo "---" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"
echo "## Relevant Document Content" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"

if [ -n "$CONTEXT_LINE_REFS" ]; then
    # Extract specific lines if line refs provided
    for LINE_NUM in $(echo "$CONTEXT_LINE_REFS" | jq -r '.[]'); do
        sed -n "${LINE_NUM}p" "$CONTEXT_DOCUMENT" >> "$CONTEXT_FILE"
    done
else
    # Include section or full document
    if [ -n "$CONTEXT_SECTION" ]; then
        # Extract section (simplified - could be enhanced)
        echo "[Section: $CONTEXT_SECTION]" >> "$CONTEXT_FILE"
    fi
    echo "(See full document at: $CONTEXT_DOCUMENT)" >> "$CONTEXT_FILE"
fi

echo "" >> "$CONTEXT_FILE"
echo "---" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"
echo "## Instructions for $TO_AGENT" >> "$CONTEXT_FILE"
echo "" >> "$CONTEXT_FILE"
echo "1. Review the issue and document context above" >> "$CONTEXT_FILE"
echo "2. Update the referenced document to resolve the ambiguity" >> "$CONTEXT_FILE"
echo "3. Execute: *resolve-feedback $FEEDBACK_ID \"[your resolution notes]\"" >> "$CONTEXT_FILE"
echo "4. Notify $FROM_AGENT that feedback has been resolved" >> "$CONTEXT_FILE"

echo "✅ Created feedback context package: $CONTEXT_FILE"
```

### Step 7: Notify Orchestrator

```bash
# Create notification for orchestrator to route feedback
NOTIFICATION=$(cat <<EOF
{
  "type": "feedback_pending",
  "feedback_id": "$FEEDBACK_ID",
  "target_agent": "$TO_AGENT",
  "priority": "${PRIORITY:-medium}",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6NZ")"
}
EOF
)

echo "📢 Feedback request ready for orchestrator routing:"
echo "$NOTIFICATION" | jq '.'

echo ""
echo "✅ Orchestrator will detect pending feedback and spawn $TO_AGENT"
```

## Outputs

```yaml
outputs:
  workflow_state:
    file: .codex/state/workflow.json
    changes:
      - feedback_requests array updated with new feedback object
      - transformation_history updated with feedback_requested event

  context_package:
    file: .codex/state/feedback/{feedback_id}-context.md
    purpose: Complete context for target agent to resolve feedback

  notification:
    type: orchestrator_event
    purpose: Alert orchestrator to route feedback to target agent

  console_output:
    feedback_id: "fb-YYYY-MM-DDTHH:MM:SS.ffffffZ"
    status: "pending"
    next_action: "Orchestrator will spawn $TO_AGENT to resolve"
```

## Integration Points

### Agent Integration

Agents invoke this task via their `*request-feedback` command:

```yaml
# Example from architect.md:
commands:
  request-feedback:
    description: "Request clarification from upstream agent"
    syntax: "*request-feedback {to_agent} {issue}"
    example: "*request-feedback pm Story 1.3: real-time latency requirement undefined"
    execution: "Invokes request-feedback.md task with agent context"
```

### Orchestrator Integration

Orchestrator monitors workflow.json for pending feedback:

```yaml
orchestrator_workflow:
  1_monitor:
    check: "workflow.json → feedback_requests array"
    filter: "status == 'pending'"

  2_route:
    action: "Spawn target agent with feedback context"
    context: "Load .codex/state/feedback/{feedback_id}-context.md"
    agent_activation: "Include feedback ID and context in agent spawn"

  3_track:
    update: "feedback.status = 'in_progress'"
    log: "transformation_history entry for feedback routing"
```

### Resolution Flow

Target agent resolves feedback using `*resolve-feedback`:

```yaml
resolution_workflow:
  1_update_document:
    agent: "Target agent updates referenced document"
    example: "PM updates docs/prd.md with specific latency requirement"

  2_resolve_feedback:
    command: "*resolve-feedback {feedback_id} {resolution}"
    action: "Updates feedback object in workflow.json"
    changes:
      - status: "resolved"
      - resolved_at: "{timestamp}"
      - resolution: "{explanation}"

  3_notify_requester:
    orchestrator: "Notifies requesting agent"
    action: "Requesting agent can proceed with updated document"
```

## Iteration Limit Enforcement

```yaml
iteration_enforcement:
  max_iterations: 3
  check_on_request: "Count existing feedback with same document+section"
  escalation_trigger: "iteration_count >= 3"

  escalation_action:
    message: "⚠️ Feedback iteration limit reached (3 max)"
    prompt: |
      Multiple feedback cycles detected for same issue.
      Options:
      1. Schedule direct user-agent clarification session
      2. Mark as blocking issue for user resolution
      3. Accept current state and proceed with caveats
    user_decision_required: true
```

## Error Handling

```yaml
error_scenarios:
  invalid_agent:
    check: "to_agent not in valid agent list"
    action: "ERROR: Invalid target agent. Must be one of: [agents]"
    exit_code: 1

  document_not_found:
    check: "context.document file does not exist"
    action: "ERROR: Referenced document not found: {path}"
    exit_code: 1

  self_feedback:
    check: "from_agent == to_agent"
    action: "ERROR: Cannot request feedback from yourself"
    exit_code: 1

  workflow_state_missing:
    check: ".codex/state/workflow.json not found"
    action: "ERROR: Workflow state not initialized. Run discovery first."
    exit_code: 1

  vague_issue:
    check: "issue length < 10 characters"
    action: "ERROR: Issue too vague. Provide specific description."
    exit_code: 1
```

## Success Indicators

```yaml
success_criteria:
  - Feedback object created with unique ID
  - workflow.json updated with feedback in pending status
  - Feedback context package created for target agent
  - Transformation history logged
  - Orchestrator notified for routing
  - Console output shows feedback ID and next steps

verification:
  - jq '.feedback_requests | last | .id' .codex/state/workflow.json
  - test -f .codex/state/feedback/fb-*.md
  - jq '.agent_context.transformation_history | last | .type' .codex/state/workflow.json | grep "feedback_requested"
```

## Anti-Patterns

```yaml
anti_patterns:
  vague_issues:
    bad: "Something unclear in PRD"
    good: "Story 1.3: 'real-time' latency requirement undefined. Need specific ms target."

  missing_context:
    bad: "Payment flow needs clarification"
    good: "docs/architecture.md:89-92 - Which fraud detection service: internal or third-party?"

  non_blocking_escalation:
    bad: "Request feedback for minor style preference"
    good: "Request feedback only when ambiguity blocks progress"

  feedback_spam:
    bad: "Multiple feedback requests without waiting for resolution"
    good: "Wait for pending feedback resolution before requesting more"
```

## Testing

```bash
# Test feedback request creation
bash -c '
  FROM_AGENT="architect"
  TO_AGENT="pm"
  ISSUE="Story 1.3 acceptance criteria unclear - real-time undefined"
  CONTEXT_DOCUMENT="docs/prd.md"
  CONTEXT_SECTION="Epic 1 → Story 1.3"
  PRIORITY="high"

  # Source and execute this task
  source .codex/tasks/request-feedback.md

  # Verify feedback created
  if jq -e \'.feedback_requests | last | .id\' .codex/state/workflow.json > /dev/null; then
    echo "✅ Test passed: Feedback request created"
  else
    echo "❌ Test failed: Feedback request not in workflow.json"
    exit 1
  fi
'
```
