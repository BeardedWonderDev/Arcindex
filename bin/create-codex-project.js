#!/usr/bin/env node

/**
 * create-codex-project - CLI entry point for CODEX project initialization
 *
 * Orchestrates:
 * - Fresh installations (copy .codex files to new or existing projects)
 * - Updates (upgrade existing CODEX installations)
 * - Version checking (warn about newer versions)
 * - Interactive workflows (prompts for configuration)
 *
 * Usage:
 *   npx create-codex-project [directory] [options]
 *   npx create-codex-project --update
 *   npx create-codex-project --help
 */

import { Command } from 'commander';
import chalk from 'chalk';
import path from 'path';
import fs from 'fs-extra';
import inquirer from 'inquirer';
import ora from 'ora';

// Import lib modules (ES modules)
import { detectExistingInstallation, detectActiveWorkflow, fetchPackageInfo } from '../lib/detector.js';
import { checkCompatibility } from '../lib/compatibility-checker.js';
import { createManifest, readManifest, updateManifest } from '../lib/manifest.js';

// Import lib modules (CommonJS - requires dynamic import or conversion)
// Note: menu.cjs, state-preserver.cjs use CommonJS, need to be imported differently
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const menu = require('../lib/menu.cjs');

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
 * Show success message after installation
 */
function showSuccessMessage(projectPath, workflow, testHarness) {
  console.log();
  console.log(chalk.bold.green('✓ CODEX Installation Complete!'));
  console.log();
  console.log(chalk.cyan('Project:') + chalk.white(` ${projectPath}`));
  console.log(chalk.cyan('Workflow:') + chalk.white(` ${workflow}`));
  console.log(chalk.cyan('Test Harness:') + chalk.white(` ${testHarness ? 'Included' : 'Not included'}`));
  console.log();
  console.log(chalk.bold('Next Steps:'));
  console.log(chalk.gray('  1. ') + chalk.white('cd ' + path.basename(projectPath)));
  console.log(chalk.gray('  2. ') + chalk.white('Review: .codex/README.md'));
  console.log(chalk.gray('  3. ') + chalk.white('Start workflow: /codex run'));
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
 * Validate target directory
 * @param {string} targetPath - Path to validate
 * @returns {Promise<Object>} Validation result
 */
async function validateTarget(targetPath) {
  try {
    const exists = await fs.pathExists(targetPath);

    if (!exists) {
      return {
        valid: true,
        exists: false,
        isEmpty: true,
        message: 'Directory will be created'
      };
    }

    // Check if directory is empty
    const files = await fs.readdir(targetPath);
    const isEmpty = files.length === 0;

    return {
      valid: true,
      exists: true,
      isEmpty: isEmpty,
      message: isEmpty ? 'Directory exists and is empty' : 'Directory exists with files'
    };
  } catch (error) {
    return {
      valid: false,
      exists: false,
      isEmpty: false,
      message: `Cannot access directory: ${error.message}`,
      error: error
    };
  }
}

/**
 * Install CODEX to target directory (fresh installation)
 * @param {string} targetPath - Target project directory
 * @param {Object} options - Installation options
 * @returns {Promise<boolean>} Success status
 */
async function installCodex(targetPath, options = {}) {
  const spinner = ora('Installing CODEX...').start();

  try {
    // Ensure target directory exists
    await fs.ensureDir(targetPath);

    // Determine source .codex directory
    // When running via npx, source is in node_modules/create-codex-project/.codex
    // When running locally, source is in the project root
    const sourceCodexPath = path.join(path.dirname(new URL(import.meta.url).pathname), '..', '.codex');

    // Check if source exists
    if (!await fs.pathExists(sourceCodexPath)) {
      throw new Error(`Source .codex directory not found at ${sourceCodexPath}`);
    }

    // Copy .codex directory
    const targetCodexPath = path.join(targetPath, '.codex');
    spinner.text = 'Copying CODEX files...';
    await fs.copy(sourceCodexPath, targetCodexPath, {
      overwrite: options.force || false,
      errorOnExist: false
    });

    // Copy .claude directory (IDE integration)
    const sourceClaudePath = path.join(path.dirname(new URL(import.meta.url).pathname), '..', '.claude');
    if (await fs.pathExists(sourceClaudePath)) {
      const targetClaudePath = path.join(targetPath, '.claude');
      spinner.text = 'Setting up IDE integration...';
      await fs.copy(sourceClaudePath, targetClaudePath, {
        overwrite: options.force || false,
        errorOnExist: false
      });
    }

    // Create install manifest
    spinner.text = 'Creating installation manifest...';
    await createManifest(targetPath, {
      codex_version: CURRENT_VERSION,
      schema_version: SCHEMA_VERSION,
      default_workflow: options.workflow || 'greenfield-generic',
      test_harness_included: options.testHarness || false,
      ide_setup: ['claude-code']
    });

    spinner.succeed('CODEX installation complete!');
    return true;

  } catch (error) {
    spinner.fail('Installation failed');
    console.error(chalk.red('\nError:'), error.message);
    if (options.verbose) {
      console.error(chalk.gray(error.stack));
    }
    return false;
  }
}

/**
 * Update existing CODEX installation
 * @param {string} projectPath - Project directory with existing CODEX
 * @param {Object} options - Update options
 * @returns {Promise<boolean>} Success status
 */
async function updateCodex(projectPath, options = {}) {
  const spinner = ora('Updating CODEX...').start();

  try {
    // Read existing manifest
    const manifest = await readManifest(projectPath);
    if (!manifest) {
      throw new Error('No existing CODEX installation found');
    }

    const oldVersion = manifest.codex_version;

    // Check compatibility
    spinner.text = 'Checking compatibility...';
    const compat = await checkCompatibility(projectPath, CURRENT_VERSION);

    if (!compat.compatible && compat.action === 'BLOCKED') {
      spinner.fail('Update blocked');
      console.error(chalk.red('\n' + compat.message));
      return false;
    }

    if (compat.requiresConfirmation) {
      spinner.stop();
      const confirmed = await menu.promptUpdateConfirmation(
        compat.currentVersion,
        compat.targetVersion,
        false // Active workflow already checked by compatibility checker
      );
      if (!confirmed) {
        console.log(chalk.yellow('Update cancelled by user'));
        return false;
      }
      spinner.start('Updating CODEX...');
    }

    // Create backup (using state-preserver)
    spinner.text = 'Creating backup...';
    const statePreserver = require('../lib/state-preserver.cjs');
    const backupPath = await statePreserver.createBackup(projectPath, oldVersion);
    console.log(chalk.gray(`  Backup created: ${path.basename(backupPath)}`));

    // Identify files to preserve
    spinner.text = 'Identifying files to preserve...';
    const filesToPreserve = await statePreserver.preserveState(projectPath, manifest);

    // Update .codex files (excluding preserved files)
    spinner.text = 'Updating CODEX files...';
    const sourceCodexPath = path.join(path.dirname(new URL(import.meta.url).pathname), '..', '.codex');
    const targetCodexPath = path.join(projectPath, '.codex');

    // Copy with exclusions for preserved files
    await fs.copy(sourceCodexPath, targetCodexPath, {
      overwrite: true,
      filter: (src, dest) => {
        const relativePath = path.relative(sourceCodexPath, src);
        const targetRelative = path.join('.codex', relativePath);
        return !filesToPreserve.includes(targetRelative);
      }
    });

    // Update manifest
    spinner.text = 'Updating installation manifest...';
    await updateManifest(projectPath, {
      codex_version: CURRENT_VERSION,
      regenerate_files: true,
      change_summary: `Updated from ${oldVersion} to ${CURRENT_VERSION}`
    });

    spinner.succeed('CODEX update complete!');
    console.log();
    console.log(chalk.cyan('Updated from:') + chalk.white(` ${oldVersion}`));
    console.log(chalk.cyan('Updated to:') + chalk.white(` ${CURRENT_VERSION}`));
    console.log();
    console.log(chalk.gray(`Backup available at: ${path.basename(backupPath)}`));
    console.log();

    return true;

  } catch (error) {
    spinner.fail('Update failed');
    console.error(chalk.red('\nError:'), error.message);
    if (options.verbose) {
      console.error(chalk.gray(error.stack));
    }
    return false;
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

    // Run update
    const success = await updateCodex(projectPath, options);
    process.exit(success ? 0 : 1);
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
      const success = await updateCodex(targetPath, options);
      process.exit(success ? 0 : 1);
    }
  }

  // FRESH INSTALLATION
  showWelcomeBanner();

  // Validate target directory
  const validation = await validateTarget(targetPath);
  if (!validation.valid) {
    console.error(chalk.red('✗ Invalid target directory:'), validation.message);
    process.exit(1);
  }

  // Prompt for workflow if not provided
  let workflow = options.workflow;
  if (!workflow) {
    workflow = await menu.promptWorkflowChoice();
  }

  // Prompt for test harness if not provided
  let testHarness = options.testHarness;
  if (testHarness === undefined) {
    testHarness = await menu.promptTestHarness();
  }

  // Confirm installation
  console.log();
  console.log(chalk.bold('Installation Summary:'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log(chalk.cyan('Target:') + '         ' + chalk.white(targetPath));
  console.log(chalk.cyan('Workflow:') + '       ' + chalk.white(workflow));
  console.log(chalk.cyan('Test Harness:') + '   ' + chalk.white(testHarness ? 'Yes' : 'No'));
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

  // Run installation
  const success = await installCodex(targetPath, {
    workflow,
    testHarness,
    force: options.force,
    verbose: options.verbose
  });

  if (success) {
    showSuccessMessage(targetPath, workflow, testHarness);
    process.exit(0);
  } else {
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
