const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const crypto = require('crypto');

/**
 * CODEX State Preservation and Backup System
 *
 * Handles state preservation, backup creation, and restoration for CODEX installer.
 * Ensures user state and modifications are never lost during updates.
 *
 * Key Principles:
 * - NEVER overwrite .codex/state/
 * - Always backup before any changes
 * - Preserve user modifications with confirmation
 */

/**
 * Create a timestamped backup of the entire .codex directory
 *
 * @param {string} projectPath - Path to the project root
 * @param {string} version - CODEX version for backup naming
 * @returns {Promise<string>} Path to created backup directory
 *
 * @example
 * const backupPath = await createBackup('/path/to/project', '0.1.0');
 * // Returns: '/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0'
 */
async function createBackup(projectPath, version) {
  const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
  const backupDirName = `.codex-backup-${timestamp}-v${version}`;
  const backupPath = path.join(projectPath, backupDirName);
  const codexPath = path.join(projectPath, '.codex');

  console.log(chalk.blue(`Creating backup: ${backupDirName}`));

  try {
    // Check if .codex directory exists
    if (!await fs.pathExists(codexPath)) {
      throw new Error('No .codex directory found to backup');
    }

    // Create backup by copying entire .codex directory
    await fs.copy(codexPath, backupPath, {
      overwrite: false,
      errorOnExist: true,
      preserveTimestamps: true
    });

    // Create backup manifest with metadata
    const manifest = {
      created_at: new Date().toISOString(),
      version: version,
      source_path: codexPath,
      backup_path: backupPath,
      files_backed_up: await countFiles(backupPath)
    };

    await fs.writeJson(path.join(backupPath, 'backup-manifest.json'), manifest, { spaces: 2 });

    console.log(chalk.green(`✓ Backup created: ${backupDirName}`));
    console.log(chalk.gray(`  Files backed up: ${manifest.files_backed_up}`));

    return backupPath;
  } catch (error) {
    console.error(chalk.red(`✗ Backup failed: ${error.message}`));
    throw error;
  }
}

/**
 * Restore CODEX from a backup
 *
 * @param {string} projectPath - Path to the project root
 * @param {string} backupPath - Path to the backup directory
 * @returns {Promise<boolean>} True if restoration successful
 *
 * @example
 * await restoreBackup('/path/to/project', '/path/to/project/.codex-backup-2024-10-09T12-30-45-v0.1.0');
 */
async function restoreBackup(projectPath, backupPath) {
  const codexPath = path.join(projectPath, '.codex');

  console.log(chalk.blue('Restoring from backup...'));

  try {
    // Validate backup exists and has manifest
    if (!await fs.pathExists(backupPath)) {
      throw new Error(`Backup not found: ${backupPath}`);
    }

    const manifestPath = path.join(backupPath, 'backup-manifest.json');
    if (!await fs.pathExists(manifestPath)) {
      throw new Error('Invalid backup: missing manifest');
    }

    const manifest = await fs.readJson(manifestPath);
    console.log(chalk.gray(`  Backup version: ${manifest.version}`));
    console.log(chalk.gray(`  Created: ${manifest.created_at}`));

    // Remove current .codex directory if it exists
    if (await fs.pathExists(codexPath)) {
      console.log(chalk.yellow('  Removing current .codex directory...'));
      await fs.remove(codexPath);
    }

    // Copy backup to .codex
    console.log(chalk.blue('  Restoring files...'));
    await fs.copy(backupPath, codexPath, {
      overwrite: true,
      preserveTimestamps: true,
      filter: (src) => !src.endsWith('backup-manifest.json') // Don't copy manifest to restored dir
    });

    console.log(chalk.green('✓ Restoration complete'));
    return true;
  } catch (error) {
    console.error(chalk.red(`✗ Restoration failed: ${error.message}`));
    return false;
  }
}

/**
 * Identify files that must be preserved during an update
 *
 * @param {string} projectPath - Path to the project root
 * @param {Object} manifest - Optional manifest with file checksums to detect modifications
 * @returns {Promise<Array<string>>} Array of relative paths to preserve
 *
 * @example
 * const filesToPreserve = await preserveState('/path/to/project', manifest);
 * // Returns: ['.codex/state/workflow.json', '.codex/state/context-checkpoints.json', ...]
 */
async function preserveState(projectPath, manifest = null) {
  const codexPath = path.join(projectPath, '.codex');
  const filesToPreserve = [];

  console.log(chalk.blue('Identifying files to preserve...'));

  try {
    // Always preserve entire state directory
    const statePath = path.join(codexPath, 'state');
    if (await fs.pathExists(statePath)) {
      const stateFiles = await getAllFiles(statePath);
      stateFiles.forEach(file => {
        const relativePath = path.relative(projectPath, file);
        filesToPreserve.push(relativePath);
      });
      console.log(chalk.green(`  ✓ State directory: ${stateFiles.length} files`));
    }

    // Check for modified config files if manifest provided
    if (manifest && manifest.files) {
      const configPath = path.join(codexPath, 'config', 'codex-config.yaml');
      if (await fs.pathExists(configPath)) {
        const isModified = await isFileModified(configPath, manifest);
        if (isModified) {
          const relativePath = path.relative(projectPath, configPath);
          if (!filesToPreserve.includes(relativePath)) {
            filesToPreserve.push(relativePath);
            console.log(chalk.yellow(`  ⚠ Modified config detected: ${relativePath}`));
          }
        }
      }
    }

    // Check for user-created custom files (not in manifest)
    const userFiles = await findUserCreatedFiles(codexPath, manifest);
    userFiles.forEach(file => {
      const relativePath = path.relative(projectPath, file);
      if (!filesToPreserve.includes(relativePath)) {
        filesToPreserve.push(relativePath);
        console.log(chalk.cyan(`  + User file: ${relativePath}`));
      }
    });

    console.log(chalk.green(`\n✓ Total files to preserve: ${filesToPreserve.length}`));
    return filesToPreserve;
  } catch (error) {
    console.error(chalk.red(`✗ Error identifying files to preserve: ${error.message}`));
    throw error;
  }
}

/**
 * Backup user-modified configuration files
 *
 * @param {string} projectPath - Path to the project root
 * @param {Object} manifest - Manifest with file checksums
 * @returns {Promise<string|null>} Path to config backup file, or null if not modified
 *
 * @example
 * const backupPath = await backupModifiedConfig('/path/to/project', manifest);
 * // Returns: '/path/to/project/.codex/config/codex-config.yaml.backup' or null
 */
async function backupModifiedConfig(projectPath, manifest) {
  const configPath = path.join(projectPath, '.codex', 'config', 'codex-config.yaml');

  if (!await fs.pathExists(configPath)) {
    return null;
  }

  try {
    // Check if config is modified
    const isModified = await isFileModified(configPath, manifest);

    if (!isModified) {
      console.log(chalk.gray('  Config file not modified, no backup needed'));
      return null;
    }

    // Create backup with timestamp
    const timestamp = new Date().toISOString().replace(/:/g, '-').split('.')[0];
    const backupPath = `${configPath}.backup-${timestamp}`;

    await fs.copy(configPath, backupPath, {
      overwrite: false,
      preserveTimestamps: true
    });

    console.log(chalk.green(`✓ Config backed up: ${path.basename(backupPath)}`));
    return backupPath;
  } catch (error) {
    console.error(chalk.red(`✗ Config backup failed: ${error.message}`));
    throw error;
  }
}

/**
 * Merge configuration after update with user review
 *
 * @param {string} projectPath - Path to the project root
 * @param {string} backupPath - Path to backed up config file
 * @param {Object} options - Merge options { interactive: boolean, strategy: 'keep'|'merge'|'replace' }
 * @returns {Promise<Object>} Merge result { applied: boolean, strategy: string, changes: Array }
 *
 * @example
 * const result = await mergeConfig(
 *   '/path/to/project',
 *   '/path/to/project/.codex/config/codex-config.yaml.backup',
 *   { interactive: true, strategy: 'merge' }
 * );
 */
async function mergeConfig(projectPath, backupPath, options = {}) {
  const configPath = path.join(projectPath, '.codex', 'config', 'codex-config.yaml');
  const { interactive = true, strategy = 'merge' } = options;

  console.log(chalk.blue('\nConfiguration Merge Required'));
  console.log(chalk.gray('━'.repeat(50)));

  try {
    if (!await fs.pathExists(backupPath)) {
      throw new Error('Backup config file not found');
    }

    if (!await fs.pathExists(configPath)) {
      throw new Error('New config file not found');
    }

    // Read both configs
    const oldConfig = await fs.readFile(backupPath, 'utf8');
    const newConfig = await fs.readFile(configPath, 'utf8');

    // Detect changes
    const changes = detectConfigChanges(oldConfig, newConfig);

    if (changes.length === 0) {
      console.log(chalk.green('✓ No configuration conflicts detected'));
      return { applied: false, strategy: 'no-change', changes: [] };
    }

    // Show diff
    console.log(chalk.yellow(`\nDetected ${changes.length} configuration differences:\n`));
    changes.forEach((change, idx) => {
      console.log(chalk.cyan(`${idx + 1}. ${change.section}`));
      console.log(chalk.red(`   - Old: ${change.oldValue}`));
      console.log(chalk.green(`   + New: ${change.newValue}`));
      console.log();
    });

    // Apply strategy
    let result;
    switch (strategy) {
      case 'keep':
        // Keep user's old config
        await fs.copy(backupPath, configPath, { overwrite: true });
        console.log(chalk.yellow('✓ User configuration preserved (old config kept)'));
        result = { applied: true, strategy: 'keep', changes };
        break;

      case 'replace':
        // Use new config (already in place)
        console.log(chalk.yellow('✓ New configuration applied (user changes discarded)'));
        result = { applied: true, strategy: 'replace', changes };
        break;

      case 'merge':
      default:
        // Manual merge required - preserve backup for user review
        console.log(chalk.yellow('⚠ Manual merge required'));
        console.log(chalk.gray(`  Old config saved: ${path.basename(backupPath)}`));
        console.log(chalk.gray(`  New config active: ${path.basename(configPath)}`));
        console.log(chalk.cyan('\n  Review both files and manually merge if needed.'));
        result = { applied: false, strategy: 'manual', changes };
        break;
    }

    console.log(chalk.gray('━'.repeat(50)));
    return result;
  } catch (error) {
    console.error(chalk.red(`✗ Config merge failed: ${error.message}`));
    throw error;
  }
}

/**
 * List all available backups for a project
 *
 * @param {string} projectPath - Path to the project root
 * @returns {Promise<Array<Object>>} Array of backup metadata objects
 */
async function listBackups(projectPath) {
  try {
    const entries = await fs.readdir(projectPath);
    const backups = [];

    for (const entry of entries) {
      if (entry.startsWith('.codex-backup-')) {
        const backupPath = path.join(projectPath, entry);
        const manifestPath = path.join(backupPath, 'backup-manifest.json');

        if (await fs.pathExists(manifestPath)) {
          const manifest = await fs.readJson(manifestPath);
          const stats = await fs.stat(backupPath);

          backups.push({
            name: entry,
            path: backupPath,
            version: manifest.version,
            created_at: manifest.created_at,
            files_count: manifest.files_backed_up,
            size_bytes: stats.size
          });
        }
      }
    }

    // Sort by creation date, newest first
    backups.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    return backups;
  } catch (error) {
    console.error(chalk.red(`Error listing backups: ${error.message}`));
    return [];
  }
}

/**
 * Clean up old backups, keeping only the most recent N backups
 *
 * @param {string} projectPath - Path to the project root
 * @param {number} keepCount - Number of recent backups to keep (default: 5)
 * @returns {Promise<number>} Number of backups removed
 */
async function cleanupOldBackups(projectPath, keepCount = 5) {
  console.log(chalk.blue(`Cleaning up old backups (keeping ${keepCount} most recent)...`));

  try {
    const backups = await listBackups(projectPath);

    if (backups.length <= keepCount) {
      console.log(chalk.gray(`  No cleanup needed (${backups.length} backups)`));
      return 0;
    }

    const toRemove = backups.slice(keepCount);
    let removedCount = 0;

    for (const backup of toRemove) {
      await fs.remove(backup.path);
      console.log(chalk.gray(`  Removed: ${backup.name}`));
      removedCount++;
    }

    console.log(chalk.green(`✓ Cleaned up ${removedCount} old backup(s)`));
    return removedCount;
  } catch (error) {
    console.error(chalk.red(`✗ Backup cleanup failed: ${error.message}`));
    return 0;
  }
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Count all files in a directory recursively
 */
async function countFiles(dirPath) {
  const files = await getAllFiles(dirPath);
  return files.length;
}

/**
 * Get all files in a directory recursively
 */
async function getAllFiles(dirPath, fileList = []) {
  const entries = await fs.readdir(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      await getAllFiles(fullPath, fileList);
    } else {
      fileList.push(fullPath);
    }
  }

  return fileList;
}

/**
 * Check if a file has been modified compared to manifest
 */
async function isFileModified(filePath, manifest) {
  if (!manifest || !manifest.files) {
    return false; // No manifest, can't determine modification
  }

  const relativePath = path.relative(path.dirname(path.dirname(filePath)), filePath);
  const manifestEntry = manifest.files[relativePath];

  if (!manifestEntry) {
    return true; // File not in manifest = user created
  }

  // Compare checksums
  const currentChecksum = await calculateChecksum(filePath);
  return currentChecksum !== manifestEntry.checksum;
}

/**
 * Calculate SHA256 checksum of a file
 */
async function calculateChecksum(filePath) {
  const content = await fs.readFile(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

/**
 * Find files created by user (not in manifest)
 */
async function findUserCreatedFiles(codexPath, manifest) {
  const userFiles = [];

  if (!manifest || !manifest.files) {
    return userFiles; // No manifest, can't determine user files
  }

  const allFiles = await getAllFiles(codexPath);

  for (const file of allFiles) {
    const relativePath = path.relative(path.dirname(codexPath), file);

    // Skip backup files and state directory (already handled)
    if (file.includes('.backup') || file.includes('/state/')) {
      continue;
    }

    // If file not in manifest, it's user-created
    if (!manifest.files[relativePath]) {
      userFiles.push(file);
    }
  }

  return userFiles;
}

/**
 * Detect changes between old and new config files
 */
function detectConfigChanges(oldConfig, newConfig) {
  const changes = [];

  // Simple line-by-line comparison
  const oldLines = oldConfig.split('\n');
  const newLines = newConfig.split('\n');

  const maxLength = Math.max(oldLines.length, newLines.length);

  for (let i = 0; i < maxLength; i++) {
    const oldLine = oldLines[i] || '';
    const newLine = newLines[i] || '';

    // Skip empty lines and comments
    if (!oldLine.trim() || oldLine.trim().startsWith('#')) continue;
    if (!newLine.trim() || newLine.trim().startsWith('#')) continue;

    if (oldLine !== newLine) {
      // Extract key from YAML line (before :)
      const key = newLine.split(':')[0]?.trim() || `line ${i + 1}`;

      changes.push({
        line: i + 1,
        section: key,
        oldValue: oldLine.trim(),
        newValue: newLine.trim()
      });
    }
  }

  return changes;
}

// ============================================================================
// Exports
// ============================================================================

module.exports = {
  createBackup,
  restoreBackup,
  preserveState,
  backupModifiedConfig,
  mergeConfig,
  listBackups,
  cleanupOldBackups
};
