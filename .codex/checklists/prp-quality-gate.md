# PRP (Project Requirements Package) Quality Gate Checklist

This checklist validates the PRP before execution to ensure one-pass implementation success. It ensures complete context, unambiguous guidance, and executable validation that enables autonomous AI implementation without additional clarification.

[[LLM: INITIALIZATION INSTRUCTIONS - PRP QUALITY GATE

Before proceeding with this checklist, ensure you have access to:

1. **The PRP document** - The Project Requirements Package being validated
2. **docs/architecture.md** - Architecture document for pattern/constraint verification
3. **docs/prd.md** - Product Requirements Document for requirement traceability
4. **Codebase files** referenced in the PRP - Verify actual accessibility
5. **.codex/state/workflow.json** - Current workflow state
6. **.codex/templates/prp-enhanced-template.md** - Template structure reference

IMPORTANT: If the PRP or any referenced files are missing, immediately request their location before proceeding.

CRITICAL PHILOSOPHY - THE ZERO-KNOWLEDGE TEST:

The PRP must enable successful implementation by someone with:
✅ General programming knowledge
✅ Access to codebase files
✅ ONLY the PRP content
❌ NO additional context or clarification
❌ NO prior knowledge of this project
❌ NO assumptions about conventions

**If the answer to "Can a fresh Claude instance implement this with ONLY the PRP?" is NO, the PRP FAILS this quality gate.**

VALIDATION APPROACH:

1. **Context Completeness** - All information needed is present and accessible
2. **Implementation Clarity** - Tasks are unambiguous with concrete guidance
3. **Validation Readiness** - All validation commands are executable, not placeholders
4. **Evidence-Based** - Cite specific PRP sections, file paths, and validation commands
5. **Zero-Knowledge Focus** - No implicit knowledge or assumptions required

EXECUTION MODE:

Ask the user which mode to use:

- **Interactive** - Review section by section, collect evidence, confirm before next section
- **Batch** - Complete full analysis, present comprehensive report at end
- **YOLO** - Skip validation (logs violation to workflow.json)

For interactive/batch modes:
- Collect specific evidence for each item (cite PRP sections/lines)
- Mark items as ⚠️ CRITICAL or standard
- Calculate score: 100 - (10 × critical_fails) - (5 × standard_fails)
- Determine status: APPROVED (90-100), CONDITIONAL (70-89), REJECTED (0-69)

After validation, save results to:
- `.codex/state/quality-gate-prp-{timestamp}.json`
- Update `workflow.json` quality_gate_results

See: `.codex/data/quality-scoring-rubric.md` for detailed scoring methodology]]

## 1. CONTEXT COMPLETENESS

[[LLM: Context completeness is the foundation of one-pass implementation success. Every reference must be:
- Accessible (files exist at specified paths)
- Specific (not generic examples)
- Complete (includes version numbers, gotchas, constraints)
- Verified (you must check file accessibility)

This section has the highest concentration of CRITICAL items because missing context = guaranteed implementation failure.

Evidence requirement: For each file reference, verify it exists. For each library/version, cite where it's specified. For each pattern, verify line numbers are correct.]]

### 1.1 File References & Accessibility

- ⚠️ [ ] All referenced codebase files exist and are accessible at specified paths
  - Evidence: "Verify each file path in 'All Needed Context' section exists via Read tool"
- ⚠️ [ ] All file paths use absolute paths (not relative)
  - Evidence: "Check all file paths start with project root or are clearly documented"
- [ ] Referenced files are read-accessible (no permission issues)
  - Evidence: "Attempt to Read each referenced file"
- [ ] File references include specific line numbers for patterns
  - Evidence: "Cite example: 'src/auth/service.swift lines 45-67 for error handling pattern'"
- [ ] No broken or outdated file references
  - Evidence: "All files referenced still exist at current commit"

### 1.2 Code Examples & Patterns

- ⚠️ [ ] Code examples are project-specific, not generic
  - Evidence: "Examples use actual project types, not placeholder 'YourModel' or 'ExampleService'"
- ⚠️ [ ] Codebase patterns cited with specific line numbers
  - Evidence: "Pattern references like 'Follow pattern in src/foo.swift:23-45' with actual numbers"
- [ ] Pattern references explain WHAT to replicate
  - Evidence: "Each pattern includes 'why' and 'what to replicate' guidance"
- [ ] Anti-patterns are documented with explanations
  - Evidence: "Anti-patterns section explains why certain approaches should be avoided"
- [ ] Existing code patterns are validated for current best practices
  - Evidence: "Patterns referenced are good examples, not legacy code to avoid"

### 1.3 Library & Technology Versions

- ⚠️ [ ] All library versions explicitly stated (not "latest" or "current")
  - Evidence: "Cite specific versions like 'React 18.2.0' not 'React latest'"
- ⚠️ [ ] Technology stack versions match architecture.md
  - Evidence: "Cross-reference versions in PRP with architecture document"
- [ ] Version compatibility constraints documented
  - Evidence: "Known version conflicts or requirements stated"
- [ ] Dependency installation commands are specific
  - Evidence: "Commands include exact versions: 'npm install react@18.2.0'"
- [ ] Breaking changes or migration notes included for versions
  - Evidence: "Known breaking changes from earlier versions documented"

### 1.4 Documentation & External References

- [ ] External URLs include section anchors where applicable
  - Evidence: "URLs like 'https://docs.example.com/guide#specific-section' not just base URL"
- [ ] Documentation references specify which sections to read
  - Evidence: "References like 'See React Hooks docs, useEffect section' not just 'Read React docs'"
- [ ] API documentation links are current and accessible
  - Evidence: "Verify links return 200 status, not 404 or redirect"
- [ ] Documentation version matches library version
  - Evidence: "Documentation URL includes version: '/v18.2/docs/hooks' not '/latest/docs/hooks'"
- [ ] Critical information from docs is summarized in PRP
  - Evidence: "Key constraints/requirements extracted into PRP, not just linked"

### 1.5 Known Gotchas & Constraints

- ⚠️ [ ] Known gotchas are explicitly documented
  - Evidence: "Section includes technology-specific constraints like 'SwiftUI requires @MainActor for UI updates'"
- ⚠️ [ ] Architectural constraints from architecture.md are included
  - Evidence: "Cross-reference constraints in PRP with architecture document"
- [ ] Performance constraints are specified with thresholds
  - Evidence: "Concrete limits like 'Batch operations limited to 5000 items' not 'Keep batches small'"
- [ ] Security requirements and constraints are clear
  - Evidence: "Specific security measures like 'All user input must use DOMPurify.sanitize()'"
- [ ] Environment-specific constraints are documented
  - Evidence: "Platform limitations like 'localStorage max 5MB in Safari' if relevant"

### 1.6 Context Window & Synthesis

- ⚠️ [ ] Zero-knowledge test explicitly addressed
  - Evidence: "PRP includes section validating fresh Claude could implement with only PRP"
- ⚠️ [ ] No assumptions of prior project knowledge
  - Evidence: "All project conventions, patterns, and structures are explained"
- [ ] Template variables are resolved (no {{PLACEHOLDER}} text)
  - Evidence: "No unresolved template syntax like {{PROJECT_NAME}} or {{TBD}}"
- [ ] Workflow context synthesis is complete
  - Evidence: "PRP synthesizes relevant info from project-brief, PRD, and architecture"
- [ ] All acronyms and domain terms are defined
  - Evidence: "First use of specialized terms includes definition or glossary reference"

## 2. IMPLEMENTATION CLARITY

[[LLM: Implementation clarity determines whether an AI agent can execute without ambiguity. Each task must be:
- Ordered by dependencies (clear sequence)
- Specific about file paths and naming
- Concrete about patterns to follow
- Measurable for success criteria

Vague guidance like "implement authentication" fails. Specific guidance like "CREATE src/auth/service.ts following pattern from src/api/base-service.ts:15-40" succeeds.

Evidence requirement: For each task, verify it has exact file path, clear pattern, and measurable validation.]]

### 2.1 Task Sequencing & Dependencies

- ⚠️ [ ] Tasks are ordered by dependencies (buildable order)
  - Evidence: "Task dependencies are explicit: 'Task 2 depends on Task 1 completion'"
- ⚠️ [ ] Each task specifies exact file paths to create/modify
  - Evidence: "Tasks use concrete paths like 'CREATE src/features/auth/login-view.tsx' not 'Create login component'"
- [ ] Parallel tasks are clearly identified
  - Evidence: "Tasks that can be done independently are marked or grouped separately"
- [ ] Critical path is identifiable
  - Evidence: "Core feature tasks vs. optional enhancements are distinguished"
- [ ] Task completion criteria are defined
  - Evidence: "Each task includes validation: 'DONE WHEN: Tests pass and component renders'"

### 2.2 File Path & Naming Guidance

- ⚠️ [ ] Naming conventions are explicitly defined
  - Evidence: "Conventions stated like 'Use kebab-case for files: user-profile.tsx'"
- [ ] File placement guidance is clear and specific
  - Evidence: "Clear structure like 'Place in src/features/[feature-name]/components/'"
- [ ] New directories are explicitly created in sequence
  - Evidence: "Tasks include 'CREATE DIRECTORY src/features/auth/' before creating files in it"
- [ ] File organization follows architecture.md structure
  - Evidence: "Cross-reference PRP file structure with architecture document"
- [ ] Related files are grouped logically in tasks
  - Evidence: "Tasks group related files: model + service + view together"

### 2.3 Pattern References & Specificity

- ⚠️ [ ] Pattern references are specific with line numbers
  - Evidence: "References like 'Follow error handling in src/utils/errors.ts:12-28' not 'Use similar error handling'"
- [ ] Patterns explain WHAT aspects to replicate
  - Evidence: "Guidance like 'Replicate async/await pattern and error boundaries' not just 'Follow this pattern'"
- [ ] Multiple patterns for complex tasks are provided
  - Evidence: "Complex features reference multiple examples for different aspects"
- [ ] Pattern adaptations are explained
  - Evidence: "When pattern needs modification: 'Use X pattern but replace Y with Z because...'"
- [ ] Conflicting patterns are resolved with guidance
  - Evidence: "If multiple patterns exist: 'Use pattern A for UI, pattern B for logic' with rationale"

### 2.4 Validation Commands & Success Criteria

- ⚠️ [ ] Validation commands are project-specific (not placeholders)
  - Evidence: "Commands like 'npm run test:auth' not '{{RUN_TESTS}}' or 'run your tests'"
- ⚠️ [ ] Success criteria are measurable and testable
  - Evidence: "Criteria like 'All 15 unit tests pass' not 'Code works correctly'"
- [ ] Each task has clear validation approach
  - Evidence: "Every task includes how to verify completion"
- [ ] Validation commands are ordered by execution
  - Evidence: "Level 1-4 validation with clear sequence: syntax → unit → integration → acceptance"
- [ ] Expected output/behavior is specified
  - Evidence: "Commands include expected results: 'Expected: 0 errors, 0 warnings'"

### 2.5 Error Handling & Edge Cases

- [ ] Error handling approach is specified
  - Evidence: "Tasks include error handling: 'Wrap in try-catch, use ErrorBoundary for UI errors'"
- [ ] Edge cases are identified and addressed
  - Evidence: "Edge cases documented: 'Handle empty state, loading state, error state'"
- [ ] Fallback strategies are defined
  - Evidence: "Fallbacks specified: 'If API fails, show cached data with stale indicator'"
- [ ] Input validation requirements are clear
  - Evidence: "Validation rules like 'Email must match RFC 5322, max 254 chars'"
- [ ] Error messages and user feedback are specified
  - Evidence: "Error UX defined: 'Show toast notification with retry button'"

### 2.6 Rollback & Recovery Strategy

- [ ] Rollback strategy is defined for risky tasks
  - Evidence: "Migration tasks include rollback: 'Keep backup table, drop after verification'"
- [ ] Partial completion handling is addressed
  - Evidence: "Guidance for interrupted tasks: 'Check if directory exists before mkdir'"
- [ ] Destructive operations are flagged with warnings
  - Evidence: "Warnings like 'DANGER: This deletes existing data. Backup first.'"
- [ ] Recovery steps for common failures are documented
  - Evidence: "Troubleshooting: 'If build fails with error X, run Y command'"
- [ ] State cleanup is included in tasks
  - Evidence: "Tasks include cleanup: 'Remove test data after validation'"

## 3. VALIDATION READINESS

[[LLM: Validation readiness ensures the PRP can be verified at every level. This is critical for:
- Immediate feedback during implementation
- Quality assurance before completion
- Acceptance testing against PRD requirements

The most critical aspect: ALL validation commands must be EXECUTABLE, not placeholders. "npm test" fails if project uses "yarn test". "{{RUN_TESTS}}" always fails.

Evidence requirement: For each validation level, cite exact commands and verify they match project configuration.]]

### 3.1 Level 1: Syntax & Style Validation

- ⚠️ [ ] Level 1 validation commands are specified and executable
  - Evidence: "Commands like 'npm run lint' or 'swiftlint --strict' not generic 'run linter'"
- ⚠️ [ ] Commands match project build tools from architecture.md
  - Evidence: "Cross-reference linting/formatting commands with architecture dev tooling section"
- [ ] Expected output is specified for passing validation
  - Evidence: "Expected: '0 errors, 0 warnings' or specific exit codes"
- [ ] Formatting requirements are defined
  - Evidence: "Formatting rules specified: 'Run prettier --write or swift-format'"
- [ ] Style guide references are included
  - Evidence: "Link to style guide or .eslintrc/.swiftlint.yml configuration"

### 3.2 Level 2: Unit Test Validation

- ⚠️ [ ] Level 2 validation commands are executable (not placeholders)
  - Evidence: "Commands like 'jest --testPathPattern=features/auth' not '{{RUN_UNIT_TESTS}}'"
- ⚠️ [ ] Test coverage requirements are defined with percentages
  - Evidence: "Coverage target: 'Minimum 80% line coverage, 70% branch coverage'"
- [ ] Test framework and structure are specified
  - Evidence: "Test structure: 'Use Jest with React Testing Library, follow AAA pattern'"
- [ ] Test file naming and location are defined
  - Evidence: "Test files: 'Place in __tests__/ or use .test.ts suffix'"
- [ ] Mock/fixture strategies are documented
  - Evidence: "Mocking approach: 'Use MSW for API mocks, fixtures in __fixtures__/'"
- [ ] All test categories are covered
  - Evidence: "Test types specified: unit tests, component tests, hook tests"

### 3.3 Level 3: Integration Test Validation

- ⚠️ [ ] Level 3 validation commands are executable
  - Evidence: "Commands like 'npm run test:integration' or 'xcodebuild test -scheme MyApp'"
- [ ] Integration test strategy is clear and specific
  - Evidence: "Integration testing: 'Test API integration with test database, validate state management'"
- [ ] Integration points from architecture are validated
  - Evidence: "Tests cover integration points listed in architecture.md"
- [ ] Environment setup for integration tests is documented
  - Evidence: "Setup: 'Run docker-compose up -d for test database before tests'"
- [ ] Integration test scope is defined
  - Evidence: "Scope: 'Test component → service → API flow, not full E2E'"
- [ ] Data seeding/cleanup is addressed
  - Evidence: "Data management: 'Seed test data before tests, cleanup in afterEach'"

### 3.4 Level 4: Acceptance Test Validation

- ⚠️ [ ] Level 4 validation commands are specified
  - Evidence: "Commands like 'npm run test:e2e' or language-specific agent validation"
- [ ] Acceptance criteria from PRD are testable
  - Evidence: "Each PRD acceptance criterion has corresponding test validation"
- [ ] User journey validation is defined
  - Evidence: "E2E tests validate complete user flows from PRD"
- [ ] Performance criteria from NFRs are validated
  - Evidence: "Performance tests: 'Load time < 2s, measured via Lighthouse or performance.now()'"
- [ ] Security requirements are validated
  - Evidence: "Security validation: 'Run OWASP ZAP scan, validate CORS policy, test auth flows'"
- [ ] Acceptance test execution environment is specified
  - Evidence: "Environment: 'Run against staging environment with production-like data'"

### 3.5 Domain-Specific Validation

- [ ] Technology-specific validation is included
  - Evidence: "Platform tests: 'iOS Simulator validation, Android emulator tests'"
- [ ] Accessibility validation is specified (if UI project)
  - Evidence: "A11y tests: 'axe-core audit, keyboard navigation testing, screen reader verification'"
- [ ] Cross-browser/platform testing is defined (if applicable)
  - Evidence: "Browser matrix: 'Test on Chrome 120+, Firefox 115+, Safari 17+'"
- [ ] Performance benchmarks are measurable
  - Evidence: "Benchmarks: 'API response < 200ms p95, render time < 16ms'"
- [ ] Load/stress testing criteria are defined (if applicable)
  - Evidence: "Load testing: 'Handle 1000 concurrent users, response time < 500ms under load'"

### 3.6 Quality Gates & Enforcement

- ⚠️ [ ] All validation levels have concrete, executable commands
  - Evidence: "No placeholders or generic 'run tests' - every level has project-specific command"
- [ ] Quality gates are enforceable (pass/fail criteria)
  - Evidence: "Clear thresholds: 'Gate fails if coverage < 80% or any test fails'"
- [ ] Validation sequence is clear (Level 1 → 2 → 3 → 4)
  - Evidence: "Levels ordered: syntax → unit → integration → acceptance"
- [ ] CI/CD validation is documented (if applicable)
  - Evidence: "CI pipeline: 'GitHub Actions runs all validation levels on PR'"
- [ ] Manual validation steps are clearly identified
  - Evidence: "Manual tests: 'Verify UI in browser, test on physical device'"

## 4. IMPLEMENTATION BLUEPRINT QUALITY

[[LLM: The implementation blueprint is the detailed roadmap for execution. It must be:
- Complete (all necessary components addressed)
- Coherent (components fit together logically)
- Concrete (specific technical details, not abstractions)
- Connected (integration points clearly defined)

This section validates that the blueprint can guide implementation without gaps or ambiguity.]]

### 4.1 Data Models & Structure

- [ ] Data models are complete with all properties
  - Evidence: "Models include all fields from PRD data requirements"
- [ ] Data types and constraints are specified
  - Evidence: "Types defined: 'email: string (validated, max 254 chars), age: number (min 0, max 150)'"
- [ ] Relationships between entities are defined
  - Evidence: "Relationships: 'User hasMany Posts, Post belongsTo User' with foreign key details"
- [ ] Validation rules are documented
  - Evidence: "Validation: 'Email matches RFC 5322, username alphanumeric 3-20 chars'"
- [ ] Persistence strategy is clear
  - Evidence: "Storage: 'PostgreSQL for relational data, Redis for session cache'"

### 4.2 API & Interface Design

- [ ] API endpoints are fully specified (if applicable)
  - Evidence: "Endpoints: 'POST /api/auth/login {email, password} → {token, user}'"
- [ ] Request/response formats are defined
  - Evidence: "Formats: 'JSON with camelCase, ISO 8601 dates, error format: {code, message, details}'"
- [ ] Authentication/authorization is specified
  - Evidence: "Auth: 'Bearer token in Authorization header, JWT with 1h expiry'"
- [ ] Error responses are documented
  - Evidence: "Errors: '400 Bad Request with validation details, 401 Unauthorized with WWW-Authenticate'"
- [ ] API versioning strategy is defined (if applicable)
  - Evidence: "Versioning: 'URL versioning /api/v1/, maintain v1 for 6 months after v2 release'"

### 4.3 Component Architecture

- [ ] Component breakdown is complete
  - Evidence: "All components from architecture.md are addressed in tasks"
- [ ] Component responsibilities are clear
  - Evidence: "Each component has defined purpose: 'AuthService handles JWT validation and refresh'"
- [ ] Component interactions are documented
  - Evidence: "Interactions: 'LoginView → AuthService → APIClient → Backend API'"
- [ ] State management approach is defined
  - Evidence: "State: 'Redux for global state, React Context for theme, local state for UI'"
- [ ] Component organization follows architecture
  - Evidence: "Organization matches architecture.md component structure"

### 4.4 Integration Points

- [ ] Internal integrations are fully documented
  - Evidence: "Internal: 'AuthService integrates with UserService for profile data'"
- [ ] External integrations are specified with details
  - Evidence: "External: 'Stripe API v2023-10-16, use test keys in dev: sk_test_...'"
- [ ] Integration authentication is defined
  - Evidence: "Integration auth: 'OAuth 2.0 for Google, API key for Mailgun in headers'"
- [ ] Data flow through integrations is clear
  - Evidence: "Flow: 'User submits → Validate → Call API → Transform response → Update state'"
- [ ] Error handling for integrations is specified
  - Evidence: "Integration errors: 'Retry 3x with exponential backoff, fallback to cache'"

### 4.5 Technical Implementation Details

- [ ] Technology-specific patterns are provided
  - Evidence: "React patterns: 'Use custom hooks for data fetching, useReducer for complex state'"
- [ ] Configuration management is addressed
  - Evidence: "Config: 'Environment variables in .env, validated with Zod schema'"
- [ ] Logging and monitoring are specified
  - Evidence: "Logging: 'Use Winston with JSON format, log levels: error/warn/info, include correlation IDs'"
- [ ] Build and deployment are documented
  - Evidence: "Build: 'Vite for bundling, env-specific builds for dev/staging/prod'"
- [ ] Performance optimizations are included
  - Evidence: "Performance: 'Code splitting by route, lazy load images, debounce search input'"

## 5. PRD & ARCHITECTURE ALIGNMENT

[[LLM: The PRP must bridge PRD requirements with architecture decisions. Every PRD requirement must have implementation guidance, and every architectural constraint must be respected.

This section validates traceability from requirements through architecture to implementation.]]

### 5.1 Requirements Traceability

- ⚠️ [ ] All PRD functional requirements are addressed in tasks
  - Evidence: "Map each PRD FR to specific tasks: 'FR-1 Authentication → Task 1-5'"
- [ ] User stories from PRD are implementable
  - Evidence: "Each user story has corresponding tasks and validation"
- [ ] Acceptance criteria from PRD are testable
  - Evidence: "PRD acceptance criteria → Level 4 validation tests"
- [ ] Non-functional requirements are addressed
  - Evidence: "PRD NFRs (performance, security, accessibility) addressed in implementation"
- [ ] Scope boundaries from PRD are respected
  - Evidence: "Out-of-scope items from PRD are not included in tasks"

### 5.2 Architecture Compliance

- ⚠️ [ ] Technology stack matches architecture.md
  - Evidence: "Cross-reference: PRP uses same languages, frameworks, libraries as architecture"
- ⚠️ [ ] Architectural patterns are followed
  - Evidence: "Architecture patterns (MVC, microservices, etc.) reflected in implementation tasks"
- [ ] Architectural constraints are respected
  - Evidence: "Constraints from architecture.md are included in PRP gotchas/constraints section"
- [ ] Component structure follows architecture
  - Evidence: "File/folder structure in tasks matches architecture.md component organization"
- [ ] Security measures from architecture are implemented
  - Evidence: "Security requirements from architecture.md addressed in tasks"

### 5.3 Design Consistency

- [ ] Naming conventions match architecture/codebase
  - Evidence: "File naming, variable naming follows existing project conventions"
- [ ] Code organization follows established patterns
  - Evidence: "Directory structure consistent with existing codebase and architecture"
- [ ] API design follows architectural standards
  - Evidence: "API endpoints follow REST/GraphQL conventions from architecture"
- [ ] Error handling follows project patterns
  - Evidence: "Error handling consistent with existing error handling patterns"
- [ ] Testing approach aligns with architecture
  - Evidence: "Test structure and frameworks match architecture testing strategy"

## 6. COMPLETENESS & COVERAGE

[[LLM: A complete PRP leaves no gaps. This section validates that all necessary aspects of implementation are addressed, from project setup through deployment.

Look for what's MISSING, not just what's present.]]

### 6.1 Implementation Coverage

- [ ] All necessary files are identified for creation/modification
  - Evidence: "Complete file list: models, services, views, tests, configs"
- [ ] Configuration files are addressed
  - Evidence: "Config files included: .env.example, tsconfig.json, package.json updates"
- [ ] Database migrations are included (if applicable)
  - Evidence: "Migration tasks: 'CREATE migration 001_add_users_table.sql'"
- [ ] Initial data/seed files are addressed (if needed)
  - Evidence: "Seed data: 'CREATE seeds/dev-users.sql for local development'"
- [ ] Documentation updates are included
  - Evidence: "Doc tasks: 'UPDATE docs/api.md with new endpoints'"

### 6.2 Environment Setup

- [ ] Development environment setup is documented
  - Evidence: "Setup: 'Install Node 20.x, PostgreSQL 15.x, run npm install'"
- [ ] Required tools and dependencies are listed
  - Evidence: "Tools: 'Docker for local DB, Git for version control, IDE with ESLint plugin'"
- [ ] Environment variables are documented
  - Evidence: "Environment vars listed with descriptions and example values"
- [ ] Local development workflow is defined
  - Evidence: "Dev workflow: 'Run docker-compose up, npm run dev, access http://localhost:3000'"
- [ ] Troubleshooting common setup issues is included
  - Evidence: "Troubleshooting: 'If port 3000 in use, kill process or change PORT env var'"

### 6.3 Testing Coverage

- [ ] All test types are addressed (unit, integration, E2E)
  - Evidence: "Test coverage: unit tests for services, integration for API, E2E for critical flows"
- [ ] Test data and fixtures are specified
  - Evidence: "Test data: 'Use factory functions for test users, mock API responses in __mocks__'"
- [ ] Test environment setup is documented
  - Evidence: "Test env: 'Use test database, mock external APIs, seed test data'"
- [ ] Edge case testing is included
  - Evidence: "Edge cases tested: empty states, validation errors, network failures"
- [ ] Performance testing is addressed (if required)
  - Evidence: "Performance tests: 'Load test with k6, validate response times under load'"

### 6.4 Deployment Readiness

- [ ] Build process is documented
  - Evidence: "Build: 'npm run build creates optimized production bundle in dist/'"
- [ ] Deployment steps are outlined
  - Evidence: "Deploy: 'Deploy to Vercel via GitHub integration, environment vars in dashboard'"
- [ ] Environment-specific configurations are defined
  - Evidence: "Environments: dev (local), staging (staging.example.com), prod (example.com)"
- [ ] Rollback procedure is documented
  - Evidence: "Rollback: 'Revert to previous Vercel deployment via dashboard or API'"
- [ ] Health checks and monitoring are specified
  - Evidence: "Monitoring: 'Health endpoint /api/health, monitor with UptimeRobot'"

## 7. CLARITY & USABILITY

[[LLM: The PRP is a communication tool. It must be clear, well-organized, and usable by an AI agent for autonomous implementation.

Evaluate from the perspective of a fresh Claude instance with no context.]]

### 7.1 Documentation Quality

- [ ] Language is clear and unambiguous
  - Evidence: "No vague terms like 'user-friendly', 'performant', 'robust' without specifics"
- [ ] Technical jargon is defined or explained
  - Evidence: "Domain terms defined on first use or in glossary"
- [ ] Structure is logical and easy to navigate
  - Evidence: "Clear sections: Goal → Context → Blueprint → Validation"
- [ ] Formatting aids comprehension (code blocks, lists, tables)
  - Evidence: "Good use of markdown: code blocks with language tags, bulleted lists, YAML tables"
- [ ] Length is appropriate (comprehensive but not verbose)
  - Evidence: "PRP includes all necessary detail without redundancy"

### 7.2 Consistency

- [ ] Terminology is consistent throughout
  - Evidence: "Same concepts use same terms: 'User' vs 'Account', 'Authentication' vs 'Auth'"
- [ ] Formatting is consistent
  - Evidence: "Consistent capitalization, punctuation, code block formatting"
- [ ] File paths are consistently formatted
  - Evidence: "All paths use same format: absolute paths or consistently relative"
- [ ] Code examples follow same style
  - Evidence: "Code examples match project style guide"
- [ ] Validation commands follow same pattern
  - Evidence: "Commands formatted consistently: 'npm run <script>' pattern"

### 7.3 Navigability

- [ ] Sections are clearly titled and organized
  - Evidence: "Section titles are descriptive and hierarchical"
- [ ] Related information is grouped together
  - Evidence: "All authentication tasks grouped, all validation in one section"
- [ ] Cross-references are clear and helpful
  - Evidence: "References like 'See architecture.md section 4.2' are specific"
- [ ] Table of contents or outline is clear (if long)
  - Evidence: "Long PRPs have clear structure visible at top"
- [ ] Key information is easily findable
  - Evidence: "Critical constraints, gotchas, validation commands are easy to locate"

### 7.4 Actionability

- [ ] Every task is actionable (has clear next step)
  - Evidence: "Tasks start with action verbs: CREATE, UPDATE, INTEGRATE, TEST"
- [ ] Ambiguity is eliminated or explicitly acknowledged
  - Evidence: "Unknowns are called out: 'INVESTIGATE: Determine if caching needed'"
- [ ] Decision points are clear
  - Evidence: "Choices documented: 'Use PostgreSQL (already chosen in architecture)'"
- [ ] Prerequisites are stated before tasks
  - Evidence: "Task dependencies clear: 'REQUIRES: Task 1 complete before Task 2'"
- [ ] Success is clearly defined for each task
  - Evidence: "Each task has 'DONE WHEN' or validation criteria"

## 8. RISK MITIGATION

[[LLM: Identify risks to implementation success and verify they're mitigated in the PRP.

Common risks:
- Scope creep (out-of-scope features slip in)
- Technical debt (shortcuts without plan to address)
- Integration failures (external dependencies fail)
- Performance issues (not considered until too late)
- Security vulnerabilities (not caught during implementation)]]

### 8.1 Technical Risks

- [ ] Complex technical challenges are identified
  - Evidence: "Challenges called out: 'COMPLEX: Real-time sync requires WebSocket management'"
- [ ] Risk mitigation strategies are provided
  - Evidence: "Mitigations: 'Use library X for WebSocket reliability, implement reconnection logic'"
- [ ] Fallback approaches are documented
  - Evidence: "Fallbacks: 'If WebSocket fails, fall back to polling every 5s'"
- [ ] External dependencies are identified as risks
  - Evidence: "Dependencies: 'External API has 99% uptime SLA, implement circuit breaker pattern'"
- [ ] Performance risks are addressed
  - Evidence: "Performance: 'Large list rendering could be slow, implement virtualization'"

### 8.2 Scope Management

- [ ] Scope boundaries are clear
  - Evidence: "In-scope vs out-of-scope clearly delineated"
- [ ] Feature creep is prevented
  - Evidence: "Tasks are minimal for MVP, future enhancements listed separately"
- [ ] Optional vs required features are distinguished
  - Evidence: "Core features vs nice-to-haves clearly marked"
- [ ] Dependencies on future work are documented
  - Evidence: "Future work dependencies: 'Full analytics dashboard deferred to v2'"
- [ ] Scope changes are tracked (if PRP has been revised)
  - Evidence: "Version history or changelog documents scope changes"

### 8.3 Quality Risks

- [ ] Testing gaps are identified and addressed
  - Evidence: "Testing: 'E2E tests for critical auth flow, unit tests for business logic'"
- [ ] Security considerations are explicit
  - Evidence: "Security: 'Input sanitization, CSRF protection, rate limiting on auth endpoints'"
- [ ] Accessibility risks are addressed (if UI)
  - Evidence: "A11y: 'Keyboard navigation for all interactive elements, ARIA labels for icons'"
- [ ] Browser/platform compatibility is considered
  - Evidence: "Compatibility: 'Test on IE 11 if required, graceful degradation for older browsers'"
- [ ] Technical debt is acknowledged
  - Evidence: "Tech debt: 'Initial implementation uses polling, refactor to WebSocket in sprint 2'"

### 8.4 Execution Risks

- [ ] Task complexity is estimated realistically
  - Evidence: "Time estimates: 'Task 1: 2-3 hours, Task 5: 6-8 hours (complex)'"
- [ ] Blockers are identified proactively
  - Evidence: "Blockers: 'Need API keys from stakeholder before Task 3'"
- [ ] Dependencies on external teams/resources are noted
  - Evidence: "External deps: 'Design team to provide final mockups by Day 2'"
- [ ] Assumptions are explicitly stated
  - Evidence: "Assumptions: 'Assuming PostgreSQL is already provisioned and accessible'"
- [ ] Contingency plans are included
  - Evidence: "Contingencies: 'If API integration fails, use mock data for demo'"

## ZERO-KNOWLEDGE VALIDATION

[[LLM: This is the ultimate test. Put yourself in the position of a fresh Claude instance with:
- Access to the PRP document
- Access to codebase files
- General programming knowledge
- NO prior context about this project

Can you implement successfully? If NO, the PRP fails this gate.]]

### The Critical Questions

- ⚠️ [ ] Can a fresh Claude instance implement with ONLY this PRP and codebase access?
  - Evidence: "Verify all context needed is in PRP, no external context required"
- ⚠️ [ ] Are all implementation decisions clearly documented (no judgment calls needed)?
  - Evidence: "Choices like 'Use X library' are made, not 'Choose appropriate library'"
- ⚠️ [ ] Are all file paths, commands, and references verifiable and accessible?
  - Evidence: "All references can be checked and accessed"
- ⚠️ [ ] Are all validation commands executable without modification?
  - Evidence: "Commands can be copy-pasted and run successfully"
- ⚠️ [ ] Is success/failure clearly determinable at each validation level?
  - Evidence: "Pass/fail criteria are objective and measurable"
- [ ] Are all necessary patterns, examples, and references included?
  - Evidence: "No need to search for additional examples or documentation"
- [ ] Are architectural constraints and conventions clear without prior knowledge?
  - Evidence: "All conventions are documented, not assumed"
- [ ] Can the implementation be validated against PRD requirements?
  - Evidence: "Clear mapping from tasks to PRD requirements enables validation"
- [ ] Would implementation questions have clear answers in the PRP?
  - Evidence: "Common questions like 'Where does this go?', 'How do I validate?' are answered"
- [ ] Is the confidence score realistic given the context completeness?
  - Evidence: "Confidence score /10 matches actual completeness and clarity"

---

## SCORING & VALIDATION SUMMARY

[[LLM: Calculate quality score and generate comprehensive report

**Scoring Calculation:**
1. Count total validation items attempted
2. Count critical failures (⚠️ items that failed)
3. Count standard failures (non-critical items that failed)
4. Calculate: Score = 100 - (10 × critical_failures) - (5 × standard_failures)
5. Determine status:
   - APPROVED (90-100): Execute PRP immediately - high confidence in one-pass success
   - CONDITIONAL (70-89): Execute with caution - minor improvements needed
   - REJECTED (0-69): BLOCK execution - critical gaps will cause implementation failure

**Report Structure:**

# PRP Quality Gate Validation Report

**Phase**: PRP
**Checklist**: prp-quality-gate.md
**PRP Document**: [path to PRP]
**Timestamp**: {iso_timestamp}
**Mode**: {interactive|batch|yolo}

## Overall Result

**Status**: {APPROVED|CONDITIONAL|REJECTED}
**Score**: {score}/100
**Total Items**: {total}
**Passed**: {passed}
**Failed**: {failed} ({critical_failures} critical, {standard_failures} standard)

## Section Results

### 1. Context Completeness (16 items)
- Passed: X/16
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 2. Implementation Clarity (16 items)
- Passed: X/16
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 3. Validation Readiness (16 items)
- Passed: X/16
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 4. Implementation Blueprint Quality (15 items)
- Passed: X/15
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 5. PRD & Architecture Alignment (11 items)
- Passed: X/11
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 6. Completeness & Coverage (14 items)
- Passed: X/14
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 7. Clarity & Usability (14 items)
- Passed: X/14
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### 8. Risk Mitigation (14 items)
- Passed: X/14
- Failed: Y (Z critical, W standard)
- Status: {✅ COMPLETE | ⚠️ NEEDS IMPROVEMENT | ❌ INCOMPLETE}

### ZERO-KNOWLEDGE VALIDATION (10 items)
- Passed: X/10
- Failed: Y (Z critical, W standard)
- Status: {✅ PASS | ❌ FAIL}

## Failed Items Detail

[For each failed item, provide:]
- Item text
- Evidence requirement
- Why it failed
- Impact on score (-5 or -10)
- Specific recommendation for fix

## Critical Findings

### BLOCKERS (Critical failures that prevent execution):
1. [Specific critical failure with impact]
2. ...

### WARNINGS (Quality issues that increase risk):
1. [Specific quality issue with risk assessment]
2. ...

## Recommendations

### High Priority (Blocking - Must Fix Before Execution)
1. [Specific action to address critical failure]
   - Location: [Where in PRP to fix]
   - Fix: [Exact change needed]
   - Impact: [Why this is critical]

### Medium Priority (Quality Improvements - Should Fix)
1. [Specific action to improve quality]
   - Location: [Where in PRP to fix]
   - Fix: [Exact change needed]
   - Impact: [Risk if not fixed]

### Low Priority (Nice to Have - Optional)
1. [Optional improvement]
   - Location: [Where in PRP to enhance]
   - Fix: [Suggested enhancement]
   - Impact: [Minor quality improvement]

## Zero-Knowledge Test Result

**Can a fresh Claude instance implement successfully with ONLY this PRP?**

{✅ YES - PASS | ❌ NO - FAIL}

**Reasoning**: [Detailed explanation of zero-knowledge test outcome]

**Missing Context** (if failed):
- [Specific context that's missing]
- [Assumptions that need to be documented]
- [References that need to be added]

## Next Steps

**If APPROVED (90-100)**:
✅ Execute PRP immediately
✅ High confidence in one-pass implementation success
✅ All critical context present, validation ready, clear guidance
✅ Expected outcome: Successful implementation with minimal clarification

**If CONDITIONAL (70-89)**:
⚠️ May execute PRP with caution
⚠️ Address high-priority recommendations
⚠️ Document known gaps for awareness during execution
⚠️ Risk: Minor clarifications may be needed during implementation
⚠️ Expected outcome: Successful implementation with some clarification

**If REJECTED (0-69)**:
❌ BLOCK PRP execution
❌ Must address all critical failures
❌ Re-run quality gate after fixes
❌ Risk: HIGH - Implementation will fail or require significant rework
❌ Expected outcome: Implementation failure without PRP improvements

## Evidence Quality Assessment

[Provide summary of evidence collection quality]
- Strong Evidence: X items (specific citations, verified references)
- Weak Evidence: Y items (vague or unverified references)
- No Evidence: Z items (assertions without proof)

## Save Results

Save validation results to:
`.codex/state/quality-gate-prp-{timestamp}.json`

Update workflow.json:
```json
{
  "quality_gate_results": {
    "prp": {
      "timestamp": "{iso_timestamp}",
      "status": "{APPROVED|CONDITIONAL|REJECTED}",
      "score": {score},
      "checklist": "prp-quality-gate.md",
      "mode": "{interactive|batch|yolo}",
      "total_items": {total},
      "passed": {passed},
      "failed": {failed},
      "critical_failures": {critical_failures},
      "standard_failures": {standard_failures},
      "zero_knowledge_test": "{PASS|FAIL}",
      "summary": "{one-line summary}",
      "prp_document": "{path to PRP}"
    }
  },
  "quality_scores": {
    "prp": {score}
  }
}
```

]]

---

**Checklist Version**: 1.0
**Total Items**: 172 (excluding zero-knowledge validation section header items)
**Critical Items**: 31 (marked with ⚠️)
**Last Updated**: 2025-10-07
**Maintained By**: CODEX Quality Team
**Related**: quality-scoring-rubric.md, prp-enhanced-template.md, execute-quality-gate.md, architect-quality-gate.md, pm-quality-gate.md
