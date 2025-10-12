# CODEX Migration Guide

> **Version migrations guide for CODEX users**
> Last Updated: 2025-10-09
> CODEX Version: Pre-v0.1.0

## Table of Contents

1. [When Do You Need to Migrate?](#when-do-you-need-to-migrate)
2. [Understanding Schema Versions](#understanding-schema-versions)
3. [General Migration Process](#general-migration-process)
4. [Version-Specific Migrations](#version-specific-migrations)
5. [Troubleshooting](#troubleshooting)
6. [Schema Version Reference](#schema-version-reference)

---

## When Do You Need to Migrate?

### Automatic vs Manual Migration

CODEX updates fall into two categories:

**🟢 Automatic Updates (Same Schema Version)**
- Patch updates: `0.1.0` → `0.1.1`
- Minor updates within same major version (usually): `0.1.0` → `0.2.0`
- Bug fixes and feature additions that don't change core structure
- **Action Required**: None - just update normally

**🟡 Manual Migration (Schema Version Change)**
- Major breaking changes to workflow structure
- Changes to state file formats
- Template format modifications
- Agent behavior changes that affect saved state
- **Action Required**: Follow this migration guide

### How to Check Schema Version

Check your current installation's schema version:

```bash
# View your install manifest
cat .codex/install-manifest.yaml
```

Look for the `schema_version` field:

```yaml
codex_version: "0.1.0"
schema_version: 1        # ← Your current schema version
installed_at: "2024-10-09T12:30:00Z"
```

When updating, CODEX will warn you if the schema version is changing.

---

## Understanding Schema Versions

### What is a Schema Version?

The **schema version** defines the structure of:
- Workflow state files (`workflow.json`)
- Configuration formats (`codex-config.yaml`)
- Template variables and formats
- Agent communication protocols
- Quality gate checklists

### Schema Version vs CODEX Version

| Version Type | Example | Changes When... |
|--------------|---------|-----------------|
| **CODEX Version** | `0.1.0` → `0.1.5` | Bug fixes, new features, improvements |
| **Schema Version** | `1` → `2` | Breaking changes to file formats or workflows |

**Important**: Multiple CODEX versions can share the same schema version:
- CODEX `0.1.0`, `0.1.1`, `0.1.2` → All use schema `1`
- CODEX `0.2.0`, `0.2.1` → All use schema `2`

### Breaking vs Non-Breaking Changes

**Non-Breaking (Same Schema):**
- New agents added
- New workflows added
- Bug fixes in existing workflows
- Documentation improvements
- New quality gates added (optional)

**Breaking (New Schema):**
- `workflow.json` structure changes
- Template variable format changes
- Required field additions to config files
- Agent handoff protocol changes
- Quality gate requirement changes

---

## General Migration Process

### Before You Begin

⚠️ **Critical Safety Checks**:

1. **Complete active workflows**
   ```bash
   # Check for active workflows
   /codex status

   # If workflow is active, complete it or cancel
   ```

2. **Review the changelog**
   ```bash
   # Read what changed
   cat CHANGELOG.md
   ```

3. **Backup your project** (manual backup)
   ```bash
   # Create manual backup (in addition to automatic backup)
   cd /path/to/your/project
   tar -czf ../my-project-backup-$(date +%Y%m%d).tar.gz .
   ```

### Step-by-Step Migration

#### Step 1: Complete Active Workflows

**Before updating**, ensure no workflows are in progress:

```bash
/codex status
```

**If workflow is active:**

```
Active workflow detected:
  Type: greenfield-swift
  Phase: architect (Phase 3 of 6)
  Project: MyApp
```

**Your options:**
1. **Complete the workflow** - Finish all phases
2. **Checkpoint and pause** - Save your progress:
   ```bash
   # State is automatically saved
   # Just don't proceed with update until complete
   ```

**DO NOT update with an active workflow!** You may lose progress or corrupt state.

#### Step 2: Update CODEX

```bash
# From your project directory
npx create-codex-project update
```

CODEX will automatically:
- Detect your current version and schema
- Check for schema compatibility
- Warn you if migration is needed
- Create automatic backup (in `.codex-backups/`)

#### Step 3: Review Migration Warning

If schema version changes, you'll see:

```
⚠️  SCHEMA VERSION CHANGE DETECTED
═══════════════════════════════════
Current:  CODEX 0.1.0 (schema v1)
Target:   CODEX 0.2.0 (schema v2)

This update includes breaking changes that may be
incompatible with your existing workflow state!

Automatic update is BLOCKED for safety.

Please review the migration guide:
https://github.com/YourRepo/CODEX/blob/main/MIGRATION.md#v01x--v020

To proceed after reviewing:
  npx create-codex-project update --force-schema
```

#### Step 4: Follow Version-Specific Migration

📖 **Go to** [Version-Specific Migrations](#version-specific-migrations) below and find your migration path.

#### Step 5: Force Schema Update (After Manual Steps)

Once you've completed version-specific migration steps:

```bash
# Force the schema update (dangerous - only after migration!)
npx create-codex-project update --force-schema
```

You'll be prompted to type `yes` to confirm:

```
⚠️  DANGEROUS SCHEMA UPGRADE DETECTED
═══════════════════════════════════
This operation cannot be undone!

Potential risks:
  • Loss of workflow state and progress
  • Incompatible template formats
  • Breaking changes to agent behavior
  • Data corruption or migration issues

A backup will be created automatically.

Type 'yes' to proceed: █
```

#### Step 6: Verify Installation

After update completes:

```bash
# Check version
cat .codex/install-manifest.yaml | grep version

# Verify files
npx create-codex-project verify

# Test basic workflow
/codex start health-check
```

---

## Version-Specific Migrations

### Migration Template

Each version migration will follow this structure:

```markdown
## v0.X.x → v0.Y.0 (Schema X → Schema Y)

**Breaking Changes**: List of what changed
**Migration Time**: Estimated time
**Risk Level**: Low/Medium/High

### Prerequisites
- Steps to complete before migration

### Manual Steps
1. Step-by-step instructions
2. With code examples
3. And verification commands

### After Update
- Verification steps
- What to check
- How to test
```

---

### v0.1.x → v0.2.0 (Schema 1 → Schema 2)

> **Status**: Template for future migration (v0.2.0 not yet released)

**This is a template for how future migrations will be documented.**

**Breaking Changes**:
- Hypothetical: `workflow.json` adds `epic_tracking` field
- Hypothetical: Quality gates now enforce minimum scores
- Hypothetical: Template variables change from `{{var:name}}` to `${name}`

**Migration Time**: ~15-30 minutes
**Risk Level**: Medium

#### Prerequisites

1. **Complete all active workflows**
   ```bash
   /codex status
   # Should show: No active workflow
   ```

2. **Back up your project**
   ```bash
   cd /path/to/your/project
   tar -czf ../backup-before-v0.2.0-$(date +%Y%m%d).tar.gz .
   ```

3. **Review your customizations**
   ```bash
   # Check if you modified config
   cat .codex/config/codex-config.yaml

   # List any custom workflows you created
   ls .codex/workflows/custom/
   ```

#### Manual Steps

**Step 1: Migrate State Files (if you have saved workflows)**

If you have saved workflow state in `.codex/state/runtime/workflow.json`:

```bash
# Before update: View your current state
cat .codex/state/runtime/workflow.json
```

**Example old format (v0.1.x - Schema 1):**
```json
{
  "workflow_type": "greenfield-swift",
  "current_phase": "architect",
  "project_name": "MyApp",
  "mode": "interactive"
}
```

**After update**, you'll need to add new fields manually:

**Example new format (v0.2.0 - Schema 2):**
```json
{
  "workflow_type": "greenfield-swift",
  "current_phase": "architect",
  "project_name": "MyApp",
  "mode": "interactive",
  "epic_tracking": {              // ← NEW FIELD
    "current_epic": 1,
    "total_epics": 3,
    "epic_name": "Authentication"
  }
}
```

**Manual fix:**
```bash
# Edit your workflow.json to add epic_tracking
vim .codex/state/runtime/workflow.json

# Add this section (if you don't have epics, use defaults):
# "epic_tracking": {
#   "current_epic": 1,
#   "total_epics": 1,
#   "epic_name": "MVP"
# }
```

**Step 2: Update Custom Templates (if you created any)**

If you created custom templates with variable syntax:

```bash
# Find templates with old variable format
grep -r "{{var:" .codex/templates/custom/
```

**Before (v0.1.x):**
```yaml
title: "{{var:project_name}} Requirements"
author: "{{var:author_name}}"
```

**After (v0.2.0):**
```yaml
title: "${project_name} Requirements"
author: "${author_name}"
```

**Update script:**
```bash
# Automated replacement for custom templates
cd .codex/templates/custom/
find . -name "*.yaml" -o -name "*.md" | while read file; do
  sed -i.bak 's/{{var:\([^}]*\)}}/\${\1}/g' "$file"
done

# Review changes
diff project-template.yaml.bak project-template.yaml

# Remove backups if satisfied
rm *.bak
```

**Step 3: Update Configuration**

If you customized `codex-config.yaml`:

```bash
# Backup your config
cp .codex/config/codex-config.yaml .codex/config/codex-config.yaml.v0.1.backup

# The update will install new config - you'll merge manually after
```

#### Perform Update

```bash
# Now run the forced update
npx create-codex-project update --force-schema
```

When prompted:
1. Type `yes` to confirm dangerous operation
2. Choose merge strategy for config:
   - `manual` (recommended) - Keep both files for review
   - `keep` - Use your old config
   - `replace` - Use new config (lose customizations)

#### After Update

**Verify installation:**

```bash
# Check schema version updated
cat .codex/install-manifest.yaml | grep schema_version
# Should show: schema_version: 2

# Verify CODEX version
cat .codex/install-manifest.yaml | grep codex_version
# Should show: codex_version: "0.2.0"
```

**Test workflow:**

```bash
# Start health check to verify everything works
/codex start health-check

# Should complete without errors
```

**Merge configuration (if you chose 'manual'):**

```bash
# Compare configs
diff .codex/config/codex-config.yaml.backup-* .codex/config/codex-config.yaml

# Manually merge your customizations into new config
vim .codex/config/codex-config.yaml
```

**Check quality gates:**

New version enforces minimum quality scores. Test on a real workflow:

```bash
# Try starting a real workflow
/codex start greenfield-swift "TestApp"

# Quality gates should show new enforcement
# Expected: Score requirements displayed at phase transitions
```

---

### Future Migrations

Additional migration guides will be added here as new schema versions are released:

- `v0.2.x → v0.3.0` (Schema 2 → Schema 3) - *TBD*
- `v0.3.x → v1.0.0` (Schema 3 → Schema 4) - *TBD*

**Sign up for notifications**: Watch the [CODEX repository](https://github.com/YourRepo/CODEX) to be notified of new releases.

---

## Troubleshooting

### Migration Failed - How to Restore

If the update fails or something goes wrong:

#### Option 1: Automatic Rollback

CODEX automatically attempts rollback on failure. Check console output:

```
✓ Backup created: .codex-backups/codex-backup-20241009-123045
✗ Update failed: File copy error
⟳ Attempting to rollback from backup...
✓ Successfully rolled back to version 0.1.0
```

Verify rollback:
```bash
cat .codex/install-manifest.yaml | grep codex_version
# Should show your old version
```

#### Option 2: Manual Restore from Backup

If automatic rollback failed:

```bash
# List available backups
ls -lh .codex-backups/

# Example output:
# codex-backup-20241009-123045/  (before failed update)

# Restore manually
rm -rf .codex
cp -r .codex-backups/codex-backup-20241009-123045 .codex

# Verify restoration
cat .codex/install-manifest.yaml | grep codex_version
```

#### Option 3: Restore from Manual Backup

If you created manual backup:

```bash
# Extract your backup
cd /path/to/your/project
rm -rf .codex  # Remove corrupted installation
tar -xzf ../my-project-backup-20241009.tar.gz .codex

# Verify
/codex status
```

### Common Migration Issues

#### Issue: "Active workflow detected"

**Error:**
```
✗ Cannot update: Active workflow in progress
  Workflow: greenfield-swift
  Phase: architect (Phase 3 of 6)

Please complete or cancel the workflow before updating.
```

**Solution:**
```bash
# Option 1: Complete the workflow
/codex continue
# ... complete all phases ...

# Option 2: Cancel and lose progress
rm .codex/state/runtime/workflow.json

# Then retry update
npx create-codex-project update
```

#### Issue: "Schema mismatch" without `--force-schema`

**Error:**
```
✗ Incompatible schema version detected
  Current: schema v1
  Target:  schema v2

Migration required. See: MIGRATION.md
```

**Solution:**
1. **DO NOT immediately use `--force-schema`**
2. Read this migration guide first
3. Follow version-specific migration steps
4. Only then use `--force-schema`

#### Issue: Modified files detected

**Warning:**
```
⚠ Modified files detected:
  .codex/config/codex-config.yaml
  .codex/workflows/custom/my-workflow.yaml

These files will be backed up but may be overwritten.
```

**Solution:**
```bash
# Backup your customizations manually
cp .codex/config/codex-config.yaml ~/codex-config-custom.yaml
cp -r .codex/workflows/custom ~/codex-workflows-custom/

# Proceed with update
npx create-codex-project update

# After update, merge your changes back
```

#### Issue: Backup creation failed

**Error:**
```
✗ Backup failed: ENOSPC (no space left on device)
```

**Solution:**
```bash
# Option 1: Free up disk space
df -h  # Check disk usage
# ... delete unnecessary files ...

# Option 2: Update without backup (NOT RECOMMENDED)
npx create-codex-project update --no-backup

# Option 3: Create backup elsewhere
tar -czf /external-drive/codex-backup.tar.gz .codex
npx create-codex-project update --no-backup
```

#### Issue: Update completed but workflow fails

**Symptoms:**
```bash
/codex start greenfield-swift "MyApp"
# Error: Unknown agent: codex-business-analyst
```

**Solution:**
```bash
# Verify installation integrity
npx create-codex-project verify

# If verification fails, check manifest
cat .codex/install-manifest.yaml

# Reinstall if necessary
rm -rf .codex
npx create-codex-project update --force-schema
```

#### Issue: Configuration merge conflict

**After update:**
```
⚠ Configuration Merge Required
──────────────────────────────
Old config: .codex/config/codex-config.yaml.backup-20241009
New config: .codex/config/codex-config.yaml

Manual merge recommended.
```

**Solution:**
```bash
# Compare files side by side
diff .codex/config/codex-config.yaml.backup-* .codex/config/codex-config.yaml

# Or use a merge tool
code --diff .codex/config/codex-config.yaml.backup-* .codex/config/codex-config.yaml

# Manually copy your customizations to new config
# Keep new structure, add your custom values
```

### Need Help?

If you encounter issues not covered here:

1. **Check the backup** - Your data is preserved in `.codex-backups/`
2. **Review error logs** - Update process shows detailed errors
3. **Search existing issues** - [GitHub Issues](https://github.com/YourRepo/CODEX/issues)
4. **Open a new issue** - Include:
   - Current CODEX version
   - Target CODEX version
   - Schema versions (current and target)
   - Full error output
   - Output of `npx create-codex-project verify`

**GitHub Issue Template:**
```markdown
**Migration Issue**

- Current version: 0.1.0 (schema 1)
- Target version: 0.2.0 (schema 2)
- Platform: macOS / Linux / Windows
- Install method: npm / npx

**Error:**
```
[paste full error output]
```

**Steps to reproduce:**
1. ...
2. ...

**Additional context:**
- [ ] Active workflow was present
- [ ] Modified configuration
- [ ] Custom templates exist
```

---

## Schema Version Reference

### Schema v1 - Initial Release

**CODEX Versions**: `0.1.0` and later (until schema v2)
**Release Date**: TBD (Pre-v0.1.0 currently)
**Status**: Current

**Structure:**

```yaml
# .codex/install-manifest.yaml
codex_version: "0.1.0"
schema_version: 1
```

**Features:**
- Basic workflow state tracking (`workflow.json`)
- 5-level progressive validation
- Elicitation enforcement system
- Interactive/Batch/YOLO modes
- Quality gates with checklists
- State persistence in `.codex/state/`

**File Formats:**

**`workflow.json` (Schema v1):**
```json
{
  "workflow_type": "greenfield-swift | greenfield-generic | brownfield-enhancement",
  "project_name": "string",
  "current_phase": "string",
  "current_agent": "string",
  "mode": "interactive | batch | yolo",
  "phases_completed": ["phase1", "phase2"],
  "validation_status": {
    "level_0": "passed | failed | pending",
    "level_1": "passed | failed | pending",
    "level_2": "passed | failed | pending",
    "level_3": "passed | failed | pending",
    "level_4": "passed | failed | pending"
  },
  "elicitation_history": [
    {
      "agent": "analyst",
      "section": "problem_statement",
      "method_used": "critique",
      "timestamp": "ISO-8601"
    }
  ],
  "documents_created": [
    "docs/project-brief.md",
    "docs/prd.md"
  ]
}
```

**`codex-config.yaml` (Schema v1):**
```yaml
version: "1.0"
workflows:
  default: "greenfield-generic"
  available:
    - greenfield-swift
    - greenfield-generic
    - brownfield-enhancement
    - health-check

validation:
  enforcement_mode: "strict"  # strict | conditional | advisory
  required_levels: [0, 1]

quality_gates:
  enabled: true
  minimum_scores:
    discovery: 80
    analyst: 85
    pm: 85
    architect: 85
    prp: 90

elicitation:
  default_mode: "interactive"
  menu_format: "1-9"

state:
  directory: ".codex/state"
  checkpoint_frequency: "phase"
  backup_enabled: true
  max_backups: 5
```

**Template Variable Format (Schema v1):**
```yaml
# Uses {{var:name}} syntax
title: "{{var:project_name}} Requirements"
author: "{{var:author_name}}"
date: "{{var:current_date}}"
```

---

### Schema v2 - Epic-Based Workflows

**CODEX Versions**: `0.2.0` and later (until schema v3)
**Release Date**: TBD
**Status**: Planned

**Changes from Schema v1:**
- **Added**: Epic tracking in `workflow.json`
- **Added**: Enhanced quality gate scoring
- **Changed**: Template variable syntax `{{var:name}}` → `${name}`
- **Added**: PRP versioning support
- **Added**: Learning capture between epics

**Migration Guide**: See [v0.1.x → v0.2.0](#v01x--v020-schema-1--schema-2) above.

---

### Future Schema Versions

Future schema versions will be documented here as they are released.

**Planned:**
- **Schema v3** - Brownfield enhancements (v0.3.x)
- **Schema v4** - Production-ready workflows (v1.0.0)

---

## Best Practices

### Before Any Migration

1. ✅ **Always complete active workflows first**
2. ✅ **Create manual backups** (in addition to automatic)
3. ✅ **Read the changelog** - Understand what changed
4. ✅ **Test in non-production projects first**
5. ✅ **Review version-specific migration guide**

### During Migration

1. 🛡️ **Never use `--force-schema` as first option**
2. 🛡️ **Follow manual migration steps BEFORE forcing**
3. 🛡️ **Keep backups until verified working**
4. 🛡️ **Document your customizations** before updating

### After Migration

1. ✓ **Verify installation** - Run health check
2. ✓ **Test workflows** - Start a test project
3. ✓ **Check quality gates** - Ensure enforcement works
4. ✓ **Merge configurations** - Restore customizations
5. ✓ **Clean up old backups** (after confirming success)

---

## Additional Resources

- **User Guide**: `CODEX-User-Guide.md` - How to use CODEX
- **Workflow Guide**: `CODEX-Workflow-Guide.md` - Workflow details
- **Changelog**: `CHANGELOG.md` - What changed in each version
- **Roadmap**: `ROADMAP.md` - Upcoming features
- **Updater Guide**: `lib/UPDATER-GUIDE.md` - Technical update details

---

## Contributing

Found an issue with this migration guide or have suggestions?

1. Open an issue: [GitHub Issues](https://github.com/YourRepo/CODEX/issues)
2. Submit a PR with improvements
3. Share your migration experience

---

**Last Updated**: 2025-10-09
**Document Version**: 1.0
**Covers**: CODEX v0.1.x migrations (schema v1)
