# Persist Discovery Summary Task

## Purpose

Automatically extract and persist discovery findings to structured JSON after the 9 discovery questions are answered. This ensures discovery insights are available to downstream phases (analyst, PM, architect) and enables template variable extraction.

## When to Execute

This task should be executed automatically after:
1. Discovery agent completes `process_answers` step
2. All 9 discovery questions have been answered by the user
3. Before elicitation menu is presented (or after elicitation completes)

## Execution Protocol

### Step 1: Read Discovery Context

```yaml
inputs:
  - .codex/state/workflow.json (discovery_data from project_discovery field)
  - User answers to 9 discovery questions

extraction_source:
  - workflow.json.project_discovery field contains structured answers
  - May need to parse from discovery agent's process_answers output
```

### Step 2: Extract Key Insights

Parse the discovery answers and extract structured information into 9 key fields:

```json
{
  "project_scope": {
    "description": "Extract from Q2 (Project Concept)",
    "content": "1-2 paragraph summary of core problem, users, and functionality",
    "source_question": "Q2: Brief Project Concept"
  },

  "target_users": {
    "description": "Extract from Q3 (Target Users & Pain Points)",
    "content": "Summary of user personas, pain points, and significance",
    "primary_users": ["persona1", "persona2"],
    "key_pain_points": ["pain1", "pain2", "pain3"],
    "source_question": "Q3: Target Users & Pain Points"
  },

  "user_research_status": {
    "description": "Extract from Q4 (User Research Status)",
    "content": "Summary of research conducted or planned",
    "research_completed": ["type1", "type2"],
    "research_planned": ["type1", "type2"],
    "validation_approach": "How user needs will be validated",
    "source_question": "Q4: User Research Status"
  },

  "competitive_landscape": {
    "description": "Extract from Q5 (Competitive Landscape)",
    "content": "Summary of competitors and differentiation",
    "competitors": [
      {
        "name": "Competitor name",
        "strengths": ["strength1", "strength2"],
        "weaknesses": ["weakness1", "weakness2"]
      }
    ],
    "differentiation": "How this solution differs",
    "source_question": "Q5: Competitive Landscape"
  },

  "market_opportunities": {
    "description": "Extract from Q6 (Market Opportunity)",
    "content": "Market trends, gaps, timing rationale",
    "trends": ["trend1", "trend2"],
    "gaps": ["gap1", "gap2"],
    "timing_rationale": "Why now is the right time",
    "demand_evidence": "Supporting evidence for market demand",
    "source_question": "Q6: Market Opportunity"
  },

  "technical_constraints": {
    "description": "Extract from Q7 (Technical Platform & Language)",
    "content": "Must-have technical requirements",
    "platforms": ["iOS", "Android", "Web", "Backend"],
    "languages": ["Swift", "Kotlin", "TypeScript"],
    "frameworks": ["framework1", "framework2"],
    "organizational_standards": "Any required standards or policies",
    "source_question": "Q7: Technical Platform & Language"
  },

  "integration_requirements": {
    "description": "Extract from Q8 (Integration Requirements)",
    "content": "External systems and integration specs",
    "systems": [
      {
        "name": "System name",
        "type": "API|Database|Service",
        "auth_requirements": "OAuth 2.0, API key, etc.",
        "data_formats": ["JSON", "XML"],
        "protocols": ["REST", "GraphQL"]
      }
    ],
    "source_question": "Q8: Integration Requirements"
  },

  "success_criteria": {
    "description": "Extract from Q9 (Success Criteria & Constraints)",
    "content": "How success will be measured",
    "metrics": ["metric1", "metric2", "metric3"],
    "critical_success_factors": ["factor1", "factor2"],
    "source_question": "Q9: Success Criteria & Constraints"
  },

  "business_goals": {
    "description": "Synthesized from Q2, Q6, Q9",
    "content": "High-level business objectives",
    "goals": [
      "Solve [pain point] for [users]",
      "Capture [market opportunity]",
      "Achieve [success metrics]"
    ],
    "constraints": {
      "timeline": "Extracted from Q9",
      "budget": "Extracted from Q9 if mentioned",
      "regulatory": "Compliance requirements from Q9",
      "organizational": "Other limitations from Q9"
    }
  },

  "discovery_metadata": {
    "timestamp": "ISO-8601 timestamp when discovery completed",
    "workflow_id": "Reference to workflow.json",
    "workflow_type": "greenfield-swift|greenfield-generic|brownfield",
    "questions_answered": 9,
    "elicitation_rounds": 0
  }
}
```

### Step 3: Intelligent Extraction Rules

**Project Scope** (from Q2):
- Take first 2-3 paragraphs verbatim
- Extract: problem statement, target users, core functionality
- Condense if > 500 words to 250-300 words

**Target Users** (from Q3):
- Extract distinct user personas mentioned
- List specific pain points with priority
- Capture "significance" rationale

**User Research Status** (from Q4):
- Categorize research as "completed" vs "planned"
- Extract validation approach
- Note if "none yet" - important context

**Competitive Landscape** (from Q5):
- Parse competitor names and create structured list
- Extract strengths/weaknesses per competitor
- Capture differentiation strategy

**Market Opportunities** (from Q6):
- Extract trends as bullet list
- Identify market gaps
- Capture timing rationale and demand evidence

**Technical Constraints** (from Q7):
- Parse platforms (iOS, Android, Web, etc.)
- Extract languages and frameworks
- Note organizational standards

**Integration Requirements** (from Q8):
- Create structured list of integration points
- Extract auth, data format, protocol details
- Flag if "none" mentioned

**Success Criteria** (from Q9):
- Extract measurable metrics
- List critical success factors
- Parse constraints (timeline, budget, regulatory)

**Business Goals** (synthesized):
- Combine insights from Q2 (problem), Q6 (opportunity), Q9 (success)
- Create 3-5 high-level business goals
- Structure constraints from Q9

### Step 4: Save to State

```yaml
save_operations:
  1_create_summary_file:
    path: ".codex/state/discovery-summary.json"
    content: "[Structured JSON from Step 2]"
    format: "JSON with 2-space indentation"

  2_update_workflow_state:
    path: ".codex/state/workflow.json"
    updates:
      - "project_discovery.discovery_completed = true"
      - "project_discovery.discovery_summary_path = '.codex/state/discovery-summary.json'"
      - "project_discovery.discovery_timestamp = [ISO-8601]"
      - "completed_phases: append 'discovery' if not present"
```

### Step 5: Validation

After saving, verify:

```yaml
validation_checks:
  - File exists: .codex/state/discovery-summary.json
  - JSON is valid and parseable
  - All 9 fields present (project_scope through business_goals)
  - Each field has non-empty content
  - workflow.json updated with discovery_completed: true
  - discovery_summary_path points to correct file
```

## Integration with Discovery Agent

This task should be called from `.codex/agents/discovery.md` in the `process_answers` or `finalize` step:

```yaml
# In discovery.md finalize step:
execution:
  1. Read workflow.json

  2. Execute persist-discovery-summary task:
     - Parse answers from workflow.json.project_discovery
     - Extract to discovery-summary.json
     - Update workflow state

  3. Update state via state-manager.md:
     - Set discovery_state: "complete"
     - Set elicitation_completed.discovery: true
     - Set current_phase: "analyst"
```

## Downstream Usage

The discovery-summary.json is consumed by:

1. **Analyst Agent**: Reads for project context when creating project-brief.md
2. **Template Variable Extraction** (Task 13): Parses for {{project_name}}, {{target_platform}}, etc.
3. **Quality Gates**: Discovery quality gate validates summary completeness
4. **Documentation**: Provides audit trail of discovery decisions

## Error Handling

```yaml
error_scenarios:
  missing_answers:
    action: Log warning and use placeholder "NOT PROVIDED"
    blocking: No - allow partial summaries

  invalid_workflow_state:
    action: Recreate workflow.json from template
    blocking: Yes - cannot proceed without state

  file_write_failure:
    action: Retry with .tmp file + atomic rename
    blocking: Yes - state must persist

  json_parse_error:
    action: Validate JSON syntax before writing
    blocking: Yes - corrupted JSON breaks workflow
```

## Example Output

```json
{
  "project_scope": "Building a task management app for remote teams that solves the problem of scattered communication across multiple tools. Target users are remote engineering teams (5-50 people) who struggle with context switching between Slack, Jira, GitHub, and email. Core functionality includes unified task view, smart notifications, and conversation threading around tasks.",

  "target_users": {
    "content": "Primary users are engineering managers and senior engineers at remote-first companies. Key pain points: (1) Missing critical updates buried in Slack threads, (2) Context switching costs 2-3 hours per day, (3) No single source of truth for task status. Significance: Engineering teams lose 30-40% productivity to tool fragmentation per recent studies.",
    "primary_users": ["Engineering Managers", "Senior Engineers", "Remote Team Leads"],
    "key_pain_points": [
      "Critical updates buried in Slack threads",
      "Context switching costs 2-3 hours/day",
      "No single source of truth for task status",
      "Notification overload from multiple tools"
    ],
    "source_question": "Q3: Target Users & Pain Points"
  },

  "user_research_status": {
    "content": "Conducted 15 user interviews with engineering managers at remote companies (10-100 employees). Surveys sent to 200+ developers with 45% response rate. Key findings: 87% use 4+ tools daily, 92% report frequent context switching, 78% miss critical updates weekly.",
    "research_completed": ["User interviews (15)", "Developer survey (90 responses)"],
    "research_planned": ["Prototype usability testing with 20 users", "Beta testing with 3 pilot teams"],
    "validation_approach": "Beta program with 3 pilot teams to validate core workflow improvements",
    "source_question": "Q4: User Research Status"
  },

  "competitive_landscape": {
    "content": "Main competitors: Linear (strong design, weak notifications), Asana (broad features, slow for developers), ClickUp (feature-rich, overwhelming UX). Our differentiation: Developer-first design, deep tool integrations, intelligent notification filtering.",
    "competitors": [
      {
        "name": "Linear",
        "strengths": ["Beautiful design", "Fast performance", "Keyboard shortcuts"],
        "weaknesses": ["Weak notification system", "Limited integrations", "No conversation threading"]
      },
      {
        "name": "Asana",
        "strengths": ["Mature platform", "Broad feature set", "Strong mobile apps"],
        "weaknesses": ["Not developer-focused", "Slow interface", "Complex for small teams"]
      },
      {
        "name": "ClickUp",
        "strengths": ["Feature-rich", "Customizable", "Good integrations"],
        "weaknesses": ["Overwhelming UX", "Performance issues", "Steep learning curve"]
      }
    ],
    "differentiation": "Developer-first design with deep tool integrations (GitHub, Slack, GitLab) and intelligent notification filtering that reduces noise by 70%",
    "source_question": "Q5: Competitive Landscape"
  },

  "market_opportunities": {
    "content": "Remote work grew 400% since 2020, creating massive tool fragmentation problem. Current solutions not purpose-built for engineering workflows. $12B project management market growing 10% annually.",
    "trends": [
      "Remote work normalization (78% of companies now hybrid/remote)",
      "Developer tool consolidation movement",
      "Shift to async-first communication",
      "Engineering productivity focus post-layoffs"
    ],
    "gaps": [
      "No tool optimized for engineering workflows",
      "Poor integration between dev tools and PM tools",
      "Notification systems not intelligent enough"
    ],
    "timing_rationale": "Post-pandemic remote work is permanent. Companies investing in productivity tools. Engineering teams have budget authority for tools.",
    "demand_evidence": "90 responses to landing page survey in 2 weeks, 250 signups for early access, 15 companies expressed interest in pilot program",
    "source_question": "Q6: Market Opportunity"
  },

  "technical_constraints": {
    "content": "Must support Web (primary), iOS, Android (future). Backend: Node.js/TypeScript (team expertise). Real-time requirements demand WebSocket support. SOC 2 compliance required for enterprise sales.",
    "platforms": ["Web", "iOS (future)", "Android (future)"],
    "languages": ["TypeScript", "React", "Node.js"],
    "frameworks": ["Next.js (frontend)", "Express.js (backend)", "React Native (mobile future)"],
    "organizational_standards": "SOC 2 compliance required, GDPR compliance for EU users, SSO integration (SAML/OAuth) mandatory for enterprise",
    "source_question": "Q7: Technical Platform & Language"
  },

  "integration_requirements": {
    "content": "Critical integrations: GitHub (webhooks + API), Slack (bot + webhooks), Jira (API sync). Auth via OAuth 2.0 for all services. REST APIs preferred, GraphQL acceptable.",
    "systems": [
      {
        "name": "GitHub",
        "type": "API",
        "auth_requirements": "OAuth 2.0 GitHub Apps",
        "data_formats": ["JSON"],
        "protocols": ["REST", "Webhooks"]
      },
      {
        "name": "Slack",
        "type": "Bot + API",
        "auth_requirements": "OAuth 2.0 Slack App",
        "data_formats": ["JSON"],
        "protocols": ["REST", "Webhooks", "WebSocket (Socket Mode)"]
      },
      {
        "name": "Jira",
        "type": "API",
        "auth_requirements": "OAuth 2.0 or API Token",
        "data_formats": ["JSON"],
        "protocols": ["REST"]
      }
    ],
    "source_question": "Q8: Integration Requirements"
  },

  "success_criteria": {
    "content": "Success measured by: (1) 30% reduction in context switching time, (2) 80% reduction in missed critical updates, (3) 50+ teams onboarded in first 6 months. Critical success factors: Deep tool integration quality, notification filtering effectiveness, sub-200ms response times.",
    "metrics": [
      "30% reduction in context switching time (measured via RescueTime integration)",
      "80% reduction in missed critical updates (user survey metric)",
      "50+ teams onboarded in first 6 months",
      "90%+ notification relevance score (user rating)",
      "< 200ms average response time",
      "95%+ uptime SLA"
    ],
    "critical_success_factors": [
      "Deep integration quality (GitHub, Slack, Jira)",
      "Notification filtering effectiveness",
      "Performance (sub-200ms response)",
      "Enterprise security compliance (SOC 2)"
    ],
    "source_question": "Q9: Success Criteria & Constraints"
  },

  "business_goals": {
    "content": "Transform engineering team productivity by eliminating tool fragmentation, capture remote work productivity market, achieve product-market fit with 50+ teams in 6 months",
    "goals": [
      "Solve tool fragmentation pain for remote engineering teams (30% time savings)",
      "Capture developer productivity market opportunity ($12B growing at 10%/year)",
      "Achieve product-market fit with 50+ teams in first 6 months",
      "Enable enterprise sales through SOC 2 compliance and SSO",
      "Build network effects through team collaboration features"
    ],
    "constraints": {
      "timeline": "MVP in 4 months, beta in 6 months, enterprise-ready in 9 months",
      "budget": "Seed stage funding, $500K runway",
      "regulatory": "SOC 2 Type 1 compliance required before enterprise sales, GDPR compliance for EU",
      "organizational": "Small team (3 engineers), must leverage existing OSS and SaaS where possible"
    }
  },

  "discovery_metadata": {
    "timestamp": "2025-10-07T23:50:00Z",
    "workflow_id": "codex-20251007-235000",
    "workflow_type": "greenfield-generic",
    "questions_answered": 9,
    "elicitation_rounds": 0
  }
}
```

## Success Criteria

- [ ] Task file created: `.codex/tasks/persist-discovery-summary.md`
- [ ] Extraction logic documented for all 9 fields
- [ ] JSON schema defined with examples
- [ ] Integration point with discovery agent specified
- [ ] Validation checks defined
- [ ] Error handling documented
- [ ] Downstream usage explained
- [ ] Example output provided

---

**Implementation Time**: 4 hours (PRP estimate)
**Dependencies**: discovery agent (Task 11), state-manager.md, workflow.json.template
**Enables**: Template variable extraction (Task 13), analyst phase context loading
