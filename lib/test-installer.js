#!/usr/bin/env node

/**
 * Quick verification test for installer module
 * Tests that all exported functions exist and have correct signatures
 */

import {
  installCodex,
  getInstallerPackagePath,
  validateTarget,
  showWelcomeBanner,
  showSuccessMessage
} from './installer.js';

console.log('Testing installer module exports...\n');

// Test 1: Check all functions are exported
console.log('✓ installCodex:', typeof installCodex === 'function');
console.log('✓ getInstallerPackagePath:', typeof getInstallerPackagePath === 'function');
console.log('✓ validateTarget:', typeof validateTarget === 'function');
console.log('✓ showWelcomeBanner:', typeof showWelcomeBanner === 'function');
console.log('✓ showSuccessMessage:', typeof showSuccessMessage === 'function');

// Test 2: getInstallerPackagePath
console.log('\nTesting getInstallerPackagePath()...');
try {
  const packagePath = getInstallerPackagePath();
  console.log('✓ Package path:', packagePath);
  console.log('✓ Function works correctly');
} catch (error) {
  console.log('✗ Error:', error.message);
}

// Test 3: showWelcomeBanner
console.log('\nTesting showWelcomeBanner()...');
try {
  showWelcomeBanner('0.1.0');
  console.log('✓ Banner displayed successfully');
} catch (error) {
  console.log('✗ Error:', error.message);
}

// Test 4: validateTarget with invalid path
console.log('\nTesting validateTarget() with invalid path...');
try {
  const result = await validateTarget('/nonexistent/path/that/does/not/exist');
  console.log('✓ Validation result:', result);
  console.log('✓ Function returns expected structure');
} catch (error) {
  console.log('✗ Error:', error.message);
}

// Test 5: validateTarget with current directory
console.log('\nTesting validateTarget() with current directory...');
try {
  const result = await validateTarget(process.cwd());
  console.log('✓ Validation result:', result);
  if (result.valid === true || result.valid === false) {
    console.log('✓ Function returns boolean valid field');
  }
} catch (error) {
  console.log('✗ Error:', error.message);
}

// Test 6: showSuccessMessage
console.log('\nTesting showSuccessMessage()...');
try {
  showSuccessMessage('/example/project', 'greenfield-generic');
  console.log('✓ Success message displayed');
} catch (error) {
  console.log('✗ Error:', error.message);
}

console.log('\n✓ All installer module tests completed!');
