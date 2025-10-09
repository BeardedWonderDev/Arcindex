#!/usr/bin/env node

/**
 * create-codex-project - CLI entry point for CODEX project initialization
 *
 * This is a thin wrapper around lib/installer.js and lib/updater.js
 * Handles: CLI argument parsing, user prompts, banners, error handling
 */

import { Command } from 'commander';
import chalk from 'chalk';
import path from 'path';
import fs from 'fs-extra';
import inquirer from 'inquirer';

// Import lib modules
import { detectExistingInstallation, fetchPackageInfo } from '../lib/detector.js';
import * as menu from '../lib/menu.js';
import { installCodex, showSuccessMessage } from '../lib/installer.js';
import { updateCodex, checkForUpdates } from '../lib/updater.js';

// Read package.json for version
const packageJson = JSON.parse(
  fs.readFileSync(new URL('../package.json', import.meta.url), 'utf8')
);

const CURRENT_VERSION = packageJson.version;
const SCHEMA_VERSION = packageJson.codex?.schemaVersion || 1;

/**
 * Show welcome banner
 */
function showWelcomeBanner() {
  console.log();
  console.log(chalk.bold.cyan('╔══════════════════════════════════════════════════════════════╗'));
  console.log(chalk.bold.cyan('║') + chalk.bold.white('                    CODEX Installer                       ') + chalk.bold.cyan('║'));
  console.log(chalk.bold.cyan('╚══════════════════════════════════════════════════════════════╝'));
  console.log();
  console.log(chalk.gray('  AI Agent Workflow Orchestration System'));
  console.log(chalk.gray(`  Version: ${CURRENT_VERSION}`));
  console.log();
}

/**
 * Check for newer version on npm registry (with timeout)
 * @param {number} timeout - Timeout in milliseconds (default: 3000)
 * @returns {Promise<Object|null>} Latest version info or null if check fails/times out
 */
async function checkForNewerVersion(timeout = 3000) {
  try {
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Timeout')), timeout)
    );

    const fetchPromise = fetchPackageInfo('create-codex-project', 'latest');

    const latestInfo = await Promise.race([fetchPromise, timeoutPromise]);

    return latestInfo;
  } catch (error) {
    // Silently fail - don't block installation if check fails
    return null;
  }
}

/**
 * Show version warning if running outdated version
 */
async function showVersionWarning() {
  const latestInfo = await checkForNewerVersion(3000);

  if (!latestInfo) {
    return; // Skip if check failed or timed out
  }

  const latestVersion = latestInfo.version;

  // Use semver comparison
  const semver = (await import('semver')).default;

  if (semver.gt(latestVersion, CURRENT_VERSION)) {
    console.log();
    console.log(chalk.yellow('⚠️  Newer version available!'));
    console.log(chalk.gray(`   Current: ${CURRENT_VERSION}`));
    console.log(chalk.gray(`   Latest:  ${latestVersion}`));
    console.log();
    console.log(chalk.cyan('   Update with: ') + chalk.white('npx create-codex-project@latest'));
    console.log();
  }
}

/**
 * Main CLI program
 */
async function main() {
  const program = new Command();

  program
    .name('create-codex-project')
    .description('Create or update a CODEX-enabled project')
    .version(CURRENT_VERSION, '-V, --version', 'Output the current version')
    .argument('[directory]', 'Target directory for CODEX installation')
    .option('--workflow <type>', 'Default workflow (greenfield-generic, greenfield-swift, brownfield-enhancement)')
    .option('--test-harness', 'Include test harness for development/validation')
    .option('--update', 'Update existing CODEX installation in current directory')
    .option('--force', 'Force installation even if directory exists')
    .option('--force-schema', 'Force schema upgrade (dangerous - may break existing workflows)')
    .option('--no-backup', 'Skip backup during updates (not recommended)')
    .option('--verbose', 'Show verbose output including stack traces')
    .helpOption('-h, --help', 'Display help for command')
    .parse(process.argv);

  const options = program.opts();
  const args = program.args;

  // Show version warning (non-blocking)
  await showVersionWarning();

  // UPDATE MODE: --update flag
  if (options.update) {
    const projectPath = process.cwd();

    console.log(chalk.bold('Update Mode'));
    console.log(chalk.gray('Target: ') + chalk.white(projectPath));
    console.log();

    // Detect existing installation
    const installation = await detectExistingInstallation(projectPath);

    if (!installation.exists) {
      console.error(chalk.red('✗ No CODEX installation found in current directory'));
      console.log(chalk.gray('  Use: ') + chalk.white('npx create-codex-project [directory]') + chalk.gray(' to install'));
      process.exit(1);
    }

    // Call lib/updater.js
    const result = await updateCodex(projectPath, 'latest', {
      forceSchema: options.forceSchema || false,
      noBackup: options.noBackup === false, // Commander negates no-backup
      verbose: options.verbose || false,
      skipConfirmation: false
    });

    if (result.success) {
      console.log(chalk.green('\n✓ Update completed successfully!'));
      process.exit(0);
    } else {
      console.error(chalk.red('\n✗ Update failed:'), result.message);
      process.exit(1);
    }
  }

  // INSTALLATION MODE: Fresh install or existing directory
  let targetPath;

  if (args.length > 0) {
    targetPath = path.resolve(process.cwd(), args[0]);
  } else {
    // Prompt for directory
    const { directory } = await inquirer.prompt([
      {
        type: 'input',
        name: 'directory',
        message: 'Project directory:',
        default: '.',
        validate: (input) => {
          if (!input || input.trim() === '') {
            return 'Directory is required';
          }
          return true;
        }
      }
    ]);
    targetPath = path.resolve(process.cwd(), directory);
  }

  // Check if CODEX already exists in target
  const installation = await detectExistingInstallation(targetPath);

  if (installation.exists) {
    // Existing installation detected - offer update
    console.log(chalk.yellow('\n⚠️  CODEX is already installed in this directory'));
    console.log(chalk.gray('  Version: ') + chalk.white(installation.version));
    console.log();

    const { action } = await inquirer.prompt([
      {
        type: 'list',
        name: 'action',
        message: 'What would you like to do?',
        choices: [
          {
            name: `Update to ${CURRENT_VERSION}`,
            value: 'update'
          },
          {
            name: 'Cancel',
            value: 'cancel'
          }
        ]
      }
    ]);

    if (action === 'cancel') {
      console.log(chalk.gray('Installation cancelled'));
      process.exit(0);
    }

    if (action === 'update') {
      // Call lib/updater.js
      const result = await updateCodex(targetPath, 'latest', {
        forceSchema: options.forceSchema || false,
        noBackup: options.noBackup === false,
        verbose: options.verbose || false,
        skipConfirmation: false
      });

      if (result.success) {
        console.log(chalk.green('\n✓ Update completed successfully!'));
        process.exit(0);
      } else {
        console.error(chalk.red('\n✗ Update failed:'), result.message);
        process.exit(1);
      }
    }
  }

  // FRESH INSTALLATION
  showWelcomeBanner();

  // Prompt for workflow if not provided
  let workflow = options.workflow;
  if (!workflow) {
    workflow = await menu.promptWorkflowChoice();
  }

  // Prompt for test harness if not provided
  let includeTestHarness = options.testHarness;
  if (includeTestHarness === undefined) {
    includeTestHarness = await menu.promptTestHarness();
  }

  // Confirm installation
  console.log();
  console.log(chalk.bold('Installation Summary:'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log(chalk.cyan('Target:') + '         ' + chalk.white(targetPath));
  console.log(chalk.cyan('Workflow:') + '       ' + chalk.white(workflow));
  console.log(chalk.cyan('Test Harness:') + '   ' + chalk.white(includeTestHarness ? 'Yes' : 'No'));
  console.log(chalk.cyan('CODEX Version:') + '  ' + chalk.white(CURRENT_VERSION));
  console.log(chalk.gray('─'.repeat(50)));
  console.log();

  const { confirmed } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'confirmed',
      message: 'Proceed with installation?',
      default: true
    }
  ]);

  if (!confirmed) {
    console.log(chalk.gray('Installation cancelled'));
    process.exit(0);
  }

  // Call lib/installer.js
  const result = await installCodex(targetPath, {
    workflow,
    includeTestHarness,
    verbose: options.verbose || false
  });

  if (result.success) {
    showSuccessMessage(targetPath, workflow, includeTestHarness);
    process.exit(0);
  } else {
    console.error(chalk.red('\n✗ Installation failed:'), result.message);
    process.exit(1);
  }
}

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log(chalk.yellow('\n\nInstallation cancelled by user'));
  process.exit(130);
});

// Handle uncaught errors
process.on('unhandledRejection', (error) => {
  console.error(chalk.red('\nUnexpected error:'), error.message);
  console.error(chalk.gray('Please report this issue at: https://github.com/BeardedWonder/CODEX/issues'));
  process.exit(1);
});

// Run main program
main().catch((error) => {
  console.error(chalk.red('\nFatal error:'), error.message);
  process.exit(1);
});
