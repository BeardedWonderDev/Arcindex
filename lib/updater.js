/**
 * CODEX Updater - Handles updating existing CODEX installations
 *
 * Provides comprehensive update logic with:
 * - Schema version compatibility checking
 * - Active workflow detection and blocking
 * - State preservation and backup
 * - Rollback on failure
 * - Configuration merge support
 */

import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import ora from 'ora';
import semver from 'semver';

// Import required modules
import { detectExistingInstallation, detectActiveWorkflow, fetchPackageInfo } from './detector.js';
import { checkCompatibility } from './compatibility-checker.js';
import {
  createBackup,
  preserveState,
  backupModifiedConfig,
  mergeConfig,
  cleanupOldBackups
} from './state-preserver.cjs';
import { copyDirectory, removeDirectory } from './file-manager.cjs';
import { readManifest, updateManifest } from './manifest.js';
import {
  promptUpdateConfirmation,
  promptForceSchemaOverride
} from './menu.cjs';

// Get __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Main update function - Orchestrates the entire update process
 *
 * @param {string} projectPath - Path to the project with existing CODEX installation
 * @param {string} targetVersion - Version to update to ('latest' or specific version like '0.1.1')
 * @param {Object} options - Update options
 * @param {boolean} [options.forceSchema=false] - Force schema override (dangerous)
 * @param {boolean} [options.noBackup=false] - Skip backup creation (not recommended)
 * @param {boolean} [options.verbose=false] - Verbose output
 * @param {boolean} [options.skipConfirmation=false] - Skip update confirmation prompt
 * @returns {Promise<Object>} Update result
 */
export async function updateCodex(projectPath, targetVersion = 'latest', options = {}) {
  const {
    forceSchema = false,
    noBackup = false,
    verbose = false,
    skipConfirmation = false
  } = options;

  const spinner = ora();
  let backupPath = null;
  let updateSuccess = false;

  try {
    // Step 1: Detect existing installation
    spinner.start('Detecting existing CODEX installation...');
    const installation = await detectExistingInstallation(projectPath);

    if (!installation.exists) {
      spinner.fail('No existing CODEX installation found');
      return {
        success: false,
        message: 'No CODEX installation detected. Use install command instead.',
        backupPath: null
      };
    }

    spinner.succeed(`Found CODEX v${installation.version} (schema v${installation.schemaVersion})`);

    // Step 2: Check compatibility (including schema version check)
    spinner.start('Checking compatibility...');
    const compatibility = await checkCompatibility(projectPath, targetVersion);

    if (verbose) {
      spinner.info(compatibility.message);
    }

    // Step 3: Handle active workflow blocking
    if (compatibility.reason === 'workflow-in-progress') {
      spinner.fail('Cannot update: Active workflow in progress');
      console.log(chalk.yellow('\nActive workflow detected:'));
      console.log(chalk.gray(`  Phase: ${compatibility.workflowDetails.phase}`));
      console.log(chalk.gray(`  Type: ${compatibility.workflowDetails.type}`));
      console.log(chalk.cyan('\nPlease complete or cancel the current workflow before updating.'));
      return {
        success: false,
        message: compatibility.message,
        backupPath: null,
        reason: 'workflow-in-progress'
      };
    }

    // Step 4: Handle schema version mismatch
    if (compatibility.reason === 'schema-mismatch') {
      spinner.warn('Schema version mismatch detected');

      const schemaResult = await handleSchemaVersionMismatch(
        compatibility.currentVersion,
        compatibility.targetVersion,
        compatibility.currentSchema,
        compatibility.targetSchema,
        forceSchema
      );

      if (!schemaResult.canProceed) {
        return {
          success: false,
          message: compatibility.message,
          backupPath: null,
          reason: 'schema-mismatch',
          schemaChange: compatibility.schemaChange
        };
      }

      if (!schemaResult.userConfirmed) {
        return {
          success: false,
          message: 'Update cancelled by user',
          backupPath: null,
          reason: 'user-cancelled'
        };
      }
    }

    spinner.succeed('Compatibility check passed');

    // Step 5: Prompt for confirmation
    if (!skipConfirmation && compatibility.requiresConfirmation) {
      const workflow = await detectActiveWorkflow(projectPath);
      const confirmed = await promptUpdateConfirmation(
        compatibility.currentVersion,
        compatibility.targetVersion,
        workflow.active
      );

      if (!confirmed) {
        return {
          success: false,
          message: 'Update cancelled by user',
          backupPath: null,
          reason: 'user-cancelled'
        };
      }
    }

    // Step 6: Create backup
    if (!noBackup) {
      spinner.start('Creating backup...');
      try {
        backupPath = await createBackup(projectPath, installation.version);
        spinner.succeed(`Backup created: ${path.basename(backupPath)}`);
      } catch (error) {
        spinner.fail('Backup creation failed');
        console.error(chalk.red(`Error: ${error.message}`));
        console.log(chalk.yellow('\nCannot proceed without backup. Use --no-backup to override (not recommended).'));
        return {
          success: false,
          message: `Backup failed: ${error.message}`,
          backupPath: null,
          reason: 'backup-failed'
        };
      }
    } else {
      console.log(chalk.yellow('⚠ Skipping backup (--no-backup flag set)'));
    }

    // Step 7: Identify files to preserve
    spinner.start('Identifying files to preserve...');
    const manifest = readManifest(projectPath);
    const filesToPreserve = await preserveState(projectPath, manifest);
    spinner.succeed(`Identified ${filesToPreserve.length} files to preserve`);

    // Step 8: Backup modified config if exists
    let configBackupPath = null;
    if (manifest) {
      spinner.start('Checking for modified configuration...');
      configBackupPath = await backupModifiedConfig(projectPath, manifest);
      if (configBackupPath) {
        spinner.succeed('Modified configuration backed up');
      } else {
        spinner.succeed('No modified configuration detected');
      }
    }

    // Step 9: Fetch target version package info
    spinner.start(`Fetching ${targetVersion} package info...`);
    let targetPackageInfo;
    try {
      targetPackageInfo = await fetchPackageInfo('create-codex-project', targetVersion);
      spinner.succeed(`Target version: ${targetPackageInfo.version}`);
    } catch (error) {
      spinner.fail('Failed to fetch target version');
      return {
        success: false,
        message: `Failed to fetch package info: ${error.message}`,
        backupPath: backupPath,
        reason: 'fetch-failed'
      };
    }

    // Step 10: Update CODEX files
    spinner.start('Updating CODEX files...');
    try {
      await updateFiles(projectPath, filesToPreserve, { verbose });
      spinner.succeed('CODEX files updated');
      updateSuccess = true;
    } catch (error) {
      spinner.fail('File update failed');
      console.error(chalk.red(`Error: ${error.message}`));

      // Attempt rollback if backup exists
      if (backupPath) {
        console.log(chalk.yellow('\nAttempting to rollback from backup...'));
        const { restoreBackup } = await import('./state-preserver.cjs');
        const restored = await restoreBackup(projectPath, backupPath);
        if (restored) {
          console.log(chalk.green('✓ Successfully rolled back to previous version'));
        } else {
          console.log(chalk.red('✗ Rollback failed. Backup preserved at: ' + backupPath));
        }
      }

      return {
        success: false,
        message: `Update failed: ${error.message}`,
        backupPath: backupPath,
        reason: 'update-failed'
      };
    }

    // Step 11: Merge config if modified
    if (configBackupPath) {
      spinner.start('Merging configuration...');
      const mergeResult = await mergeConfig(projectPath, configBackupPath, {
        interactive: false,
        strategy: 'manual'
      });

      if (mergeResult.applied) {
        spinner.succeed('Configuration merged');
      } else {
        spinner.warn('Manual configuration merge required');
        console.log(chalk.cyan('\nReview both configuration files and merge manually if needed:'));
        console.log(chalk.gray(`  Old: ${path.basename(configBackupPath)}`));
        console.log(chalk.gray(`  New: codex-config.yaml`));
      }
    }

    // Step 12: Update manifest
    spinner.start('Updating installation manifest...');
    try {
      await updateManifest(projectPath, {
        codex_version: targetPackageInfo.version,
        regenerate_files: true,
        change_summary: `Updated from ${installation.version} to ${targetPackageInfo.version}`
      });
      spinner.succeed('Installation manifest updated');
    } catch (error) {
      spinner.warn('Manifest update failed (non-critical)');
      if (verbose) {
        console.log(chalk.gray(`  ${error.message}`));
      }
    }

    // Step 13: Cleanup old backups
    if (!noBackup) {
      spinner.start('Cleaning up old backups...');
      const removed = await cleanupOldBackups(projectPath, 5);
      if (removed > 0) {
        spinner.succeed(`Cleaned up ${removed} old backup(s)`);
      } else {
        spinner.succeed('No old backups to clean up');
      }
    }

    // Success!
    console.log(chalk.green.bold('\n✓ Update completed successfully!'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log(chalk.cyan('Previous version:') + ' ' + chalk.white(installation.version));
    console.log(chalk.cyan('New version:')      + '     ' + chalk.white(targetPackageInfo.version));
    if (backupPath) {
      console.log(chalk.cyan('Backup location:')  + ' ' + chalk.gray(path.basename(backupPath)));
    }
    console.log(chalk.gray('─'.repeat(50)));

    return {
      success: true,
      message: `Successfully updated from ${installation.version} to ${targetPackageInfo.version}`,
      backupPath: backupPath,
      previousVersion: installation.version,
      newVersion: targetPackageInfo.version
    };

  } catch (error) {
    if (spinner.isSpinning) {
      spinner.fail('Update failed');
    }

    console.error(chalk.red('\nUnexpected error during update:'));
    console.error(chalk.red(error.message));

    if (verbose && error.stack) {
      console.error(chalk.gray('\nStack trace:'));
      console.error(chalk.gray(error.stack));
    }

    // Attempt rollback if we started updating
    if (updateSuccess === false && backupPath) {
      console.log(chalk.yellow('\nAttempting to rollback from backup...'));
      const { restoreBackup } = await import('./state-preserver.cjs');
      const restored = await restoreBackup(projectPath, backupPath);
      if (restored) {
        console.log(chalk.green('✓ Successfully rolled back to previous version'));
      } else {
        console.log(chalk.red('✗ Rollback failed. Backup preserved at: ' + backupPath));
      }
    }

    return {
      success: false,
      message: `Update failed: ${error.message}`,
      backupPath: backupPath,
      reason: 'unexpected-error',
      error: error.message
    };
  }
}

/**
 * Check npm registry for available updates
 *
 * @param {string} currentVersion - Currently installed version
 * @returns {Promise<Object>} Update availability result
 */
export async function checkForUpdates(currentVersion) {
  try {
    // Fetch latest package info from npm
    const latestPackageInfo = await fetchPackageInfo('create-codex-project', 'latest');
    const latestVersion = latestPackageInfo.version;

    // Validate versions
    if (!semver.valid(currentVersion)) {
      return {
        updateAvailable: false,
        latestVersion: latestVersion,
        currentVersion: currentVersion,
        error: 'Invalid current version format'
      };
    }

    if (!semver.valid(latestVersion)) {
      return {
        updateAvailable: false,
        latestVersion: latestVersion,
        currentVersion: currentVersion,
        error: 'Invalid latest version format'
      };
    }

    // Compare versions
    const updateAvailable = semver.gt(latestVersion, currentVersion);

    return {
      updateAvailable,
      latestVersion,
      currentVersion,
      releaseType: updateAvailable ? semver.diff(currentVersion, latestVersion) : null
    };

  } catch (error) {
    return {
      updateAvailable: false,
      latestVersion: null,
      currentVersion: currentVersion,
      error: error.message
    };
  }
}

/**
 * Handle schema version mismatch - block or prompt for dangerous override
 *
 * @param {string} currentVersion - Current CODEX version
 * @param {string} targetVersion - Target CODEX version
 * @param {number} currentSchema - Current schema version
 * @param {number} targetSchema - Target schema version
 * @param {boolean} forceSchema - Whether --force-schema flag is set
 * @returns {Promise<Object>} Result with canProceed and userConfirmed flags
 */
async function handleSchemaVersionMismatch(
  currentVersion,
  targetVersion,
  currentSchema,
  targetSchema,
  forceSchema
) {
  // If not forcing, block with migration guide
  if (!forceSchema) {
    console.log(chalk.red.bold('\n✗ Incompatible Schema Version'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log(chalk.red('This update includes breaking changes to the schema version.'));
    console.log('');
    console.log(chalk.cyan('Current schema:') + ' ' + chalk.white(`v${currentSchema}`));
    console.log(chalk.cyan('Target schema:')  + '  ' + chalk.white(`v${targetSchema}`));
    console.log('');
    console.log(chalk.yellow('To proceed with this update:'));
    console.log(chalk.gray('  1. Review the migration guide: https://github.com/BeardedWonder/CODEX/blob/main/MIGRATION.md'));
    console.log(chalk.gray('  2. Back up your current .codex directory'));
    console.log(chalk.gray('  3. Complete or checkpoint any active workflows'));
    console.log(chalk.gray('  4. Use --force-schema flag to override this check'));
    console.log('');
    console.log(chalk.red.bold('WARNING: Forcing schema upgrade may cause data loss or corruption!'));
    console.log(chalk.gray('─'.repeat(50)));

    return {
      canProceed: false,
      userConfirmed: false
    };
  }

  // If forcing, prompt for dangerous confirmation
  const userConfirmed = await promptForceSchemaOverride(
    currentVersion,
    targetVersion,
    currentSchema,
    targetSchema
  );

  if (!userConfirmed) {
    console.log(chalk.yellow('\n✓ Schema override cancelled. Your installation is safe.'));
    return {
      canProceed: false,
      userConfirmed: false
    };
  }

  console.log(chalk.yellow('\n⚠ Proceeding with forced schema override...'));
  return {
    canProceed: true,
    userConfirmed: true
  };
}

/**
 * Update CODEX files while preserving specified files
 *
 * @param {string} projectPath - Path to the project
 * @param {string[]} filesToPreserve - Array of relative file paths to preserve
 * @param {Object} options - Update options
 * @param {boolean} [options.verbose=false] - Verbose output
 * @returns {Promise<void>}
 * @throws {Error} If update fails
 */
async function updateFiles(projectPath, filesToPreserve, options = {}) {
  const { verbose = false } = options;

  try {
    // Get source directory (the template .codex directory in this package)
    // When installed via npm, files are in node_modules/create-codex-project/
    const sourceCodexPath = path.join(__dirname, '..', '.codex');
    const targetCodexPath = path.join(projectPath, '.codex');

    // Verify source exists
    if (!await fs.pathExists(sourceCodexPath)) {
      throw new Error(`Source .codex directory not found at ${sourceCodexPath}`);
    }

    // Create temp directory for preserved files
    const tempDir = path.join(projectPath, '.codex-temp-preserve');
    await fs.ensureDir(tempDir);

    // Step 1: Copy preserved files to temp location
    if (verbose) {
      console.log(chalk.gray(`\n  Preserving ${filesToPreserve.length} files...`));
    }

    for (const relPath of filesToPreserve) {
      const sourcePath = path.join(projectPath, relPath);
      const tempPath = path.join(tempDir, relPath);

      if (await fs.pathExists(sourcePath)) {
        await fs.ensureDir(path.dirname(tempPath));
        await fs.copy(sourcePath, tempPath, { overwrite: true });
        if (verbose) {
          console.log(chalk.gray(`    ✓ ${relPath}`));
        }
      }
    }

    // Step 2: Remove old .codex directory
    if (verbose) {
      console.log(chalk.gray('\n  Removing old .codex directory...'));
    }
    await removeDirectory(targetCodexPath);

    // Step 3: Copy new .codex directory
    if (verbose) {
      console.log(chalk.gray('  Copying new .codex directory...'));
    }
    await copyDirectory(sourceCodexPath, targetCodexPath);

    // Step 4: Restore preserved files
    if (verbose) {
      console.log(chalk.gray(`\n  Restoring ${filesToPreserve.length} preserved files...`));
    }

    for (const relPath of filesToPreserve) {
      const tempPath = path.join(tempDir, relPath);
      const targetPath = path.join(projectPath, relPath);

      if (await fs.pathExists(tempPath)) {
        await fs.ensureDir(path.dirname(targetPath));
        await fs.copy(tempPath, targetPath, { overwrite: true });
        if (verbose) {
          console.log(chalk.gray(`    ✓ ${relPath}`));
        }
      }
    }

    // Step 5: Update .claude/commands/codex.md
    const sourceClaudeCommand = path.join(__dirname, '..', '.claude', 'commands', 'codex.md');
    const targetClaudeCommand = path.join(projectPath, '.claude', 'commands', 'codex.md');

    if (await fs.pathExists(sourceClaudeCommand)) {
      await fs.ensureDir(path.dirname(targetClaudeCommand));
      await fs.copy(sourceClaudeCommand, targetClaudeCommand, { overwrite: true });
      if (verbose) {
        console.log(chalk.gray('  ✓ Updated .claude/commands/codex.md'));
      }
    }

    // Step 6: Cleanup temp directory
    await removeDirectory(tempDir);

    if (verbose) {
      console.log(chalk.gray('\n  File update complete'));
    }

  } catch (error) {
    // Cleanup temp directory on error
    const tempDir = path.join(projectPath, '.codex-temp-preserve');
    if (await fs.pathExists(tempDir)) {
      await removeDirectory(tempDir).catch(() => {
        // Ignore cleanup errors
      });
    }

    throw new Error(`Failed to update files: ${error.message}`);
  }
}

/**
 * Get disk space available at given path (basic check)
 *
 * @param {string} dirPath - Path to check
 * @returns {Promise<Object>} Disk space info
 */
async function checkDiskSpace(dirPath) {
  try {
    // Simple check: try to get stats on the directory
    const stats = await fs.stat(dirPath);

    // For more robust disk space checking, you'd use a library like 'check-disk-space'
    // For now, we'll just verify the path is accessible
    return {
      available: true,
      accessible: true
    };
  } catch (error) {
    return {
      available: false,
      accessible: false,
      error: error.message
    };
  }
}

// Export all functions
export default {
  updateCodex,
  checkForUpdates,
  checkDiskSpace
};
