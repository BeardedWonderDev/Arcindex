# Distribution Methods - Quick Comparison Table

**Research Date:** October 9, 2025

---

## Method Overview

| Method | Install Command | Platforms | Dependencies | Auto-Update |
|--------|----------------|-----------|--------------|-------------|
| **npm/npx** | `npm install -g tool` | All | Node.js | Yes |
| **Homebrew** | `brew install tool` | macOS, Linux | None | Yes |
| **Scoop** | `scoop install tool` | Windows | None | Manual |
| **Winget** | `winget install tool` | Windows | None | Manual |
| **Binary Script** | `curl URL \| sh` | Linux, macOS | curl/wget | Manual |
| **Docker** | `docker pull tool` | All | Docker | Manual |
| **Git Template** | `degit user/repo` | All | git | N/A |
| **GoReleaser** | N/A (automation) | All | None | Varies |

---

## Detailed Comparison

### User Experience

| Method | Installation Speed | User Friction | Learning Curve | Uninstall Ease |
|--------|-------------------|---------------|----------------|----------------|
| **npm/npx** | Fast | Low | Low | Easy |
| **Homebrew** | Medium | Low | Low | Easy |
| **Scoop** | Medium | Low | Low | Easy |
| **Winget** | Medium | Low | Low | Easy |
| **Binary Script** | Fast | Low | Low | Manual |
| **Docker** | Slow | Medium | Medium | N/A |
| **Git Template** | Fast | Low | Low | N/A |

### Maintainer Perspective

| Method | Initial Setup | Ongoing Effort | Automation | Documentation Needed |
|--------|--------------|----------------|------------|---------------------|
| **npm/npx** | Low | Low | High | Low |
| **Homebrew** | Medium | Low | High | Medium |
| **Scoop** | Medium | Low | High | Medium |
| **Winget** | Medium | Low | High | Medium |
| **Binary Script** | Medium | Very Low | High | Medium |
| **Docker** | Medium-High | Medium | High | High |
| **Git Template** | Low | Very Low | N/A | Low |
| **GoReleaser** | High | Very Low | Very High | Medium |

### Technical Capabilities

| Method | Version Pinning | Rollback Support | Offline Install | Multi-Version | Security |
|--------|-----------------|------------------|-----------------|---------------|----------|
| **npm/npx** | Excellent | Yes | Cached | Yes | Medium |
| **Homebrew** | Limited | Difficult | Cached | No | High |
| **Scoop** | Good | Yes | Cached | No | High |
| **Winget** | Good | Yes | Cached | No | High |
| **Binary Script** | Good | Manual | No | Manual | User Trust |
| **Docker** | Excellent | Yes | No | Yes | High |
| **Git Template** | Excellent | Yes | Cached | N/A | High |

### Platform Support Matrix

| Method | macOS | Linux | Windows | WSL | Architecture Support |
|--------|-------|-------|---------|-----|---------------------|
| **npm/npx** | Yes | Yes | Yes | Yes | All (Node.js runs on) |
| **Homebrew** | Yes | Yes | No | Yes | x64, ARM64 |
| **Scoop** | No | No | Yes | No | x64 |
| **Winget** | No | No | Yes | No | x64, ARM64 |
| **Binary Script** | Yes | Yes | WSL only | Yes | Detect + download |
| **Docker** | Yes | Yes | Yes | Yes | Multi-arch builds |
| **Git Template** | Yes | Yes | Yes | Yes | N/A (source code) |

---

## Use Case Matrix

### Best Method for Each Scenario

| Use Case | Primary Method | Secondary Method | Avoid |
|----------|---------------|------------------|-------|
| **Simple CLI tool** | Binary Script | Homebrew | Docker |
| **Node.js tool** | npm | Binary Script | N/A |
| **Complex dependencies** | Docker | N/A | Binary Script |
| **Project scaffolding** | Git Template / npx | N/A | Docker |
| **Enterprise deployment** | Package Managers | Docker | Binary Script |
| **CI/CD usage** | Docker | Binary Script | Package Managers |
| **Developer power users** | mise/asdf | Homebrew | npm |
| **Windows developers** | Scoop | Winget | Homebrew |
| **macOS developers** | Homebrew | Binary Script | Scoop |
| **Linux sysadmins** | apt/yum | Binary Script | npm |
| **Cross-platform tool** | Binary Script + Homebrew + Scoop | Docker | Single platform |
| **Offline environments** | Manual binaries | N/A | All others |

---

## Real-World Tool Distribution Strategies

### GitHub CLI (gh)

| Platform | Methods Used |
|----------|-------------|
| **macOS** | Homebrew, MacPorts, Conda, .pkg installer |
| **Windows** | Winget, Scoop, Chocolatey, MSI installer |
| **Linux** | apt, dnf, zypper, Snap, manual binaries |

**Strategy:** Maximum platform coverage with native package managers

---

### Stripe CLI

| Platform | Methods Used |
|----------|-------------|
| **macOS** | Homebrew |
| **Windows** | Scoop, manual zip |
| **Linux** | apt, yum, manual tar.gz |
| **All** | Docker image |

**Strategy:** Developer-focused package managers + Docker for CI/CD

---

### Vercel CLI

| Platform | Methods Used |
|----------|-------------|
| **All** | npm (primary and only) |

**Strategy:** Leverage existing Node.js ecosystem

---

### Deno

| Platform | Methods Used |
|----------|-------------|
| **macOS** | Shell installer, Homebrew |
| **Windows** | PowerShell installer, Scoop, Chocolatey |
| **Linux** | Shell installer, Cargo, manual binaries |

**Strategy:** Shell installer (primary) + package managers (discoverability)

---

### Rust (rustup)

| Platform | Methods Used |
|----------|-------------|
| **All** | Shell installer (primary) |
| **Optional** | Package managers available but not recommended |

**Strategy:** Shell installer only (full control over installation)

---

## Pros & Cons Summary

### npm/npx
**Pros:**
- Largest package registry (20M+ developers)
- Excellent version management
- Auto-updates built-in
- Great for Node.js ecosystem

**Cons:**
- Requires Node.js (large dependency)
- Security concerns (npm supply chain)
- Bloated node_modules
- Not ideal for non-JS tools

---

### Homebrew
**Pros:**
- macOS standard (5M+ users)
- Excellent UX
- Automatic updates
- High trust factor
- Dependency management

**Cons:**
- macOS/Linux only
- Version pinning complex (2025)
- Formula maintenance required
- Update delays (PR review)

---

### Scoop (Windows)
**Pros:**
- No admin rights required
- Developer-friendly
- Clean user-local installation
- Unix-like philosophy

**Cons:**
- Windows only
- Smaller community than Chocolatey
- Less enterprise adoption

---

### Winget (Windows)
**Pros:**
- Microsoft official
- Pre-installed (Windows 11)
- Free and open-source
- Growing ecosystem

**Cons:**
- Windows only
- Smaller package count (8K+)
- Less mature than Chocolatey

---

### Binary Script (curl | bash)
**Pros:**
- No dependencies
- Works everywhere (Unix-like)
- Fastest adoption
- Version control easy
- Full control

**Cons:**
- Security stigma
- No automatic updates
- No discoverability
- PATH management manual

---

### Docker
**Pros:**
- Perfect isolation
- Consistent everywhere
- Multi-version support
- CI/CD standard
- Sandboxed execution

**Cons:**
- Docker required (large dep)
- Performance overhead
- Complex for end users
- Verbose commands
- Large image sizes

---

### Git Template
**Pros:**
- No persistent installation
- Includes examples/docs
- Low maintenance
- Fast setup
- Full customization

**Cons:**
- No updates after init
- No CLI logic (unless npx)
- git dependency
- No discoverability

---

## Feature Importance by Audience

### End-User Developers
| Feature | Importance | Best Methods |
|---------|------------|-------------|
| Easy install | Critical | Homebrew, npm, Binary Script |
| Auto-updates | High | Homebrew, npm |
| No dependencies | High | Binary Script, Homebrew |
| Familiar tools | High | Package managers |
| Version pinning | Medium | npm, Docker, mise |

### DevOps/Enterprise
| Feature | Importance | Best Methods |
|---------|------------|-------------|
| Automation | Critical | Docker, Package managers |
| Security | Critical | Package managers, Docker |
| Reproducibility | Critical | Docker, version managers |
| Offline support | High | Manual binaries |
| Audit trail | High | Package managers |

### Open Source Contributors
| Feature | Importance | Best Methods |
|---------|------------|-------------|
| Easy contribution | Critical | Git-based |
| Version flexibility | Critical | mise/asdf, Docker |
| Multi-version | High | Docker, version managers |
| Fast setup | High | Binary script, Template |

---

## Distribution Effort Estimates

### Time to Implement (First Release)

| Method | Initial Setup | Testing | Documentation | Total |
|--------|--------------|---------|---------------|-------|
| **npm** | 2 hours | 1 hour | 1 hour | 4 hours |
| **Homebrew** | 4 hours | 2 hours | 2 hours | 8 hours |
| **Scoop** | 3 hours | 2 hours | 1 hour | 6 hours |
| **Binary Script** | 6 hours | 4 hours | 2 hours | 12 hours |
| **Docker** | 8 hours | 4 hours | 3 hours | 15 hours |
| **Git Template** | 2 hours | 1 hour | 2 hours | 5 hours |
| **GoReleaser (all)** | 16 hours | 8 hours | 4 hours | 28 hours |

### Time per Release (Ongoing)

| Method | Build | Test | Deploy | Total |
|--------|-------|------|--------|-------|
| **npm** | 0 min | 5 min | 2 min | 7 min |
| **Homebrew** | 5 min | 5 min | 5 min | 15 min |
| **Scoop** | 5 min | 5 min | 5 min | 15 min |
| **Binary Script** | 10 min | 10 min | 5 min | 25 min |
| **Docker** | 15 min | 10 min | 10 min | 35 min |
| **Git Template** | 0 min | 0 min | 0 min | 0 min |
| **GoReleaser (all)** | 0 min | 15 min | 5 min | 20 min |

*Assumes automation is set up*

---

## Cost Analysis

### Hosting Costs

| Method | Storage | Bandwidth | Other | Monthly Cost |
|--------|---------|-----------|-------|--------------|
| **npm** | Free | Free | None | $0 |
| **Homebrew** | GitHub | Free | None | $0 |
| **Scoop** | GitHub | Free | None | $0 |
| **Binary Script** | GitHub Releases | Free | None | $0 |
| **Docker** | Docker Hub (Free tier) | Free | None | $0 - $5 |
| **Git Template** | GitHub | Free | None | $0 |
| **GoReleaser** | GitHub | Free | None | $0 |

*Assuming GitHub for hosting*

### Developer Time Cost

| Method | Setup Cost | Maintenance (per release) | Annual Cost (12 releases) |
|--------|-----------|--------------------------|---------------------------|
| **npm** | 4 hrs | 5 min | 5 hrs |
| **Homebrew** | 8 hrs | 10 min | 10 hrs |
| **Scoop** | 6 hrs | 10 min | 8 hrs |
| **Binary Script** | 12 hrs | 15 min | 15 hrs |
| **Docker** | 15 hrs | 20 min | 19 hrs |
| **Git Template** | 5 hrs | 0 min | 5 hrs |
| **Multi (GoReleaser)** | 28 hrs | 20 min | 32 hrs |

*Developer time at $100/hr = $500-$3,200 first year*

---

## 2025 Trends & Predictions

### Growing in Popularity
- **mise/asdf:** Universal version managers
- **pnpm:** Monorepo-friendly npm alternative
- **Binary scripts:** Simplicity wins
- **GoReleaser:** Automation standard
- **Docker:** CI/CD ubiquitous (92% IT pros)

### Declining
- **Language-specific version managers:** (nvm, pyenv, rbenv → mise)
- **Chocolatey free tier:** Paywall driving to alternatives
- **npm for non-JS tools:** Binary scripts preferred

### Stable
- **Homebrew:** macOS standard, not going anywhere
- **apt/yum:** Linux system packages eternal
- **Docker Desktop alternatives:** Licensing drove innovation

---

## Quick Decision Tree

```
Do you have a Node.js tool?
├─ Yes → Use npm/npx
└─ No → Continue

Is it primarily project scaffolding?
├─ Yes → Use Git Template or npx create-*
└─ No → Continue

Does it have complex dependencies?
├─ Yes → Use Docker
└─ No → Continue

Do you want maximum reach?
├─ Yes → Binary Script + Homebrew + Scoop
└─ No → Continue

Is it macOS-focused?
├─ Yes → Use Homebrew (primary)
└─ No → Continue

Is it Windows-focused?
├─ Yes → Use Scoop + Winget
└─ No → Continue

Do you have time for initial setup?
├─ Yes → Use GoReleaser (multi-platform)
└─ No → Binary Script only (expand later)
```

---

## Recommended Combinations

### Minimal (MVP)
- Binary Script + GitHub Releases
- **Time:** 12 hours setup
- **Reach:** ~60% of developers

### Standard (Recommended)
- Binary Script + Homebrew + Scoop
- **Time:** 20 hours setup + GoReleaser
- **Reach:** ~90% of developers

### Comprehensive (Mature)
- All package managers + Docker + Version managers
- **Time:** 40 hours setup
- **Reach:** ~98% of developers

### Node.js Specific
- npm (primary) + Binary Script (non-Node users)
- **Time:** 8 hours
- **Reach:** 100% intended audience

### Enterprise
- Package managers (all platforms) + Docker
- **Time:** 30 hours
- **Reach:** 95% enterprise users

---

## Key Takeaways

1. **No single method is perfect** - support multiple for maximum reach
2. **Start simple** - binary script + Homebrew gets you 70% there
3. **Automate everything** - GoReleaser pays for itself after 3-4 releases
4. **Security matters** - checksums, signatures, HTTPS
5. **Documentation is critical** - users need clear instructions
6. **Version management** - consider mise/asdf plugin for power users
7. **Package managers = discoverability** - worth the effort
8. **Docker for CI/CD** - not for end users (usually)

---

## Resources

- **Full Analysis:** [distribution-methods-analysis.md](./distribution-methods-analysis.md)
- **Summary:** [distribution-methods-summary.md](./distribution-methods-summary.md)
- **GoReleaser:** https://goreleaser.com/
- **Homebrew Docs:** https://docs.brew.sh/
- **mise Docs:** https://mise.jdx.dev/

---

**For CODEX:** Recommended hybrid approach—Template for scaffolding + CLI tool for ongoing use, distributed via binary script + Homebrew + Scoop + Docker (optional).
