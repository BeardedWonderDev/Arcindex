const inquirer = require('inquirer');
const chalk = require('chalk');

/**
 * Prompt user to select default workflow for CODEX installation
 *
 * @returns {Promise<string>} Selected workflow ID: 'greenfield-generic', 'greenfield-swift', or 'brownfield-enhancement'
 */
async function promptWorkflowChoice() {
  const { workflow } = await inquirer.prompt([
    {
      type: 'list',
      name: 'workflow',
      message: 'Select default workflow:',
      default: 'greenfield-generic',
      choices: [
        {
          name: 'Greenfield Generic (Python, JS, Go, etc.)',
          value: 'greenfield-generic',
        },
        {
          name: 'Greenfield Swift (iOS/macOS projects)',
          value: 'greenfield-swift',
        },
        {
          name: 'Brownfield Enhancement (Existing codebases)',
          value: 'brownfield-enhancement',
        },
      ],
    },
  ]);

  return workflow;
}

/**
 * Prompt user to decide if test harness should be installed
 *
 * @returns {Promise<boolean>} true if user wants test harness, false otherwise
 */
async function promptTestHarness() {
  const { installTestHarness } = await inquirer.prompt([
    {
      type: 'list',
      name: 'installTestHarness',
      message: 'Install test harness?',
      default: false,
      choices: [
        {
          name: 'No (default for users)',
          value: false,
        },
        {
          name: 'Yes (for development/validation)',
          value: true,
        },
      ],
    },
  ]);

  return installTestHarness;
}

/**
 * Prompt user to confirm CODEX update
 *
 * @param {string} currentVersion - Current installed version
 * @param {string} targetVersion - Target version to update to
 * @param {boolean} hasActiveWorkflow - Whether there's an active workflow in progress
 * @returns {Promise<boolean>} true if user confirms update, false otherwise
 */
async function promptUpdateConfirmation(currentVersion, targetVersion, hasActiveWorkflow) {
  console.log('\n' + chalk.bold('CODEX Update Available'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log(chalk.cyan('Current version:') + ' ' + chalk.white(currentVersion));
  console.log(chalk.cyan('Target version:')  + '  ' + chalk.white(targetVersion));

  if (hasActiveWorkflow) {
    console.log('\n' + chalk.yellow('⚠️  Warning: Active workflow detected!'));
    console.log(chalk.gray('   Updating may disrupt your current workflow state.'));
    console.log(chalk.gray('   Consider completing or checkpointing your work first.'));
  }

  console.log(chalk.gray('─'.repeat(50)) + '\n');

  const { confirmed } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'confirmed',
      message: hasActiveWorkflow
        ? 'Proceed with update despite active workflow?'
        : 'Proceed with update?',
      default: !hasActiveWorkflow,
    },
  ]);

  return confirmed;
}

/**
 * Prompt user to confirm dangerous schema upgrade with forced override
 * Requires typing "yes" to confirm (not just Y/n)
 *
 * @param {string} currentVersion - Current installed version
 * @param {string} targetVersion - Target version to update to
 * @param {string} currentSchema - Current schema version
 * @param {string} targetSchema - Target schema version
 * @returns {Promise<boolean>} true if user confirms with "yes", false otherwise
 */
async function promptForceSchemaOverride(currentVersion, targetVersion, currentSchema, targetSchema) {
  console.log('\n' + chalk.red.bold('⚠️  DANGEROUS SCHEMA UPGRADE DETECTED'));
  console.log(chalk.gray('═'.repeat(60)));
  console.log(chalk.red('This update includes a schema version change that may be'));
  console.log(chalk.red('incompatible with your existing workflow state!'));
  console.log('');
  console.log(chalk.cyan('Current version:') + ' ' + chalk.white(currentVersion) + ' ' + chalk.gray(`(schema ${currentSchema})`));
  console.log(chalk.cyan('Target version:')  + '  ' + chalk.white(targetVersion)  + ' ' + chalk.gray(`(schema ${targetSchema})`));
  console.log('');
  console.log(chalk.yellow('Potential risks:'));
  console.log(chalk.gray('  • Loss of workflow state and progress'));
  console.log(chalk.gray('  • Incompatible template formats'));
  console.log(chalk.gray('  • Breaking changes to agent behavior'));
  console.log(chalk.gray('  • Data corruption or migration issues'));
  console.log('');
  console.log(chalk.red.bold('This operation cannot be undone!'));
  console.log(chalk.gray('═'.repeat(60)));
  console.log('');
  console.log(chalk.yellow('Recommended actions:'));
  console.log(chalk.gray('  1. Back up your current .codex directory'));
  console.log(chalk.gray('  2. Complete or checkpoint active workflows'));
  console.log(chalk.gray('  3. Review the changelog for breaking changes'));
  console.log(chalk.gray('  4. Test the update in a non-production environment'));
  console.log(chalk.gray('═'.repeat(60)) + '\n');

  const { confirmation } = await inquirer.prompt([
    {
      type: 'input',
      name: 'confirmation',
      message: chalk.red('Type "yes" to force schema override (or anything else to cancel):'),
      validate: (input) => {
        if (input === 'yes') {
          return true;
        }
        return 'Schema override cancelled. Please type "yes" to confirm or press Ctrl+C to exit.';
      },
    },
  ]);

  return confirmation === 'yes';
}

module.exports = {
  promptWorkflowChoice,
  promptTestHarness,
  promptUpdateConfirmation,
  promptForceSchemaOverride,
};
