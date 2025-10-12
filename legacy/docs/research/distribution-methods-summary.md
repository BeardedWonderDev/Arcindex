# Developer Tool Distribution Methods - Executive Summary

**Research Date:** October 9, 2025
**Full Analysis:** [distribution-methods-analysis.md](./distribution-methods-analysis.md)

---

## Quick Reference: Distribution Methods

### 1. Package Managers

#### Homebrew (macOS/Linux)
- **Install:** `brew install tool`
- **Pros:** Best macOS UX, auto-updates, high trust
- **Cons:** macOS/Linux only, requires formula maintenance
- **Maintainer Complexity:** Medium
- **Best for:** macOS-first CLI tools

#### Scoop/Winget (Windows)
- **Install:** `scoop install tool` or `winget install tool`
- **Pros:** Windows-native, Scoop needs no admin
- **Cons:** Must support 2-3 Windows managers, fragmented
- **Maintainer Complexity:** Medium-High
- **Best for:** Windows developer tools

#### apt/yum (Linux)
- **Install:** `apt install tool` or `dnf install tool`
- **Pros:** Native system integration
- **Cons:** Must maintain per-distro packages, high complexity
- **Maintainer Complexity:** High
- **Best for:** System-level tools

---

### 2. Direct Binary Downloads

#### Shell Installer (curl | bash)
- **Install:** `curl -fsSL https://tool.com/install.sh | sh`
- **Pros:** No dependencies, works everywhere, fast adoption
- **Cons:** Security concerns, no auto-updates
- **Maintainer Complexity:** Low-Medium
- **Best for:** Cross-platform CLI tools

**Real-World Examples:**
- Deno: `curl -fsSL https://deno.land/install.sh | sh`
- Bun: `curl -fsSL https://bun.sh/install | bash`
- Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

---

### 3. Docker-Based Distribution

#### Container as Tool
- **Install:** `docker pull tool/cli`
- **Pros:** Isolation, consistency, multi-version support
- **Cons:** Docker required, performance overhead, verbose commands
- **Maintainer Complexity:** Medium-High
- **Best for:** Complex dependencies, CI/CD, enterprise

**Usage Pattern:**
```bash
docker run --rm -it -v $(pwd):/workspace tool/cli command
```

---

### 4. Git-Based Templates

#### GitHub Templates / degit
- **Install:** `npx create-tool my-project` or `degit user/repo my-project`
- **Pros:** No persistent tool, includes examples, low maintenance
- **Cons:** No updates, no CLI logic, git required
- **Maintainer Complexity:** Low
- **Best for:** Project scaffolding, initial setup

**Real-World Examples:**
- Svelte: `degit sveltejs/template`
- Next.js: `npx create-next-app`
- Vite: `npm create vite@latest`

---

### 5. Multi-Platform Automation

#### GoReleaser
- **Purpose:** Automate releases for all platforms from single config
- **Supports:** Binaries, Homebrew, Scoop, Docker, checksums, signatures
- **Pros:** One tag → all platforms updated, highly automated
- **Cons:** High initial setup
- **Maintainer Complexity:** High initially, very low ongoing
- **Best for:** Mature projects supporting multiple platforms

**Release Process:**
```bash
git tag v1.0.0 && git push --tags
# GitHub Actions + GoReleaser handle everything
```

---

## Comparison Matrix

| Method | Speed | Friction | Cross-Platform | Auto-Update | Discoverability |
|--------|-------|----------|----------------|-------------|-----------------|
| **npm/npx** | Fast | Low | Yes | Yes | High |
| **Homebrew** | Medium | Low | macOS/Linux | Yes | High |
| **Scoop/Winget** | Medium | Low | Windows | Manual | Medium |
| **Binary Script** | Fast | Low | Yes | Manual | Low |
| **Docker** | Slow | Medium | Yes | Manual | Medium |
| **Git Template** | Fast | Low | Yes | N/A | Low |

---

## Real-World Tool Analysis

### GitHub CLI (gh)
**Distribution Methods:**
- Homebrew (macOS/Linux)
- Scoop, Winget, Chocolatey (Windows)
- apt/yum (Linux)
- Manual binary downloads
- **Does NOT use:** npm, Docker (primary)

**Why:** Broad reach, native experience on all platforms, high discoverability

---

### Stripe CLI
**Distribution Methods:**
- Homebrew (macOS)
- Scoop (Windows)
- Docker image
- Manual binary downloads
- **Does NOT use:** npm, Winget

**Why:** Developer-focused package managers, Docker for CI/CD

---

### Vercel CLI
**Distribution Methods:**
- npm (primary)
- **Does NOT use:** Homebrew, Scoop, Docker

**Why:** Node.js tool, leverages existing npm ecosystem

---

### Deno
**Distribution Methods:**
- Shell installer (primary)
- Homebrew, Cargo
- Manual downloads
- **Does NOT use:** npm (by design), Docker (primary)

**Why:** Fast adoption with shell script, package managers for discoverability

---

## Decision Framework

### Choose npm/npx if:
- Tool is Node.js-based
- Target audience already uses npm
- Need version management and auto-updates
- Want to leverage npm ecosystem

### Choose Package Managers (Homebrew/Scoop) if:
- CLI tool for developers
- Want high discoverability
- Can maintain per-platform packages
- Target professional developers

### Choose Binary Downloads if:
- Want fastest adoption
- Cross-platform support critical
- Minimal dependencies
- Users in air-gapped environments

### Choose Docker if:
- Complex dependencies
- Need strong isolation
- CI/CD is primary use case
- Target enterprise/DevOps

### Choose Git Template if:
- Tool is really project scaffolding
- One-time setup (not persistent tool)
- Want to include examples/workflows
- Low maintenance preferred

### Choose Multi-Platform (GoReleaser) if:
- Mature project
- Supporting multiple platforms
- Can invest in initial setup
- Want automated releases

---

## Version Management in 2025

### mise (formerly rtx)
**What:** Universal version manager for developer tools
**Why:** Replaces nvm, pyenv, rbenv, asdf—all in one
**Speed:** 0ms overhead (no shims), written in Rust

**Installation:**
```bash
curl https://mise.run | sh
```

**Usage:**
```bash
mise install node@20.10.0
mise install python@3.11.0
mise local node@18.17.0  # Per-project
```

**Why It Matters:**
- Professional developers expect version management
- Single tool for all runtimes
- Compatible with asdf plugins
- Becoming industry standard (2025 trend)

---

## Security Best Practices

### For Shell Installers
1. Wrap code in functions (prevent partial execution)
2. Verify checksums before installation
3. Provide inspection option (download first)
4. Use HTTPS exclusively
5. Fail fast on errors
6. Minimal sudo usage

### For Package Distribution
1. Generate checksums for all binaries
2. Sign releases (GPG or code signing)
3. HTTPS-only downloads
4. Automated security scanning
5. Dependency auditing

### For Users
1. Inspect scripts before running: `curl URL | less`
2. Download first: `curl URL -o script.sh && bash script.sh`
3. Verify signatures when available
4. Trust the source (GitHub, official domains)

**Reality:** Trust model is identical for `curl | bash` vs download-then-execute. Users who can't audit scripts must trust the author either way.

---

## CODEX-Specific Recommendations

### Recommended: Hybrid Approach

**1. Template for Project Structure**
```bash
npx create-codex-project my-project
```
- Quick initialization
- Includes workflows, agents, docs
- Low maintenance

**2. CLI Tool for Ongoing Use**
```bash
# Install
brew install beardedwonder/tap/codex
curl -fsSL https://codex.dev/install.sh | sh

# Use
codex run workflow
codex task create
codex update
```
- Persistent tooling
- Distributed via Homebrew, Scoop, binary script
- Automated with GoReleaser

**3. Docker for CI/CD (Optional)**
```yaml
- uses: docker://beardedwonder/codex:latest
```

---

## Implementation Roadmap

### Phase 1: MVP (Week 1-2)
- [ ] Decide architecture (Template vs CLI vs Hybrid)
- [ ] Create template repository
- [ ] Binary downloads + shell installer
- [ ] GitHub Releases
- [ ] Basic documentation

### Phase 2: Automation (Week 3-4)
- [ ] Interactive scaffolder (`create-codex-project`)
- [ ] Homebrew tap
- [ ] GoReleaser configuration
- [ ] GitHub Actions release workflow

### Phase 3: Growth (Ongoing)
- [ ] Scoop/Winget (Windows)
- [ ] Docker image (optional)
- [ ] mise/asdf plugin
- [ ] Linux packages

### Phase 4: Maturity (Future)
- [ ] Code signing
- [ ] Enterprise docs
- [ ] Custom repositories
- [ ] Additional package managers

---

## Key Statistics (2025)

### Package Manager Adoption
- **Homebrew:** 5M+ users (macOS standard)
- **npm:** 20M+ developers (largest registry)
- **Docker:** 92% container usage among IT pros, 30% across all industries
- **Scoop:** Growing Windows developer adoption
- **Winget:** Pre-installed Windows 11 (official)

### Distribution Trends
- **pnpm:** Becoming default for monorepos (Next.js, Vite, Nuxt migrated)
- **mise/asdf:** Replacing language-specific version managers
- **Deno:** URL imports (no package manager)
- **Binary downloads:** Gold standard for CLI tools
- **GoReleaser:** Industry standard for multi-platform releases

---

## Resources

### Documentation
- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [GoReleaser Docs](https://goreleaser.com/)
- [mise Documentation](https://mise.jdx.dev/)
- [Scoop Documentation](https://scoop.sh/)

### Example Projects
- [GitHub CLI](https://github.com/cli/cli) - Multi-platform excellence
- [Deno](https://github.com/denoland/deno) - Shell installer pattern
- [Stripe CLI](https://github.com/stripe/stripe-cli) - Docker + package managers

### Tools
- [GoReleaser](https://goreleaser.com/) - Release automation
- [cargo-dist](https://github.com/axodotdev/cargo-dist) - Rust equivalent
- [degit](https://github.com/Rich-Harris/degit) - Template cloning
- [mise](https://mise.jdx.dev/) - Version management

---

## Conclusion

**For maximum reach and user satisfaction:**
1. **Start simple:** Binary downloads + shell installer
2. **Add discoverability:** Homebrew (macOS) + Scoop (Windows)
3. **Automate everything:** GoReleaser + GitHub Actions
4. **Support version management:** mise/asdf plugin
5. **Consider Docker:** For CI/CD and complex setups

**The hybrid approach (template + CLI) offers the best user experience for tools like CODEX that need both initial scaffolding and ongoing management capabilities.**

---

**Next Steps:**
1. Review full analysis: [distribution-methods-analysis.md](./distribution-methods-analysis.md)
2. Decide on CODEX architecture (Template vs CLI vs Hybrid)
3. Implement Phase 1 (MVP distribution)
4. Set up automation (GoReleaser + GitHub Actions)
5. Document installation methods comprehensively
