# CODEX Updater Module Guide

## Overview

The `updater.js` module provides comprehensive update orchestration for existing CODEX installations. It handles version compatibility checking, schema validation, state preservation, backup creation, and rollback on failure.

## Architecture

### Module Dependencies

```
updater.js
├── detector.js              (Installation & workflow detection)
├── compatibility-checker.js (Version & schema compatibility)
├── state-preserver.cjs      (Backup & state preservation)
├── file-manager.cjs         (File operations)
├── manifest.js              (Manifest operations)
└── menu.js                  (User prompts)
```

### Key Functions

#### `updateCodex(projectPath, targetVersion, options)`

Main update orchestration function that handles the entire update process.

**Parameters:**
- `projectPath` (string): Path to project with existing CODEX installation
- `targetVersion` (string): Version to update to ('latest' or specific version)
- `options` (Object):
  - `forceSchema` (boolean): Force schema override (dangerous) - default: false
  - `noBackup` (boolean): Skip backup creation - default: false
  - `verbose` (boolean): Verbose output - default: false
  - `skipConfirmation` (boolean): Skip update confirmation - default: false

**Returns:** Promise<Object>
```javascript
{
  success: boolean,
  message: string,
  backupPath: string|null,
  previousVersion: string,  // if successful
  newVersion: string,       // if successful
  reason: string            // if failed
}
```

**Update Process Flow:**

```
1. Detect existing installation
   ├─ Read install-manifest.yaml
   └─ Extract version and schema version

2. Check compatibility
   ├─ Verify no active workflow
   ├─ Check schema version compatibility
   └─ Validate version upgrade path

3. Handle blocking conditions
   ├─ Active workflow → BLOCK
   ├─ Schema mismatch without --force-schema → BLOCK
   └─ Schema mismatch with --force-schema → Prompt dangerous confirmation

4. Prompt for confirmation
   └─ Show versions, warn about active workflow

5. Create backup
   ├─ Copy entire .codex directory
   └─ Generate backup manifest

6. Identify files to preserve
   ├─ All files in .codex/state/
   ├─ Modified config files
   └─ User-created custom files

7. Backup modified config
   └─ Create timestamped backup if config was modified

8. Fetch target version
   └─ Get package info from npm registry

9. Update CODEX files
   ├─ Save preserved files to temp directory
   ├─ Remove old .codex directory
   ├─ Copy new .codex directory
   ├─ Restore preserved files
   └─ Update .claude/commands/codex.md

10. Merge configuration
    └─ Prompt for merge strategy if config was modified

11. Update manifest
    ├─ Update codex_version
    ├─ Regenerate file list with new hashes
    └─ Add update record to history

12. Cleanup old backups
    └─ Keep only 5 most recent backups

13. Success / Rollback
    ├─ Success → Show summary
    └─ Failure → Attempt rollback from backup
```

#### `checkForUpdates(currentVersion)`

Check npm registry for available updates.

**Parameters:**
- `currentVersion` (string): Currently installed version

**Returns:** Promise<Object>
```javascript
{
  updateAvailable: boolean,
  latestVersion: string,
  currentVersion: string,
  releaseType: 'major'|'minor'|'patch'|null,
  error: string  // if error occurred
}
```

**Example:**
```javascript
const result = await checkForUpdates('0.1.0');
if (result.updateAvailable) {
  console.log(`Update available: ${result.latestVersion} (${result.releaseType})`);
}
```

#### `handleSchemaVersionMismatch()` (internal)

Handles schema version mismatches by blocking or prompting for dangerous override.

**Behavior:**
- Without `--force-schema`: Blocks with migration guide URL
- With `--force-schema`: Prompts for dangerous confirmation requiring "yes" input

**Schema Protection:**
- Schema changes indicate breaking changes to workflow state structure
- Cannot proceed without explicit override to prevent data corruption
- Users must acknowledge risks before proceeding

#### `updateFiles(projectPath, filesToPreserve, options)` (internal)

Updates CODEX files while preserving specified files.

**Transaction-like behavior:**
1. Save preserved files to temp directory
2. Remove old installation
3. Copy new installation
4. Restore preserved files
5. Cleanup temp directory
6. On error: cleanup and throw (rollback handled by caller)

## Edge Cases Handled

### 1. Network Errors

**Scenario:** Unable to reach npm registry

**Handling:**
- Catch fetch errors from `fetchPackageInfo()`
- Return detailed error message with reason
- Preserve current installation (no changes made)

**Example:**
```javascript
{
  success: false,
  message: 'Failed to fetch package info: Network error',
  backupPath: null,
  reason: 'fetch-failed'
}
```

### 2. Active Workflow

**Scenario:** Workflow is in progress during update attempt

**Handling:**
- Detected in compatibility check
- BLOCKS update completely
- Shows current phase and workflow type
- Instructs user to complete or cancel workflow first

**Detection:**
```javascript
// From detector.js
const workflow = await detectActiveWorkflow(projectPath);
if (workflow.active) {
  // Block with detailed message
}
```

### 3. Schema Version Mismatch

**Scenario:** Target version has different schema version

**Without `--force-schema`:**
- BLOCKS update
- Shows migration guide URL
- Explains risks
- Provides instructions to proceed safely

**With `--force-schema`:**
- Shows dangerous warning
- Requires typing "yes" to confirm
- Creates backup before proceeding
- Updates with preserved state (may be incompatible)

**Example warning:**
```
⚠️  DANGEROUS SCHEMA UPGRADE DETECTED
═══════════════════════════════════
This update includes a schema version change that may be
incompatible with your existing workflow state!

Current version: 0.1.0 (schema 1)
Target version:  0.2.0 (schema 2)

Potential risks:
  • Loss of workflow state and progress
  • Incompatible template formats
  • Breaking changes to agent behavior
  • Data corruption or migration issues

This operation cannot be undone!
```

### 4. Disk Space Issues

**Scenario:** Insufficient disk space for backup or update

**Handling:**
- `fs-extra` operations will throw ENOSPC error
- Caught by try-catch in `updateCodex()`
- Backup creation failure → ABORT (no changes made)
- Update failure → ROLLBACK from backup

**Prevention:**
- Could add `checkDiskSpace()` before backup (currently basic implementation)
- Future: Add disk space check at start of update process

### 5. Backup Creation Failure

**Scenario:** Cannot create backup (permissions, disk space, etc.)

**Handling:**
- Catch error in backup creation step
- ABORT update immediately (no changes made)
- Show error message
- Suggest using `--no-backup` if user wants to override (not recommended)

**Example:**
```javascript
if (!noBackup) {
  try {
    backupPath = await createBackup(projectPath, installation.version);
  } catch (error) {
    // ABORT - cannot proceed without backup
    return {
      success: false,
      message: `Backup failed: ${error.message}`,
      backupPath: null,
      reason: 'backup-failed'
    };
  }
}
```

### 6. File Update Failure (Mid-Update)

**Scenario:** Error occurs during file copying

**Handling:**
1. Catch error in `updateFiles()`
2. Cleanup temp directory
3. Throw error to `updateCodex()`
4. `updateCodex()` attempts rollback from backup
5. If rollback succeeds: restored to previous state
6. If rollback fails: backup preserved for manual restoration

**Rollback logic:**
```javascript
catch (error) {
  if (backupPath) {
    console.log('Attempting to rollback from backup...');
    const restored = await restoreBackup(projectPath, backupPath);
    if (restored) {
      console.log('✓ Successfully rolled back');
    } else {
      console.log('✗ Rollback failed. Backup preserved at: ' + backupPath);
    }
  }
}
```

### 7. Manifest Update Failure

**Scenario:** Cannot update install-manifest.yaml

**Handling:**
- Treated as non-critical warning (files already updated)
- Logs warning but continues
- Returns success (update completed despite manifest issue)
- User can manually fix manifest or reinstall

**Rationale:**
- File update is the critical operation
- Manifest is metadata (can be regenerated)
- Better to have working files with stale manifest than rollback

### 8. Modified Configuration

**Scenario:** User has modified codex-config.yaml

**Detection:**
- Compare file checksums against manifest
- Identified in `preserveState()`

**Handling:**
1. Backup modified config with timestamp
2. Proceed with update (installs new config)
3. Show merge prompt:
   - `keep`: Use old config (overwrite new)
   - `replace`: Use new config (discard changes)
   - `manual`: Keep both for manual review (default)

**Manual merge output:**
```
Configuration Merge Required
──────────────────────────────
Detected 3 configuration differences:

1. template_paths
   - Old: "./templates"
   + New: "./.codex/templates"

2. state_dir
   - Old: "./.codex/workflow-state"
   + New: "./.codex/state"

⚠ Manual merge required
  Old config saved: codex-config.yaml.backup-2024-10-09T12-30-45
  New config active: codex-config.yaml

  Review both files and manually merge if needed.
```

## Usage Examples

### Basic Update

```javascript
import { updateCodex } from './lib/updater.js';

const result = await updateCodex('/path/to/project', 'latest');

if (result.success) {
  console.log(`Updated from ${result.previousVersion} to ${result.newVersion}`);
} else {
  console.error(`Update failed: ${result.message}`);
}
```

### Update with Options

```javascript
const result = await updateCodex('/path/to/project', '0.1.5', {
  verbose: true,          // Show detailed progress
  skipConfirmation: true, // Don't prompt for confirmation
  noBackup: false,        // Always create backup (recommended)
  forceSchema: false      // Block on schema mismatch (safe)
});
```

### Check for Updates

```javascript
import { checkForUpdates } from './lib/updater.js';

const check = await checkForUpdates('0.1.0');

if (check.updateAvailable) {
  console.log(`Update available: ${check.latestVersion}`);
  console.log(`Release type: ${check.releaseType}`);

  // Then update
  await updateCodex('/path/to/project', check.latestVersion);
}
```

### Dangerous Schema Override

```bash
# Command line usage (when integrated into CLI)
$ create-codex-project update --force-schema

# Will prompt with dangerous warning and require typing "yes"
```

```javascript
// Programmatic usage
const result = await updateCodex('/path/to/project', 'latest', {
  forceSchema: true,  // Allows schema mismatch (will prompt)
  skipConfirmation: false  // User must still confirm danger
});
```

## Integration with CLI

The updater module is designed to be integrated into the main CLI tool:

```javascript
// In bin/create-codex-project.js
import { updateCodex, checkForUpdates } from './lib/updater.js';

program
  .command('update [version]')
  .description('Update CODEX installation')
  .option('--force-schema', 'Force schema version override (dangerous)')
  .option('--no-backup', 'Skip backup creation')
  .option('--verbose', 'Show verbose output')
  .action(async (version, options) => {
    const projectPath = process.cwd();
    const targetVersion = version || 'latest';

    const result = await updateCodex(projectPath, targetVersion, options);

    if (!result.success) {
      process.exit(1);
    }
  });

program
  .command('check-updates')
  .description('Check for available updates')
  .action(async () => {
    const installation = await detectExistingInstallation(process.cwd());

    if (!installation.exists) {
      console.log('No CODEX installation found');
      return;
    }

    const result = await checkForUpdates(installation.version);

    if (result.updateAvailable) {
      console.log(`Update available: ${result.latestVersion} (${result.releaseType})`);
    } else {
      console.log('Already running latest version');
    }
  });
```

## Testing

### Unit Tests

Run unit tests:
```bash
node --test lib/updater.test.js
```

### Manual Testing

1. **Create test project:**
   ```bash
   mkdir test-update
   cd test-update
   npx create-codex-project@0.1.0 .
   ```

2. **Modify some files to test preservation:**
   ```bash
   # Create some state
   echo '{"test": "data"}' > .codex/state/test.json

   # Modify config
   vim .codex/config/codex-config.yaml
   ```

3. **Test update:**
   ```bash
   npx create-codex-project update
   ```

4. **Verify:**
   - State files preserved
   - Modified config backed up
   - Manifest updated
   - Backup created

### Integration Testing

See `lib/updater.test.js` for integration test scenarios.

## Error Messages

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No CODEX installation detected` | No `.codex` directory | Use `install` command instead |
| `Active workflow in progress` | Workflow is running | Complete or cancel workflow first |
| `Incompatible schema version` | Schema mismatch without --force-schema | Review migration guide, use --force-schema cautiously |
| `Backup failed: ENOSPC` | Insufficient disk space | Free up disk space |
| `Failed to fetch package info` | Network error | Check internet connection |
| `Update failed: EACCES` | Permission denied | Check file permissions |

## Best Practices

### For Users

1. **Always allow backup creation** (don't use `--no-backup`)
2. **Complete active workflows before updating**
3. **Review changelogs** before major updates
4. **Test updates in non-production environments first**
5. **Never force schema override unless you understand the risks**

### For Developers

1. **Always increment schema version for breaking changes**
2. **Document migration paths in MIGRATION.md**
3. **Test update paths from previous versions**
4. **Preserve backward compatibility within same schema version**
5. **Keep update process transaction-like (rollback on failure)**

## Future Enhancements

1. **Partial updates**: Update specific components only
2. **Update preview**: Show what will change before applying
3. **Automatic migration**: Migrate data between schema versions
4. **Update channels**: stable, beta, nightly
5. **Delta updates**: Only download changed files
6. **Disk space check**: Verify sufficient space before starting
7. **Update hooks**: Allow custom pre/post update scripts

## Related Files

- `lib/detector.js` - Installation and workflow detection
- `lib/compatibility-checker.js` - Compatibility validation
- `lib/state-preserver.cjs` - Backup and state preservation
- `lib/file-manager.cjs` - File operations
- `lib/manifest.js` - Manifest operations
- `lib/menu.js` - User prompts
- `MIGRATION.md` - Migration guides for schema changes

## Support

For issues with the updater:
1. Check backup directory for restoration
2. Review error messages and logs
3. Consult MIGRATION.md for schema changes
4. Report bugs with full error output and versions
