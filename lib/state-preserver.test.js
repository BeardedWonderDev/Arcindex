/**
 * State Preserver Usage Examples and Tests
 *
 * This file demonstrates how to use the state-preserver module
 * in the CODEX installer workflow.
 */

import * as statePreserver from './state-preserver.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================================
// Example Usage Scenarios
// ============================================================================

/**
 * Scenario 1: Before Update - Create Backup
 */
async function exampleCreateBackup() {
  console.log('\n=== Example: Create Backup ===\n');

  const projectPath = '/path/to/project';
  const version = '0.1.0';

  try {
    const backupPath = await statePreserver.createBackup(projectPath, version);
    console.log('Backup created at:', backupPath);
    // Returns: /path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0
  } catch (error) {
    console.error('Backup failed:', error.message);
  }
}

/**
 * Scenario 2: During Update - Preserve User State
 */
async function examplePreserveState() {
  console.log('\n=== Example: Preserve State ===\n');

  const projectPath = '/path/to/project';

  // Example manifest (from installer package)
  const manifest = {
    files: {
      '.codex/config/codex-config.yaml': {
        checksum: 'abc123...',
        size: 2048
      },
      '.codex/workflows/greenfield-swift.yaml': {
        checksum: 'def456...',
        size: 4096
      }
      // ... more files
    }
  };

  try {
    const filesToPreserve = await statePreserver.preserveState(projectPath, manifest);

    console.log('Files to preserve:');
    filesToPreserve.forEach(file => console.log(`  - ${file}`));

    // Expected output:
    // - .codex/state/workflow.json
    // - .codex/state/context-checkpoints.json
    // - .codex/config/codex-config.yaml (if modified)
    // - .codex/custom-workflow.yaml (if user-created)

  } catch (error) {
    console.error('Preserve state failed:', error.message);
  }
}

/**
 * Scenario 3: Backup Modified Config Before Update
 */
async function exampleBackupModifiedConfig() {
  console.log('\n=== Example: Backup Modified Config ===\n');

  const projectPath = '/path/to/project';

  const manifest = {
    files: {
      '.codex/config/codex-config.yaml': {
        checksum: 'abc123originalchecksum',
        size: 2048
      }
    }
  };

  try {
    const backupPath = await statePreserver.backupModifiedConfig(projectPath, manifest);

    if (backupPath) {
      console.log('Config backed up to:', backupPath);
      // Returns: /path/to/project/.codex/config/codex-config.yaml.backup-2024-10-09T12-30-45
    } else {
      console.log('Config not modified, no backup needed');
    }
  } catch (error) {
    console.error('Config backup failed:', error.message);
  }
}

/**
 * Scenario 4: After Update - Merge Config
 */
async function exampleMergeConfig() {
  console.log('\n=== Example: Merge Config ===\n');

  const projectPath = '/path/to/project';
  const backupPath = '/path/to/project/.codex/config/codex-config.yaml.backup-2024-10-09T12-30-45';

  try {
    // Interactive merge with diff display
    const result = await statePreserver.mergeConfig(projectPath, backupPath, {
      interactive: true,
      strategy: 'merge' // 'keep' | 'merge' | 'replace'
    });

    console.log('Merge result:', result);
    // {
    //   applied: false,
    //   strategy: 'manual',
    //   changes: [
    //     { line: 5, section: 'default_workflow', oldValue: 'health-check', newValue: 'greenfield-swift' },
    //     { line: 15, section: 'checkpoint_frequency', oldValue: '300', newValue: '600' }
    //   ]
    // }

  } catch (error) {
    console.error('Config merge failed:', error.message);
  }
}

/**
 * Scenario 5: Emergency Restore from Backup
 */
async function exampleRestoreBackup() {
  console.log('\n=== Example: Restore Backup ===\n');

  const projectPath = '/path/to/project';
  const backupPath = '/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0';

  try {
    const success = await statePreserver.restoreBackup(projectPath, backupPath);

    if (success) {
      console.log('Successfully restored from backup');
    } else {
      console.log('Restoration failed');
    }
  } catch (error) {
    console.error('Restore failed:', error.message);
  }
}

/**
 * Scenario 6: List Available Backups
 */
async function exampleListBackups() {
  console.log('\n=== Example: List Backups ===\n');

  const projectPath = '/path/to/project';

  try {
    const backups = await statePreserver.listBackups(projectPath);

    console.log(`Found ${backups.length} backup(s):\n`);
    backups.forEach(backup => {
      console.log(`  ${backup.name}`);
      console.log(`    Version: ${backup.version}`);
      console.log(`    Created: ${backup.created_at}`);
      console.log(`    Files: ${backup.files_count}`);
      console.log();
    });
  } catch (error) {
    console.error('List backups failed:', error.message);
  }
}

/**
 * Scenario 7: Cleanup Old Backups
 */
async function exampleCleanupBackups() {
  console.log('\n=== Example: Cleanup Old Backups ===\n');

  const projectPath = '/path/to/project';
  const keepCount = 5; // Keep 5 most recent backups

  try {
    const removedCount = await statePreserver.cleanupOldBackups(projectPath, keepCount);
    console.log(`Removed ${removedCount} old backup(s)`);
  } catch (error) {
    console.error('Cleanup failed:', error.message);
  }
}

// ============================================================================
// Complete Installer Workflow Example
// ============================================================================

/**
 * Complete workflow: Update CODEX with state preservation
 */
async function completeUpdateWorkflow() {
  console.log('\n=== Complete Update Workflow ===\n');

  const projectPath = process.cwd();
  const currentVersion = '0.0.9';
  const newVersion = '0.1.0';

  console.log('Step 1: Create pre-update backup...');
  const backupPath = await statePreserver.createBackup(projectPath, currentVersion);

  console.log('\nStep 2: Identify files to preserve...');
  const manifest = { files: {} }; // Load from installer package
  const filesToPreserve = await statePreserver.preserveState(projectPath, manifest);

  console.log('\nStep 3: Backup modified config...');
  const configBackup = await statePreserver.backupModifiedConfig(projectPath, manifest);

  console.log('\nStep 4: Extract new CODEX files...');
  // (installer extracts new files here)

  console.log('\nStep 5: Restore preserved files...');
  // (installer restores preserved files here)

  if (configBackup) {
    console.log('\nStep 6: Merge configuration...');
    const mergeResult = await statePreserver.mergeConfig(projectPath, configBackup, {
      interactive: true,
      strategy: 'merge'
    });
    console.log('Merge result:', mergeResult.strategy);
  }

  console.log('\nStep 7: Cleanup old backups...');
  await statePreserver.cleanupOldBackups(projectPath, 5);

  console.log('\n✓ Update complete!');
}

// ============================================================================
// Run Examples (if called directly)
// ============================================================================

// Check if this module is being run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('State Preserver Usage Examples');
  console.log('================================');

  // Uncomment to run specific examples:
  // await exampleCreateBackup();
  // await examplePreserveState();
  // await exampleBackupModifiedConfig();
  // await exampleMergeConfig();
  // await exampleRestoreBackup();
  // await exampleListBackups();
  // await exampleCleanupBackups();
  // await completeUpdateWorkflow();

  console.log('\nEdit this file to run specific examples.');
}

export {
  exampleCreateBackup,
  examplePreserveState,
  exampleBackupModifiedConfig,
  exampleMergeConfig,
  exampleRestoreBackup,
  exampleListBackups,
  exampleCleanupBackups,
  completeUpdateWorkflow
};
