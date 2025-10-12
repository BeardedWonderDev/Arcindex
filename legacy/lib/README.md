# CODEX Library Modules

Node.js library modules for CODEX installer operations.

---

## manifest.js - Install Manifest Operations

Handles creation, reading, updating, and verification of `install-manifest.yaml` files.

### Functions

#### `createManifest(projectPath, options)`

Creates a new install manifest for a CODEX project.

**Parameters:**
- `projectPath` (string): Project root directory
- `options` (object):
  - `codex_version` (string, required): CODEX version (e.g., "0.1.0")
  - `schema_version` (number, default: 1): Manifest schema version
  - `default_workflow` (string, default: "greenfield-generic"): Default workflow
  - `test_harness_included` (boolean, default: false): Whether test harness is included
  - `ide_setup` (string[], default: ["claude-code"]): IDE integrations set up

**Returns:** Promise<Object> - Created manifest object

**Example:**
```javascript
import { createManifest } from './lib/manifest.js';

const manifest = await createManifest('/path/to/project', {
  codex_version: '0.1.0',
  default_workflow: 'greenfield-generic',
  test_harness_included: true,
  ide_setup: ['claude-code']
});
```

#### `readManifest(projectPath)`

Reads an existing manifest from `.codex/install-manifest.yaml`.

**Parameters:**
- `projectPath` (string): Project root directory

**Returns:** Object | null - Manifest object or null if not found

#### `updateManifest(projectPath, updates)`

Updates an existing manifest with new data.

**Parameters:**
- `projectPath` (string): Project root directory
- `updates` (object):
  - `codex_version` (string, optional): New CODEX version
  - `default_workflow` (string, optional): New default workflow
  - `test_harness_included` (boolean, optional): Test harness status
  - `ide_setup` (string[], optional): IDE integrations
  - `regenerate_files` (boolean, default: false): Regenerate file list with new hashes
  - `change_summary` (string, optional): Description of changes

**Returns:** Promise<Object> - Updated manifest object

#### `verifyManifest(projectPath)`

Verifies manifest integrity by checking file existence and hash matching.

**Returns:** Object - Validation results with `valid`, `totalFiles`, `missingFiles`, `modifiedFiles`, `missing`, `modified`, and `errors` properties.

#### `getManifestSummary(projectPath)`

Gets a summary of manifest information without full file details.

**Returns:** Object | null - Summary with version, workflow, file_count, etc.

### Manifest Schema

```yaml
codex_version: "0.1.0"
schema_version: 1
installed_at: "2025-10-09T20:00:00.000Z"
default_workflow: "greenfield-generic"
test_harness_included: false
ide_setup:
  - claude-code
files:
  - path: ".codex/agents/orchestrator.md"
    hash: "47dd7b50af765df2"  # SHA256 (truncated to 16 chars)
    modified: false
updates: []
```

### Testing

```bash
node lib/manifest.test.js
```

---

## state-preserver.js - State Preservation Library

State preservation and backup system for CODEX installer. Ensures user state and modifications are never lost during updates.

## Key Principles

1. **NEVER overwrite `.codex/state/`** - State directory is always preserved
2. **Always backup before changes** - Create timestamped backups before any modifications
3. **Preserve user modifications** - Detect and backup user-modified files with confirmation

## API Reference

### Core Functions

#### `createBackup(projectPath, version)`

Create a timestamped backup of the entire `.codex` directory.

**Parameters:**
- `projectPath` (string) - Path to project root
- `version` (string) - CODEX version for backup naming

**Returns:** `Promise<string>` - Path to created backup directory

**Example:**
```javascript
const backupPath = await createBackup('/path/to/project', '0.1.0');
// Returns: /path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0
```

**Backup Structure:**
```
.codex-backup-2024-10-09T12-30-45-v0.1.0/
├── backup-manifest.json          # Backup metadata
├── config/
├── workflows/
├── state/
└── ... (complete .codex copy)
```

---

#### `restoreBackup(projectPath, backupPath)`

Restore CODEX from a backup directory.

**Parameters:**
- `projectPath` (string) - Path to project root
- `backupPath` (string) - Path to backup directory

**Returns:** `Promise<boolean>` - True if restoration successful

**Example:**
```javascript
const success = await restoreBackup(
  '/path/to/project',
  '/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0'
);
```

**Safety:**
- Validates backup exists and has manifest
- Removes current `.codex` directory before restoration
- Preserves timestamps from backup

---

#### `preserveState(projectPath, manifest)`

Identify files that must be preserved during an update.

**Parameters:**
- `projectPath` (string) - Path to project root
- `manifest` (Object) - Optional manifest with file checksums to detect modifications

**Returns:** `Promise<Array<string>>` - Array of relative paths to preserve

**Example:**
```javascript
const manifest = {
  files: {
    '.codex/config/codex-config.yaml': {
      checksum: 'abc123...',
      size: 2048
    }
  }
};

const filesToPreserve = await preserveState('/path/to/project', manifest);
// Returns: [
//   '.codex/state/workflow.json',
//   '.codex/state/context-checkpoints.json',
//   '.codex/config/codex-config.yaml',  // if modified
//   '.codex/custom-workflow.yaml'       // if user-created
// ]
```

**Preservation Rules:**
1. **Always preserve:** Entire `.codex/state/` directory
2. **Conditionally preserve:** Modified config files (detected via checksum)
3. **Conditionally preserve:** User-created files (not in manifest)

---

#### `backupModifiedConfig(projectPath, manifest)`

Backup user-modified configuration files before update.

**Parameters:**
- `projectPath` (string) - Path to project root
- `manifest` (Object) - Manifest with file checksums

**Returns:** `Promise<string|null>` - Path to config backup file, or null if not modified

**Example:**
```javascript
const backupPath = await backupModifiedConfig('/path/to/project', manifest);
// Returns: /path/to/project/.codex/config/codex-config.yaml.backup-2024-10-09T12-30-45
// Or: null (if not modified)
```

---

#### `mergeConfig(projectPath, backupPath, options)`

Merge configuration after update with user review.

**Parameters:**
- `projectPath` (string) - Path to project root
- `backupPath` (string) - Path to backed up config file
- `options` (Object) - Merge options
  - `interactive` (boolean) - Show interactive diff (default: true)
  - `strategy` (string) - Merge strategy: `'keep'` | `'merge'` | `'replace'`

**Returns:** `Promise<Object>` - Merge result

**Merge Strategies:**

1. **`keep`** - Keep user's old config (restore backup over new config)
2. **`replace`** - Use new config (discard user changes)
3. **`merge`** (default) - Manual merge required (preserve both for review)

**Example:**
```javascript
const result = await mergeConfig(projectPath, backupPath, {
  interactive: true,
  strategy: 'merge'
});

// Result:
// {
//   applied: false,
//   strategy: 'manual',
//   changes: [
//     {
//       line: 5,
//       section: 'default_workflow',
//       oldValue: 'health-check',
//       newValue: 'greenfield-swift'
//     },
//     {
//       line: 15,
//       section: 'checkpoint_frequency',
//       oldValue: '300',
//       newValue: '600'
//     }
//   ]
// }
```

---

#### `listBackups(projectPath)`

List all available backups for a project.

**Parameters:**
- `projectPath` (string) - Path to project root

**Returns:** `Promise<Array<Object>>` - Array of backup metadata objects

**Example:**
```javascript
const backups = await listBackups('/path/to/project');

// Returns:
// [
//   {
//     name: '.codex-backup-2024-10-09T12-30-45-v0.1.0',
//     path: '/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0',
//     version: '0.1.0',
//     created_at: '2024-10-09T12:30:45Z',
//     files_count: 42,
//     size_bytes: 2048576
//   }
// ]
```

---

#### `cleanupOldBackups(projectPath, keepCount)`

Clean up old backups, keeping only the most recent N backups.

**Parameters:**
- `projectPath` (string) - Path to project root
- `keepCount` (number) - Number of recent backups to keep (default: 5)

**Returns:** `Promise<number>` - Number of backups removed

**Example:**
```javascript
const removedCount = await cleanupOldBackups('/path/to/project', 5);
// Keeps 5 most recent, removes older backups
```

---

## Complete Installer Workflow

```javascript
const statePreserver = require('./lib/state-preserver');

async function updateCODEX(projectPath, currentVersion, newVersion, installerManifest) {
  console.log('Starting CODEX update...\n');

  // Step 1: Create pre-update backup
  console.log('Step 1: Creating backup...');
  const backupPath = await statePreserver.createBackup(projectPath, currentVersion);

  // Step 2: Identify files to preserve
  console.log('\nStep 2: Identifying files to preserve...');
  const filesToPreserve = await statePreserver.preserveState(projectPath, installerManifest);

  // Step 3: Backup modified config
  console.log('\nStep 3: Backing up modified config...');
  const configBackup = await statePreserver.backupModifiedConfig(projectPath, installerManifest);

  // Step 4: Extract new CODEX files
  console.log('\nStep 4: Extracting new CODEX files...');
  // (installer extracts new files, avoiding preserved paths)

  // Step 5: Restore preserved files
  console.log('\nStep 5: Restoring preserved files...');
  // (installer restores files from filesToPreserve)

  // Step 6: Merge configuration if needed
  if (configBackup) {
    console.log('\nStep 6: Merging configuration...');
    const mergeResult = await statePreserver.mergeConfig(projectPath, configBackup, {
      interactive: true,
      strategy: 'merge'
    });

    if (mergeResult.changes.length > 0) {
      console.log('\n⚠ Configuration merge required - please review changes');
    }
  }

  // Step 7: Cleanup old backups
  console.log('\nStep 7: Cleaning up old backups...');
  await statePreserver.cleanupOldBackups(projectPath, 5);

  console.log('\n✓ Update complete!');
}
```

## File Modification Detection

The module uses SHA256 checksums to detect file modifications:

1. **Manifest Format:**
   ```json
   {
     "files": {
       ".codex/config/codex-config.yaml": {
         "checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
         "size": 2048
       }
     }
   }
   ```

2. **Detection Logic:**
   - Compare current file checksum vs. manifest checksum
   - If checksums differ → file modified by user
   - If file not in manifest → user-created file

## Backup Manifest Structure

Each backup includes a `backup-manifest.json`:

```json
{
  "created_at": "2024-10-09T12:30:45.000Z",
  "version": "0.1.0",
  "source_path": "/path/to/project/.codex",
  "backup_path": "/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0",
  "files_backed_up": 42
}
```

## Error Handling

All functions include comprehensive error handling:

```javascript
try {
  const backupPath = await createBackup(projectPath, version);
} catch (error) {
  console.error('Backup failed:', error.message);
  // Handle error appropriately
}
```

## Dependencies

- `fs-extra` - Enhanced file operations with promises
- `chalk` - Terminal output styling
- `crypto` - SHA256 checksums (built-in Node.js module)
- `path` - Path manipulation (built-in Node.js module)

## Testing

See `state-preserver.test.js` for usage examples and test scenarios.

Run examples:
```bash
node lib/state-preserver.test.js
```

## Best Practices

1. **Always backup before modifications**
   ```javascript
   const backupPath = await createBackup(projectPath, currentVersion);
   ```

2. **Check for preserved files before extraction**
   ```javascript
   const filesToPreserve = await preserveState(projectPath, manifest);
   // Skip these files during extraction
   ```

3. **Handle config merges interactively**
   ```javascript
   if (configBackup) {
     const result = await mergeConfig(projectPath, configBackup, {
       strategy: 'merge'  // Let user review
     });
   }
   ```

4. **Clean up old backups regularly**
   ```javascript
   await cleanupOldBackups(projectPath, 5);  // Keep 5 most recent
   ```

## Integration with Installer

The installer should:

1. Load manifest from installer package
2. Create backup before any changes
3. Identify files to preserve
4. Extract new files (skip preserved paths)
5. Restore preserved files over extracted files
6. Handle config merges
7. Clean up old backups

See `state-preserver.test.js` for complete workflow example.

---

## updater.js - CODEX Update Orchestration

Comprehensive update orchestration for existing CODEX installations. Handles version compatibility, schema validation, state preservation, backup creation, and rollback on failure.

**See [UPDATER-GUIDE.md](./UPDATER-GUIDE.md) for complete documentation.**

### Core Functions

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

**Example:**
```javascript
import { updateCodex } from './lib/updater.js';

const result = await updateCodex('/path/to/project', 'latest', {
  verbose: true,
  skipConfirmation: false,
  forceSchema: false
});

if (result.success) {
  console.log(`Updated from ${result.previousVersion} to ${result.newVersion}`);
} else {
  console.error(`Update failed: ${result.message}`);
}
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
import { checkForUpdates } from './lib/updater.js';

const check = await checkForUpdates('0.1.0');

if (check.updateAvailable) {
  console.log(`Update available: ${check.latestVersion} (${check.releaseType})`);
}
```

### Update Process Flow

1. **Detect existing installation** - Read manifest, extract version and schema
2. **Check compatibility** - Verify no active workflow, check schema compatibility
3. **Handle blocking conditions** - Active workflow, schema mismatch
4. **Prompt for confirmation** - Show versions, warn about active workflow
5. **Create backup** - Copy entire .codex directory
6. **Identify files to preserve** - State, modified config, user files
7. **Backup modified config** - Create timestamped backup if modified
8. **Fetch target version** - Get package info from npm registry
9. **Update CODEX files** - Transaction-like file operations with rollback
10. **Merge configuration** - Prompt for merge strategy if config modified
11. **Update manifest** - Update version, regenerate file list
12. **Cleanup old backups** - Keep only 5 most recent
13. **Success / Rollback** - Show summary or attempt rollback

### Edge Cases Handled

- **Network errors** - Catch fetch errors, preserve installation
- **Active workflow** - Detect and BLOCK update
- **Schema version mismatch** - Block without --force-schema, dangerous prompt with flag
- **Disk space issues** - Backup failure → ABORT, update failure → ROLLBACK
- **Backup creation failure** - ABORT immediately, no changes made
- **File update failure** - Rollback from backup
- **Modified configuration** - Backup and merge with user review

### Schema Version Protection

Schema changes indicate breaking changes to workflow state structure:

**Without `--force-schema`:**
- BLOCKS update
- Shows migration guide URL
- Explains risks
- Provides safe upgrade instructions

**With `--force-schema`:**
- Shows dangerous warning
- Requires typing "yes" to confirm
- Creates backup before proceeding
- Proceeds with preserved state (may be incompatible)

### Testing

```bash
node --test lib/updater.test.js
```

### Dependencies

Integrates with:
- `detector.js` - Installation and workflow detection
- `compatibility-checker.js` - Version and schema compatibility
- `state-preserver.cjs` - Backup and state preservation
- `file-manager.cjs` - File operations
- `manifest.js` - Manifest operations
- `menu.cjs` - User prompts

---

## detector.js - Installation Detection

Detects existing CODEX installations and active workflow status.

### Functions

#### `detectExistingInstallation(projectPath)`

Detect if CODEX is already installed.

**Returns:**
```javascript
{
  exists: boolean,
  version: string|null,
  schemaVersion: number|null,
  manifest: Object|null
}
```

#### `detectActiveWorkflow(projectPath)`

Detect if there's an active workflow in progress.

**Returns:**
```javascript
{
  active: boolean,
  phase: string|null,
  workflowType: string|null,
  workflowState: Object|null
}
```

#### `fetchPackageInfo(packageName, version)`

Fetch package.json information from npm registry.

**Returns:** Promise<Object> - Package information

---

## compatibility-checker.js - Compatibility Validation

Validates compatibility between installed and target CODEX versions.

### Functions

#### `checkCompatibility(projectPath, targetVersion)`

Check compatibility between current installation and target version.

**Returns:**
```javascript
{
  compatible: boolean,
  reason: string|null,
  severity: 'critical'|'warning'|null,
  currentVersion: string,
  targetVersion: string,
  currentSchema: number,
  targetSchema: number,
  message: string,
  action: 'BLOCKED'|'WARNING'|null,
  requiresConfirmation: boolean,
  schemaChange: Object|null  // if schema mismatch
}
```

**Checks:**
- Existing installation detection
- Active workflow detection (BLOCKS if active)
- Schema version compatibility (BLOCKS on mismatch)
- Semantic version validation
- Upgrade/downgrade/reinstall scenarios

---

## file-manager.cjs - File Operations

Robust file operations for CODEX installer.

### Functions

#### `copyDirectory(source, target, options)`

Copy directory with optional exclusion patterns.

**Parameters:**
- `source` (string): Source directory path
- `target` (string): Target directory path
- `options.exclude` (string[]): Patterns to exclude

#### `removeDirectory(dirPath)`

Remove directory and all contents recursively.

#### `fileExists(filePath)`

Check if a file exists.

#### `readJsonFile(filePath)`

Read and parse a JSON file.

#### `writeJsonFile(filePath, data)`

Write an object to a JSON file.

---

## menu.cjs - User Prompts

Interactive prompts for installer operations.

### Functions

#### `promptWorkflowChoice()`

Prompt user to select default workflow.

**Returns:** Promise<string> - Selected workflow ID

#### `promptTestHarness()`

Prompt user to decide if test harness should be installed.

**Returns:** Promise<boolean>

#### `promptUpdateConfirmation(currentVersion, targetVersion, hasActiveWorkflow)`

Prompt user to confirm CODEX update.

**Returns:** Promise<boolean>

#### `promptForceSchemaOverride(currentVersion, targetVersion, currentSchema, targetSchema)`

Prompt user to confirm dangerous schema upgrade with forced override.
Requires typing "yes" to confirm (not just Y/n).

**Returns:** Promise<boolean>

---

## installer.js - Core Installation Logic

Main installation orchestrator for CODEX. Handles directory validation, file copying, manifest creation, and user feedback.

### Functions

#### `installCodex(targetPath, options)`

Main installation function that orchestrates the complete installation workflow.

**Parameters:**
- `targetPath` (string): Directory to install CODEX
- `options` (object):
  - `workflow` (string, default: 'greenfield-generic'): Selected workflow
  - `includeTestHarness` (boolean, default: false): Include test harness
  - `verbose` (boolean, default: false): Enable verbose logging

**Returns:** Promise<{success: boolean, message: string}>

**Example:**
```javascript
import { installCodex } from './lib/installer.js';

const result = await installCodex('/path/to/project', {
  workflow: 'greenfield-generic',
  includeTestHarness: false,
  verbose: true
});

if (result.success) {
  console.log('Installation complete!');
} else {
  console.error(result.message);
}
```

**Installation Steps:**
1. Validate target directory (permissions, space, existing installation)
2. Get installer package path (handles npm link and installed package)
3. Prepare target directory
4. Copy `.codex/` directory (excluding test harness if not requested)
5. Copy `.claude/commands/codex.md` for IDE integration
6. Create installation manifest with version tracking
7. Copy documentation files to project root
8. Report success with visual feedback

#### `getInstallerPackagePath()`

Get the path to the installer package root containing `.codex/` and `.claude/` directories.

**Returns:** string - Absolute path to package root

**Example:**
```javascript
const packageRoot = getInstallerPackagePath();
// Returns: /Users/.../CODEX/v0.1-implementation
```

**Features:**
- Works with development mode (`npm link`)
- Works with installed package (`npm install -g`)
- Works with local installation (`npx`)
- Validates required directories exist

#### `validateTarget(targetPath)`

Validate target directory before installation.

**Parameters:**
- `targetPath` (string): Directory to validate

**Returns:** Promise<{valid: boolean, reason?: string}>

**Validation Checks:**
1. Directory exists
2. Is actually a directory (not a file)
3. Has write permissions (tests by creating temp file)
4. Has sufficient disk space (50MB minimum)
5. Does not already contain `.codex/` directory

**Example:**
```javascript
const validation = await validateTarget('/path/to/project');

if (!validation.valid) {
  console.error(`Cannot install: ${validation.reason}`);
  process.exit(1);
}
```

**Error Messages:**
- `"Target directory does not exist"`
- `"Target path is not a directory"`
- `"No write permission for target directory"`
- `"Insufficient disk space (need 50MB, have XMB)"`
- `"CODEX already installed (.codex directory exists). Use update command instead."`

#### `showWelcomeBanner(version)`

Display installation welcome banner with styling.

**Parameters:**
- `version` (string): CODEX version being installed

**Example:**
```javascript
showWelcomeBanner('0.1.0');
```

**Output:**
```
╔════════════════════════════════════════════════════════╗
║          CODEX Installation                        ║
║          AI Agent Workflow Orchestration               ║
╚════════════════════════════════════════════════════════╝

  Version: 0.1.0
  License: MIT
```

#### `showSuccessMessage(targetPath, workflow)`

Display success message with next steps and pro tips.

**Parameters:**
- `targetPath` (string): Installation directory
- `workflow` (string): Selected workflow name

**Example:**
```javascript
showSuccessMessage('/path/to/project', 'greenfield-generic');
```

**Output Sections:**
1. **Next Steps** - Navigate, start CODEX, review workflow
2. **Documentation** - User Guide, Workflow Guide, Contributing
3. **Pro Tips** - Status checking, help command, configuration

### Complete Installation Example

```javascript
import {
  installCodex,
  showWelcomeBanner,
  showSuccessMessage
} from './lib/installer.js';
import { promptWorkflowChoice, promptTestHarness } from './lib/menu.js';

// 1. Show banner
showWelcomeBanner('0.1.0');

// 2. Get options from user
const workflow = await promptWorkflowChoice();
const includeTestHarness = await promptTestHarness();

// 3. Run installation
const result = await installCodex('/path/to/project', {
  workflow,
  includeTestHarness,
  verbose: true
});

// 4. Show result
if (result.success) {
  showSuccessMessage('/path/to/project', workflow);
} else {
  console.error(result.message);
  process.exit(1);
}
```

### File Operations

#### .codex/ Directory Copy
- **Source**: `${packageRoot}/.codex/`
- **Target**: `${targetPath}/.codex/`
- **Exclusions**: Optionally excludes `test-harness/` directory
- **Behavior**: Overwrites existing files, creates directories

#### .claude/commands/codex.md Copy
- **Source**: `${packageRoot}/.claude/commands/codex.md`
- **Target**: `${targetPath}/.claude/commands/codex.md`
- **Behavior**: Does NOT overwrite if file exists

#### Documentation Files Copy
- Files: `CODEX-User-Guide.md`, `CODEX-Workflow-Guide.md`, `CONTRIBUTING.md`
- **Target**: Project root
- **Behavior**: Does NOT overwrite existing files

### Testing

```bash
node lib/test-installer.js
node lib/verify-installer.js
```

### Performance

- **Small projects** (~500 files): 1-2 seconds
- **With test harness** (~1000 files): 2-3 seconds
- **Memory usage**: <50MB peak

### Dependencies

- `fs-extra` - Enhanced file operations
- `chalk` - Terminal styling
- `ora` - Progress spinners
- `manifest.js` - Manifest creation
