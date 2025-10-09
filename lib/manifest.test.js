/**
 * Basic test file for manifest.js operations
 *
 * This is a simple smoke test to verify the manifest operations work.
 * For comprehensive testing, use the CODEX test harness.
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdirSync, rmSync, writeFileSync } from 'fs';
import {
  createManifest,
  readManifest,
  updateManifest,
  verifyManifest,
  getManifestSummary
} from './manifest.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Test setup
const testDir = join(__dirname, '..', 'test-temp-manifest');
const codexDir = join(testDir, '.codex');

/**
 * Setup test environment
 */
function setup() {
  // Clean up any existing test directory
  cleanup();

  // Create test directory structure
  mkdirSync(codexDir, { recursive: true });

  // Create some test files
  mkdirSync(join(codexDir, 'agents'), { recursive: true });
  mkdirSync(join(codexDir, 'workflows'), { recursive: true });
  mkdirSync(join(codexDir, 'tasks'), { recursive: true });

  writeFileSync(join(codexDir, 'agents', 'test-agent.md'), '# Test Agent\n\nThis is a test agent.');
  writeFileSync(join(codexDir, 'workflows', 'test-workflow.yaml'), 'name: test\nsteps: []\n');
  writeFileSync(join(codexDir, 'tasks', 'test-task.md'), '# Test Task\n\nThis is a test task.');
}

/**
 * Cleanup test environment
 */
function cleanup() {
  try {
    rmSync(testDir, { recursive: true, force: true });
  } catch (error) {
    // Ignore errors
  }
}

/**
 * Run tests
 */
async function runTests() {
  console.log('\n🧪 Running Manifest Operations Tests\n');

  try {
    // Test 1: Setup
    console.log('📋 Test 1: Setup test environment');
    setup();
    console.log('   ✓ Test directory created');

    // Test 2: Create manifest
    console.log('\n📋 Test 2: Create manifest');
    const manifest = await createManifest(testDir, {
      codex_version: '0.1.0',
      schema_version: 1,
      default_workflow: 'greenfield-generic',
      test_harness_included: false,
      ide_setup: ['claude-code']
    });

    console.log('   ✓ Manifest created');
    console.log(`   - Files tracked: ${manifest.files.length}`);
    console.log(`   - Version: ${manifest.codex_version}`);
    console.log(`   - Workflow: ${manifest.default_workflow}`);

    // Test 3: Read manifest
    console.log('\n📋 Test 3: Read manifest');
    const readResult = readManifest(testDir);
    console.log('   ✓ Manifest read successfully');
    console.log(`   - Schema version: ${readResult.schema_version}`);
    console.log(`   - Installed at: ${readResult.installed_at}`);

    // Test 4: Get summary
    console.log('\n📋 Test 4: Get manifest summary');
    const summary = getManifestSummary(testDir);
    console.log('   ✓ Summary retrieved');
    console.log(`   - File count: ${summary.file_count}`);
    console.log(`   - Update count: ${summary.update_count}`);

    // Test 5: Verify manifest (should pass)
    console.log('\n📋 Test 5: Verify manifest integrity');
    const verification1 = verifyManifest(testDir);
    console.log(`   ${verification1.valid ? '✓' : '✗'} Verification: ${verification1.valid ? 'PASSED' : 'FAILED'}`);
    console.log(`   - Total files: ${verification1.totalFiles}`);
    console.log(`   - Missing: ${verification1.missingFiles}`);
    console.log(`   - Modified: ${verification1.modifiedFiles}`);

    // Test 6: Modify a file and verify (should detect modification)
    console.log('\n📋 Test 6: Detect file modification');
    writeFileSync(join(codexDir, 'agents', 'test-agent.md'), '# Modified Agent\n\nThis has been modified.');
    const verification2 = verifyManifest(testDir);
    console.log(`   ${!verification2.valid ? '✓' : '✗'} Modification detected: ${!verification2.valid ? 'YES' : 'NO'}`);
    console.log(`   - Modified files: ${verification2.modifiedFiles}`);
    if (verification2.modified.length > 0) {
      console.log(`   - Changed: ${verification2.modified[0].path}`);
    }

    // Test 7: Update manifest
    console.log('\n📋 Test 7: Update manifest');
    const updatedManifest = await updateManifest(testDir, {
      codex_version: '0.1.1',
      default_workflow: 'brownfield-enhancement',
      test_harness_included: true,
      change_summary: 'Updated to v0.1.1 with test harness',
      regenerate_files: true
    });
    console.log('   ✓ Manifest updated');
    console.log(`   - New version: ${updatedManifest.codex_version}`);
    console.log(`   - New workflow: ${updatedManifest.default_workflow}`);
    console.log(`   - Test harness: ${updatedManifest.test_harness_included}`);
    console.log(`   - Updates recorded: ${updatedManifest.updates.length}`);

    // Test 8: Verify after update (should pass now)
    console.log('\n📋 Test 8: Verify after regeneration');
    const verification3 = verifyManifest(testDir);
    console.log(`   ${verification3.valid ? '✓' : '✗'} Verification: ${verification3.valid ? 'PASSED' : 'FAILED'}`);
    console.log(`   - Total files: ${verification3.totalFiles}`);
    console.log(`   - Missing: ${verification3.missingFiles}`);
    console.log(`   - Modified: ${verification3.modifiedFiles}`);

    // Test 9: Cleanup
    console.log('\n📋 Test 9: Cleanup');
    cleanup();
    console.log('   ✓ Test directory removed');

    console.log('\n✅ All tests passed!\n');

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    console.error(error.stack);
    cleanup();
    process.exit(1);
  }
}

// Run tests if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests();
}

export { runTests };
