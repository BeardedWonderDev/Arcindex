# Architect Quality Gate Checklist

This checklist validates the Architecture Document before transitioning to the PRP phase. It ensures comprehensive, clear, and implementation-ready architecture that enables successful AI-driven development.

[[LLM: INITIALIZATION INSTRUCTIONS - ARCHITECT QUALITY GATE

Before proceeding with this checklist, ensure you have access to:

1. **docs/architecture.md** - The primary architecture document
2. **docs/prd.md** - Product Requirements Document for alignment validation
3. **docs/frontend-architecture.md** or **fe-architecture.md** - If this is a UI project (check docs/)
4. **architecture-template.yaml** - Template structure reference
5. **.codex/state/workflow.json** - Current workflow state
6. **Any system diagrams** referenced in the architecture
7. **API documentation** if available
8. **Technology stack details** and version specifications

IMPORTANT: If any required documents are missing, immediately request their location before proceeding.

PROJECT TYPE DETECTION:

CODEX focuses on **greenfield projects**. Skip any brownfield-specific validations.

First, determine the project type by checking:
- Does the architecture include a frontend/UI component?
- Is there a frontend-architecture.md or fe-architecture.md document?
- Does the PRD mention user interfaces or frontend requirements?

If this is a **backend-only** or **service-only** project:
- Skip all sections marked with **[[FRONTEND ONLY]]**
- Focus extra attention on API design, service architecture, and integration patterns
- Note in your final report that frontend sections were skipped due to project type

VALIDATION APPROACH:

For each section, you must:

1. **Deep Analysis** - Don't just check boxes, thoroughly analyze each item against the provided documentation
2. **Evidence-Based** - Cite specific sections, line numbers, or quotes from the documents when validating
3. **Critical Thinking** - Question assumptions and identify gaps, not just confirm what's present
4. **Risk Assessment** - Consider what could go wrong with each architectural decision
5. **AI Agent Readiness** - Verify architecture is clear enough for autonomous AI implementation
6. **PRD Alignment** - Ensure architecture directly supports all PRD requirements

EXECUTION MODE:

Ask the user which mode to use:

- **Interactive** - Review section by section, present findings, get confirmation before proceeding
- **Batch** - Complete full analysis and present comprehensive report at end
- **YOLO** - Skip validation (logs violation to workflow.json)

For interactive/batch modes:
- Collect specific evidence for each item (cite architecture.md sections/lines)
- Mark items as ⚠️ CRITICAL or standard
- Calculate score: 100 - (10 × critical_fails) - (5 × standard_fails)
- Determine status: APPROVED (90-100), CONDITIONAL (70-89), REJECTED (0-69)

After validation, save results to:
- `.codex/state/quality-gate-architect-{timestamp}.json`
- Update `workflow.json` quality_gate_results

See: `.codex/data/quality-scoring-rubric.md` for detailed scoring methodology]]

## 1. REQUIREMENTS ALIGNMENT

[[LLM: Before evaluating this section, fully understand the product's purpose from the PRD. What is the core problem being solved? Who are the users? What are the critical success factors? Keep these in mind as you validate alignment.

For each item, don't just check if it's mentioned - verify that the architecture provides a concrete, actionable technical solution that directly addresses the requirement.

Evidence requirement: Cite both architecture.md AND prd.md sections proving alignment]]

### 1.1 Functional Requirements Coverage

- ⚠️ [ ] Architecture supports ALL functional requirements in the PRD
  - Evidence: "Map each PRD epic/feature to specific architecture components/sections"
- ⚠️ [ ] Technical approaches for all epics and stories are addressed
  - Evidence: "Cite architecture sections addressing each epic's technical needs"
- [ ] Edge cases and performance scenarios are considered
  - Evidence: "Cite sections addressing error handling, fallbacks, load scenarios"
- ⚠️ [ ] All required integrations are accounted for
  - Evidence: "Cite PRD integration requirements and corresponding architecture sections"
- [ ] User journeys are supported by the technical architecture
  - Evidence: "Map PRD user flows to architecture data flows and component interactions"

### 1.2 Non-Functional Requirements Alignment

- ⚠️ [ ] Performance requirements are addressed with specific solutions
  - Evidence: "Cite PRD performance targets and architecture performance strategies"
- [ ] Scalability considerations are documented with approach
  - Evidence: "Cite scaling targets from PRD and architecture scaling strategy"
- ⚠️ [ ] Security requirements have corresponding technical controls
  - Evidence: "Map each PRD security requirement to specific architecture security measures"
- [ ] Reliability and resilience approaches are defined
  - Evidence: "Cite uptime/availability requirements and architecture resilience patterns"
- [ ] Compliance requirements have technical implementations
  - Evidence: "Cite PRD compliance needs (GDPR, etc.) and architecture compliance sections"

### 1.3 Technical Constraints Adherence

- ⚠️ [ ] All technical constraints from PRD are satisfied
  - Evidence: "Cite PRD constraints and verify architecture respects them"
- ⚠️ [ ] Platform/language requirements are followed
  - Evidence: "Verify technology stack matches PRD requirements"
- [ ] Infrastructure constraints are accommodated
  - Evidence: "Cite deployment/hosting requirements and architecture infrastructure design"
- [ ] Third-party service constraints are addressed
  - Evidence: "Verify PRD required services are integrated in architecture"
- [ ] Organizational technical standards are followed
  - Evidence: "Cite standards from discovery/PRD and verify architecture compliance"

## 2. ARCHITECTURE FUNDAMENTALS

[[LLM: Architecture clarity is crucial for successful AI-driven implementation. As you review this section, visualize the system as if you were explaining it to a new developer or AI agent.

Are there any ambiguities that could lead to misinterpretation? Would an AI agent be able to implement this architecture without confusion or making incorrect assumptions?

Look for:
- Specific diagrams (not just descriptions)
- Clear component definitions with boundaries
- Explicit interaction patterns
- Data flow clarity
- Technology choices tied to components

Remember: Explicit is better than implicit. Assume zero prior knowledge.]]

### 2.1 Architecture Clarity

- ⚠️ [ ] Architecture is documented with clear diagrams
  - Evidence: "Cite system context, container, or component diagrams (C4 model preferred)"
- ⚠️ [ ] Major components and their responsibilities are defined
  - Evidence: "Cite component list with single-responsibility descriptions"
- [ ] Component interactions and dependencies are mapped
  - Evidence: "Cite interaction diagrams or dependency sections"
- [ ] Data flows are clearly illustrated
  - Evidence: "Cite data flow diagrams or descriptions of data movement"
- ⚠️ [ ] Technology choices for each component are specified
  - Evidence: "Each component has explicit tech stack assignment"

### 2.2 Separation of Concerns

- [ ] Clear boundaries between UI, business logic, and data layers
  - Evidence: "Cite layered architecture or clear separation descriptions"
- [ ] Responsibilities are cleanly divided between components
  - Evidence: "No overlapping or ambiguous responsibilities between components"
- ⚠️ [ ] Interfaces between components are well-defined
  - Evidence: "Cite API contracts, protocols, or interface definitions"
- [ ] Components adhere to single responsibility principle
  - Evidence: "Each component has one clear purpose"
- [ ] Cross-cutting concerns (logging, auth, etc.) are properly addressed
  - Evidence: "Cite how logging, authentication, monitoring are handled across system"

### 2.3 Design Patterns & Best Practices

- [ ] Appropriate design patterns are employed
  - Evidence: "Cite specific patterns used (MVC, Repository, Factory, etc.)"
- [ ] Industry best practices are followed
  - Evidence: "Architecture follows established patterns for chosen technologies"
- [ ] Anti-patterns are avoided
  - Evidence: "No god objects, circular dependencies, or known anti-patterns"
- [ ] Consistent architectural style throughout
  - Evidence: "Patterns applied uniformly across all components"
- [ ] Pattern usage is documented and explained
  - Evidence: "Rationale for pattern choices is clear"

### 2.4 Modularity & Maintainability

- [ ] System is divided into cohesive, loosely-coupled modules
  - Evidence: "Cite module boundaries and minimal inter-module dependencies"
- [ ] Components can be developed and tested independently
  - Evidence: "Clear isolation allows parallel development"
- [ ] Changes can be localized to specific components
  - Evidence: "Feature changes don't require modifications across multiple components"
- [ ] Code organization promotes discoverability
  - Evidence: "Cite project structure with logical file/folder organization"
- ⚠️ [ ] Architecture specifically designed for AI agent implementation
  - Evidence: "Clear patterns, consistent structure, explicit guidance for AI agents"

## 3. TECHNICAL STACK & DECISIONS

[[LLM: Technology choices have long-term implications. For each technology decision, consider:

- Is this the simplest solution that could work?
- Are we over-engineering or under-engineering?
- Will this scale to PRD requirements?
- What are the maintenance implications?
- Are there security vulnerabilities in the chosen versions?
- Is the team (or AI agents) familiar with this stack?

**CRITICAL VALIDATION**: Verify that specific versions are defined, NOT ranges.
- ✅ "React 18.2.0" or "React ^18.2.0"
- ❌ "React 18" or "Latest React" or "React 17+"

Vague versioning is a CRITICAL failure - it leads to dependency conflicts and inconsistent environments.]]

### 3.1 Technology Selection

- ⚠️ [ ] Selected technologies meet all requirements
  - Evidence: "Map each technology choice to PRD requirements it satisfies"
- ⚠️ [ ] Technology versions are specifically defined (not ranges)
  - Evidence: "Cite version table with exact versions (e.g., React 18.2.0, Node 20.10.0)"
- ⚠️ [ ] Technology choices are justified with clear rationale
  - Evidence: "Cite 'Rationale' column or decision explanations for each tech choice"
- [ ] Alternatives considered are documented with pros/cons
  - Evidence: "Cite 'Alternatives Considered' sections showing evaluation process"
- [ ] Selected stack components work well together
  - Evidence: "No incompatibilities or integration challenges between chosen technologies"
- [ ] All chosen technologies have active maintenance and security support
  - Evidence: "Verify no deprecated or end-of-life technologies in the stack"
- [ ] Technology stack aligns with team expertise or learning goals
  - Evidence: "Cite rationale for unfamiliar technologies and learning plan if needed"

### 3.2 Frontend Architecture [[FRONTEND ONLY]]

[[LLM: Skip this entire subsection if this is a backend-only or service-only project. Only evaluate if the project includes a user interface.

If evaluating, ensure alignment between the main architecture.md and any frontend-specific architecture document (frontend-architecture.md).]]

- ⚠️ [ ] UI framework and libraries are specifically selected
  - Evidence: "Cite React/Vue/Angular/etc. with exact version"
- [ ] State management approach is defined
  - Evidence: "Cite Redux/MobX/Context/etc. with usage patterns"
- [ ] Component structure and organization is specified
  - Evidence: "Cite component hierarchy, atomic design, or structure approach"
- [ ] Responsive/adaptive design approach is outlined
  - Evidence: "Cite responsive framework (Tailwind/MUI/etc.) or custom approach"
- [ ] Build and bundling strategy is determined
  - Evidence: "Cite Vite/Webpack/etc. with configuration approach"

### 3.3 Backend Architecture

- ⚠️ [ ] API design and standards are defined
  - Evidence: "Cite REST/GraphQL/gRPC choice with versioning strategy"
- [ ] Service organization and boundaries are clear
  - Evidence: "Cite monolith/microservices/modular monolith decision"
- ⚠️ [ ] Authentication and authorization approach is specified
  - Evidence: "Cite JWT/OAuth/session-based with implementation details"
- [ ] Error handling strategy is outlined
  - Evidence: "Cite error response formats, logging, and recovery approaches"
- [ ] Backend scaling approach is defined
  - Evidence: "Cite horizontal/vertical scaling strategy"
- [ ] Caching strategy is defined for performance optimization
  - Evidence: "Cite Redis/Memcached/CDN usage, cache invalidation strategy"
- [ ] Rate limiting and throttling mechanisms are specified
  - Evidence: "Cite rate limit tiers, throttling algorithms, and implementation approach"

### 3.4 Data Architecture

- ⚠️ [ ] Data models are fully defined
  - Evidence: "Cite entity definitions, relationships, or data model diagrams"
- ⚠️ [ ] Database technologies are selected with justification
  - Evidence: "Cite PostgreSQL/MongoDB/etc. with version and rationale"
- [ ] Data access patterns are documented
  - Evidence: "Cite ORM, query patterns, or data access layer design"
- [ ] Data migration/seeding approach is specified
  - Evidence: "Cite migration tools and strategy for schema evolution"
- [ ] Data backup and recovery strategies are outlined
  - Evidence: "Cite backup frequency, retention, and recovery procedures"
- [ ] Data consistency and transaction management approach is defined
  - Evidence: "Cite ACID compliance, eventual consistency, or distributed transaction handling"
- [ ] Database indexing strategy is specified for performance
  - Evidence: "Cite key indexes, query optimization approach, and index maintenance plan"

## 4. FRONTEND DESIGN & IMPLEMENTATION [[FRONTEND ONLY]]

[[LLM: This entire section should be skipped for backend-only projects. Only evaluate if the project includes a user interface.

When evaluating, ensure alignment between:
1. Main architecture document (architecture.md)
2. Frontend-specific architecture document (frontend-architecture.md or fe-architecture.md)
3. PRD user interface requirements

Look for consistency in framework choices, component structure, and state management across all documents.]]

### 4.1 Frontend Philosophy & Patterns

- ⚠️ [ ] Framework & Core Libraries align with main architecture document
  - Evidence: "Verify frontend-architecture.md framework matches architecture.md technology stack"
- [ ] Component Architecture (e.g., Atomic Design) is clearly described
  - Evidence: "Cite component organization pattern with examples"
- [ ] State Management Strategy is appropriate for application complexity
  - Evidence: "Cite state management choice matches app complexity (simple apps don't need Redux)"
- [ ] Data Flow patterns are consistent and clear
  - Evidence: "Cite unidirectional data flow or other patterns with diagrams"
- [ ] Styling Approach is defined and tooling specified
  - Evidence: "Cite CSS-in-JS/Tailwind/SCSS with version and configuration"

### 4.2 Frontend Structure & Organization

- [ ] Directory structure is clearly documented with ASCII diagram
  - Evidence: "Cite src/ folder structure tree diagram"
- [ ] Component organization follows stated patterns
  - Evidence: "Folder structure matches declared component architecture (atoms/molecules/etc.)"
- [ ] File naming conventions are explicit
  - Evidence: "Cite naming standards (PascalCase components, kebab-case files, etc.)"
- [ ] Structure supports chosen framework's best practices
  - Evidence: "React apps follow React conventions, Vue apps follow Vue conventions"
- [ ] Clear guidance on where new components should be placed
  - Evidence: "Rules for when to create atoms vs molecules vs organisms"

### 4.3 Component Design

- [ ] Component template/specification format is defined
  - Evidence: "Cite component structure (props, state, lifecycle, events)"
- [ ] Component props, state, and events are well-documented
  - Evidence: "Cite TypeScript interfaces or PropTypes for component contracts"
- [ ] Shared/foundational components are identified
  - Evidence: "Cite Button, Input, Card, etc. base components"
- [ ] Component reusability patterns are established
  - Evidence: "Cite composition patterns, HOCs, render props, or hooks"
- [ ] Accessibility requirements are built into component design
  - Evidence: "Cite ARIA attributes, semantic HTML requirements in component specs"

### 4.4 Frontend-Backend Integration

- ⚠️ [ ] API interaction layer is clearly defined
  - Evidence: "Cite service layer, API client, or data fetching approach"
- [ ] HTTP client setup and configuration documented
  - Evidence: "Cite axios/fetch configuration with base URLs, interceptors"
- [ ] Error handling for API calls is comprehensive
  - Evidence: "Cite error boundaries, error states, retry logic"
- [ ] Service definitions follow consistent patterns
  - Evidence: "All API calls use same pattern (e.g., React Query hooks)"
- [ ] Authentication integration with backend is clear
  - Evidence: "Cite token storage, refresh logic, authenticated request handling"

### 4.5 Routing & Navigation

- [ ] Routing strategy and library are specified
  - Evidence: "Cite React Router/Vue Router/etc. with version"
- [ ] Route definitions table is comprehensive
  - Evidence: "Cite route table with paths, components, and access rules"
- [ ] Route protection mechanisms are defined
  - Evidence: "Cite auth guards, protected routes, redirect logic"
- [ ] Deep linking considerations addressed
  - Evidence: "Cite URL structure supports direct navigation to any app state"
- [ ] Navigation patterns are consistent
  - Evidence: "Cite menu structure, breadcrumbs, navigation components"

### 4.6 Frontend Performance

- [ ] Image optimization strategies defined
  - Evidence: "Cite lazy loading, responsive images, CDN usage, WebP format"
- [ ] Code splitting approach documented
  - Evidence: "Cite route-based or component-based code splitting"
- [ ] Lazy loading patterns established
  - Evidence: "Cite React.lazy, dynamic imports, or framework-specific lazy loading"
- [ ] Re-render optimization techniques specified
  - Evidence: "Cite React.memo, useMemo, useCallback, or framework-specific optimizations"
- [ ] Performance monitoring approach defined
  - Evidence: "Cite Core Web Vitals tracking, performance budgets, monitoring tools"

## 5. RESILIENCE & OPERATIONAL READINESS

[[LLM: Production systems fail in unexpected ways. As you review this section, think about Murphy's Law - what could go wrong?

Consider real-world scenarios:
- What happens during peak load (Black Friday, viral post)?
- How does the system behave when a critical service is down (database, third-party API)?
- Can the operations team diagnose issues at 3 AM without the original developer?
- What if the network is slow or intermittent?

Look for specific resilience patterns, not just mentions of "error handling":
- Circuit breakers with specific thresholds
- Retry policies with backoff strategies
- Fallback behaviors clearly defined
- Monitoring dashboards and alerts specified]]

### 5.1 Error Handling & Resilience

- ⚠️ [ ] Error handling strategy is comprehensive
  - Evidence: "Cite error handling at each layer (UI, API, business logic, data)"
- [ ] Retry policies are defined where appropriate
  - Evidence: "Cite retry strategies for network calls, transient failures"
- [ ] Circuit breakers or fallbacks are specified for critical services
  - Evidence: "Cite circuit breaker thresholds and fallback behaviors"
- [ ] Graceful degradation approaches are defined
  - Evidence: "Cite how system operates with reduced functionality when services fail"
- [ ] System can recover from partial failures
  - Evidence: "Cite self-healing mechanisms or recovery procedures"

### 5.2 Monitoring & Observability

- [ ] Logging strategy is defined
  - Evidence: "Cite logging framework, log levels, structured logging format"
- [ ] Monitoring approach is specified
  - Evidence: "Cite monitoring tools (Datadog, New Relic, CloudWatch, etc.)"
- [ ] Key metrics for system health are identified
  - Evidence: "Cite specific metrics: response time, error rate, throughput, etc."
- [ ] Alerting thresholds and strategies are outlined
  - Evidence: "Cite when alerts fire and who receives them"
- [ ] Debugging and troubleshooting capabilities are built in
  - Evidence: "Cite trace IDs, debug endpoints, diagnostic tools"

### 5.3 Performance & Scaling

- [ ] Performance bottlenecks are identified and addressed
  - Evidence: "Cite potential bottlenecks (database queries, API calls) and optimizations"
- [ ] Caching strategy is defined where appropriate
  - Evidence: "Cite caching layers (CDN, Redis, in-memory) with TTL strategies"
- [ ] Load balancing approach is specified
  - Evidence: "Cite load balancer configuration and distribution strategy"
- [ ] Horizontal and vertical scaling strategies are outlined
  - Evidence: "Cite auto-scaling rules, instance types, scaling triggers"
- [ ] Resource sizing recommendations are provided
  - Evidence: "Cite CPU, memory, storage estimates for each component"

### 5.4 Deployment & DevOps

- [ ] Deployment strategy is defined
  - Evidence: "Cite blue-green, canary, rolling deployment approach"
- [ ] CI/CD pipeline approach is outlined
  - Evidence: "Cite GitHub Actions/Jenkins/etc. with build, test, deploy stages"
- [ ] Environment strategy (dev, staging, prod) is specified
  - Evidence: "Cite environment configurations and promotion process"
- [ ] Infrastructure as Code approach is defined
  - Evidence: "Cite Terraform/CloudFormation/etc. for infrastructure management"
- [ ] Rollback and recovery procedures are outlined
  - Evidence: "Cite rollback strategy and recovery time objectives"

## 6. SECURITY & COMPLIANCE

[[LLM: Security is not optional. Review this section with a hacker's mindset - how could someone exploit this system?

Consider attack vectors:
- Injection attacks (SQL, XSS, command injection)
- Authentication bypass
- Authorization escalation
- Data exposure
- Man-in-the-middle attacks

Also consider compliance: Are there industry-specific regulations that apply?
- GDPR (European users)
- CCPA (California users)
- HIPAA (healthcare)
- PCI-DSS (payments)
- SOC2 (enterprise customers)

Ensure the architecture addresses these proactively with SPECIFIC security controls, not just general statements like "we will secure the system".]]

### 6.1 Authentication & Authorization

- ⚠️ [ ] Authentication mechanism is clearly defined
  - Evidence: "Cite JWT/OAuth 2.0/Session-based with implementation details"
- ⚠️ [ ] Authorization model is specified
  - Evidence: "Cite RBAC/ABAC/claims-based authorization approach"
- [ ] Role-based access control is outlined if required
  - Evidence: "Cite roles, permissions, and access rules"
- [ ] Session management approach is defined
  - Evidence: "Cite token expiration, refresh logic, session storage"
- [ ] Credential management is addressed
  - Evidence: "Cite password hashing (bcrypt/Argon2), secret storage (vault/env vars)"

### 6.2 Data Security

- ⚠️ [ ] Data encryption approach (at rest and in transit) is specified
  - Evidence: "Cite TLS 1.3 for transit, AES-256 for rest, key management"
- ⚠️ [ ] Sensitive data handling procedures are defined
  - Evidence: "Cite PII masking, encryption, access controls"
- [ ] Data retention and purging policies are outlined
  - Evidence: "Cite retention periods and automated purging processes"
- [ ] Backup encryption is addressed if required
  - Evidence: "Cite encrypted backups and key management"
- [ ] Data access audit trails are specified if required
  - Evidence: "Cite audit logging for sensitive data access"

### 6.3 API & Service Security

- [ ] API security controls are defined
  - Evidence: "Cite API authentication, authorization, request signing"
- [ ] Rate limiting and throttling approaches are specified
  - Evidence: "Cite rate limits per user/IP, throttling strategies"
- [ ] Input validation strategy is outlined
  - Evidence: "Cite validation frameworks, sanitization, type checking"
- [ ] CSRF/XSS prevention measures are addressed
  - Evidence: "Cite CSRF tokens, Content Security Policy, input sanitization"
- [ ] Secure communication protocols are specified
  - Evidence: "Cite HTTPS only, TLS version, certificate management"

### 6.4 Infrastructure Security

- [ ] Network security design is outlined
  - Evidence: "Cite VPC, subnets, security groups, network isolation"
- [ ] Firewall and security group configurations are specified
  - Evidence: "Cite ingress/egress rules, port restrictions"
- [ ] Service isolation approach is defined
  - Evidence: "Cite container isolation, service mesh, network policies"
- [ ] Least privilege principle is applied
  - Evidence: "Cite IAM roles, service accounts with minimal permissions"
- [ ] Security monitoring strategy is outlined
  - Evidence: "Cite intrusion detection, vulnerability scanning, security alerts"

## 7. IMPLEMENTATION GUIDANCE

[[LLM: Clear implementation guidance prevents costly mistakes and enables autonomous AI agent implementation.

As you review this section, imagine you're a developer (or AI agent) starting on day one:
- Do they have everything they need to be productive?
- Are coding standards clear enough to maintain consistency?
- Can they write tests without asking questions?
- Is the development workflow obvious?

Look for:
- Specific examples, not just principles
- Code snippets showing patterns
- Clear file naming and organization rules
- Testing patterns with examples
- Development workflow steps

Remember: AI agents excel when patterns are explicit and consistent.]]

### 7.1 Coding Standards & Practices

- [ ] Coding standards are defined
  - Evidence: "Cite language-specific standards, linting rules (ESLint, Prettier)"
- [ ] Documentation requirements are specified
  - Evidence: "Cite inline comment expectations, JSDoc/TSDoc usage"
- ⚠️ [ ] Testing expectations are outlined
  - Evidence: "Cite test coverage targets (80%+), test types required"
- [ ] Code organization principles are defined
  - Evidence: "Cite file organization, module structure, dependency rules"
- [ ] Naming conventions are specified
  - Evidence: "Cite variable, function, class, file naming standards"

### 7.2 Testing Strategy

- ⚠️ [ ] Unit testing approach is defined
  - Evidence: "Cite testing framework (Jest, Vitest), mocking strategy, coverage targets"
- [ ] Integration testing strategy is outlined
  - Evidence: "Cite integration test approach, test environment setup"
- [ ] E2E testing approach is specified
  - Evidence: "Cite E2E framework (Playwright, Cypress), critical path coverage"
- [ ] Performance testing requirements are outlined
  - Evidence: "Cite load testing tools, performance benchmarks"
- [ ] Security testing approach is defined
  - Evidence: "Cite security testing tools (OWASP ZAP, Snyk), scan frequency"
- [ ] Test data management and seeding strategy is defined
  - Evidence: "Cite test fixtures, database seeding, mock data generation approach"
- [ ] CI/CD integration for automated testing is specified
  - Evidence: "Cite test execution in pipeline, test reporting, failure handling"

### 7.3 Frontend Testing [[FRONTEND ONLY]]

[[LLM: Skip this subsection for backend-only projects.]]

- [ ] Component testing scope and tools defined
  - Evidence: "Cite React Testing Library/Vue Test Utils with component test patterns"
- [ ] UI integration testing approach specified
  - Evidence: "Cite user flow testing, interaction testing approach"
- [ ] Visual regression testing considered
  - Evidence: "Cite Chromatic/Percy or screenshot comparison approach"
- [ ] Accessibility testing tools identified
  - Evidence: "Cite axe-core, WAVE, or accessibility testing approach"
- [ ] Frontend-specific test data management addressed
  - Evidence: "Cite mock data, fixtures, API mocking (MSW, etc.)"

### 7.4 Development Environment

- [ ] Local development environment setup is documented
  - Evidence: "Cite setup instructions, prerequisites, environment variables"
- [ ] Required tools and configurations are specified
  - Evidence: "Cite IDE, Node version (nvm), Docker, database setup"
- [ ] Development workflows are outlined
  - Evidence: "Cite branch strategy, commit conventions, PR process"
- [ ] Environment variable management and secrets handling is defined
  - Evidence: "Cite .env structure, secrets manager usage, local vs production config"
- [ ] Debugging and troubleshooting guidance is provided
  - Evidence: "Cite logging levels, debug tools, common issues and solutions"
- [ ] Source control practices are defined
  - Evidence: "Cite Git workflow, branch naming, commit message format"
- [ ] Dependency management approach is specified
  - Evidence: "Cite package manager (npm/yarn/pnpm), lock file usage"

### 7.5 Technical Documentation

- [ ] API documentation standards are defined
  - Evidence: "Cite OpenAPI/Swagger, API doc generation tools"
- [ ] Architecture documentation requirements are specified
  - Evidence: "Cite ADRs, architecture diagrams, component documentation"
- [ ] Code documentation expectations are outlined
  - Evidence: "Cite inline comments, README standards, doc generation"
- [ ] System diagrams and visualizations are included
  - Evidence: "Cite C4 diagrams, sequence diagrams, data flow diagrams"
- [ ] Decision records for key choices are included
  - Evidence: "Cite ADR format and examples for major decisions"

## 8. DEPENDENCY & INTEGRATION MANAGEMENT

[[LLM: Dependencies are often the source of production issues. For each dependency, consider:

- What happens if it's unavailable (downtime, API limits)?
- Is there a newer version with security patches?
- Are we locked into a vendor (vendor lock-in)?
- What's our contingency plan if the service shuts down?
- Are licensing terms acceptable?

Verify:
- Specific versions defined (not "latest")
- Fallback strategies for critical dependencies
- Update/patching process clear
- No circular dependencies]]

### 8.1 External Dependencies

- ⚠️ [ ] All external dependencies are identified
  - Evidence: "Cite complete list of third-party libraries, APIs, services"
- ⚠️ [ ] Versioning strategy for dependencies is defined
  - Evidence: "Cite version pinning strategy, update frequency, compatibility checks"
- [ ] Fallback approaches for critical dependencies are specified
  - Evidence: "Cite what happens if third-party API fails, alternative services"
- [ ] Licensing implications are addressed
  - Evidence: "Cite license compatibility check, no GPL in proprietary code"
- [ ] Update and patching strategy is outlined
  - Evidence: "Cite Dependabot/Renovate, security patch process"

### 8.2 Internal Dependencies

- [ ] Component dependencies are clearly mapped
  - Evidence: "Cite dependency graph or component dependency list"
- [ ] Build order dependencies are addressed
  - Evidence: "Cite build sequence for multi-package projects"
- [ ] Shared services and utilities are identified
  - Evidence: "Cite shared libraries, common utilities, design system packages"
- [ ] Circular dependencies are eliminated
  - Evidence: "Verify no circular imports or component dependencies"
- [ ] Versioning strategy for internal components is defined
  - Evidence: "Cite semantic versioning, changelog, breaking change process"

### 8.3 Third-Party Integrations

- [ ] All third-party integrations are identified
  - Evidence: "Cite payment gateways, analytics, email services, etc."
- [ ] Integration approaches are defined
  - Evidence: "Cite SDK usage, direct API calls, webhook handling"
- ⚠️ [ ] Authentication with third parties is addressed
  - Evidence: "Cite API key management, OAuth flows, secret storage"
- [ ] Error handling for integration failures is specified
  - Evidence: "Cite retry logic, fallbacks, user messaging for integration failures"
- [ ] Rate limits and quotas are considered
  - Evidence: "Cite rate limiting awareness, quota monitoring, throttling"

## 9. AI AGENT IMPLEMENTATION SUITABILITY

[[LLM: This architecture may be implemented by AI agents. Review with extreme clarity in mind.

AI agents excel when:
- Patterns are consistent and predictable
- Complexity is minimized and well-documented
- File structures are logical and hierarchical
- Naming conventions are clear
- Examples are provided for unfamiliar patterns

AI agents struggle when:
- Implicit knowledge is required
- Patterns vary across components
- Complex interactions without clear documentation
- Ambiguous naming or structure
- "Clever" code without explanation

As you validate, ask:
- Would an AI agent make incorrect assumptions?
- Are patterns explicit and consistent?
- Is complexity justified and well-documented?
- Are examples provided for complex patterns?

Remember: Explicit > Implicit, Simple > Clever, Consistent > Creative]]

### 9.1 Modularity for AI Agents

- ⚠️ [ ] Components are sized appropriately for AI agent implementation
  - Evidence: "Components are 200-500 lines max, single responsibility"
- [ ] Dependencies between components are minimized
  - Evidence: "Loose coupling, minimal cross-component dependencies"
- [ ] Clear interfaces between components are defined
  - Evidence: "Explicit API contracts, TypeScript interfaces, prop definitions"
- [ ] Components have singular, well-defined responsibilities
  - Evidence: "Each component does one thing well, no god objects"
- ⚠️ [ ] File and code organization optimized for AI agent understanding
  - Evidence: "Logical file structure, predictable naming, clear hierarchy"

### 9.2 Clarity & Predictability

- ⚠️ [ ] Patterns are consistent and predictable
  - Evidence: "Same patterns used throughout (e.g., all API calls use same service layer pattern)"
- [ ] Complex logic is broken down into simpler steps
  - Evidence: "Complex algorithms explained with comments, broken into helper functions"
- [ ] Architecture avoids overly clever or obscure approaches
  - Evidence: "No magic, no hidden behavior, no implicit conventions"
- [ ] Examples are provided for unfamiliar patterns
  - Evidence: "Code examples or references for non-standard patterns"
- [ ] Component responsibilities are explicit and clear
  - Evidence: "Component purpose stated clearly in documentation"

### 9.3 Implementation Guidance

- ⚠️ [ ] Detailed implementation guidance is provided
  - Evidence: "Step-by-step implementation instructions, not just high-level descriptions"
- [ ] Code structure templates are defined
  - Evidence: "Cite component templates, file boilerplate, code scaffolding"
- [ ] Specific implementation patterns are documented
  - Evidence: "Cite patterns with code examples (hooks, HOCs, services, etc.)"
- [ ] Common pitfalls are identified with solutions
  - Evidence: "Cite known issues and how to avoid them"
- [ ] References to similar implementations are provided when helpful
  - Evidence: "Cite reference projects, libraries, or documentation"

### 9.4 Error Prevention & Handling

- [ ] Design reduces opportunities for implementation errors
  - Evidence: "Type safety, validation, guard clauses prevent errors"
- [ ] Validation and error checking approaches are defined
  - Evidence: "Cite input validation, runtime checks, type guards"
- [ ] Self-healing mechanisms are incorporated where possible
  - Evidence: "Cite auto-retry, fallbacks, default values"
- [ ] Testing patterns are clearly defined
  - Evidence: "Cite test templates, testing utilities, test patterns"
- [ ] Debugging guidance is provided
  - Evidence: "Cite logging statements, debug endpoints, troubleshooting steps"

### 9.5 AI Coding Standards & Infrastructure

[[LLM: AI agents need explicit infrastructure, automation, and operational clarity. Implicit conventions and manual processes create implementation barriers. Validate that the architecture explicitly defines:
- Build and deployment automation
- Development environment reproducibility
- Clear operational procedures
- Infrastructure as code patterns]]

- ⚠️ [ ] Code organization designed for AI agent navigation
  - Evidence: "Logical directory structure, consistent file placement, predictable module organization"
- ⚠️ [ ] File naming conventions are consistent and predictable
  - Evidence: "All files follow same naming pattern (kebab-case, PascalCase, etc.)"
- [ ] Dependencies are explicitly declared (no implicit imports)
  - Evidence: "All imports explicit, no global dependencies, dependency injection used"
- [ ] Configuration is externalized (no hardcoded values)
  - Evidence: "Environment variables, config files, feature flags - no magic values in code"
- ⚠️ [ ] Validation commands are project-specific and executable
  - Evidence: "npm test, npm run lint commands defined and functional"
- [ ] Test patterns are consistent across all components
  - Evidence: "All tests follow same structure (AAA, Given-When-Then), same tools/mocking"
- [ ] Error messages are descriptive and actionable
  - Evidence: "Errors include context, suggested fixes, not just 'Something went wrong'"
- [ ] Documentation is inline and up-to-date
  - Evidence: "JSDoc/TSDoc comments, inline explanations for complex logic"
- [ ] API contracts are explicit (OpenAPI, GraphQL schema, etc.)
  - Evidence: "API documented with schemas, types, validation rules"
- [ ] Database migrations are version-controlled
  - Evidence: "Migration files timestamped, reversible, tracked in version control"
- [ ] Build process is automated and documented
  - Evidence: "README explains build steps, CI/CD automates builds"
- [ ] Local development environment is reproducible
  - Evidence: "Docker Compose, detailed setup docs, dependency versions locked"
- ⚠️ [ ] Deployment process is documented step-by-step
  - Evidence: "Deployment runbook, automated deployment scripts, rollback procedures"
- [ ] Monitoring and logging infrastructure defined
  - Evidence: "Logging framework configured, metrics collection setup, dashboards planned"
- [ ] Rollback procedures documented
  - Evidence: "Database rollback scripts, deployment rollback process, data recovery plan"

## 10. ACCESSIBILITY IMPLEMENTATION [[FRONTEND ONLY]]

[[LLM: Skip this section for backend-only projects. Accessibility is a core requirement for any user interface.

Accessibility is not optional or nice-to-have - it's:
1. A legal requirement (ADA, Section 508)
2. A business opportunity (15% of population has disabilities)
3. A UX best practice (benefits all users)

When validating, ensure:
- Semantic HTML is the default, not ARIA-heavy hacks
- Keyboard navigation works for ALL interactive elements
- Screen reader support is first-class, not an afterthought
- Color contrast meets WCAG AA minimum
- Focus management is intentional and clear]]

### 10.1 Accessibility Standards

- [ ] Semantic HTML usage is emphasized
  - Evidence: "Cite requirement to use <button>, <nav>, <main>, etc. over <div>"
- [ ] ARIA implementation guidelines provided
  - Evidence: "Cite when to use ARIA, aria-label requirements, role usage"
- [ ] Keyboard navigation requirements defined
  - Evidence: "Cite tab order, keyboard shortcuts, focus management"
- [ ] Focus management approach specified
  - Evidence: "Cite focus trap in modals, focus restoration, skip links"
- [ ] Screen reader compatibility addressed
  - Evidence: "Cite screen reader testing, announcements, live regions"

### 10.2 Accessibility Testing

- [ ] Accessibility testing tools identified
  - Evidence: "Cite axe DevTools, WAVE, Lighthouse accessibility audits"
- [ ] Testing process integrated into workflow
  - Evidence: "Cite automated a11y tests in CI, manual testing checklist"
- [ ] Compliance targets (WCAG level) specified
  - Evidence: "Cite WCAG 2.1 AA compliance target or higher"
- [ ] Manual testing procedures defined
  - Evidence: "Cite keyboard-only testing, screen reader testing process"
- [ ] Automated testing approach outlined
  - Evidence: "Cite jest-axe, pa11y, or automated a11y testing in pipeline"

---

## SCORING & VALIDATION SUMMARY

[[LLM: Calculate quality score and generate comprehensive report

**Scoring Calculation:**

1. Count total validation items attempted (exclude skipped sections)
2. Count critical failures (⚠️ items that failed)
3. Count standard failures (non-critical items that failed)
4. Calculate: **Score = 100 - (10 × critical_failures) - (5 × standard_failures)**
5. Determine status:
   - **APPROVED (90-100)**: Proceed to PRP phase immediately
   - **CONDITIONAL (70-89)**: Proceed with noted improvements
   - **REJECTED (0-69)**: Must fix critical issues before proceeding

**Report Structure:**

# Architect Quality Gate Validation Report

**Phase**: Architect
**Checklist**: architect-quality-gate.md
**Document**: docs/architecture.md
**Timestamp**: {iso_timestamp}
**Mode**: {interactive|batch|yolo}

## Overall Result

**Status**: {APPROVED|CONDITIONAL|REJECTED}
**Score**: {score}/100
**Total Items**: {total}
**Passed**: {passed}
**Failed**: {failed} ({critical_failures} critical, {standard_failures} standard)

## Section Results

### 1. Requirements Alignment (15 items)
- Passed: X/15
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 2. Architecture Fundamentals (21 items)
- Passed: X/21
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 3. Technical Stack & Decisions (21 items)
- Passed: X/21
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 4. Frontend Design & Implementation [[FRONTEND ONLY]] (36 items)
- Passed: X/36
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE | 🚫 SKIPPED}

### 5. Resilience & Operational Readiness (20 items)
- Passed: X/20
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 6. Security & Compliance (16 items)
- Passed: X/16
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 7. Implementation Guidance (23 items)
- Passed: X/23
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 8. Dependency & Integration Management (15 items)
- Passed: X/15
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 9. AI Agent Implementation Suitability (16 items)
- Passed: X/16
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 10. Accessibility Implementation [[FRONTEND ONLY]] (10 items)
- Passed: X/10
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE | 🚫 SKIPPED}

## Failed Items Detail

[For each failed item, provide:]

**Item**: {checklist item text}
**Section**: {section number and name}
**Criticality**: {⚠️ CRITICAL | STANDARD}
**Evidence Requirement**: {what evidence was expected}
**Why It Failed**: {specific reason for failure}
**Impact on Score**: {-5 or -10}
**Recommendation**: {specific action to fix}

## Recommendations

### High Priority (Blocking or Critical)

1. **[Specific action to address critical failure]**
   - Why: {impact of not fixing}
   - How: {specific steps to resolve}
   - Effort: {time estimate}

2. ...

### Medium Priority (Quality Improvements)

1. **[Specific action to improve quality]**
   - Why: {benefit of fixing}
   - How: {specific steps to resolve}
   - Effort: {time estimate}

2. ...

### Low Priority (Nice to Have)

1. **[Optional improvements]**
   - Why: {minor benefit}
   - How: {specific steps to resolve}
   - Effort: {time estimate}

2. ...

## Risk Assessment

### Top 5 Risks by Severity

1. **{Risk Name}**
   - Severity: {High|Medium|Low}
   - Likelihood: {High|Medium|Low}
   - Impact: {description of potential impact}
   - Mitigation: {recommended mitigation strategy}

2. ...

## AI Implementation Readiness

**Overall AI Readiness**: {High|Medium|Low}

### Specific Concerns for AI Agent Implementation
- {Concern 1: specific area of ambiguity or complexity}
- {Concern 2: inconsistent patterns}
- {Concern 3: missing implementation guidance}
- ...

### Areas Needing Additional Clarification
- {Area 1: unclear component interactions}
- {Area 2: vague error handling}
- {Area 3: missing examples}
- ...

### Complexity Hotspots to Address
- {Hotspot 1: overly complex component}
- {Hotspot 2: unclear data flow}
- {Hotspot 3: implicit dependencies}
- ...

## Frontend-Specific Assessment (if applicable)

**Frontend Architecture Completeness**: {High|Medium|Low}

### Alignment Between Main and Frontend Architecture Docs
- {Assessment of consistency between architecture.md and frontend-architecture.md}
- {Conflicts or discrepancies identified}
- {Recommendations for alignment}

### UI/UX Specification Coverage
- {Assessment of UI component coverage}
- {Missing UI specifications}
- {Clarity of component contracts}

### Component Design Clarity
- {Assessment of component architecture}
- {Reusability and composability}
- {State management clarity}

## Next Steps

**If APPROVED (90-100)**:
✅ Proceed to PRP phase immediately
✅ All critical requirements met
✅ High confidence in AI agent implementation success
✅ Architecture is clear, complete, and actionable

**If CONDITIONAL (70-89)**:
⚠️ May proceed to PRP phase
⚠️ Address high-priority recommendations during or after PRP creation
⚠️ Document known gaps in PRP phase
⚠️ Risk: Minor clarifications may be needed during implementation (5-10 hours potential rework)
⚠️ Consider addressing critical gaps before PRP if time permits

**If REJECTED (0-69)**:
❌ **BLOCK** progression to PRP phase
❌ Must address all critical failures before proceeding
❌ Re-run architect quality gate after fixes
❌ Risk: High downstream rework if proceeding (20+ hours of rework expected)
❌ Implementation will likely fail without architecture improvements

## Evidence Summary

**Evidence Collection Quality**:
- Strong Evidence: X items (specific citations, line numbers, quotes)
- Weak Evidence: Y items (vague references, general statements)
- No Evidence: Z items (assumptions, no citations)

**Evidence-Based Confidence**: {High|Medium|Low}

## Project Type Classification

**Project Type**: {Full-Stack | Frontend-Only | Backend-Only | Service/API}
**Sections Evaluated**: {total sections applicable to this project type}
**Sections Skipped**: {sections skipped due to project type}

**Skipped Sections**:
- {Section name} - Reason: {why skipped}
- ...

## Save Results

Save validation results to:
`.codex/state/quality-gate-architect-{timestamp}.json`

Update workflow.json:
```json
{
  "quality_gate_results": {
    "architect": {
      "timestamp": "{iso_timestamp}",
      "status": "{APPROVED|CONDITIONAL|REJECTED}",
      "score": {score},
      "checklist": "architect-quality-gate.md",
      "mode": "{interactive|batch|yolo}",
      "total_items": {total},
      "passed": {passed},
      "failed": {failed},
      "critical_failures": {critical_failures},
      "standard_failures": {standard_failures},
      "project_type": "{full-stack|frontend-only|backend-only|service}",
      "sections_skipped": {count},
      "summary": "{one-line summary}"
    }
  },
  "quality_scores": {
    "architect": {score}
  }
}
```

After presenting the report, ask the user if they would like:
1. Detailed analysis of any specific section
2. Specific recommendations for failed items
3. Code examples for implementation guidance gaps
4. Architectural decision record (ADR) templates for key decisions

]]

---

**Checklist Version**: 1.0
**Total Items**: 177 (excludes conditional frontend sections for backend-only projects)
**Critical Items**: 38 (marked with ⚠️)
**Last Updated**: 2025-10-07
**Maintained By**: CODEX Quality Team
**Related Documents**:
- quality-scoring-rubric.md (scoring methodology)
- architecture-template.yaml (architecture structure)
- prd-template.yaml (requirements reference)
- pm-quality-gate.md (previous phase validation)
- execute-quality-gate.md (quality gate execution guide)
