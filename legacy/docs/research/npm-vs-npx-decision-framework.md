# npm vs npx: Comprehensive Decision Framework

**Research Date:** October 9, 2025
**Purpose:** Strategic decision-making guide for choosing between npm global installation and npx execution
**Target Audience:** Tool authors, package maintainers, technical decision-makers

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Decision Criteria](#decision-criteria)
3. [Decision Tree](#decision-tree)
4. [Scoring Matrix](#scoring-matrix)
5. [Risk Assessment](#risk-assessment)
6. [Hybrid Strategies](#hybrid-strategies)
7. [Recommendations Format](#recommendations-format)
8. [Real-World Case Studies](#real-world-case-studies)
9. [Implementation Patterns](#implementation-patterns)

---

## Executive Summary

### Quick Decision Guide

**Choose npm global (`npm install -g`) when:**
- Tool is used frequently (daily/weekly)
- Tool maintains state or configuration
- Performance matters (startup time critical)
- Users expect persistent commands
- Tool integrates with other persistent tools

**Choose npx (`npx package-name`) when:**
- Tool is used once or rarely (scaffolding, initialization)
- Tool should always use latest version
- Tool has no persistent state
- Disk space conservation matters
- Version conflicts are a concern

**Choose Hybrid (support both) when:**
- Large user base with diverse needs
- Tool can operate in both modes
- You have resources for dual support
- Community expectations vary

---

## 1. Decision Criteria

### 1.1 Tool Lifespan

**Ephemeral (npx-friendly):**
- Project scaffolders (create-react-app, create-next-app)
- One-time setup tools
- Migration utilities
- Temporary development tools

**Persistent (npm global-friendly):**
- Daily-use CLI tools
- Build tools
- Linters and formatters
- Development servers
- Package managers themselves

**Scoring:**
- Ephemeral (1-2 uses): +5 for npx
- Occasional (monthly): Neutral
- Frequent (weekly): +3 for npm
- Daily use: +5 for npm

---

### 1.2 Command Frequency

**One-time or Rare:**
```bash
# Project initialization
npx create-react-app my-app
npx degit user/template my-project

# Database migrations
npx prisma migrate deploy

# Version bumping
npx standard-version
```
**Recommendation:** npx (score +5)

**Daily Use:**
```bash
# Build tools
npm run build    # Uses local npm
vercel deploy    # Global install expected

# Linters
eslint src/      # Global or local
prettier --write # Global or local

# Git helpers
gh pr create     # Global install expected
```
**Recommendation:** npm global (score +5)

**Scoring Scale:**
- Used once: +5 npx
- Used < 5 times/project: +3 npx
- Used 5-20 times/project: Neutral
- Used weekly: +3 npm
- Used daily: +5 npm

---

### 1.3 State Requirements

**Stateless (npx-friendly):**
- Pure functions (input → output)
- No configuration files
- No persistent data
- No global preferences

**Stateful (npm global-friendly):**
```bash
# Tools with state
~/.gitconfig
~/.npmrc
~/.docker/config.json
~/.aws/credentials
~/.codex/state/
```

**Examples:**

**Stateless (npx):**
- create-react-app (generates files, then done)
- cowsay (pure output)
- json-server (temporary server)

**Stateful (npm):**
- gh (GitHub CLI with auth tokens)
- vercel (deployment configuration)
- docker (daemon configuration)
- codex (workflow state management)

**Scoring:**
- Fully stateless: +5 npx
- Minimal state (per-project): +2 npx
- Moderate state (global config): +3 npm
- Heavy state (multiple files/dirs): +5 npm

---

### 1.4 Update Frequency

**Fast-Moving (npx-friendly):**
- Framework scaffolders (weekly updates)
- Security tools (frequent patches)
- Experimental tools (rapid iteration)

**Stable (npm global-friendly):**
- Mature CLI tools (quarterly updates)
- Build tools (monthly updates)
- Well-established standards

**Real-World Examples:**

**Fast-Moving:**
```bash
# Always get latest template
npx create-next-app@latest

# Always get newest features
npx create-vite@latest

# Security scanners want latest rules
npx audit-ci --config .audit-ci.json
```

**Stable:**
```bash
# Stable, infrequent updates
npm install -g typescript
npm install -g eslint
npm install -g prettier
```

**Scoring:**
- Major updates weekly: +5 npx
- Updates monthly: +2 npx
- Updates quarterly: Neutral
- Updates semi-annually: +3 npm
- Updates rarely (1-2/year): +5 npm

---

### 1.5 User Skill Level

**Beginners (npx-friendly):**
- Don't understand global vs local
- Don't know about PATH
- Intimidated by installation
- Want "just works" experience

**Experts (npm global-friendly):**
- Comfortable with PATH management
- Understand version management
- Use version managers (mise, asdf)
- Want performance and control

**Consideration:**
```bash
# Beginner-friendly
npx create-react-app my-app
# vs
npm install -g create-react-app
create-react-app my-app

# Expert-friendly
npm install -g typescript
tsc --version
# vs
npx typescript --version  # Slower, downloads each time
```

**Scoring:**
- Target: Beginners → +3 npx
- Target: Intermediate → Neutral
- Target: Experts → +3 npm
- Target: Mixed → Hybrid approach

---

### 1.6 Installation Friction Tolerance

**Low Tolerance (npx-friendly):**
- Tutorial/course participants
- Casual contributors
- Hackathon participants
- Exploratory users

**High Tolerance (npm global-friendly):**
- Professional developers
- Team standardization
- Enterprise environments
- Long-term users

**Example Scenarios:**

**Low Friction:**
```bash
# Tutorial: "Run this one command"
npx create-remix@latest
# vs
# Tutorial: "First install globally, then run..."
npm install -g create-remix
create-remix
```

**High Friction OK:**
```bash
# Professional setup
npm install -g typescript prettier eslint
npm install -g @vercel/cli
npm install -g gh
# Users expect setup time
```

**Scoring:**
- Tutorial/demo use: +5 npx
- Exploratory use: +3 npx
- Professional use: +3 npm
- Enterprise use: +5 npm

---

### 1.7 Disk Space Sensitivity

**Space-Constrained (npx cache-friendly):**
- CI/CD environments (cached layers)
- Limited disk quotas
- Shared hosting
- Edge environments

**Space-Abundant (npm global-friendly):**
- Developer workstations
- Build servers
- Modern infrastructure

**Reality Check:**

**npx caching:**
```bash
# First run: Downloads package
npx create-react-app my-app
# Cached in ~/.npm/_npx/
# Subsequent runs: Uses cache (but still checks for updates)

# Cache size can grow:
du -sh ~/.npm/_npx/
# 2.4GB (example after heavy usage)
```

**npm global:**
```bash
# One-time install
npm install -g create-react-app
# Lives in global node_modules
# Size: Known and fixed per version
```

**Scoring:**
- Disk very limited (<10GB): +3 npx
- Disk moderate (10-50GB): Neutral
- Disk abundant (>50GB): +2 npm
- CI/CD environment: +3 npx (layer caching)

---

### 1.8 Version Pinning Needs

**Version-Sensitive (npm global-friendly):**
- Build reproducibility required
- CI/CD pipelines
- Monorepo tooling
- Team standardization

**Version-Flexible (npx-friendly):**
- Always want latest
- Breaking changes rare
- Experimental usage
- One-off tasks

**Version Control Strategies:**

**npm global with version managers:**
```bash
# mise (recommended 2025)
mise install typescript@5.2.0
mise use typescript@5.2.0

# asdf
asdf install nodejs 20.10.0
asdf local nodejs 20.10.0
```

**npx with version pinning:**
```bash
# Pin to specific version
npx create-react-app@4.0.0 my-app

# Pin in package.json scripts
{
  "scripts": {
    "create": "npx create-react-app@4.0.0"
  }
}
```

**Scoring:**
- Version pinning critical: +5 npm (with mise/asdf)
- Version pinning preferred: +3 npm
- Version flexibility OK: Neutral
- Latest always preferred: +3 npx
- Version doesn't matter: +5 npx

---

## 2. Decision Tree

### 2.1 Primary Decision Flow

```
START: Choosing npm vs npx

├─ Q1: Is this a scaffolding/initialization tool?
│  ├─ YES → Strong recommendation: npx (+5 npx)
│  │  └─ Examples: create-react-app, create-next-app, degit
│  └─ NO → Continue to Q2

├─ Q2: Does it need to be available globally?
│  ├─ YES → Does it maintain global state?
│  │  ├─ YES → Strong recommendation: npm global (+5 npm)
│  │  │  └─ Examples: gh, docker, vercel
│  │  └─ NO → Continue to Q3
│  └─ NO → Continue to Q3

├─ Q3: Do users run it frequently (daily/weekly)?
│  ├─ YES → Recommendation: npm global (+3 npm)
│  │  └─ Examples: typescript, eslint, prettier
│  └─ NO → Continue to Q4

├─ Q4: Is it fast-moving with frequent updates?
│  ├─ YES → Recommendation: npx (+3 npx)
│  │  └─ Examples: security scanners, experimental tools
│  └─ NO → Continue to Q5

├─ Q5: Is it a one-time use tool?
│  ├─ YES → Definite recommendation: npx (+5 npx)
│  │  └─ Examples: migration scripts, setup wizards
│  └─ NO → Continue to Q6

├─ Q6: Does performance matter (startup time)?
│  ├─ YES → Recommendation: npm global (+3 npm)
│  │  └─ Cold start: npx adds 1-3 seconds
│  └─ NO → Continue to Q7

├─ Q7: Target audience skill level?
│  ├─ Beginners → Recommendation: npx (+2 npx)
│  ├─ Mixed → Recommendation: Hybrid approach
│  └─ Experts → Recommendation: npm global (+2 npm)

└─ RESULT: Sum scores and apply scoring matrix (see Section 3)
```

---

### 2.2 Special Cases Flow

```
SPECIAL CASES

├─ Case: Tool is part of larger ecosystem
│  ├─ Ecosystem uses npm (Node.js, TypeScript)
│  │  └─ Follow ecosystem convention (likely npm)
│  └─ Ecosystem uses npx (React, Next.js, Vite)
│     └─ Follow ecosystem convention (npx)

├─ Case: Tool already exists with opposite approach
│  ├─ Migration path available?
│  │  ├─ YES → Consider switching
│  │  └─ NO → Stay with current approach
│  └─ Can support both?
│     └─ YES → Implement hybrid strategy

├─ Case: Enterprise adoption critical
│  └─ Preference: npm global
│     └─ Reason: Version control, offline install, standardization

├─ Case: Tutorial/education focus
│  └─ Preference: npx
│     └─ Reason: Lowest friction, always latest

└─ Case: CI/CD primary use
   └─ Preference: npx or Docker
      └─ Reason: Reproducibility, no global pollution
```

---

### 2.3 Red Flags (Avoid These)

**Red Flags for npm global:**
- Tool used once per project
- Updates break frequently
- User base is mostly beginners
- Installation steps exceed 3 commands
- Global pollution concerns

**Red Flags for npx:**
- Tool used 10+ times per day
- Performance critical (hot path)
- Heavy dependencies (>100MB)
- Network unreliable in target environment
- State management required

---

## 3. Scoring Matrix

### 3.1 Scoring System

Rate your tool on each criterion (1-10 scale):

| Criterion | Weight | npx Score (1-10) | npm Score (1-10) | Weighted npx | Weighted npm |
|-----------|--------|------------------|------------------|--------------|--------------|
| **Lifespan** | 3x | [1=persistent, 10=ephemeral] | [10=persistent, 1=ephemeral] | | |
| **Frequency** | 3x | [1=daily, 10=once] | [10=daily, 1=once] | | |
| **State** | 2x | [1=stateful, 10=stateless] | [10=stateful, 1=stateless] | | |
| **Updates** | 2x | [1=stable, 10=fast-moving] | [10=stable, 1=fast-moving] | | |
| **Skill Level** | 1.5x | [1=experts, 10=beginners] | [10=experts, 1=beginners] | | |
| **Friction** | 1.5x | [1=high tolerance, 10=low] | [10=high tolerance, 1=low] | | |
| **Disk Space** | 1x | [1=abundant, 10=limited] | [10=abundant, 1=limited] | | |
| **Versioning** | 2x | [1=pinning critical, 10=latest OK] | [10=pinning critical, 1=latest OK] | | |

**Total Weight:** 16x

**Calculate:**
```
Total npx Score = Σ(Weighted npx scores)
Total npm Score = Σ(Weighted npm scores)
Max Possible = 160 (16 * 10)
```

**Recommendation:**
- **npx > 100:** Strong recommendation for npx
- **npx 80-100:** Recommendation for npx
- **npm/npx 60-80:** Hybrid approach or context-dependent
- **npm 80-100:** Recommendation for npm
- **npm > 100:** Strong recommendation for npm

---

### 3.2 User Experience Scoring

| Factor | npx Score | npm Score | Notes |
|--------|-----------|-----------|-------|
| **First-time UX** (1-10) | | | How easy is first use? |
| **Repeat-use UX** (1-10) | | | How easy is repeated use? |
| **Update UX** (1-10) | | | How easy to update? |
| **Uninstall UX** (1-10) | | | How easy to remove? |
| **Error Messages** (1-10) | | | How clear are errors? |
| **Documentation** (1-10) | | | How clear are docs? |
| **Total UX Score** (max 60) | | | Sum of above |

**Weight:** 10% of final decision (user experience matters!)

---

### 3.3 Performance Scoring

| Metric | npx | npm global | Difference | Acceptable? |
|--------|-----|------------|------------|-------------|
| **Cold Start** | 1-3s | 10-50ms | 1-3s slower | Depends on use case |
| **Warm Start** | 500ms-1s | 10-50ms | 500ms slower | Depends on frequency |
| **Disk Usage** | Cache grows | Fixed | Varies | Check actual size |
| **Network Dependency** | Yes (first run) | No (after install) | Critical for offline? | |
| **Memory Footprint** | Same | Same | N/A | |

**Scoring:**
- Performance critical (hot path, 10+ runs/day): +5 npm
- Performance matters (warm path, daily use): +3 npm
- Performance doesn't matter (rare use): +3 npx

---

### 3.4 Maintenance Burden Scoring

| Task | npx Effort | npm Effort | Winner |
|------|------------|------------|--------|
| **Initial Setup** | Document one command | Document install + usage | npx |
| **Version Updates** | Automatic (latest) | Users must update | npx |
| **Breaking Changes** | Can break users | Users control timing | npm |
| **Bug Fixes** | Fast propagation | Slow adoption | npx |
| **Support Burden** | Version confusion | Version consistency | npm |
| **Documentation** | Simpler | More complex | npx |

**For Developers (Tool Authors):**
- Prefer rapid iteration: +3 npx
- Prefer stability: +3 npm
- Prefer low support burden: +2 npm (consistent versions)

**For Users:**
- Prefer auto-updates: +3 npx
- Prefer control: +3 npm

---

### 3.5 Security Posture Scoring

| Factor | npx | npm global | Notes |
|--------|-----|------------|-------|
| **Supply Chain** | Downloads on every run* | Downloaded once | *npx uses cache |
| **Version Control** | Can pin, but awkward | Easy with version managers | |
| **Audit Trail** | npm audit works | npm audit works | Both support auditing |
| **Typosquatting** | Risk on first run | Risk on install | Same risk |
| **Compromised Package** | Auto-updates to bad version | Stays on safe version | npm wins |
| **Offline Security** | Requires network | Works offline | npm wins |

**Scoring:**
- Security critical environment: +3 npm (version control)
- Rapid security patches needed: +3 npx (auto-update)
- Offline requirements: +5 npm

---

## 4. Risk Assessment

### 4.1 Risks of Choosing npm Global

#### Risk 1: Installation Friction
**Severity:** Medium
**Likelihood:** High (especially for beginners)

**Problem:**
```bash
# Multi-step process
npm install -g my-tool
# User must understand PATH
# User must have permissions
# User must know to update
```

**Mitigation:**
- Excellent installation documentation
- Provide alternative methods (Homebrew, Scoop)
- Shell installer script as alternative
- Clear error messages for common issues

---

#### Risk 2: Version Fragmentation
**Severity:** High
**Likelihood:** Medium

**Problem:**
- Users on different versions
- Hard to support all versions
- Breaking changes cause pain
- "Works on my machine" syndrome

**Mitigation:**
- Semantic versioning (strict)
- Clear deprecation policy
- Version detection in tool (`tool --version`)
- Graceful degradation for old versions
- Update notifications in tool

---

#### Risk 3: Global Namespace Pollution
**Severity:** Low
**Likelihood:** Medium

**Problem:**
- Name conflicts with other tools
- Multiple versions can't coexist
- Uninstall leaves artifacts

**Mitigation:**
- Unique, descriptive package name
- Namespacing (@org/tool)
- Clean uninstall process
- Version managers (mise/asdf)

---

#### Risk 4: Update Adoption Lag
**Severity:** Medium
**Likelihood:** High

**Problem:**
- Users don't update regularly
- Security patches don't reach users
- Bug fixes slow to propagate

**Mitigation:**
- Update notifications in tool
- Auto-update mechanism (optional)
- Clear changelog and release notes
- Security alerts for critical updates

---

### 4.2 Risks of Choosing npx

#### Risk 1: Performance Overhead
**Severity:** Low-High (depends on usage)
**Likelihood:** High

**Problem:**
```bash
# First run: Downloads package (1-3s)
npx my-tool

# Cached run: Still checks registry (500ms-1s)
npx my-tool

# For daily-use tools, this adds up:
# 30 runs/day * 500ms = 15 seconds/day = 90 hours/year
```

**Mitigation:**
- Document performance characteristics
- Recommend npm global for power users
- Optimize package size
- Provide hybrid approach

---

#### Risk 2: Network Dependency
**Severity:** High
**Likelihood:** Medium

**Problem:**
- First run requires internet
- Registry downtime blocks usage
- Offline environments broken
- Corporate proxies/firewalls

**Mitigation:**
- Document offline usage (cache)
- Provide alternative install methods
- Support --offline flag
- Document proxy configuration

---

#### Risk 3: Version Unpredictability
**Severity:** Medium-High
**Likelihood:** Medium

**Problem:**
```bash
# "Latest" can change between runs
npx my-tool@latest

# Can break CI/CD pipelines
# Can break tutorials (version drift)
# Users can't reproduce issues
```

**Mitigation:**
- Pin versions in documentation
- Pin versions in package.json scripts
- Provide version detection
- Support explicit version syntax

---

#### Risk 4: Cache Confusion
**Severity:** Medium
**Likelihood:** High

**Problem:**
```bash
# Users don't understand npx cache
# "Why is it downloading again?"
# "How do I clear the cache?"
# "Where is the cache?"

# Cache location:
~/.npm/_npx/
# Can grow large (2-5GB+)
```

**Mitigation:**
- Document caching behavior
- Provide cache management docs
- Consider cache size in design
- Optimize package size

---

#### Risk 5: Breaking Changes Auto-Propagate
**Severity:** High
**Likelihood:** Medium

**Problem:**
```bash
# Yesterday: Tool worked
npx my-tool

# Today: New version released with breaking change
npx my-tool  # BROKEN

# User has no control
# Can't rollback easily
```

**Mitigation:**
- Strict semantic versioning
- Deprecation warnings (one version ahead)
- Support pinned versions
- Conservative breaking changes
- Clear migration guides

---

### 4.3 Common Pitfalls and Solutions

#### Pitfall 1: Mixing Approaches

**Problem:**
```bash
# User installs globally
npm install -g my-tool

# Documentation says npx
npx my-tool

# Which version runs? Confusion!
```

**Solution:**
- Pick one primary approach
- Document both clearly if hybrid
- Tool detects execution method
- Clear messaging in docs

---

#### Pitfall 2: Assuming Network Availability

**Problem:**
```bash
# User tries npx offline
npx my-tool  # Hangs or fails
```

**Solution:**
- Document offline behavior
- Provide npm global alternative
- Support --offline flag
- Clear error messages

---

#### Pitfall 3: Ignoring Windows Users

**Problem:**
```bash
# Works on Mac/Linux
npx my-tool

# Windows: PATH issues, permissions, etc.
```

**Solution:**
- Test on Windows extensively
- Provide Windows-specific docs
- Support Windows package managers (Scoop)
- Clear Windows error messages

---

#### Pitfall 4: Poor Error Messages

**Problem:**
```bash
npx my-tool
# Error: EACCES permission denied

# User: ???
```

**Solution:**
- Detect common errors
- Provide actionable error messages
- Link to troubleshooting docs
- Suggest fixes automatically

---

## 5. Hybrid Strategies

### 5.1 When to Support Both

**Support both npm and npx when:**
1. Large, diverse user base
2. Tool can operate in both modes
3. You have resources for dual support
4. Performance matters to some users
5. Simplicity matters to others

---

### 5.2 Implementation Patterns

#### Pattern 1: Detection and Warning

```javascript
// detect-execution-method.js

function detectExecutionMethod() {
  // Check if globally installed
  const globalPath = process.env.npm_config_prefix || '/usr/local';
  const isGlobal = __filename.includes(globalPath);

  // Check if via npx
  const isNpx = process.env.npm_execpath?.includes('npx');

  return { isGlobal, isNpx };
}

function provideGuidance() {
  const { isGlobal, isNpx } = detectExecutionMethod();

  if (isNpx) {
    console.log('ℹ️  Running via npx (one-time use)');
    console.log('   For daily use, install globally: npm install -g my-tool');
  }

  if (isGlobal) {
    console.log('✓ Globally installed (fast startup)');
  }
}
```

---

#### Pattern 2: Performance-Based Recommendation

```javascript
// recommend-install-method.js

let executionCount = 0;

function trackUsage() {
  const configPath = path.join(os.homedir(), '.my-tool', 'usage.json');

  if (fs.existsSync(configPath)) {
    const data = JSON.parse(fs.readFileSync(configPath));
    executionCount = data.count || 0;
  }

  executionCount++;

  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, JSON.stringify({ count: executionCount }));
}

function recommendInstallMethod() {
  const { isNpx } = detectExecutionMethod();

  if (isNpx && executionCount >= 5) {
    console.log('');
    console.log('💡 Tip: You\'ve used this tool 5 times via npx.');
    console.log('   Consider installing globally for better performance:');
    console.log('   npm install -g my-tool');
    console.log('');
  }
}
```

---

#### Pattern 3: Mode-Specific Features

```javascript
// mode-specific-features.js

function setupTool() {
  const { isGlobal, isNpx } = detectExecutionMethod();

  if (isGlobal) {
    // Enable features that benefit from persistence
    enableConfigCaching();
    enableUpdateChecking();
    enableShellCompletion();
  }

  if (isNpx) {
    // Optimize for one-time use
    disableUpdateChecks(); // Don't slow down npx
    skipConfigSetup();     // Don't create global config
    showQuickStartTips();  // Help first-time users
  }
}
```

---

#### Pattern 4: Documentation Strategy

**Structure documentation with tabs:**

```markdown
# Installation

=== "Quick Start (npx)"
    For one-time use or trying out the tool:

    ```bash
    npx my-tool init my-project
    ```

    No installation required. Always uses the latest version.

=== "Persistent Install (npm)"
    For daily use and better performance:

    ```bash
    npm install -g my-tool
    my-tool init my-project
    ```

    Faster startup, works offline, version control.

=== "Which Should I Choose?"
    - **Use npx if:** You're trying the tool for the first time, or you use it occasionally
    - **Use npm global if:** You use the tool daily, or you need offline access
```

---

### 5.3 Communication Approaches

#### Approach 1: Banner Messages

```bash
$ npx my-tool
┌────────────────────────────────────────────────────┐
│                                                    │
│   You're running my-tool via npx (one-time use)   │
│                                                    │
│   For daily use, install globally:                │
│   npm install -g my-tool                          │
│                                                    │
│   This message won't show again.                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

#### Approach 2: README Badges

```markdown
# My Tool

[![npm](https://img.shields.io/npm/v/my-tool)](https://www.npmjs.com/package/my-tool)
[![downloads](https://img.shields.io/npm/dt/my-tool)](https://www.npmjs.com/package/my-tool)

**Quick Start:**
```bash
npx my-tool init  # One-time use
```

**Install for daily use:**
```bash
npm install -g my-tool
```
```

---

#### Approach 3: Interactive Prompts

```javascript
// first-run-experience.js

async function firstRunExperience() {
  const { isNpx } = detectExecutionMethod();

  if (isNpx && !hasRunBefore()) {
    console.log('Welcome to my-tool! 👋\n');

    const response = await inquirer.prompt([{
      type: 'list',
      name: 'installPreference',
      message: 'How would you like to use my-tool?',
      choices: [
        {
          name: 'Just once (continue with npx)',
          value: 'npx'
        },
        {
          name: 'Install globally (recommended for regular use)',
          value: 'global'
        },
        {
          name: 'Learn more about the differences',
          value: 'learn'
        }
      ]
    }]);

    if (response.installPreference === 'global') {
      console.log('\nTo install globally, run:');
      console.log('  npm install -g my-tool\n');
      process.exit(0);
    }

    if (response.installPreference === 'learn') {
      showInstallMethodComparison();
    }
  }
}
```

---

### 5.4 Dual Support Checklist

**Implementation:**
- [ ] Tool works correctly via both npm and npx
- [ ] Detection of execution method
- [ ] Mode-specific optimizations
- [ ] Clear messaging for each mode
- [ ] Performance considerations documented

**Documentation:**
- [ ] Both methods documented clearly
- [ ] Comparison guide (when to use which)
- [ ] Migration guide (npx → npm or vice versa)
- [ ] Troubleshooting for both methods
- [ ] FAQ addressing common confusion

**Testing:**
- [ ] Test suite covers both execution methods
- [ ] Performance benchmarks for both
- [ ] Edge cases (cache, offline, permissions)
- [ ] Cross-platform testing (Windows, Mac, Linux)

**Communication:**
- [ ] README shows both methods
- [ ] Changelog mentions execution method changes
- [ ] Release notes highlight recommendations
- [ ] Community (Discord, forum) educated

---

## 6. Recommendations Format

### 6.1 Recommendation Template

```markdown
## Recommendation for [Tool Name]

### Primary Recommendation: [npm global / npx / hybrid]

**Confidence:** [High / Medium / Low]

**Rationale:**
- [Criterion 1]: [Score] - [Explanation]
- [Criterion 2]: [Score] - [Explanation]
- [Criterion 3]: [Score] - [Explanation]

**Final Score:**
- npm: [X/160]
- npx: [Y/160]
- Winner: [npm/npx] by [difference] points

---

### Alternative Approaches

#### Alternative 1: [npm/npx]
**When to consider:**
- [Scenario 1]
- [Scenario 2]

**Trade-offs:**
- Pros: [List]
- Cons: [List]

#### Alternative 2: [Hybrid]
**When to consider:**
- [Scenario]

**Implementation notes:**
- [Note 1]
- [Note 2]

---

### Trade-Off Analysis

| Factor | npm | npx | Winner | Notes |
|--------|-----|-----|--------|-------|
| First-time UX | | | | |
| Repeat-use UX | | | | |
| Performance | | | | |
| Simplicity | | | | |
| Version Control | | | | |
| Offline Support | | | | |

---

### Implementation Considerations

**For npm global approach:**
- [ ] Create comprehensive install docs
- [ ] Support version managers (mise/asdf)
- [ ] Provide update mechanism
- [ ] Handle permissions issues
- [ ] Test on Windows

**For npx approach:**
- [ ] Optimize package size
- [ ] Document caching behavior
- [ ] Support version pinning
- [ ] Handle offline gracefully
- [ ] Test performance

**For hybrid approach:**
- [ ] Implement execution detection
- [ ] Provide clear guidance
- [ ] Mode-specific optimizations
- [ ] Documentation with tabs
- [ ] Test both paths

---

### Migration Path

**If changing from current approach:**

**Current:** [npm/npx]
**Target:** [npm/npx]

**Migration Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Timeline:** [Duration]

**User Impact:** [Low/Medium/High]

**Communication Plan:**
- Announcement: [When]
- Deprecation: [When]
- Removal: [When]

---

### Success Metrics

**How to measure if this was the right choice:**

- User adoption rate
- Installation success rate
- Support ticket volume
- Performance metrics (if tracked)
- User satisfaction (surveys)
- GitHub stars / npm downloads

**Review Timeline:** [6 months / 1 year]
```

---

### 6.2 Real-World Recommendation Example

```markdown
## Recommendation for CODEX

### Primary Recommendation: Hybrid (Template + CLI with npm global)

**Confidence:** High

**Rationale:**
- **Lifespan:** Mixed (scaffolding + persistent tool) → Hybrid approach
- **Frequency:** Varies (setup once, use frequently) → Hybrid approach
- **State:** Stateful (workflow state, config) → npm global (+5)
- **Updates:** Moderate (monthly releases) → Neutral
- **Skill Level:** Expert developers → npm global (+3)
- **Friction:** Professionals (high tolerance) → npm global (+3)
- **Disk Space:** Developer workstations (abundant) → npm global (+2)
- **Versioning:** CI/CD pipelines need pinning → npm global (+5)

**Final Score:**
- npm: 118/160 (Strong recommendation)
- npx: 67/160 (Moderate)
- Winner: npm by 51 points

**However:** Project initialization benefits from npx, so hybrid recommended.

---

### Recommended Implementation

**Phase 1: Project Initialization (npx)**
```bash
npx create-codex-project my-project
```
- Uses npx for one-time scaffolding
- Always gets latest template
- Low friction for new users

**Phase 2: CLI Tool (npm global)**
```bash
npm install -g @codex/cli
# or
brew install codex
# or
curl -fsSL https://codex.dev/install.sh | sh

codex run workflow-name
codex task create "Task"
codex update
```
- Installed globally for daily use
- Fast startup (< 50ms)
- Offline support
- Version control with mise

---

### Alternative Approaches

#### Alternative 1: Pure npx (Not Recommended)
**Trade-offs:**
- Pros: Simplest docs, always latest
- Cons: Poor performance for daily use, state management awkward

**Why rejected:**
CODEX is used frequently (daily) and maintains state. npx overhead (500ms-1s per invocation) adds up to hours per year.

#### Alternative 2: Pure npm (Considered)
**Trade-offs:**
- Pros: Best performance, full control
- Cons: Higher initial friction, template distribution awkward

**Why not chosen:**
Project scaffolding genuinely benefits from npx (latest template). Hybrid captures best of both.

---

### Trade-Off Analysis

| Factor | Template (npx) | CLI (npm) | Winner | Notes |
|--------|----------------|-----------|--------|-------|
| First-time UX | Excellent | Good | npx | One command vs install first |
| Repeat-use UX | N/A | Excellent | npm | Fast, offline, familiar |
| Performance | Good (once) | Excellent | npm | 50ms vs 500ms |
| Simplicity | Excellent | Good | npx | No install step |
| Version Control | Template pinned | mise/asdf | npm | CI/CD needs pinning |
| Offline Support | Cached | Full | npm | Critical for dev |

---

### Implementation Considerations

**Template (npx):**
- [ ] Create create-codex-project package
- [ ] Interactive prompts (inquirer)
- [ ] Template versioning strategy
- [ ] Update mechanism for existing projects
- [ ] Documentation on template customization

**CLI (npm global):**
- [ ] Multi-platform binaries (GoReleaser)
- [ ] Homebrew tap (macOS)
- [ ] Scoop bucket (Windows)
- [ ] Shell installer (cross-platform)
- [ ] mise/asdf plugin (version management)
- [ ] Update mechanism (self-update command)

**Documentation:**
- [ ] Quick Start guide (both methods)
- [ ] When to use which
- [ ] Migration guides
- [ ] Troubleshooting for both
- [ ] FAQ on execution methods

---

### Migration Path

**Current:** Pre-v0.1.0 (no published distribution)

**Target:** Hybrid (Template + CLI)

**Timeline:**
- Week 1-2: Create template repository
- Week 2-3: Build CLI tool (Go/Rust)
- Week 3-4: Set up distribution (GoReleaser, Homebrew, Scoop)
- Week 4: Documentation and launch

**User Impact:** None (net new)

---

### Success Metrics

**6-month review:**
- Template usage (npx create-codex-project): 100+ uses/month
- CLI installs (npm/Homebrew/etc): 50+ active users
- Support tickets: < 5/month for install issues
- User feedback: Positive sentiment on installation experience

**Indicators of success:**
- Low installation friction (quick start works)
- Fast daily operations (< 100ms)
- Positive community feedback
```

---

## 7. Real-World Case Studies

### 7.1 Case Study: create-react-app

**Decision:** npx (primary)

**Context:**
- Project scaffolder (one-time use)
- Fast-moving (frequent updates)
- Target: Beginners to experts
- Want latest template always

**Implementation:**
```bash
npx create-react-app my-app
```

**Why it works:**
- Used once per project
- Always get latest React template
- No global install burden
- Simple documentation

**Score:** npx 140/160 (near-perfect fit)

**Lessons:**
- npx is ideal for scaffolding
- Version pinning available but rarely needed
- Global install option exists but rarely used

---

### 7.2 Case Study: TypeScript (tsc)

**Decision:** npm global (primary)

**Context:**
- Used frequently (every build)
- Stable (quarterly updates)
- Performance matters
- Version pinning critical

**Implementation:**
```bash
npm install -g typescript
tsc --version
```

**Why it works:**
- Daily use tool
- Fast startup critical
- Offline support needed
- Version control with mise/asdf

**Score:** npm 145/160 (excellent fit)

**Lessons:**
- npm global for daily-use tools
- Version managers solve multi-version needs
- Performance matters at scale

---

### 7.3 Case Study: Prettier

**Decision:** Hybrid (npm local preferred, npx supported)

**Context:**
- Used frequently (on save, pre-commit)
- Stable (monthly updates)
- Performance matters
- Team consistency critical

**Implementation:**
```bash
# Preferred: Local install
npm install --save-dev prettier

# Supported: Quick format
npx prettier --write .

# Supported: Global
npm install -g prettier
```

**Why hybrid works:**
- Local install for consistency
- npx for quick one-off formatting
- Global for personal use

**Score:** Local 120/160, npx 70/160, Global 90/160

**Lessons:**
- Formatting tools benefit from local install
- npx useful for quick operations
- Support all three for flexibility

---

### 7.4 Case Study: Vercel CLI

**Decision:** npm global (primary)

**Context:**
- Used frequently (multiple deployments/day)
- Stateful (authentication, config)
- Performance matters
- Professional developers

**Implementation:**
```bash
npm install -g vercel
vercel login
vercel deploy
```

**Why it works:**
- Frequent use (daily)
- Maintains authentication state
- Fast startup critical
- Professional audience

**Score:** npm 130/160 (strong fit)

**Lessons:**
- Stateful tools need npm global
- Auth/config storage requires persistence
- Professional users expect global install

---

### 7.5 Case Study: cowsay

**Decision:** npm global (traditional), works via npx

**Context:**
- Novelty tool
- Infrequent use
- Stateless
- No performance requirements

**Implementation:**
```bash
# Traditional
npm install -g cowsay
cowsay "Hello"

# Modern
npx cowsay "Hello"
```

**Why both work:**
- Stateless operation
- Infrequent use
- No performance impact
- Simple tool

**Score:** npx 100/160, npm 90/160 (slight npx preference)

**Lessons:**
- Simple, stateless tools work well with npx
- Legacy tools can adapt to npx
- Performance less critical for fun tools

---

## 8. Implementation Patterns

### 8.1 Package Structure

#### For npm global:
```
my-tool/
├── bin/
│   └── my-tool           # Executable script
├── lib/
│   ├── cli.js            # CLI logic
│   ├── commands/         # Command implementations
│   └── utils/            # Utilities
├── package.json          # With "bin" field
└── README.md
```

**package.json:**
```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "bin": {
    "my-tool": "./bin/my-tool"
  },
  "preferGlobal": true,
  "engines": {
    "node": ">=18"
  }
}
```

---

#### For npx:
```
create-my-project/
├── bin/
│   └── create-my-project # Executable
├── templates/            # Project templates
│   ├── default/
│   ├── minimal/
│   └── advanced/
├── lib/
│   ├── scaffold.js       # Scaffolding logic
│   ├── prompts.js        # Interactive prompts
│   └── templates.js      # Template handling
└── package.json
```

**package.json:**
```json
{
  "name": "create-my-project",
  "version": "1.0.0",
  "bin": {
    "create-my-project": "./bin/create-my-project"
  },
  "files": [
    "bin",
    "lib",
    "templates"
  ]
}
```

---

### 8.2 Execution Detection

```javascript
// detect-execution.js

function detectExecutionContext() {
  const context = {
    method: 'unknown',
    isGlobal: false,
    isNpx: false,
    isLocal: false,
    version: require('./package.json').version
  };

  // Check if via npx
  if (process.env.npm_execpath?.includes('npx-cli.js') ||
      process.env.npm_execpath?.includes('npx')) {
    context.method = 'npx';
    context.isNpx = true;
    return context;
  }

  // Check if global install
  const globalPaths = [
    process.env.npm_config_prefix,
    '/usr/local',
    '/usr',
    process.env.APPDATA, // Windows
    process.env.LOCALAPPDATA // Windows
  ].filter(Boolean);

  const isGlobalPath = globalPaths.some(p => __filename.includes(p));

  if (isGlobalPath) {
    context.method = 'global';
    context.isGlobal = true;
    return context;
  }

  // Likely local install (project dependency)
  context.method = 'local';
  context.isLocal = true;
  return context;
}

module.exports = { detectExecutionContext };
```

---

### 8.3 Performance Optimization

```javascript
// performance-optimization.js

const { detectExecutionContext } = require('./detect-execution');

function optimizeForContext() {
  const context = detectExecutionContext();

  if (context.isNpx) {
    // Optimize for one-time use
    return {
      skipUpdateCheck: true,      // Don't slow down npx
      skipAnalytics: true,         // No persistent tracking
      minimalOutput: false,        // Show helpful info
      cacheConfig: false,          // Don't create ~/.my-tool
      loadPluginsLazily: true,     // Faster startup
      skipTelemetry: true          // No phone home
    };
  }

  if (context.isGlobal) {
    // Optimize for repeat use
    return {
      skipUpdateCheck: false,      // Weekly check
      skipAnalytics: false,        // Track usage
      minimalOutput: true,         // Assume familiarity
      cacheConfig: true,           // Cache in ~/.my-tool
      loadPluginsLazily: false,    // Pre-load for speed
      skipTelemetry: false         // Optional telemetry
    };
  }

  // Local (default)
  return {
    skipUpdateCheck: true,         // Managed by package.json
    skipAnalytics: true,
    minimalOutput: true,
    cacheConfig: false,
    loadPluginsLazily: true,
    skipTelemetry: true
  };
}

module.exports = { optimizeForContext };
```

---

### 8.4 User Guidance

```javascript
// user-guidance.js

const chalk = require('chalk');
const { detectExecutionContext } = require('./detect-execution');

function provideExecutionGuidance() {
  const context = detectExecutionContext();

  if (context.isNpx) {
    console.log(chalk.blue('ℹ️  Running via npx (one-time use)'));

    const usageFile = path.join(os.homedir(), '.my-tool', 'usage.json');
    let usageCount = 0;

    if (fs.existsSync(usageFile)) {
      const data = JSON.parse(fs.readFileSync(usageFile));
      usageCount = data.count || 0;
    }

    if (usageCount >= 5) {
      console.log('');
      console.log(chalk.yellow('💡 You\'ve used this tool multiple times!'));
      console.log(chalk.yellow('   Consider installing globally for better performance:'));
      console.log(chalk.cyan('   npm install -g my-tool'));
      console.log('');
    }
  }

  if (context.isGlobal) {
    // Optional: Show update availability
    checkForUpdates().then(update => {
      if (update.available) {
        console.log('');
        console.log(chalk.yellow(`📦 Update available: ${update.latest}`));
        console.log(chalk.yellow(`   Current: ${context.version}`));
        console.log(chalk.cyan('   npm install -g my-tool@latest'));
        console.log('');
      }
    }).catch(() => {
      // Silently fail (don't slow down tool)
    });
  }
}

async function checkForUpdates() {
  // Implementation: Check npm registry for latest version
  // Cache result for 24 hours
  // Return { available: boolean, latest: string }
}

module.exports = { provideExecutionGuidance };
```

---

### 8.5 Documentation Templates

#### README.md Template:

```markdown
# My Tool

> One-line description of what the tool does

[![npm version](https://badge.fury.io/js/my-tool.svg)](https://www.npmjs.com/package/my-tool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start

### Option 1: One-Time Use (npx)

Perfect for trying out the tool or occasional use:

```bash
npx my-tool [command] [options]
```

**Pros:** No installation, always latest version
**Cons:** Slower startup, requires internet connection

### Option 2: Install Globally (npm)

Recommended for daily use:

```bash
npm install -g my-tool
my-tool [command] [options]
```

**Pros:** Fast startup, works offline
**Cons:** Requires installation step

### Which Should I Choose?

- **Use npx** if you're trying the tool for the first time or use it occasionally
- **Install globally** if you use the tool daily or need offline access

## Installation

### npm (recommended for regular use)

```bash
npm install -g my-tool
```

### Homebrew (macOS/Linux)

```bash
brew install my-org/tap/my-tool
```

### Scoop (Windows)

```bash
scoop bucket add my-org https://github.com/my-org/scoop-bucket
scoop install my-tool
```

### Binary Downloads

Download pre-built binaries from [Releases](https://github.com/my-org/my-tool/releases).

## Usage

[Usage examples here]

## Documentation

[Link to full documentation]

## FAQ

### Why is npx slower than npm global?

npx downloads the package on first use and checks for updates on subsequent runs. Global installation downloads once and runs immediately.

### Can I use a specific version?

```bash
# With npx
npx my-tool@1.2.3

# With npm global
npm install -g my-tool@1.2.3
```

### How do I update?

```bash
# npm global
npm update -g my-tool

# npx
# Automatically uses latest unless version pinned
```

## License

MIT
```

---

## 9. Conclusion and Quick Reference

### 9.1 Decision Summary Table

| Tool Type | Recommendation | Primary Reason |
|-----------|---------------|----------------|
| **Project Scaffolder** | npx | One-time use, always latest |
| **Daily CLI Tool** | npm global | Performance, offline support |
| **Build Tool** | npm local | Version consistency per-project |
| **Stateful Tool** | npm global | Config/auth persistence |
| **Security Scanner** | npx | Always latest signatures |
| **Formatter/Linter** | npm local | Team consistency |
| **Deployment CLI** | npm global | Frequent use, state |
| **Migration Script** | npx | One-time, no install burden |
| **Developer Server** | npm local | Project-specific config |
| **Package Manager** | npm global or native | System-level tool |

---

### 9.2 Quick Checklist

**Choose npx if:**
- [ ] Used once or rarely (< 5 times/project)
- [ ] Project scaffolding or initialization
- [ ] Always want latest version
- [ ] Stateless operation
- [ ] Target audience is beginners
- [ ] Installation friction is a problem

**Choose npm global if:**
- [ ] Used daily or very frequently
- [ ] Maintains configuration or state
- [ ] Performance matters (startup time)
- [ ] Offline support needed
- [ ] Version control critical
- [ ] Professional developer audience

**Choose Hybrid if:**
- [ ] Large, diverse user base
- [ ] Tool can work both ways
- [ ] Resources for dual support
- [ ] Scaffolding + persistent tool
- [ ] Educational content + daily use

---

### 9.3 Final Recommendation Framework

```
1. Score your tool using Section 3 (Scoring Matrix)
2. Run through Decision Tree (Section 2)
3. Assess risks (Section 4)
4. If score is close, consider hybrid (Section 5)
5. Use recommendation template (Section 6)
6. Study similar tools (Section 7)
7. Implement with best practices (Section 8)
```

---

### 9.4 Resources

**Tools:**
- **mise:** Universal version manager ([mise.jdx.dev](https://mise.jdx.dev))
- **GoReleaser:** Multi-platform releases ([goreleaser.com](https://goreleaser.com))
- **npx documentation:** [npm docs](https://docs.npmjs.com/cli/v10/commands/npx)

**Examples:**
- **npx-first:** create-react-app, create-next-app, create-vite
- **npm-first:** typescript, eslint, prettier, gh, vercel
- **Hybrid:** many modern tools support both

**Community:**
- npm forums
- GitHub Discussions (tool-specific)
- Stack Overflow

---

## Appendix: Quick Decision Tool

### Interactive Questions

Answer these questions to get a recommendation:

1. **How often will users run your tool?**
   - Once per project → +5 npx
   - Weekly → Neutral
   - Daily → +5 npm

2. **Does it maintain state or configuration?**
   - Yes → +5 npm
   - No → +5 npx

3. **Is performance critical?**
   - Yes (hot path) → +5 npm
   - No → +3 npx

4. **Target audience?**
   - Beginners → +3 npx
   - Professionals → +3 npm

5. **Update frequency?**
   - Weekly updates → +3 npx
   - Quarterly updates → +3 npm

**Score:**
- npm > 15: Recommend npm global
- npx > 15: Recommend npx
- Tie: Recommend hybrid

---

**End of Framework**

This framework provides a systematic approach to choosing between npm global and npx for your tool. Remember: there's no universal right answer—the best choice depends on your specific tool, users, and use case.
