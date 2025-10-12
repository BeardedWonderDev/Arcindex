# Vertical Slice Pattern for AI-Friendly Story Development

## Definition

A **vertical slice** is a complete, deployable feature that spans all architectural layers from user interface to data persistence. Unlike horizontal layers (all models, then all services, then all UI), a vertical slice delivers end-to-end functionality for a specific user capability.

## Why Vertical Slices for AI Implementation?

AI agents excel at implementing vertical slices because:

1. **Clear Boundaries**: All code for a feature is in one story, reducing context switching
2. **Independently Testable**: Complete feature can be validated without external dependencies
3. **Incremental Delivery**: Each slice delivers shippable user value
4. **Reduced Context**: AI doesn't need to understand entire system, just the slice's scope
5. **Autonomous Completion**: AI can implement, test, and validate without human intervention

## Vertical Slice Structure

Every vertical slice should include these layers:

### 1. Entry Point (API endpoint or UI component)
- REST/GraphQL endpoint definition
- Request/response schemas
- Route configuration
- UI component triggering the flow

### 2. Business Logic (service layer)
- Core feature logic
- Validation rules
- Business rule enforcement
- Error handling

### 3. Data Layer (model/schema)
- Database schema/model
- Data access patterns
- Persistence logic
- Query optimization

### 4. Tests (unit + integration)
- Unit tests for business logic
- Integration tests for full flow
- API contract tests
- Edge case coverage

### 5. Validation (acceptance criteria)
- Programmatically testable criteria
- Performance benchmarks
- Security validation
- Error scenario coverage

## Examples

### ✅ Good Vertical Slice Examples

#### Example 1: User Registration with Email Verification
**Story**: "As a new user, I can register with email and receive a verification link"

**Vertical Slice Includes**:
- **Entry Point**: `POST /api/auth/register` endpoint
- **Business Logic**:
  - Email validation service
  - Password hashing service
  - Verification token generation
  - Email sending service
- **Data Layer**:
  - User model with email/password fields
  - Verification token model
  - User repository with create/findByEmail methods
- **Tests**:
  - Unit: Email validation, password hashing
  - Integration: Full registration flow, email sending
  - Edge cases: Duplicate email, invalid format
- **Validation**:
  - AC1: Valid registration returns 201 with user ID
  - AC2: Verification email sent within 5 seconds
  - AC3: Duplicate email returns 409 error
  - AC4: Password is hashed before storage

**Why This Works**: Complete registration feature from API to database, independently testable, no dependencies on other stories.

#### Example 2: Task Creation with Auto-Assignment
**Story**: "As a team member, I can create a task that auto-assigns to the next available developer"

**Vertical Slice Includes**:
- **Entry Point**: `POST /api/tasks` endpoint
- **Business Logic**:
  - Task validation service
  - Auto-assignment algorithm
  - Notification service
- **Data Layer**:
  - Task model
  - Assignment model
  - Task repository
- **Tests**:
  - Unit: Assignment algorithm logic
  - Integration: Full task creation + assignment flow
  - Edge cases: No available developers, priority override
- **Validation**:
  - AC1: Task created with valid data returns 201
  - AC2: Task auto-assigned to developer with fewest active tasks
  - AC3: Assigned developer receives notification
  - AC4: Task defaults to priority P2 if not specified

**Why This Works**: Complete feature delivering user value, all layers included, testable without other stories.

### ❌ Bad Examples (Anti-Patterns)

#### Anti-Pattern 1: Horizontal Layer - "All User Models"
**Problem Story**: "Create all user-related database models"

**Why This Fails**:
- No deliverable user value
- Cannot be tested independently
- Blocks other stories from starting
- No clear acceptance criteria
- AI has no context for "why" these models exist

**Better Approach**: Split into vertical slices:
- Story 1: User registration (includes User model)
- Story 2: User profile editing (includes Profile model)
- Story 3: User preferences (includes Preferences model)

#### Anti-Pattern 2: Incomplete Slice - "Build User Registration UI"
**Problem Story**: "Create user registration form components"

**Why This Fails**:
- Only UI layer, no backend
- Cannot be tested end-to-end
- Requires separate backend story (dependency)
- No complete user value
- AI cannot validate the full flow

**Better Approach**: Combine into complete slice:
- "User Registration with Email Verification" (includes UI, API, database, tests)

#### Anti-Pattern 3: Too-Large Slice - "Complete User Management System"
**Problem Story**: "Implement all user CRUD operations, authentication, authorization, profile management, and admin controls"

**Why This Fails**:
- Far exceeds 4-8 hour AI implementation window
- Multiple features bundled together
- Complex dependencies within story
- Difficult to test as a unit
- High risk of partial completion

**Better Approach**: Split into sequential slices:
1. User registration (4 hours)
2. User login (3 hours)
3. User profile view (2 hours)
4. User profile edit (3 hours)
5. User deletion (2 hours)
6. Admin user management (5 hours)

## AI Implementation Workflow

### Story Setup (Before AI Implementation)
1. **Story Definition**: Clear title and description
2. **Acceptance Criteria**: 3-7 programmatically testable ACs
3. **Dependencies**: Explicitly list prerequisites
4. **Context**: Link to relevant PRD/architecture sections
5. **Time Estimate**: Confirm 4-8 hour range

### AI Implementation Flow
1. **Load Context**: AI reads story + linked PRD/architecture
2. **Layer 1 - Data**: Create models/schemas
3. **Layer 2 - Business Logic**: Implement services
4. **Layer 3 - Entry Point**: Create API/UI
5. **Layer 4 - Tests**: Write unit + integration tests
6. **Layer 5 - Validation**: Verify acceptance criteria

### Validation
1. **Unit Tests**: Run and pass (100% coverage for new code)
2. **Integration Tests**: Full flow validation
3. **Acceptance Criteria**: Programmatically verified
4. **Code Quality**: Linting, formatting, security checks
5. **Deployment**: Verify deployability (no broken dependencies)

## Story Sizing Guidelines for AI

### Ideal Size: 4-8 Hours
- **4 hours**: Simple CRUD with basic validation
- **6 hours**: Feature with business logic and multiple endpoints
- **8 hours**: Complex feature with integrations or algorithms

### Size Indicators

**Too Small (<2 hours)**:
- Only configuration changes
- Simple text/content updates
- Might be bundled with another story

**Just Right (4-8 hours)**:
- Complete vertical slice
- 1-3 API endpoints or UI components
- Moderate business logic
- 10-20 test cases
- 3-7 acceptance criteria

**Too Large (>8 hours)**:
- Multiple features in one story
- Complex state management
- Novel algorithms or research needed
- 10+ API endpoints
- Cross-cutting concerns

### Splitting Strategies

When a story is too large, split using these patterns:

1. **By CRUD Operations**:
   - Create → Read → Update → Delete (4 stories)

2. **By User Journey**:
   - Registration → Verification → First Login (3 stories)

3. **By Complexity**:
   - Basic feature → Advanced options → Admin controls (3 stories)

4. **By Integration**:
   - Core feature → External API integration → Webhooks (3 stories)

## Vertical Slice Checklist

Use this checklist when defining stories:

- [ ] **User Value**: Story delivers complete user capability
- [ ] **Entry Point**: API endpoint or UI component defined
- [ ] **Business Logic**: Service layer logic scoped
- [ ] **Data Layer**: Models and persistence included
- [ ] **Tests**: Unit and integration tests specified
- [ ] **ACs**: 3-7 programmatically testable criteria
- [ ] **Time**: Estimated 4-8 hours for AI implementation
- [ ] **Dependencies**: Prerequisites explicitly listed
- [ ] **Independent**: Can be built and tested standalone
- [ ] **Deployable**: Can be shipped to production independently
- [ ] **Testable**: No subjective "looks good" criteria
- [ ] **Rollback**: Clear strategy if validation fails

## Benefits Summary

### For AI Agents
- ✅ Clear scope and boundaries
- ✅ Complete context in one story
- ✅ Autonomous implementation possible
- ✅ Programmatic validation
- ✅ Reduced context switching

### For Teams
- ✅ Incremental delivery of value
- ✅ Parallel development possible
- ✅ Early feedback on features
- ✅ Reduced integration complexity
- ✅ Clear progress tracking

### For Quality
- ✅ Comprehensive test coverage
- ✅ Isolated failure domains
- ✅ Simplified debugging
- ✅ Better code organization
- ✅ Reduced technical debt

## Anti-Patterns Summary

Avoid these common mistakes:

- ❌ **Horizontal Layers**: "All models" or "All services"
- ❌ **Incomplete Slices**: Only UI or only backend
- ❌ **Too-Large Slices**: Multiple features bundled
- ❌ **Vague ACs**: Subjective or untestable criteria
- ❌ **Hidden Dependencies**: Implicit prerequisites
- ❌ **Human-in-Loop**: Stories requiring manual review during implementation

## References

- **PM Quality Gate Checklist**: Section 6.4 "Story Sizing & Complexity"
- **PRD Template**: Epic and story structure guidelines
- **Architecture Template**: Component architecture and testing strategy
- **CODEX Workflow**: Phase-specific validation requirements

---

**Pattern Status**: Core CODEX pattern for AI-assisted development
**Last Updated**: Phase 1, Week 3
**Related Patterns**: Epic structure, acceptance criteria, test-driven development
