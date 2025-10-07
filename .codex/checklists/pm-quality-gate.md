# Product Manager (PM) Quality Gate Checklist

This checklist validates the Product Requirements Document (PRD) before transitioning to the Architecture phase. It ensures complete, well-structured requirements that enable successful one-pass implementation.

[[LLM: INITIALIZATION INSTRUCTIONS - PM QUALITY GATE

Before proceeding with this checklist, ensure you have access to:

1. **docs/prd.md** - The Product Requirements Document
2. **prd-template.yaml** - Template structure reference
3. **docs/project-brief.md** - Context from analyst phase
4. **.codex/state/workflow.json** - Current workflow state

IMPORTANT: If the PRD is missing, immediately request its location before proceeding.

PROJECT TYPE:
CODEX focuses on greenfield projects. Skip any brownfield-specific validations.

VALIDATION APPROACH:

1. **Evidence-Based** - Cite specific PRD sections proving each requirement
2. **User-Centric** - Every requirement must tie back to user value
3. **MVP Focus** - Ensure scope is truly minimal while viable
4. **Testable** - Requirements must be verifiable
5. **Implementation-Ready** - Sufficient detail for architecture phase

EXECUTION MODE:
Ask the user which mode to use:

- **Interactive** - Review section by section, collect evidence, confirm before next section
- **Batch** - Complete full analysis, present comprehensive report at end
- **YOLO** - Skip validation (logs violation to workflow.json)

For interactive/batch modes:
- Collect specific evidence for each item (cite PRD sections/lines)
- Mark items as ⚠️ CRITICAL or standard
- Calculate score: 100 - (10 × critical_fails) - (5 × standard_fails)
- Determine status: APPROVED (90-100), CONDITIONAL (70-89), REJECTED (0-69)

After validation, save results to:
- `.codex/state/quality-gate-pm-{timestamp}.json`
- Update `workflow.json` quality_gate_results

See: `.codex/data/quality-scoring-rubric.md` for detailed scoring methodology]]

## 1. PROBLEM DEFINITION & CONTEXT

[[LLM: The foundation of any product is a clear problem statement. As you review:

1. Verify the problem is real and worth solving
2. Target audience must be specific, not "everyone"
3. Success metrics must be measurable, not vague
4. Look for evidence from discovery/analyst phases
5. Problem-solution fit must be logical

Evidence requirement: Cite PRD section proving each item is satisfied]]

### 1.1 Problem Statement

- ⚠️ [ ] Clear articulation of the problem being solved
  - Evidence: "Cite PRD section 1 'Problem Statement' with specific problem description"
- ⚠️ [ ] Identification of who experiences the problem (target users)
  - Evidence: "Cite PRD section identifying specific user personas or demographics"
- [ ] Explanation of why solving this problem matters (business value)
  - Evidence: "Cite section explaining impact or value of solving problem"
- [ ] Quantification of problem impact (metrics, scale, frequency)
  - Evidence: "Cite quantitative data: # of affected users, frequency, cost, etc."
- [ ] Differentiation from existing solutions
  - Evidence: "Cite competitive analysis showing gaps in existing solutions"

### 1.2 Business Goals & Success Metrics

- ⚠️ [ ] Specific, measurable business objectives defined
  - Evidence: "Cite business goals with concrete metrics (not 'increase engagement' but 'increase daily active users by 20%')"
- ⚠️ [ ] Clear success metrics and KPIs established
  - Evidence: "Cite section defining how success will be measured"
- [ ] Metrics are tied to user and business value
  - Evidence: "Show connection between KPIs and user/business outcomes"
- [ ] Baseline measurements identified (if applicable)
  - Evidence: "Cite current state metrics that will be improved"
- [ ] Timeframe for achieving goals specified
  - Evidence: "Cite timeline for MVP and success metric targets"

### 1.3 User Research & Insights

- ⚠️ [ ] Target user personas clearly defined
  - Evidence: "Cite PRD section with persona definitions (from project-brief.md user-research)"
- [ ] User needs and pain points documented
  - Evidence: "Cite specific user pain points and needs"
- [ ] User research findings summarized (if available)
  - Evidence: "Cite project-brief.md user research section or discovery findings"
- [ ] Competitive analysis included
  - Evidence: "Cite project-brief.md competitive analysis section"
- [ ] Market context provided
  - Evidence: "Cite market opportunities or trends section"

## 2. MVP SCOPE DEFINITION

[[LLM: MVP scope is critical - too much = wasted resources, too little = can't validate. Check:

1. Is this truly minimal? Challenge every feature
2. Does each feature directly address the core problem?
3. "Nice-to-haves" clearly separated from "must-haves"?
4. Rationale for inclusion/exclusion documented?
5. Can you ship this MVP in target timeframe?

Remember: MVP = Minimum **Viable** Product, not Minimum Product]]

### 2.1 Core Functionality

- ⚠️ [ ] Essential features clearly distinguished from nice-to-haves
  - Evidence: "Cite MVP scope section separating must-have from nice-to-have"
- ⚠️ [ ] Features directly address defined problem statement
  - Evidence: "Show each epic/feature ties to problem in section 1"
- ⚠️ [ ] Each Epic ties back to specific user needs
  - Evidence: "Cite epic definitions showing user need mapping"
- [ ] Features and Stories described from user perspective
  - Evidence: "Verify stories use 'As a [user], I want [goal]' format"
- [ ] Minimum requirements for success defined
  - Evidence: "Cite minimum feature set for MVP viability"

### 2.2 Scope Boundaries

- [ ] Clear articulation of what is OUT of scope
  - Evidence: "Cite 'Out of Scope' or 'Future Enhancements' section"
- [ ] Future enhancements section included
  - Evidence: "Cite section documenting deferred features"
- [ ] Rationale for scope decisions documented
  - Evidence: "Cite explanations for why features included/excluded"
- [ ] MVP minimizes functionality while maximizing learning
  - Evidence: "Show MVP focuses on core hypothesis validation"
- [ ] Scope reviewed and refined multiple times
  - Evidence: "Check elicitation_history in workflow.json for scope iterations"

### 2.3 MVP Validation Approach

- [ ] Method for testing MVP success defined
  - Evidence: "Cite how MVP will be validated (user testing, metrics, etc.)"
- [ ] Initial user feedback mechanisms planned
  - Evidence: "Cite feedback collection approach"
- [ ] Criteria for moving beyond MVP specified
  - Evidence: "Cite success criteria that trigger next phase"
- [ ] Learning goals for MVP articulated
  - Evidence: "Cite specific hypotheses or questions MVP will answer"
- [ ] Timeline expectations set
  - Evidence: "Cite MVP delivery timeline"

## 3. USER EXPERIENCE REQUIREMENTS

[[LLM: UX requirements bridge user needs and technical implementation. Validate:

1. User flows cover primary use cases completely
2. Edge cases are identified (even if deferred to future)
3. Accessibility isn't an afterthought
4. Performance expectations are realistic for MVP
5. Error states and recovery are planned

Skip this entire section if project is backend-only/no UI]]

### 3.1 User Journeys & Flows

- [ ] Primary user flows documented
  - Evidence: "Cite user journey descriptions or flow diagrams"
- [ ] Entry and exit points for each flow identified
  - Evidence: "Cite flow start/end points"
- [ ] Decision points and branches mapped
  - Evidence: "Cite conditional flows or user choices"
- [ ] Critical path highlighted
  - Evidence: "Cite primary happy path users will take"
- [ ] Edge cases considered
  - Evidence: "Cite edge cases, error conditions, or alternate paths"

### 3.2 Usability Requirements

- [ ] Accessibility considerations documented
  - Evidence: "Cite accessibility requirements or standards (WCAG, etc.)"
- [ ] Platform/device compatibility specified
  - Evidence: "Cite supported platforms (iOS, Android, web, desktop)"
- [ ] Performance expectations from user perspective defined
  - Evidence: "Cite user-facing performance goals (load time, response time)"
- [ ] Error handling and recovery approaches outlined
  - Evidence: "Cite error message strategy and recovery flows"
- [ ] User feedback mechanisms identified
  - Evidence: "Cite in-app feedback, help, or support features"

### 3.3 UI Requirements

- [ ] Information architecture outlined
  - Evidence: "Cite high-level screen structure or navigation"
- [ ] Critical UI components identified
  - Evidence: "Cite key UI elements (forms, lists, dashboards, etc.)"
- [ ] Visual design guidelines referenced (if applicable)
  - Evidence: "Cite design system, style guide, or design references"
- [ ] Content requirements specified
  - Evidence: "Cite content needs (copy, images, data to display)"
- [ ] High-level navigation structure defined
  - Evidence: "Cite app navigation or routing approach"

## 4. FUNCTIONAL REQUIREMENTS

[[LLM: Functional requirements must be implementation-ready. Check:

1. Requirements focus on WHAT not HOW (no impl details)
2. Each requirement is testable (how would QA verify?)
3. Dependencies are explicit (build order clear)
4. Consistent terminology throughout
5. Complex features broken into manageable stories

Requirements should enable architect to design without ambiguity]]

### 4.1 Feature Completeness

- ⚠️ [ ] All required features for MVP documented
  - Evidence: "Verify all epics/features from scope section have requirements"
- ⚠️ [ ] Features have clear, user-focused descriptions
  - Evidence: "Cite feature descriptions in user value terms"
- [ ] Feature priority/criticality indicated
  - Evidence: "Cite epic ordering or priority designations"
- ⚠️ [ ] Requirements are testable and verifiable
  - Evidence: "Each requirement has clear pass/fail criteria"
- [ ] Dependencies between features identified
  - Evidence: "Cite epic dependencies or prerequisite features"

### 4.2 Requirements Quality

- ⚠️ [ ] Requirements are specific and unambiguous
  - Evidence: "No vague terms like 'user-friendly', 'fast', 'simple'"
- [ ] Requirements focus on WHAT not HOW
  - Evidence: "No implementation details (algorithms, data structures)"
- [ ] Requirements use consistent terminology
  - Evidence: "Same concepts use same terms throughout"
- [ ] Complex requirements broken into simpler parts
  - Evidence: "Large epics broken into bite-sized stories"
- [ ] Technical jargon minimized or explained
  - Evidence: "Terms defined in glossary or explained in context"

### 4.3 User Stories & Acceptance Criteria

- ⚠️ [ ] Stories follow consistent format ("As a [user], I want [goal], so that [benefit]")
  - Evidence: "Cite stories using standard user story format"
- ⚠️ [ ] Acceptance criteria are testable
  - Evidence: "Each AC has clear verification method"
- [ ] Stories are sized appropriately (not too large)
  - Evidence: "Stories are 4-8 hours for AI implementation"
- [ ] Stories are independent where possible
  - Evidence: "Stories can be implemented in parallel when feasible"
- [ ] Stories include necessary context
  - Evidence: "Stories reference problem, user need, or business value"
- [ ] Local testability requirements defined in ACs for backend/data stories
  - Evidence: "Backend stories specify CLI or test harness for local validation"

## 5. NON-FUNCTIONAL REQUIREMENTS

[[LLM: NFRs are often overlooked but critical for production readiness. Validate that quality attributes are defined with measurable targets]]

### 5.1 Performance Requirements

- [ ] Response time expectations defined
  - Evidence: "Cite acceptable latency for user actions"
- [ ] Throughput/capacity requirements specified
  - Evidence: "Cite expected load (requests/sec, concurrent users)"
- [ ] Scalability needs documented
  - Evidence: "Cite growth expectations and scaling approach"
- [ ] Resource utilization constraints identified
  - Evidence: "Cite memory, CPU, storage constraints"
- [ ] Load handling expectations set
  - Evidence: "Cite behavior under peak load"

### 5.2 Security & Compliance

- ⚠️ [ ] Data protection requirements specified
  - Evidence: "Cite data encryption, storage security requirements"
- ⚠️ [ ] Authentication/authorization needs defined
  - Evidence: "Cite who can access what, auth mechanism"
- [ ] Compliance requirements documented (if applicable)
  - Evidence: "Cite GDPR, HIPAA, SOC2, or other standards"
- [ ] Security testing requirements outlined
  - Evidence: "Cite security validation approach"
- [ ] Privacy considerations addressed
  - Evidence: "Cite PII handling, data retention policies"

### 5.3 Reliability & Resilience

- [ ] Availability requirements defined
  - Evidence: "Cite uptime target (99%, 99.9%, etc.)"
- [ ] Backup and recovery needs documented
  - Evidence: "Cite backup frequency, recovery time objectives"
- [ ] Fault tolerance expectations set
  - Evidence: "Cite how system handles failures"
- [ ] Error handling requirements specified
  - Evidence: "Cite error logging, monitoring, alerting needs"
- [ ] Maintenance and support considerations included
  - Evidence: "Cite maintenance windows, support processes"

### 5.4 Technical Constraints

- ⚠️ [ ] Platform/technology constraints documented
  - Evidence: "Cite required platforms, languages, frameworks from discovery"
- [ ] Integration requirements outlined
  - Evidence: "Cite external systems to integrate with"
- [ ] Third-party service dependencies identified
  - Evidence: "Cite APIs, services, libraries required"
- [ ] Infrastructure requirements specified
  - Evidence: "Cite hosting, deployment, environment needs"
- [ ] Development environment needs identified
  - Evidence: "Cite local development setup requirements"

## 6. EPIC & STORY STRUCTURE

[[LLM: Epic and story structure directly impacts implementation success. For AI agents:
- Epics must be cohesive vertical slices
- Stories must be 4-8 hours (AI sweet spot)
- Clear dependencies enable parallel work
- First epic must establish foundation

Validate that structure supports autonomous AI implementation]]

### 6.1 Epic Definition

- ⚠️ [ ] Epics represent cohesive units of functionality
  - Evidence: "Each epic is a complete vertical slice (UI + logic + data)"
- ⚠️ [ ] Epics focus on user/business value delivery
  - Evidence: "Each epic delivers shippable value, not horizontal layers"
- [ ] Epic goals clearly articulated
  - Evidence: "Each epic has clear success criteria"
- [ ] Epics sized appropriately for incremental delivery
  - Evidence: "Epics deliverable in 1-2 weeks or less"
- [ ] Epic sequence and dependencies identified
  - Evidence: "Epic order logical, dependencies documented"

### 6.2 Story Breakdown

- ⚠️ [ ] Stories broken down to appropriate size (4-8 hours)
  - Evidence: "No stories larger than 8 hours of AI implementation"
- ⚠️ [ ] Stories have clear, independent value
  - Evidence: "Each story is testable and deployable independently"
- [ ] Stories include appropriate acceptance criteria
  - Evidence: "3-7 testable ACs per story"
- [ ] Story dependencies and sequence documented
  - Evidence: "Prerequisites and order clear"
- [ ] Stories aligned with epic goals
  - Evidence: "Each story contributes to epic objective"

### 6.3 First Epic Completeness

- ⚠️ [ ] First epic includes all necessary setup steps
  - Evidence: "Epic 1 includes project initialization, scaffolding"
- [ ] Project scaffolding and initialization addressed
  - Evidence: "Repo setup, initial structure in Epic 1"
- [ ] Core infrastructure setup included
  - Evidence: "Database, auth, core services in Epic 1"
- [ ] Development environment setup addressed
  - Evidence: "Local dev setup, dependencies in Epic 1"
- [ ] Local testability established early
  - Evidence: "Test framework, CI/CD basics in Epic 1"

## 7. TECHNICAL GUIDANCE

[[LLM: Technical guidance helps architect make aligned decisions. This section bridges PM and architect roles]]

### 7.1 Architecture Guidance

- [ ] Initial architecture direction provided
  - Evidence: "Cite architectural style or approach (monolith, microservices, etc.)"
- ⚠️ [ ] Technical constraints clearly communicated
  - Evidence: "Cite must-use technologies or constraints from discovery"
- [ ] Integration points identified
  - Evidence: "Cite external systems or APIs to integrate"
- [ ] Performance considerations highlighted
  - Evidence: "Cite performance-critical features or bottlenecks"
- ⚠️ [ ] Security requirements articulated
  - Evidence: "Cite security needs that impact architecture"
- [ ] Known areas of high complexity flagged for architectural deep-dive
  - Evidence: "Cite complex features needing detailed design"

### 7.2 Technical Decision Framework

- [ ] Decision criteria for technical choices provided
  - Evidence: "Cite principles guiding tech selection (cost, scalability, etc.)"
- [ ] Trade-offs articulated for key decisions
  - Evidence: "Cite pros/cons of considered approaches"
- [ ] Non-negotiable technical requirements highlighted
  - Evidence: "Cite hard requirements (must use X, cannot use Y)"
- [ ] Areas requiring technical investigation identified
  - Evidence: "Cite unknowns needing architect research or spikes"

### 7.3 Implementation Considerations

- [ ] Development approach guidance provided
  - Evidence: "Cite incremental delivery, test-first, or other approaches"
- ⚠️ [ ] Testing requirements articulated
  - Evidence: "Cite test coverage targets, test types required"
- [ ] Deployment expectations set
  - Evidence: "Cite deployment frequency, environments, process"
- [ ] Monitoring needs identified
  - Evidence: "Cite metrics to track, alerting requirements"
- [ ] Documentation requirements specified
  - Evidence: "Cite README, API docs, inline comments expectations"

## 8. CROSS-FUNCTIONAL REQUIREMENTS

[[LLM: Cross-functional concerns impact all features. Ensure they're addressed systematically]]

### 8.1 Data Requirements

- ⚠️ [ ] Data entities and relationships identified
  - Evidence: "Cite primary domain entities and their relationships"
- [ ] Data storage requirements specified
  - Evidence: "Cite database type, storage needs, retention policies"
- [ ] Data quality requirements defined
  - Evidence: "Cite validation rules, data integrity constraints"
- [ ] Schema changes planned iteratively, tied to stories
  - Evidence: "Database changes incremental, not big bang"

### 8.2 Integration Requirements

- [ ] External system integrations identified
  - Evidence: "Cite third-party APIs or services to integrate"
- [ ] API requirements documented
  - Evidence: "Cite API endpoints to expose or consume"
- [ ] Authentication for integrations specified
  - Evidence: "Cite API keys, OAuth, or auth mechanism for integrations"
- [ ] Data exchange formats defined
  - Evidence: "Cite JSON, XML, protobuf, or data format"
- [ ] Integration testing requirements outlined
  - Evidence: "Cite how integrations will be tested"

### 8.3 Operational Requirements

- [ ] Deployment frequency expectations set
  - Evidence: "Cite how often deployments occur (daily, per epic, etc.)"
- [ ] Environment requirements defined
  - Evidence: "Cite dev, staging, production environments"
- [ ] Monitoring and alerting needs identified
  - Evidence: "Cite metrics dashboards, alerts, logging"
- [ ] Support requirements documented
  - Evidence: "Cite support model, escalation, SLAs"
- [ ] Performance monitoring approach specified
  - Evidence: "Cite APM tools, metrics to track"

## 9. CLARITY & COMMUNICATION

[[LLM: Clear documentation enables successful implementation. Ambiguity causes rework]]

### 9.1 Documentation Quality

- [ ] Documents use clear, consistent language
  - Evidence: "No contradictions, consistent terminology"
- [ ] Documents are well-structured and organized
  - Evidence: "Logical flow, clear sections, easy navigation"
- [ ] Technical terms are defined where necessary
  - Evidence: "Glossary or inline definitions for domain terms"
- [ ] Diagrams/visuals included where helpful
  - Evidence: "User flows, architecture diagrams, data models"
- [ ] Documentation versioned appropriately
  - Evidence: "Check workflow.json documents.prd.version"

### 9.2 Stakeholder Alignment

- [ ] Key stakeholders identified
  - Evidence: "Cite project sponsors, key users, decision makers"
- [ ] Stakeholder input incorporated
  - Evidence: "Check elicitation_history for stakeholder feedback"
- [ ] Communication plan for updates established
  - Evidence: "Cite how/when stakeholders are updated"
- [ ] Approval process defined
  - Evidence: "Cite who approves PRD before architect phase"

---

## SCORING & VALIDATION SUMMARY

[[LLM: Calculate quality score and generate comprehensive report

**Scoring Calculation:**
1. Count total validation items attempted (exclude skipped sections)
2. Count critical failures (⚠️ items that failed)
3. Count standard failures (non-critical items that failed)
4. Calculate: Score = 100 - (10 × critical_failures) - (5 × standard_failures)
5. Determine status:
   - APPROVED (90-100): Proceed to architect phase immediately
   - CONDITIONAL (70-89): Proceed with noted improvements
   - REJECTED (0-69): Must fix critical issues before proceeding

**Report Structure:**

# PM Quality Gate Validation Report

**Phase**: PM
**Checklist**: pm-quality-gate.md
**Document**: docs/prd.md
**Timestamp**: {iso_timestamp}
**Mode**: {interactive|batch|yolo}

## Overall Result

**Status**: {APPROVED|CONDITIONAL|REJECTED}
**Score**: {score}/100
**Total Items**: {total}
**Passed**: {passed}
**Failed**: {failed} ({critical_failures} critical, {standard_failures} standard)

## Section Results

### 1. Problem Definition & Context (15 items)
- Passed: X/15
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

[Repeat for all 9 sections]

## Failed Items Detail

[For each failed item, provide:]
- Item text
- Evidence requirement
- Why it failed
- Impact on score (-5 or -10)
- Recommendation for fix

## Recommendations

### High Priority (Blocking or Critical)
1. [Specific action to address critical failure]
2. ...

### Medium Priority (Quality Improvements)
1. [Specific action to improve quality]
2. ...

### Low Priority (Nice to Have)
1. [Optional improvements]
2. ...

## Next Steps

**If APPROVED (90-100)**:
✅ Proceed to architect phase immediately
✅ All critical requirements met
✅ High confidence in implementation success

**If CONDITIONAL (70-89)**:
⚠️ May proceed to architect phase
⚠️ Address high-priority recommendations
⚠️ Document known gaps in architecture phase
⚠️ Risk: Minor rework possible

**If REJECTED (0-69)**:
❌ BLOCK progression to architect phase
❌ Must address all critical failures
❌ Re-run quality gate after fixes
❌ Risk: High downstream rework if proceeding

## Evidence Summary

[Provide summary of evidence collection quality]
- Strong Evidence: X items
- Weak Evidence: Y items
- No Evidence: Z items

## Save Results

Save validation results to:
`.codex/state/quality-gate-pm-{timestamp}.json`

Update workflow.json:
```json
{
  "quality_gate_results": {
    "pm": {
      "timestamp": "{iso_timestamp}",
      "status": "{APPROVED|CONDITIONAL|REJECTED}",
      "score": {score},
      "checklist": "pm-quality-gate.md",
      "mode": "{interactive|batch|yolo}",
      "total_items": {total},
      "passed": {passed},
      "failed": {failed},
      "critical_failures": {critical_failures},
      "standard_failures": {standard_failures},
      "summary": "{one-line summary}"
    }
  },
  "quality_scores": {
    "pm": {score}
  }
}
```

]]

---

**Checklist Version**: 1.0
**Total Items**: 93 (excluding conditional UI sections)
**Critical Items**: 28 (marked with ⚠️)
**Last Updated**: 2024-01-15
**Maintained By**: CODEX Quality Team
**Related**: quality-scoring-rubric.md, prd-template.yaml, execute-quality-gate.md
