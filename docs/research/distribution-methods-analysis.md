# Developer Tool Distribution Methods: Comprehensive Analysis (2025)

**Research Date:** October 9, 2025
**Purpose:** Evaluate alternative distribution methods beyond npm/npx for CODEX and similar developer tools

---

## Executive Summary

This analysis examines five primary distribution strategies for developer tools in 2025:
1. **Package Managers** (Homebrew, Scoop, Winget, apt/yum)
2. **Direct Binary Downloads** (curl/wget install scripts)
3. **Docker-Based Distribution**
4. **Git-Based Templates** (degit, GitHub templates)
5. **Multi-Platform Strategies** (GoReleaser, cross-platform automation)

Each method serves different use cases, with trade-offs in installation UX, update management, platform compatibility, and maintainer complexity.

---

## 1. Package Managers

### 1.1 Homebrew (macOS/Linux)

#### Overview
Homebrew is the de facto package manager for macOS, with growing Linux adoption. Tools like `gh` (GitHub CLI), Stripe CLI, and Vercel provide Homebrew formulae for streamlined installation.

#### Installation Experience
```bash
# Install
brew install gh

# Upgrade
brew upgrade gh

# Uninstall
brew uninstall gh
```

#### Formula Structure
Homebrew formulae are Ruby files defining:
- `desc`: Short description
- `homepage`: Project website
- `url`: Download location (tarball/zip)
- `sha256`: Checksum for verification
- Build instructions and dependencies

**Example (simplified):**
```ruby
class Gh < Formula
  desc "GitHub CLI"
  homepage "https://github.com/cli/cli"
  url "https://github.com/cli/cli/archive/v2.40.0.tar.gz"
  sha256 "abc123..."

  depends_on "go" => :build

  def install
    system "make", "install", "prefix=#{prefix}"
  end
end
```

#### Distribution Approaches

**A. Main Repository (homebrew-core)**
- Highest visibility and trust
- Strict review process
- Must be stable, well-maintained projects
- No commercial restrictions

**B. Custom Tap**
- More control over releases
- Faster updates (no PR review delay)
- Example: `brew tap stripe/stripe-cli`
- Allows pre-release versions

#### Version Management
```bash
# Install specific version (complex, requires finding old formula)
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/<commit>/Formula/g/gh.rb

# Pin version (prevent upgrades)
brew pin gh

# Unpin
brew unpin gh
```

**Important Note (2025):** As of Homebrew 4.4 (August 2025), installing from local `.rb` files is deprecated. Version management has become more challenging.

#### Platform Compatibility
- **macOS:** Native, first-class support
- **Linux:** Growing adoption (Homebrew on Linux)
- **Windows:** Not supported

#### Pros
- Excellent user experience for macOS developers
- Automatic dependency management
- Single-command install/update/uninstall
- Built-in integrity verification (checksums)
- Updates managed by `brew upgrade`
- High trust factor (especially homebrew-core)
- Easy to discover via `brew search`

#### Cons
- macOS/Linux only (no Windows)
- Formula creation requires Ruby knowledge
- homebrew-core has strict acceptance criteria
- Update propagation depends on maintainers
- Version pinning/rollback is complex
- Can't control when users upgrade
- Requires building infrastructure for binary hosting

#### Maintainer Complexity: **Medium**
- Initial setup: Create formula, test on multiple macOS versions
- Ongoing: Update formula for each release
- Custom tap option reduces friction

---

### 1.2 Windows Package Managers

#### Overview
Windows has three competing package managers in 2025: **Winget** (Microsoft official), **Chocolatey** (most packages), and **Scoop** (developer-focused).

#### Comparison Table

| Feature | Winget | Chocolatey | Scoop |
|---------|--------|------------|-------|
| **Owner** | Microsoft | Chocolatey Software | Open-source community |
| **Package Count** | 8,000+ | 10,000+ | 6,000+ |
| **Pre-installed** | Yes (Win11) | No | No |
| **Cost** | Free | Free/Paid tiers | Free |
| **Install Location** | Global (Program Files) | Global | User-local (~\scoop) |
| **Admin Required** | Yes | Yes | No |
| **Auto-updates** | Manual | Yes (paid) | Manual |
| **Target Audience** | General users | Enterprise/automation | Developers |

#### Installation Examples

**Winget:**
```powershell
winget install --id GitHub.cli
winget upgrade GitHub.cli
```

**Chocolatey:**
```powershell
choco install gh
choco upgrade gh
```

**Scoop:**
```powershell
scoop bucket add main
scoop install gh
scoop update gh
```

#### Platform Compatibility
- **Windows:** All three work on Windows 10+
- **macOS/Linux:** None supported

#### Pros
- **Winget:** Pre-installed on Windows 11, official Microsoft support
- **Chocolatey:** Largest package ecosystem, best enterprise/automation features
- **Scoop:** No admin required, developer-friendly, Unix-like philosophy
- All three: Single-command installation

#### Cons
- **Winget:** Smaller package count, less mature than competitors
- **Chocolatey:** Advanced features paywalled, requires admin
- **Scoop:** Smaller community, less enterprise adoption
- All three: Windows-only, fragmented ecosystem (must support multiple)

#### Maintainer Complexity: **Medium-High**
- Must create/maintain packages for 2-3 different systems
- Each has different manifest formats
- Testing required across multiple Windows versions

#### Recommendation
For developer tools in 2025:
- **Support Winget** (official, pre-installed)
- **Consider Scoop** (developer audience, no admin required)
- **Optional Chocolatey** (if targeting enterprise/DevOps)

---

### 1.3 Linux Package Managers

#### Overview
Traditional package managers (apt, yum/dnf, pacman) plus modern universal formats (Snap, Flatpak, AppImage).

#### Traditional Package Managers

**Debian/Ubuntu (apt):**
```bash
# Add repository
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install
sudo apt update
sudo apt install gh
```

**RedHat/Fedora (dnf):**
```bash
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh
```

#### Universal Package Formats (2025 Status)

**Comparison:**

| Feature | Snap | Flatpak | AppImage |
|---------|------|---------|----------|
| **Developer** | Canonical | Red Hat/Collabora | Community |
| **Repository** | Snap Store (centralized) | Flathub (decentralized) | No central repo |
| **Installation** | System-wide daemon | System-wide daemon | No installation |
| **Sandboxing** | Yes (strong) | Yes (strong) | No (default) |
| **Auto-updates** | Yes (4x/day) | Manual/automatic | No |
| **Size** | Larger | Medium | Smaller |
| **Startup Speed** | Slower | Medium | Fast |
| **Dependencies** | Bundled | Shared runtimes | Bundled |
| **Best For** | Ubuntu users | Fedora users | Portability |

#### Universal Format Details

**Snap:**
```bash
sudo snap install gh
sudo snap refresh gh  # Update
```
- Auto-updates 4 times per day (can't disable in free version)
- Good Ubuntu integration
- Controversial in Linux community (centralized, proprietary backend)

**Flatpak:**
```bash
flatpak install flathub com.github.cli
flatpak update com.github.cli
```
- More accepted in community
- Strong Fedora/Red Hat support
- Better for GUI applications than CLI tools

**AppImage:**
```bash
wget https://github.com/cli/cli/releases/download/v2.40.0/gh-linux-amd64.AppImage
chmod +x gh-linux-amd64.AppImage
./gh-linux-amd64.AppImage
```
- No installation required
- Fully portable
- No automatic updates
- Not sandboxed by default

#### 2025 Trends
- **Native packages** remain dominant for system software and developer tools
- **Flatpak/Snap** gaining traction for GUI applications
- **AppImage** popular for portable, single-binary tools
- Power users and developers prefer native packages for CLI tools

#### Pros
- **Native packages:** Best performance, system integration
- **Snap/Flatpak:** Sandboxing, dependency isolation, cross-distro
- **AppImage:** Ultimate portability, no installation

#### Cons
- **Native packages:** Must maintain packages for multiple distros
- **Snap:** Controversial, slower startup, Ubuntu-centric
- **Flatpak:** Less suited for CLI tools, requires Flathub account
- **AppImage:** No auto-updates, no discoverability

#### Maintainer Complexity: **High**
- Native packages require per-distro maintenance
- Must handle different package formats (.deb, .rpm, .pkg.tar.zst)
- Signing keys and repository hosting
- Universal formats add more maintenance burden

#### Recommendation for Developer Tools
1. Provide native .deb and .rpm packages
2. Offer direct binary downloads (see section 2)
3. Skip Snap/Flatpak unless GUI application
4. AppImage if single-binary, portable tool

---

## 2. Direct Binary Downloads

### 2.1 Overview

Modern developer tools like Deno, Bun, Rust (rustup), and many others use shell scripts that download and install platform-specific binaries. This approach has become the gold standard for cross-platform CLI tools.

### 2.2 The "Curl Pipe Bash" Pattern

#### Standard Installation Pattern
```bash
curl -fsSL https://deno.land/install.sh | sh
curl -fsSL https://bun.sh/install | bash
curl -fsSL https://sh.rustup.rs | sh
```

**Script Responsibilities:**
1. Detect OS and architecture
2. Download appropriate binary from GitHub Releases
3. Verify checksums (security)
4. Extract and install to user directory
5. Update PATH in shell profile
6. Display post-install instructions

#### Real-World Examples

**Deno Install Script Features:**
- Single binary executable (no dependencies)
- Installs to `~/.deno/bin`
- Supports version selection: `curl -fsSL https://deno.land/install.sh | sh -s v1.38.0`
- Can verify with SHA256SUM
- Requires `unzip` or `7z` on target system

**Bun Install Script Features:**
- Single binary executable
- Installs to `~/.bun/bin`
- Version pinning: `curl -fsSL https://bun.sh/install | bash -s "bun-v1.2.23"`
- Automatically detects CPU architecture (x64, ARM64, AVX2 support)
- Smart fallback for older CPUs

### 2.3 Security Considerations

#### The Debate
The "curl | bash" pattern is controversial in security circles:

**Arguments Against:**
- Servers can detect piping and serve malicious code
- Network interruptions could cause partial execution (`rm -rf /$TMP_DIR` → `rm -rf /`)
- Running arbitrary code from the internet with shell access
- Difficult to audit what will execute

**Arguments For:**
- Same trust model as downloading and executing
- Uses same TLS channel as downloading signing keys
- Modern scripts use functions to prevent partial execution
- Transparency: users can inspect script before running
- Convenience drives adoption

#### Best Practices for Script Authors (2025)

**1. Wrap Code in Functions**
```bash
#!/bin/bash
main() {
  # Entire script here
  detect_platform
  download_binary
  verify_checksum
  install_binary
  update_path
}

# Execute only if script fully downloaded
main "$@"
```

**2. Checksum Verification**
```bash
verify_checksum() {
  local file="$1"
  local expected_sha="$2"
  local computed_sha=$(sha256sum "$file" | cut -d' ' -f1)

  if [ "$computed_sha" != "$expected_sha" ]; then
    echo "Checksum verification failed!"
    exit 1
  fi
}
```

**3. Provide Inspection Option**
```bash
# Download script for inspection
curl -fsSL https://deno.land/install.sh > install.sh
less install.sh
bash install.sh
```

**4. Sign Scripts and Provide Signatures**
```bash
# GPG signature verification
curl -fsSL https://example.com/install.sh.sig -o install.sh.sig
gpg --verify install.sh.sig install.sh
```

#### Best Practices for Users

1. **Inspect before executing:**
   ```bash
   curl -fsSL https://tool.com/install.sh | less
   ```

2. **Download first, inspect, then execute:**
   ```bash
   curl -fsSL https://tool.com/install.sh -o install.sh
   cat install.sh  # Review content
   bash install.sh
   ```

3. **Verify signatures if available**

4. **Trust the source** (GitHub, official domain)

### 2.4 Version Management

#### Approach 1: Script Parameter
```bash
curl -fsSL https://deno.land/install.sh | sh -s v1.38.0
```

#### Approach 2: Environment Variable
```bash
VERSION=v2.0.1 curl -fsSL https://tool.com/install.sh | bash
```

#### Approach 3: Version Managers
- **asdf**: Universal version manager for multiple tools
- **mise** (formerly rtx): Rust-based, faster than asdf, replaces nvm, pyenv, rbenv, etc.

**mise Example:**
```bash
# Install mise
curl https://mise.run | sh

# Install specific tool versions
mise install node@20.10.0
mise install python@3.11.0
mise install go@1.21.0

# Per-project versions
cd my-project
mise local node@18.17.0
```

**mise Advantages (2025):**
- No shims (faster than asdf, adds 0ms vs asdf's ~120ms)
- Manages environment variables (like direnv)
- Manages tasks (like make)
- Written in Rust (performance)
- Fully compatible with asdf plugins
- Single config file (`~/.config/mise/config.toml`)

### 2.5 Manual Binary Downloads

#### GitHub Releases Pattern
```bash
# Download specific version
wget https://github.com/cli/cli/releases/download/v2.40.0/gh_2.40.0_linux_amd64.tar.gz

# Extract
tar -xzf gh_2.40.0_linux_amd64.tar.gz

# Move to PATH
sudo mv gh_2.40.0_linux_amd64/bin/gh /usr/local/bin/

# Verify
gh version
```

#### Benefits
- Full control over installation location
- Air-gapped environment support
- Corporate firewall compatibility
- No script execution concerns

### 2.6 Platform Compatibility

**Cross-Platform Support:**
- Scripts can detect OS (Linux, macOS, Windows via WSL)
- Architecture detection (x86_64, ARM64, ARMv7)
- CPU feature detection (AVX2, SSE4.2)

**Windows Support:**
- PowerShell equivalent:
  ```powershell
  irm https://tool.com/install.ps1 | iex
  ```
- Or provide .exe/.msi installers

### 2.7 Pros

- **User Experience:** Single command installation
- **No Dependencies:** Doesn't require package manager
- **Cross-Platform:** Works on any Unix-like system
- **Fast Adoption:** Lowest barrier to entry
- **Version Control:** Easy to specify versions
- **Offline Installation:** Can download and archive installers
- **Update Control:** Users control when to upgrade

### 2.8 Cons

- **Security Concerns:** "Curl pipe bash" stigma
- **No Automatic Updates:** Users must manually re-run installer
- **No Discoverability:** Can't search like package managers
- **PATH Management:** Script must modify shell profiles
- **Network Required:** Initial installation needs internet
- **Trust Required:** Users trust your domain/scripts

### 2.9 Maintainer Complexity: **Low-Medium**

**Initial Setup:**
- Write install script (bash/PowerShell)
- Test on multiple platforms
- Set up GitHub Releases or CDN

**Ongoing Maintenance:**
- Upload binaries for each release
- Update script if needed (rare)
- Maintain checksums

**Automation Tools:**
- GoReleaser (see section 5)
- GitHub Actions for release automation

### 2.10 Recommendation

**Best for:**
- CLI tools with single-binary distribution
- Cross-platform developer tools
- Projects wanting fastest adoption
- Tools used in CI/CD environments

**Combine with:**
- Package managers for discoverability
- Version managers (mise/asdf) for professional users
- Manual download option for security-conscious users

---

## 3. Docker-Based Distribution

### 3.1 Overview

Docker provides an alternative distribution model where tools run inside containers rather than being installed on the host system. This is popular for:
- Tools with complex dependencies
- Development environment standardization
- CI/CD pipelines
- Cross-platform consistency

### 3.2 Distribution Patterns

#### Pattern 1: Dockerized CLI Tool

**User Experience:**
```bash
# Pull image
docker pull stripe/stripe-cli:latest

# Run command
docker run --rm -it stripe/stripe-cli version

# Common usage with volume mounts
docker run --rm -it \
  -v $(pwd):/workspace \
  -w /workspace \
  stripe/stripe-cli listen --forward-to localhost:4242
```

**Shell Alias Improvement:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias stripe='docker run --rm -it -v $(pwd):/workspace stripe/stripe-cli'

# Now use like native command
stripe version
stripe listen
```

#### Pattern 2: Docker Compose Integration

**Example: Development Environment**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    image: node:20
    volumes:
      - .:/app
    working_dir: /app
    command: npm run dev

  codex:
    image: codex/cli:latest
    volumes:
      - .:/workspace
      - ~/.codex:/root/.codex
    working_dir: /workspace
    command: codex run
```

#### Pattern 3: Docker Init/Bootstrap

Some tools use Docker for initial setup:
```bash
docker run --rm -it -v $(pwd):/init codex/init:latest create my-project
```

This creates project files in current directory, then Docker is no longer needed.

### 3.3 Real-World Examples

#### Stripe CLI
- Official Docker image: `stripe/stripe-cli`
- Used in CI/CD for testing webhooks
- Provides consistent environment across machines

#### Docker MCP Catalog (2025 Innovation)
- Docker Hub now surfaces containerized MCP servers
- Enables AI agent development with Docker containers
- Part of Docker's Beta features for agentic AI

#### DevContainers (VS Code)
- Development inside containers
- Consistent tooling across team
- Defined in `.devcontainer/devcontainer.json`

### 3.4 Version Management

```bash
# Specific version
docker run stripe/stripe-cli:v1.2.3 version

# Latest
docker run stripe/stripe-cli:latest version

# Pin in docker-compose.yml
services:
  tool:
    image: tool/cli:1.2.3  # Pinned version
```

**Update Process:**
```bash
# Pull new version
docker pull tool/cli:latest

# Or use Docker Compose
docker-compose pull
```

### 3.5 Platform Compatibility

**Excellent Cross-Platform:**
- **Windows:** Docker Desktop or WSL2
- **macOS:** Docker Desktop (ARM64 and Intel)
- **Linux:** Native Docker Engine

**Caveats:**
- Docker Desktop licensing changes (2021) drove alternatives
- Performance overhead on macOS (VM layer)
- Windows requires WSL2 or Hyper-V

### 3.6 Pros

- **Consistency:** Identical environment everywhere
- **Dependency Isolation:** No conflicts with host system
- **Security:** Sandboxed execution
- **Multi-Version:** Run multiple versions simultaneously
- **CI/CD Friendly:** Standard for pipelines
- **No Installation:** Pull and run
- **Cross-Platform:** Same image works everywhere
- **Version Pinning:** Easy to lock versions

### 3.7 Cons

- **Docker Requirement:** Users must install Docker first (large dependency)
- **Performance:** Overhead compared to native binaries
- **Complexity:** Docker concepts have learning curve
- **UX Friction:** Verbose commands, need aliases
- **File Permissions:** Volume mount permission issues (especially Linux)
- **Networking:** Port mapping can be confusing
- **Size:** Images are large compared to binaries
- **Startup Time:** Container startup adds latency
- **Resource Usage:** Docker daemon memory/CPU

### 3.8 Maintainer Complexity: **Medium-High**

**Initial Setup:**
- Create Dockerfile
- Multi-stage builds for optimization
- Set up automated builds (Docker Hub, GitHub Actions)
- Test on different architectures (amd64, arm64)

**Ongoing Maintenance:**
- Keep base image updated (security patches)
- Maintain multi-arch builds
- Optimize image size
- Handle breaking changes in base images

**Example Multi-Arch Build:**
```dockerfile
# Dockerfile
FROM --platform=$BUILDPLATFORM golang:1.21 AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM
WORKDIR /build
COPY . .
RUN go build -o app

FROM alpine:latest
COPY --from=builder /build/app /usr/local/bin/
ENTRYPOINT ["app"]
```

**Build and Push:**
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t tool/cli:latest --push .
```

### 3.9 Recommendation

**Best for:**
- Tools with complex dependencies (databases, services)
- Development environment setup
- CI/CD pipelines
- Enterprise environments with Docker expertise
- Tools needing strong isolation

**Not ideal for:**
- Simple CLI tools (overhead not justified)
- End-user developer tools (friction too high)
- Performance-critical operations
- Users without Docker knowledge

**Hybrid Approach:**
- Offer Docker as *optional* distribution method
- Primary: native binaries/package managers
- Docker: for CI/CD, complex setups, or testing

---

## 4. Git-Based Templates

### 4.1 Overview

Git-based distribution uses repository templates or scaffolding tools to bootstrap projects. Rather than installing a persistent tool, users clone/copy a template repository.

### 4.2 Approaches

#### Approach 1: GitHub Template Repositories

**Setup:**
1. Mark repository as "Template" in GitHub settings
2. Users click "Use this template" button
3. GitHub creates new repository with template contents

**Benefits:**
- Zero-to-healthy in one click
- Includes workflows, labels, branch protection
- CODEOWNERS file carries over
- Can include sample code, documentation structure

**Example Flow:**
```bash
# Via GitHub UI
Click "Use this template" → Name new repo → Create

# Via gh CLI
gh repo create my-project --template owner/template-repo
```

#### Approach 2: degit (Direct Git Cloning)

**What is degit?**
- Created by Rich Harris (Svelte creator)
- Downloads latest commit without .git history
- Much faster than `git clone`
- Supports GitHub, GitLab, Bitbucket, Sourcehut

**Usage:**
```bash
# Install degit
npm install -g degit

# Clone template (no git history)
degit user/repo my-project

# Specific branch/tag
degit user/repo#dev my-project
degit user/repo#v2.0.0 my-project

# Subdirectory
degit user/repo/subdirectory my-project

# Private repos
degit --mode=git user/private-repo my-project
```

**Advantages over `git clone`:**
- No `.git` folder with template history
- Faster (downloads tarball, not full history)
- Less typing
- Offline support (caches tarballs)

**Real-World Usage:**
- Svelte templates: `degit sveltejs/template my-app`
- Vite templates: `degit vitejs/vite-react-template`
- Next.js (uses similar approach internally)

#### Approach 3: npx/npm init

**Pattern:**
```bash
# Next.js
npx create-next-app my-app

# Vite
npm create vite@latest my-app

# Custom scaffolder
npx create-my-tool my-project
```

**How it Works:**
1. npx downloads `create-my-tool` package
2. Runs interactive CLI prompts
3. Generates project based on answers
4. Installs dependencies

**Benefits over degit:**
- Interactive configuration
- Conditional file generation
- Custom logic during setup
- Can validate inputs

#### Approach 4: Git Submodules/Subtrees

**Use Case:** Sharing configuration/tooling across multiple projects

**Git Submodules:**
```bash
# Add submodule
git submodule add https://github.com/user/shared-config.git .codex

# Clone repo with submodules
git clone --recursive https://github.com/user/my-project.git

# Update submodules
git submodule update --remote
```

**Pros:**
- Updates from source
- Versioned references

**Cons:**
- Complex for users unfamiliar with submodules
- Requires explicit update commands
- Can break if not careful

### 4.3 Comparison Matrix

| Method | Speed | Interactivity | Git History | Offline | Private Repos |
|--------|-------|---------------|-------------|---------|---------------|
| GitHub Template | Medium | No | New repo | No | Yes (with access) |
| degit | Fast | No | None | Yes (cached) | Yes (--mode=git) |
| npx create-* | Medium | Yes | None | No | N/A |
| git clone | Slow | No | Full history | No | Yes (with access) |
| Git Submodules | Medium | No | Referenced | No | Yes (with access) |

### 4.4 Version Management

**degit:**
```bash
# Pin to tag
degit user/repo#v2.0.0 my-project

# Pin to commit
degit user/repo#abc1234 my-project

# Pin to branch
degit user/repo#stable my-project
```

**npx create-*:**
```bash
# Specific version of scaffolder
npx create-next-app@13.4.0 my-app
```

**GitHub Template:**
- No built-in versioning
- Template creator can use branches/tags
- User gets latest commit at creation time

### 4.5 Platform Compatibility

**All Methods:**
- Cross-platform (Windows, macOS, Linux)
- Require git installed (except npx approach)
- npx requires Node.js/npm

### 4.6 Pros

- **No Installation:** No persistent tool to maintain
- **Fast Setup:** Project ready in seconds
- **Versioned Templates:** Can evolve templates over time
- **Customizable:** Users can modify after cloning
- **Examples Included:** Template includes working code
- **Documentation Included:** README, guides in template
- **CI/CD Ready:** Workflows included in template
- **Low Maintenance:** Template is the only thing to update

### 4.7 Cons

- **No CLI Logic:** Can't run conditional setup code (except npx)
- **No Updates:** Users don't get template updates automatically
- **Git Required:** Users must have git installed
- **No Validation:** Can't validate user inputs during setup
- **Discoverability:** Harder to find templates than packages
- **Fragmentation:** Many templates for same purpose

### 4.8 Maintainer Complexity: **Low**

**Initial Setup:**
- Create template repository
- Add example code, workflows, documentation
- Mark as template (GitHub)

**Ongoing Maintenance:**
- Update template with improvements
- Users get updates only if they manually sync
- No version management burden
- No binary compilation/distribution

### 4.9 Real-World Examples

**Major Projects Using Templates:**
- **Svelte:** `degit sveltejs/template`
- **Vite:** `npm create vite@latest`
- **Next.js:** `npx create-next-app`
- **Astro:** `npm create astro@latest`
- **Python PyScaffold:** Template generator for Python projects

### 4.10 Recommendation

**Best for:**
- Project scaffolding/initialization
- When tool is really "project template + workflows"
- Open-source starter templates
- When users need full customization

**Not ideal for:**
- Persistent CLI tools
- Tools that need updates after initial setup
- Complex interactive setup flows (use npx create-* instead)

**CODEX Consideration:**
If CODEX is primarily workflows + task files + agents, a template approach could work:
```bash
# Option 1: degit
degit beardedwonder/codex my-project

# Option 2: Interactive scaffolder
npx create-codex-project my-project
```

This would include:
- `.codex/` directory structure
- Example workflows
- Default agents and tasks
- GitHub Actions for CODEX
- Documentation

**Hybrid Approach:**
- Template for initial setup
- Optional CLI tool for ongoing management (installed separately)

---

## 5. Multi-Platform Installers & Automation

### 5.1 Overview

Modern developer tools support multiple distribution methods simultaneously. Tools like GoReleaser automate the creation of binaries, packages, and installers for all platforms from a single configuration.

### 5.2 GoReleaser

#### What is GoReleaser?

GoReleaser automates release engineering for Go, Rust, Zig, TypeScript, and Python projects. It builds binaries, creates GitHub releases, generates Homebrew taps, builds Docker images, and more—all from a single YAML configuration.

**Key Features (2025):**
- Multi-platform binary builds (Windows, macOS, Linux)
- Multi-architecture support (amd64, arm64, armv7, etc.)
- GitHub/GitLab Releases integration
- Homebrew tap generation
- Scoop manifest creation
- Snapcraft package creation
- Docker image builds (multi-arch)
- Checksum generation
- Changelog automation
- Signing (GPG, code signing)

#### Basic Configuration

**`.goreleaser.yaml`:**
```yaml
# Build configuration
builds:
  - id: codex
    binary: codex
    main: ./cmd/codex
    env:
      - CGO_ENABLED=0
    goos:
      - linux
      - windows
      - darwin
    goarch:
      - amd64
      - arm64
      - arm
    goarm:
      - 7

# Archive configuration
archives:
  - id: codex
    name_template: "{{ .ProjectName }}_{{ .Version }}_{{ .Os }}_{{ .Arch }}"
    format_overrides:
      - goos: windows
        format: zip

# Checksum generation
checksum:
  name_template: "checksums.txt"

# GitHub Release
release:
  github:
    owner: beardedwonder
    name: codex
  name_template: "v{{ .Version }}"

# Homebrew tap
brews:
  - name: codex
    repository:
      owner: beardedwonder
      name: homebrew-tap
    folder: Formula
    homepage: https://github.com/beardedwonder/codex
    description: "AI Agent Workflow System"
    license: MIT
    install: |
      bin.install "codex"

# Scoop manifest
scoop:
  bucket:
    owner: beardedwonder
    name: scoop-bucket
  homepage: https://github.com/beardedwonder/codex
  description: "AI Agent Workflow System"
  license: MIT

# Docker images
dockers:
  - image_templates:
      - "beardedwonder/codex:{{ .Version }}-amd64"
      - "beardedwonder/codex:latest-amd64"
    use: buildx
    build_flag_templates:
      - "--platform=linux/amd64"
      - "--label=org.opencontainers.image.version={{ .Version }}"
  - image_templates:
      - "beardedwonder/codex:{{ .Version }}-arm64"
      - "beardedwonder/codex:latest-arm64"
    use: buildx
    build_flag_templates:
      - "--platform=linux/arm64"
```

#### GitHub Actions Integration

**`.github/workflows/release.yml`:**
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  goreleaser:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21'

      - name: Run GoReleaser
        uses: goreleaser/goreleaser-action@v5
        with:
          version: latest
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Release Process

```bash
# 1. Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. GitHub Actions automatically:
#    - Builds binaries for all platforms
#    - Creates GitHub Release with binaries
#    - Updates Homebrew tap
#    - Updates Scoop bucket
#    - Builds and pushes Docker images
#    - Generates checksums
#    - Creates changelog
```

### 5.3 Alternatives to GoReleaser

#### cargo-dist (for Rust)

**Purpose:** Rust equivalent of GoReleaser

**Features:**
- Multi-platform binary builds
- GitHub Releases integration
- Homebrew tap generation
- npm package generation (run Rust binary via npm)
- Installer scripts (curl | sh)

**Configuration (`Cargo.toml`):**
```toml
[workspace.metadata.dist]
cargo-dist-version = "0.4.0"
installers = ["shell", "homebrew"]
targets = ["x86_64-unknown-linux-gnu", "x86_64-apple-darwin", "aarch64-apple-darwin"]
```

#### release-please (Google)

**Purpose:** Automated release creation based on conventional commits

**Features:**
- Parses conventional commits
- Generates changelogs
- Creates GitHub Releases
- Updates version files
- Language-agnostic (Go, Rust, Node.js, Python, etc.)

#### semantic-release

**Purpose:** Automated versioning and publishing (npm-focused but extensible)

**Features:**
- Conventional commit parsing
- Semantic versioning
- npm publishing
- GitHub Releases
- Plugin system

### 5.4 Cross-Platform Build Tools

#### Cross (Rust)

**Purpose:** Zero-setup cross-compilation for Rust

**Features:**
- Uses Docker containers with toolchains
- Supports many targets (Linux, Windows, macOS, ARM, MIPS, etc.)
- Integrates with CI/CD

**Usage:**
```bash
# Install
cargo install cross

# Build for different target
cross build --target x86_64-unknown-linux-gnu
cross build --target aarch64-unknown-linux-gnu
cross build --target x86_64-pc-windows-gnu
```

#### Docker Buildx

**Purpose:** Multi-architecture Docker image builds

**Usage:**
```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t tool/cli:latest --push .
```

### 5.5 Complete Distribution Strategy

#### Recommended Multi-Platform Approach

**For a tool like CODEX, support multiple distribution methods:**

1. **Primary: Direct Binary Downloads**
   - Shell installer: `curl -fsSL https://codex.dev/install.sh | sh`
   - PowerShell installer for Windows
   - Manual downloads from GitHub Releases
   - **Reason:** Lowest barrier, works everywhere

2. **Package Managers:**
   - **Homebrew** (macOS/Linux)
   - **Scoop** (Windows, developer-focused)
   - **Winget** (Windows, official)
   - **Optional:** apt/yum repositories
   - **Reason:** Discoverability, easy updates for users

3. **Version Managers:**
   - **mise/asdf plugin**
   - **Reason:** Professional developers expect this

4. **Language Package Managers (if applicable):**
   - **npm** (if Node.js based)
   - **cargo** (if Rust based)
   - **Reason:** Existing ecosystem integration

5. **Docker (optional):**
   - For CI/CD and complex setups
   - **Reason:** Enterprise adoption, isolation

6. **Template Repository (if applicable):**
   - For initial project setup
   - **Reason:** Include workflows, examples

#### Automation Setup

**Tools to Use:**
- **GoReleaser** (if Go project)
- **cargo-dist** (if Rust project)
- **GitHub Actions** for release automation
- **Homebrew tap** (custom repository)
- **Scoop bucket** (custom repository)

**Release Workflow:**
```bash
# 1. Developer creates tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. GitHub Actions triggers:
#    - GoReleaser builds for all platforms
#    - Creates GitHub Release
#    - Updates Homebrew tap
#    - Updates Scoop bucket
#    - Builds Docker images
#    - Generates install scripts with checksums

# 3. Users can install via:
brew install beardedwonder/tap/codex
scoop bucket add beardedwonder https://github.com/beardedwonder/scoop-bucket
scoop install codex
curl -fsSL https://codex.dev/install.sh | sh
docker pull beardedwonder/codex:latest
```

### 5.6 Pros of Multi-Platform Strategy

- **Maximum Reach:** Users can choose preferred method
- **Discoverability:** Package managers help users find tool
- **Professional Image:** Shows maturity and seriousness
- **Automation:** One release → all platforms updated
- **Consistency:** Same version everywhere
- **Reduced Support:** Users get what works for them

### 5.7 Cons of Multi-Platform Strategy

- **Initial Setup:** Significant configuration work
- **Testing Burden:** Must test on all platforms
- **Maintenance:** More distribution channels = more to maintain
- **Complexity:** Must understand each platform's requirements
- **Repository Hosting:** Need tap/bucket repositories

### 5.8 Maintainer Complexity: **High Initially, Low Ongoing**

**Initial Setup (1-2 weeks):**
- Configure GoReleaser or equivalent
- Create Homebrew tap repository
- Create Scoop bucket repository
- Set up GitHub Actions workflow
- Test on all platforms
- Write installation documentation

**Ongoing Maintenance (per release):**
- Tag release (git tag)
- Push tag (automation handles rest)
- Verify releases worked correctly
- Update documentation if needed

**Time per Release: ~30 minutes** (mostly verification)

### 5.9 Recommendation

**Start Small, Grow Over Time:**

**Phase 1 (MVP):**
- GitHub Releases with binaries
- Shell installer script
- Basic installation docs

**Phase 2 (Growing):**
- Homebrew tap
- GoReleaser automation
- Docker image (optional)

**Phase 3 (Mature):**
- Windows package managers (Scoop/Winget)
- Linux packages (.deb, .rpm)
- Version manager plugins (mise/asdf)

**Phase 4 (Enterprise):**
- Signed binaries
- Custom repositories
- Enterprise support docs

---

## 6. Comprehensive Comparison Matrix

### 6.1 Feature Comparison

| Feature | npm/npx | Homebrew | Scoop/Winget | Binary Script | Docker | Git Template |
|---------|---------|----------|--------------|---------------|--------|--------------|
| **Installation Speed** | Fast | Medium | Medium | Fast | Slow | Fast |
| **User Friction** | Low | Low | Low | Low | Medium | Low |
| **Cross-Platform** | Yes | macOS/Linux | Windows | Yes | Yes | Yes |
| **Auto-Updates** | Yes | Yes | Manual | Manual | Manual | N/A |
| **Offline Install** | Cached | Cached | Cached | No | No | Cached (degit) |
| **Version Pinning** | Yes | Complex | Yes | Yes | Yes | Yes |
| **Discoverability** | High | High | Medium | Low | Medium | Low |
| **Dependencies** | Node.js | None | None | None | Docker | Git |
| **Security** | npm registry | High | High | User must trust | High | High |
| **Uninstall** | Easy | Easy | Easy | Manual | N/A | N/A |

### 6.2 Use Case Recommendations

| Use Case | Recommended Method | Reasoning |
|----------|-------------------|-----------|
| **Simple CLI tool** | Binary script + Homebrew | Fast adoption, broad reach |
| **Node.js tool** | npm + Binary script | Leverage existing ecosystem |
| **Complex dependencies** | Docker | Isolation, consistency |
| **Project scaffolding** | Git template or npx create-* | One-time setup |
| **Enterprise tool** | Package managers (all platforms) | IT department approval |
| **Developer power users** | mise/asdf plugin + Homebrew | Flexibility, version control |
| **CI/CD usage** | Docker or Binary script | Automation-friendly |
| **Offline environments** | Manual binaries | Air-gapped support |
| **Windows developers** | Scoop + Binary script | Developer-friendly |
| **macOS developers** | Homebrew + Binary script | Native experience |
| **Linux system admins** | apt/yum packages | System integration |

### 6.3 Pros & Cons Summary

#### npm/npx
**Pros:** Largest package registry, excellent for Node.js projects, auto-updates, version management
**Cons:** Requires Node.js, npm security concerns, bloated node_modules

#### Homebrew
**Pros:** macOS standard, great UX, dependency management, high trust
**Cons:** macOS/Linux only, version pinning complex, formula maintenance

#### Scoop/Winget
**Pros:** Windows-native, no admin (Scoop), official (Winget)
**Cons:** Windows-only, fragmented (must support multiple), smaller ecosystems

#### Binary Downloads (curl | sh)
**Pros:** No dependencies, fast, cross-platform, version control
**Cons:** Security concerns, no auto-updates, PATH management

#### Docker
**Pros:** Isolation, consistency, multi-version, CI/CD standard
**Cons:** Docker required, performance overhead, complex for end users

#### Git Templates
**Pros:** No installation, includes examples, low maintenance
**Cons:** No updates, no CLI logic, git required

### 6.4 Maintainer Effort Comparison

| Method | Initial Effort | Ongoing Effort | Automation Potential |
|--------|---------------|----------------|---------------------|
| **npm/npx** | Low | Low | High |
| **Homebrew** | Medium | Low | High (with GoReleaser) |
| **Scoop/Winget** | Medium | Low | High (with GoReleaser) |
| **Binary Script** | Medium | Very Low | High |
| **Docker** | Medium-High | Medium | High |
| **Git Template** | Low | Very Low | N/A |
| **Multi-Platform (GoReleaser)** | High | Very Low | Very High |

---

## 7. CODEX-Specific Recommendations

### 7.1 Current State Analysis

**CODEX is:**
- AI agent workflow system
- Pre-v0.1.0 (beta development)
- Product code in `.codex/` directory
- Uses GitHub Actions workflows
- Designed for developers using Claude Code

**Questions to Answer:**
1. Is CODEX a persistent CLI tool or primarily project scaffolding?
2. Does CODEX need to be installed globally or per-project?
3. What are the runtime dependencies?
4. Who is the target audience?

### 7.2 Scenario A: CODEX as Project Template

**If CODEX is primarily:**
- Workflow files (.github/workflows/)
- Task definitions (.codex/tasks/)
- Agent configurations (.codex/agents/)
- Project structure

**Recommended Distribution:**

**Primary: Git Template + Interactive Scaffolder**

```bash
# Option 1: GitHub Template
gh repo create my-project --template beardedwonder/codex

# Option 2: degit
degit beardedwonder/codex my-project

# Option 3: Interactive scaffolder (best UX)
npx create-codex-project my-project
```

**Interactive Scaffolder Features:**
```bash
npx create-codex-project my-project

? Project name: my-project
? Description: My awesome project
? Include example workflows? Yes
? Include example agents? Yes
? Include test harness? Yes
? GitHub repository: beardedwonder/my-project

Creating CODEX project...
✓ Created .codex/ directory structure
✓ Added GitHub Actions workflows
✓ Configured example agents
✓ Added development documentation
✓ Initialized git repository

Next steps:
  cd my-project
  git add .
  git commit -m "Initial commit with CODEX"
  git push -u origin main

Run workflows with:
  ./.codex/workflows/analyze.sh
  ./.codex/workflows/test.sh
```

**Advantages:**
- Lowest friction for project initialization
- Includes all workflows, examples, documentation
- Users get full control (can modify everything)
- No persistent tool to install/update
- Works anywhere git/Node.js is available

**Implementation:**
1. Create `create-codex-project` npm package
2. Interactive prompts (using `inquirer` or similar)
3. Clone template, customize based on answers
4. Initialize git, optionally push to GitHub
5. Display next steps

**Ongoing Updates:**
Users don't get automatic updates (template model), but can:
- Check for template updates manually
- Re-run scaffolder to see new features
- Implement a `.codex/update.sh` script that pulls template changes

---

### 7.3 Scenario B: CODEX as CLI Tool

**If CODEX has:**
- Commands to run workflows
- Task management CLI
- Agent orchestration commands
- State management

**Recommended Distribution: Multi-Platform Strategy**

**Phase 1: Core Distribution**
1. **Binary Downloads + Shell Installer**
   ```bash
   curl -fsSL https://codex.dev/install.sh | sh
   ```
   - Primary installation method
   - Cross-platform (Linux, macOS, Windows via WSL)
   - No dependencies

2. **Homebrew (macOS/Linux)**
   ```bash
   brew install beardedwonder/tap/codex
   ```
   - Best macOS experience
   - Automatic updates with `brew upgrade`

3. **Scoop (Windows)**
   ```bash
   scoop bucket add beardedwonder https://github.com/beardedwonder/scoop-bucket
   scoop install codex
   ```
   - Developer-friendly Windows install
   - No admin required

**Phase 2: Additional Channels**
4. **npm (if Node.js-based)**
   ```bash
   npm install -g @beardedwonder/codex
   ```
   - Leverage npm ecosystem
   - Easy for JavaScript developers

5. **mise/asdf Plugin**
   ```bash
   mise install codex@latest
   mise use codex@0.1.0
   ```
   - Version management for power users
   - Per-project versions

6. **Docker (optional, for CI/CD)**
   ```bash
   docker run --rm -it -v $(pwd):/workspace beardedwonder/codex
   ```
   - Consistent CI/CD environments

**Automation:**
Use **GoReleaser** to automate all releases:

**`.goreleaser.yaml`:**
```yaml
project_name: codex

before:
  hooks:
    - go mod tidy

builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - windows
      - darwin
    goarch:
      - amd64
      - arm64

archives:
  - format: tar.gz
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: 'checksums.txt'

release:
  github:
    owner: beardedwonder
    name: codex

brews:
  - name: codex
    repository:
      owner: beardedwonder
      name: homebrew-tap
    homepage: https://github.com/beardedwonder/codex
    description: "AI Agent Workflow System"
    install: |
      bin.install "codex"

scoop:
  bucket:
    owner: beardedwonder
    name: scoop-bucket
  homepage: https://github.com/beardedwonder/codex
  description: "AI Agent Workflow System"
```

**Release Process:**
```bash
# Tag and push
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# GoReleaser (via GitHub Actions) automatically:
# - Builds for all platforms
# - Updates Homebrew tap
# - Updates Scoop bucket
# - Creates GitHub Release
# - Generates checksums
```

---

### 7.4 Scenario C: Hybrid Approach (Recommended)

**Best of Both Worlds:**

**CODEX = Template + CLI Tool**

**Template for:**
- Initial project setup
- Workflow files
- Example tasks and agents
- Documentation structure

**CLI Tool for:**
- Running workflows
- Managing state
- Orchestrating agents
- Updating CODEX itself

**User Flow:**

```bash
# 1. Initialize project with template
npx create-codex-project my-project
cd my-project

# 2. Install CODEX CLI (if not already installed)
curl -fsSL https://codex.dev/install.sh | sh
# or
brew install beardedwonder/tap/codex

# 3. Use CLI to run workflows
codex run analyze
codex task create "Implement feature"
codex status

# 4. CLI can update template files
codex update
```

**Benefits:**
- Clean separation of concerns
- Template provides project structure
- CLI provides persistent tooling
- Users can use template without CLI (and vice versa)
- Best UX for both use cases

**Implementation Strategy:**

**1. Template Repository:**
- `beardedwonder/codex-template`
- Contains `.codex/` structure
- GitHub Actions workflows
- Documentation

**2. CLI Tool:**
- `beardedwonder/codex`
- Go/Rust binary
- Commands: `run`, `task`, `status`, `update`, etc.
- Distributed via Homebrew, Scoop, binary script

**3. Scaffolder (optional):**
- `create-codex-project` npm package
- Interactive project setup
- Clones template, customizes, installs CLI

**Documentation:**
```markdown
# Quick Start

## Initialize New Project
npx create-codex-project my-project
cd my-project

## Install CODEX CLI
brew install beardedwonder/tap/codex

## Run Workflows
codex run analyze
codex task create "My first task"

## Update CODEX
codex update  # Updates CLI
codex sync    # Syncs template files
```

---

### 7.5 Implementation Roadmap

**Phase 1: MVP (1-2 weeks)**
- [ ] Decide on architecture (Template vs CLI vs Hybrid)
- [ ] Create template repository
- [ ] Write install script (if CLI tool)
- [ ] GitHub Releases with binaries
- [ ] Basic installation documentation

**Phase 2: Polish (2-3 weeks)**
- [ ] Interactive scaffolder (`create-codex-project`)
- [ ] Homebrew tap
- [ ] GoReleaser automation
- [ ] GitHub Actions release workflow
- [ ] Comprehensive docs

**Phase 3: Growth (ongoing)**
- [ ] Scoop/Winget support (Windows)
- [ ] Docker image (optional)
- [ ] mise/asdf plugin
- [ ] Linux packages (.deb, .rpm)
- [ ] npm package (if applicable)

---

## 8. Security Best Practices

### 8.1 Binary Distribution Security

**Checksum Verification:**
```bash
# Generate checksums
sha256sum codex-* > checksums.txt

# Verify before installation
sha256sum -c checksums.txt
```

**GPG Signing:**
```bash
# Sign release
gpg --detach-sign --armor checksums.txt

# Verify signature
gpg --verify checksums.txt.asc checksums.txt
```

**Code Signing (macOS/Windows):**
- macOS: Sign with Apple Developer certificate
- Windows: Sign with code signing certificate
- Prevents "unknown developer" warnings

### 8.2 Install Script Security

**For Script Authors:**
1. **Use functions** to prevent partial execution
2. **Verify checksums** before extracting
3. **Provide inspection option** (download first)
4. **Use HTTPS** for all downloads
5. **Validate inputs** before executing
6. **Fail fast** on errors (set -e)
7. **Don't require sudo** unless absolutely necessary
8. **Minimal dependencies** (bash, curl/wget, tar)

**Example Secure Install Script:**
```bash
#!/bin/bash
set -euo pipefail

REPO="beardedwonder/codex"
VERSION="${VERSION:-latest}"

main() {
  echo "Installing CODEX ${VERSION}..."

  detect_platform
  download_binary
  verify_checksum
  install_binary
  update_path

  echo "CODEX installed successfully!"
  echo "Run 'codex --version' to verify."
}

detect_platform() {
  OS="$(uname -s)"
  ARCH="$(uname -m)"

  case "$OS" in
    Linux)  OS="linux" ;;
    Darwin) OS="darwin" ;;
    *)      echo "Unsupported OS: $OS" && exit 1 ;;
  esac

  case "$ARCH" in
    x86_64)  ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    arm64)   ARCH="arm64" ;;
    *)       echo "Unsupported architecture: $ARCH" && exit 1 ;;
  esac

  FILENAME="codex_${VERSION}_${OS}_${ARCH}.tar.gz"
}

download_binary() {
  DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${VERSION}/${FILENAME}"
  echo "Downloading from ${DOWNLOAD_URL}..."

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$DOWNLOAD_URL" -o "$FILENAME"
  elif command -v wget >/dev/null 2>&1; then
    wget -q "$DOWNLOAD_URL" -O "$FILENAME"
  else
    echo "Error: curl or wget required" && exit 1
  fi
}

verify_checksum() {
  echo "Verifying checksum..."

  CHECKSUM_URL="https://github.com/${REPO}/releases/download/${VERSION}/checksums.txt"
  curl -fsSL "$CHECKSUM_URL" -o checksums.txt

  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c --ignore-missing checksums.txt
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 -c --ignore-missing checksums.txt
  else
    echo "Warning: Cannot verify checksum (sha256sum not found)"
  fi
}

install_binary() {
  echo "Extracting..."
  tar -xzf "$FILENAME"

  INSTALL_DIR="${HOME}/.local/bin"
  mkdir -p "$INSTALL_DIR"
  mv codex "$INSTALL_DIR/"
  chmod +x "${INSTALL_DIR}/codex"

  rm -f "$FILENAME" checksums.txt
}

update_path() {
  INSTALL_DIR="${HOME}/.local/bin"

  if [[ ":$PATH:" != *":${INSTALL_DIR}:"* ]]; then
    echo ""
    echo "Add to your shell profile:"
    echo "  export PATH=\"${INSTALL_DIR}:\$PATH\""

    # Detect shell and provide specific instructions
    case "$SHELL" in
      */zsh)  echo "  echo 'export PATH=\"${INSTALL_DIR}:\$PATH\"' >> ~/.zshrc" ;;
      */bash) echo "  echo 'export PATH=\"${INSTALL_DIR}:\$PATH\"' >> ~/.bashrc" ;;
      *)      echo "  (Add to your shell's config file)" ;;
    esac
  fi
}

main "$@"
```

### 8.3 Package Manager Security

**Homebrew:**
- Formulae are reviewed by maintainers
- Checksums verified automatically
- HTTPS downloads only

**npm:**
- Use `npm audit` to check dependencies
- Enable 2FA for npm account
- Review package before publishing
- Use `--ignore-scripts` for installs if concerned

**Docker:**
- Use official base images
- Scan images with `docker scan`
- Pin base image versions
- Multi-stage builds (minimize attack surface)

---

## 9. Version Management Strategies

### 9.1 Semantic Versioning

Follow **semver** (MAJOR.MINOR.PATCH):
- **MAJOR:** Breaking changes (v1.0.0 → v2.0.0)
- **MINOR:** New features, backward compatible (v1.0.0 → v1.1.0)
- **PATCH:** Bug fixes (v1.0.0 → v1.0.1)

**Pre-releases:**
- v0.1.0-alpha.1
- v0.1.0-beta.2
- v0.1.0-rc.1

### 9.2 Version Update Mechanisms

**Automatic Updates:**
- Package managers handle this (brew upgrade, apt update)
- Docker: Pull new tags
- npm: `npm update -g`

**Manual Updates:**
- Binary script: Re-run installer
- User checks GitHub Releases
- CLI tool can have `codex update` command

**Self-Update Command:**
```go
// Example self-update implementation
func (c *CLI) Update() error {
    latest, err := getLatestVersion()
    if err != nil {
        return err
    }

    if latest.Equal(currentVersion) {
        fmt.Println("Already up to date!")
        return nil
    }

    fmt.Printf("Updating from %s to %s...\n", currentVersion, latest)
    return downloadAndReplace(latest)
}
```

### 9.3 Version Pinning

**Homebrew:**
```bash
brew pin codex    # Prevent upgrades
brew unpin codex
```

**npm:**
```json
{
  "dependencies": {
    "codex": "0.1.0"  // Exact version
  }
}
```

**mise/asdf:**
```bash
# Per-project version
mise local codex@0.1.0

# Global version
mise global codex@0.1.5
```

**Docker:**
```yaml
# docker-compose.yml
services:
  tool:
    image: codex:0.1.0  # Pin specific version
```

---

## 10. Documentation Requirements

### 10.1 Installation Documentation

**Must Include:**
1. **Multiple installation methods** with examples
2. **Platform-specific instructions** (macOS, Linux, Windows)
3. **Prerequisites** (if any)
4. **Verification steps** (how to confirm installation worked)
5. **Troubleshooting** common issues
6. **Update instructions**
7. **Uninstall instructions**

**Example:**
```markdown
# Installation

## macOS / Linux

### Homebrew (Recommended)
brew install beardedwonder/tap/codex

### Install Script
curl -fsSL https://codex.dev/install.sh | sh

### Manual Download
1. Download from [Releases](https://github.com/beardedwonder/codex/releases)
2. Extract: `tar -xzf codex_*.tar.gz`
3. Move to PATH: `mv codex /usr/local/bin/`

## Windows

### Scoop
scoop bucket add beardedwonder https://github.com/beardedwonder/scoop-bucket
scoop install codex

### PowerShell
irm https://codex.dev/install.ps1 | iex

## Verification
codex --version

## Update
brew upgrade codex             # Homebrew
scoop update codex             # Scoop
curl -fsSL https://codex.dev/install.sh | sh  # Re-run installer

## Uninstall
brew uninstall codex           # Homebrew
scoop uninstall codex          # Scoop
rm ~/.local/bin/codex          # Manual
```

---

## 11. Conclusion & Final Recommendations

### 11.1 Best Practices Summary

1. **Support Multiple Channels:**
   - Start with binary downloads (lowest friction)
   - Add package managers for discoverability
   - Consider version managers for power users

2. **Automate Everything:**
   - Use GoReleaser or equivalent
   - GitHub Actions for releases
   - One tag → all platforms updated

3. **Security First:**
   - Checksums for all binaries
   - GPG signatures for sensitive tools
   - Secure install scripts (functions, validation)

4. **Documentation Matters:**
   - Clear installation instructions
   - Multiple methods with examples
   - Troubleshooting section

5. **Version Management:**
   - Follow semver strictly
   - Provide update mechanism
   - Support version pinning

### 11.2 For CODEX Specifically

**Recommended Hybrid Approach:**

**1. Template for Project Structure**
```bash
npx create-codex-project my-project
```
- Quick project initialization
- Includes workflows, agents, docs
- Low maintenance for you

**2. CLI Tool for Ongoing Use**
```bash
# Install
brew install beardedwonder/tap/codex
# or
curl -fsSL https://codex.dev/install.sh | sh

# Use
codex run workflow-name
codex task create "Task name"
codex update
```
- Distributed via Homebrew, Scoop, binary script
- Automated with GoReleaser
- Self-update capability

**3. Docker for CI/CD (Optional)**
```yaml
# .github/workflows/test.yml
- uses: docker://beardedwonder/codex:latest
  with:
    args: run test
```
- Consistent CI environments
- Optional, not primary distribution

### 11.3 Implementation Priority

**High Priority:**
1. Template repository or interactive scaffolder
2. Binary downloads + shell installer
3. Homebrew tap
4. Documentation

**Medium Priority:**
5. GoReleaser automation
6. Scoop bucket (Windows)
7. Docker image

**Low Priority (Future):**
8. mise/asdf plugin
9. Linux packages (.deb, .rpm)
10. Winget support

### 11.4 Key Takeaways

| Distribution Method | Best For | Avoid If |
|---------------------|----------|----------|
| **npm/npx** | Node.js tools, scaffolders | Non-JS projects |
| **Homebrew** | macOS/Linux CLI tools | Windows-only tools |
| **Scoop/Winget** | Windows developer tools | macOS/Linux-only |
| **Binary Script** | Cross-platform CLIs | Complex dependencies |
| **Docker** | Complex setups, CI/CD | Simple CLIs, end-users |
| **Git Template** | Project scaffolding | Persistent tools |
| **GoReleaser** | Multi-platform automation | Non-compiled languages |

### 11.5 Resources

**Official Documentation:**
- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [GoReleaser Documentation](https://goreleaser.com/)
- [Scoop Documentation](https://scoop.sh/)
- [Docker Documentation](https://docs.docker.com/)
- [mise Documentation](https://mise.jdx.dev/)

**Example Projects:**
- [GitHub CLI (gh)](https://github.com/cli/cli) - Multi-platform distribution
- [Deno](https://github.com/denoland/deno) - Shell installer + package managers
- [Stripe CLI](https://github.com/stripe/stripe-cli) - Homebrew + Scoop + Docker

---

**End of Analysis**

This comprehensive research provides everything needed to make informed decisions about distributing CODEX or any developer tool in 2025. The hybrid approach (template + CLI) is recommended for maximum flexibility and user satisfaction.
