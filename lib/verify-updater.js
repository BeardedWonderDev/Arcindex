#!/usr/bin/env node

/**
 * Verification script for updater.js implementation
 *
 * Checks that all required functions exist and have proper signatures.
 * Does not execute functions (to avoid side effects), just verifies structure.
 */

import chalk from 'chalk';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log(chalk.bold('\n🔍 CODEX Updater Verification\n'));

let allPassed = true;

// Test 1: Import updater module
console.log(chalk.blue('Test 1: Importing updater module...'));
try {
  const updater = await import('./updater.js');
  console.log(chalk.green('  ✓ Module imported successfully'));

  // Test 2: Check exported functions
  console.log(chalk.blue('\nTest 2: Checking exported functions...'));

  const requiredFunctions = [
    'updateCodex',
    'checkForUpdates'
  ];

  const missingFunctions = [];
  for (const funcName of requiredFunctions) {
    if (typeof updater[funcName] === 'function') {
      console.log(chalk.green(`  ✓ ${funcName} exists`));
    } else {
      console.log(chalk.red(`  ✗ ${funcName} missing or not a function`));
      missingFunctions.push(funcName);
      allPassed = false;
    }
  }

  if (missingFunctions.length === 0) {
    console.log(chalk.green('\n  All required functions present'));
  }

  // Test 3: Check default export
  console.log(chalk.blue('\nTest 3: Checking default export...'));
  if (updater.default && typeof updater.default === 'object') {
    console.log(chalk.green('  ✓ Default export exists'));

    const defaultFunctions = Object.keys(updater.default);
    console.log(chalk.gray(`    Functions in default: ${defaultFunctions.join(', ')}`));
  } else {
    console.log(chalk.yellow('  ⚠ No default export (named exports only)'));
  }

  // Test 4: Verify function signatures
  console.log(chalk.blue('\nTest 4: Verifying function signatures...'));

  // updateCodex should accept 3 parameters
  if (updater.updateCodex.length === 3) {
    console.log(chalk.green('  ✓ updateCodex has correct parameter count (3)'));
  } else {
    console.log(chalk.yellow(`  ⚠ updateCodex has ${updater.updateCodex.length} parameters (expected 3)`));
  }

  // checkForUpdates should accept 1 parameter
  if (updater.checkForUpdates.length === 1) {
    console.log(chalk.green('  ✓ checkForUpdates has correct parameter count (1)'));
  } else {
    console.log(chalk.yellow(`  ⚠ checkForUpdates has ${updater.checkForUpdates.length} parameters (expected 1)`));
  }

} catch (error) {
  console.log(chalk.red('  ✗ Failed to import module'));
  console.log(chalk.red(`    Error: ${error.message}`));
  allPassed = false;
}

// Test 5: Import dependent modules
console.log(chalk.blue('\nTest 5: Checking dependent modules...'));

const dependencies = [
  './detector.js',
  './compatibility-checker.js',
  './state-preserver.cjs',
  './file-manager.cjs',
  './manifest.js',
  './menu.cjs'
];

for (const dep of dependencies) {
  try {
    await import(dep);
    console.log(chalk.green(`  ✓ ${path.basename(dep)} imports successfully`));
  } catch (error) {
    console.log(chalk.red(`  ✗ ${path.basename(dep)} failed to import`));
    console.log(chalk.red(`    Error: ${error.message}`));
    allPassed = false;
  }
}

// Test 6: Check documentation files
console.log(chalk.blue('\nTest 6: Checking documentation files...'));

const fs = await import('fs');
const docFiles = [
  'UPDATER-GUIDE.md',
  'UPDATER-IMPLEMENTATION-SUMMARY.md',
  'README.md'
];

for (const docFile of docFiles) {
  const docPath = path.join(__dirname, docFile);
  if (fs.existsSync(docPath)) {
    console.log(chalk.green(`  ✓ ${docFile} exists`));
  } else {
    console.log(chalk.red(`  ✗ ${docFile} missing`));
    allPassed = false;
  }
}

// Test 7: Check test file
console.log(chalk.blue('\nTest 7: Checking test file...'));

const testPath = path.join(__dirname, 'updater.test.js');
if (fs.existsSync(testPath)) {
  console.log(chalk.green('  ✓ updater.test.js exists'));

  try {
    await import('./updater.test.js');
    console.log(chalk.green('  ✓ Test file imports successfully'));
  } catch (error) {
    console.log(chalk.yellow('  ⚠ Test file has import issues (may be expected)'));
    console.log(chalk.gray(`    ${error.message}`));
  }
} else {
  console.log(chalk.red('  ✗ updater.test.js missing'));
  allPassed = false;
}

// Final result
console.log(chalk.bold('\n' + '═'.repeat(50)));
if (allPassed) {
  console.log(chalk.green.bold('✓ All verification checks passed!'));
  console.log(chalk.gray('\nThe updater module is ready for integration.'));
  console.log(chalk.gray('\nNext steps:'));
  console.log(chalk.gray('  1. Add update command to bin/create-codex-project.js'));
  console.log(chalk.gray('  2. Add check-updates command'));
  console.log(chalk.gray('  3. Run integration tests'));
  console.log(chalk.gray('  4. Test rollback scenarios'));
} else {
  console.log(chalk.red.bold('✗ Some verification checks failed'));
  console.log(chalk.yellow('\nPlease review the errors above.'));
  process.exit(1);
}
console.log(chalk.bold('═'.repeat(50) + '\n'));
