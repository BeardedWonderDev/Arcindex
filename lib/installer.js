/**
 * CODEX Installer - Core installation logic
 *
 * Handles the complete installation workflow:
 * - Directory validation and preparation
 * - Copying .codex and .claude files from package
 * - Test harness exclusion
 * - Manifest creation
 * - User feedback and next steps
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs-extra';
import { createManifest } from './manifest.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Get the path to the installer package root
 * Works for both development (npm link) and installed package
 *
 * @returns {string} Absolute path to package root containing .codex/ and .claude/
 */
export function getInstallerPackagePath() {
  // lib/installer.js -> package root
  const packageRoot = join(__dirname, '..');

  // Validate that required directories exist
  const codexPath = join(packageRoot, '.codex');
  const claudePath = join(packageRoot, '.claude');

  if (!fs.existsSync(codexPath)) {
    throw new Error(`Package .codex directory not found at ${codexPath}`);
  }

  if (!fs.existsSync(claudePath)) {
    throw new Error(`Package .claude directory not found at ${claudePath}`);
  }

  return packageRoot;
}

/**
 * Validate target directory for CODEX installation
 *
 * @param {string} targetPath - Directory to validate
 * @returns {Promise<{valid: boolean, reason?: string}>} Validation result
 */
export async function validateTarget(targetPath) {
  try {
    // Check if target path exists
    const targetExists = await fs.pathExists(targetPath);

    if (!targetExists) {
      return { valid: false, reason: 'Target directory does not exist' };
    }

    // Check if it's a directory
    const stats = await fs.stat(targetPath);
    if (!stats.isDirectory()) {
      return { valid: false, reason: 'Target path is not a directory' };
    }

    // Check write permissions by attempting to create a test file
    try {
      const testFile = join(targetPath, '.codex-install-test');
      await fs.writeFile(testFile, 'test');
      await fs.remove(testFile);
    } catch (error) {
      return { valid: false, reason: 'No write permission for target directory' };
    }

    // Check available disk space (need at least 50MB = 52428800 bytes)
    try {
      const stat = await fs.statfs(targetPath);
      const availableSpace = stat.bavail * stat.bsize;
      const requiredSpace = 52428800; // 50MB

      if (availableSpace < requiredSpace) {
        return {
          valid: false,
          reason: `Insufficient disk space (need 50MB, have ${Math.round(availableSpace / 1024 / 1024)}MB)`
        };
      }
    } catch (error) {
      // If we can't check disk space, proceed with warning
      console.log(chalk.yellow('⚠ Could not verify disk space, proceeding anyway'));
    }

    // Check if .codex already exists
    const codexPath = join(targetPath, '.codex');
    if (await fs.pathExists(codexPath)) {
      return {
        valid: false,
        reason: 'CODEX already installed (.codex directory exists). Use update command instead.'
      };
    }

    return { valid: true };
  } catch (error) {
    return { valid: false, reason: `Validation error: ${error.message}` };
  }
}

/**
 * Display welcome banner for CODEX installation
 *
 * @param {string} version - CODEX version being installed
 */
export function showWelcomeBanner(version) {
  console.log();
  console.log(chalk.cyan.bold('╔════════════════════════════════════════════════════════╗'));
  console.log(chalk.cyan.bold('║') + chalk.white.bold('          CODEX Installation') + '                        ' + chalk.cyan.bold('║'));
  console.log(chalk.cyan.bold('║') + chalk.gray('          AI Agent Workflow Orchestration               ') + chalk.cyan.bold('║'));
  console.log(chalk.cyan.bold('╚════════════════════════════════════════════════════════╝'));
  console.log();
  console.log(chalk.gray('  Version: ') + chalk.white(version));
  console.log(chalk.gray('  License: ') + chalk.white('MIT'));
  console.log();
}

/**
 * Display success message with next steps
 *
 * @param {string} targetPath - Installation directory path
 * @param {string} workflow - Selected workflow name
 */
export function showSuccessMessage(targetPath, workflow) {
  console.log();
  console.log(chalk.green.bold('✓ CODEX Installation Complete!'));
  console.log();
  console.log(chalk.white.bold('Next Steps:'));
  console.log();
  console.log(chalk.cyan('1. ') + chalk.white('Navigate to your project:'));
  console.log(chalk.gray('   $ ') + chalk.white(`cd ${targetPath}`));
  console.log();
  console.log(chalk.cyan('2. ') + chalk.white('Start CODEX in your IDE (Claude Code):'));
  console.log(chalk.gray('   ') + chalk.white('/codex start'));
  console.log();
  console.log(chalk.cyan('3. ') + chalk.white(`Review workflow configuration:`));
  console.log(chalk.gray('   ') + chalk.white(`.codex/workflows/${workflow}.yaml`));
  console.log();
  console.log(chalk.white.bold('Documentation:'));
  console.log(chalk.gray('  • User Guide:     ') + chalk.cyan('CODEX-User-Guide.md'));
  console.log(chalk.gray('  • Workflow Guide: ') + chalk.cyan('CODEX-Workflow-Guide.md'));
  console.log(chalk.gray('  • Contributing:   ') + chalk.cyan('CONTRIBUTING.md'));
  console.log();
  console.log(chalk.white.bold('Pro Tips:'));
  console.log(chalk.gray('  • Use ') + chalk.cyan('/codex status') + chalk.gray(' to check workflow progress'));
  console.log(chalk.gray('  • Use ') + chalk.cyan('/codex help') + chalk.gray(' for available commands'));
  console.log(chalk.gray('  • Review ') + chalk.cyan('.codex/config/codex-config.yaml') + chalk.gray(' for customization'));
  console.log();
  console.log(chalk.green('Happy coding! 🚀'));
  console.log();
}

/**
 * Main installation function - orchestrates the complete installation
 *
 * @param {string} targetPath - Directory to install CODEX
 * @param {Object} options - Installation options
 * @param {string} options.workflow - Selected workflow (e.g., 'greenfield-generic')
 * @param {boolean} options.includeTestHarness - Whether to include test harness
 * @param {boolean} options.verbose - Enable verbose logging
 * @returns {Promise<{success: boolean, message: string}>} Installation result
 */
export async function installCodex(targetPath, options = {}) {
  const {
    workflow = 'greenfield-generic',
    includeTestHarness = false,
    verbose = false
  } = options;

  let spinner;

  try {
    // Validate target directory
    if (verbose) console.log(chalk.gray('Validating target directory...'));
    const validation = await validateTarget(targetPath);

    if (!validation.valid) {
      return {
        success: false,
        message: `Installation failed: ${validation.reason}`
      };
    }

    // Get installer package path
    const packageRoot = getInstallerPackagePath();
    if (verbose) console.log(chalk.gray(`Package root: ${packageRoot}`));

    // Ensure target directory exists
    spinner = ora('Preparing target directory...').start();
    await fs.ensureDir(targetPath);
    spinner.succeed('Target directory ready');

    // Copy .codex directory
    spinner = ora('Installing CODEX core files...').start();
    const codexSource = join(packageRoot, '.codex');
    const codexTarget = join(targetPath, '.codex');

    const excludePatterns = [];

    // Exclude test harness if not requested
    if (!includeTestHarness) {
      excludePatterns.push('test-harness/**');
      excludePatterns.push('test-harness');
    }

    // Copy with exclusions
    await fs.copy(codexSource, codexTarget, {
      overwrite: true,
      errorOnExist: false,
      filter: (src) => {
        // Get relative path from source
        const relativePath = src.replace(codexSource, '').replace(/^[\/\\]/, '');

        // Check against exclude patterns
        for (const pattern of excludePatterns) {
          if (relativePath.startsWith(pattern.replace('/**', ''))) {
            if (verbose) console.log(chalk.gray(`  Excluding: ${relativePath}`));
            return false;
          }
        }

        return true;
      }
    });

    spinner.succeed('CODEX core files installed');

    // Copy .claude/commands/codex.md
    spinner = ora('Installing Claude Code integration...').start();
    const claudeCommandSource = join(packageRoot, '.claude', 'commands', 'codex.md');
    const claudeCommandTarget = join(targetPath, '.claude', 'commands', 'codex.md');

    // Ensure .claude/commands directory exists
    await fs.ensureDir(join(targetPath, '.claude', 'commands'));

    // Copy codex.md
    await fs.copy(claudeCommandSource, claudeCommandTarget, {
      overwrite: false,
      errorOnExist: false
    });

    spinner.succeed('Claude Code integration installed');

    // Create installation manifest
    spinner = ora('Creating installation manifest...').start();

    // Get package version
    const packageJsonPath = join(packageRoot, 'package.json');
    const packageJson = await fs.readJson(packageJsonPath);
    const version = packageJson.version;

    await createManifest(targetPath, {
      codex_version: version,
      schema_version: 1,
      default_workflow: workflow,
      test_harness_included: includeTestHarness,
      ide_setup: ['claude-code']
    });

    spinner.succeed('Installation manifest created');

    // Copy documentation files to project root
    spinner = ora('Copying documentation...').start();
    const docsToRoot = [
      'CODEX-User-Guide.md',
      'CODEX-Workflow-Guide.md',
      'CONTRIBUTING.md'
    ];

    for (const doc of docsToRoot) {
      const docSource = join(packageRoot, doc);
      const docTarget = join(targetPath, doc);

      if (await fs.pathExists(docSource)) {
        await fs.copy(docSource, docTarget, {
          overwrite: false,
          errorOnExist: false
        });
      }
    }

    spinner.succeed('Documentation copied');

    return {
      success: true,
      message: 'CODEX installed successfully'
    };

  } catch (error) {
    if (spinner) spinner.fail('Installation failed');

    return {
      success: false,
      message: `Installation error: ${error.message}`
    };
  }
}

export default {
  installCodex,
  getInstallerPackagePath,
  validateTarget,
  showWelcomeBanner,
  showSuccessMessage
};
