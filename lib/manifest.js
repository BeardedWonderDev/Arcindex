/**
 * CODEX Installer Manifest Operations
 *
 * Handles creation, reading, updating, and verification of install-manifest.yaml files.
 * Used to track installed files, versions, and integrity of CODEX installations.
 */

import { readFileSync, writeFileSync, existsSync, statSync } from 'fs';
import { join, relative } from 'path';
import { createHash } from 'crypto';
import yaml from 'js-yaml';
import { glob } from 'glob';

/**
 * Generate SHA256 hash for a file (truncated to 16 chars for readability)
 * @param {string} filePath - Absolute path to file
 * @returns {string} Truncated hash string
 */
function generateFileHash(filePath) {
  try {
    const content = readFileSync(filePath, 'utf8');
    const hash = createHash('sha256').update(content).digest('hex');
    return hash.substring(0, 16); // Match BMAD format
  } catch (error) {
    throw new Error(`Failed to hash file ${filePath}: ${error.message}`);
  }
}

/**
 * Get all files in .codex directory recursively
 * @param {string} projectPath - Project root directory
 * @returns {Array<{path: string, hash: string, modified: boolean}>}
 */
async function getCodexFiles(projectPath) {
  const codexPath = join(projectPath, '.codex');

  if (!existsSync(codexPath)) {
    throw new Error(`.codex directory not found at ${codexPath}`);
  }

  // Get all files in .codex directory
  const pattern = join(codexPath, '**/*');
  const files = await glob(pattern, {
    nodir: true,
    dot: true
  });

  return files.map(absolutePath => {
    const relativePath = relative(projectPath, absolutePath);
    const hash = generateFileHash(absolutePath);

    return {
      path: relativePath,
      hash: hash,
      modified: false
    };
  }).sort((a, b) => a.path.localeCompare(b.path));
}

/**
 * Create a new install manifest
 *
 * @param {string} projectPath - Project root directory
 * @param {Object} options - Manifest options
 * @param {string} options.codex_version - CODEX version (e.g., "0.1.0")
 * @param {number} [options.schema_version=1] - Manifest schema version
 * @param {string} [options.default_workflow="greenfield-generic"] - Default workflow
 * @param {boolean} [options.test_harness_included=false] - Whether test harness is included
 * @param {string[]} [options.ide_setup=["claude-code"]] - IDE integrations set up
 * @returns {Promise<Object>} Created manifest object
 */
export async function createManifest(projectPath, options = {}) {
  const {
    codex_version,
    schema_version = 1,
    default_workflow = 'greenfield-generic',
    test_harness_included = false,
    ide_setup = ['claude-code']
  } = options;

  if (!codex_version) {
    throw new Error('codex_version is required');
  }

  if (!existsSync(projectPath)) {
    throw new Error(`Project path does not exist: ${projectPath}`);
  }

  // Generate file list with hashes
  const files = await getCodexFiles(projectPath);

  // Create manifest object
  const manifest = {
    codex_version,
    schema_version,
    installed_at: new Date().toISOString(),
    default_workflow,
    test_harness_included,
    ide_setup,
    files,
    updates: []
  };

  // Write manifest to .codex/install-manifest.yaml
  const manifestPath = join(projectPath, '.codex', 'install-manifest.yaml');
  const yamlContent = yaml.dump(manifest, {
    indent: 2,
    lineWidth: -1, // Don't wrap lines
    noRefs: true
  });

  writeFileSync(manifestPath, yamlContent, 'utf8');

  return manifest;
}

/**
 * Read existing manifest
 *
 * @param {string} projectPath - Project root directory
 * @returns {Object|null} Manifest object or null if not found
 */
export function readManifest(projectPath) {
  const manifestPath = join(projectPath, '.codex', 'install-manifest.yaml');

  if (!existsSync(manifestPath)) {
    return null;
  }

  try {
    const content = readFileSync(manifestPath, 'utf8');
    const manifest = yaml.load(content);
    return manifest;
  } catch (error) {
    throw new Error(`Failed to read manifest: ${error.message}`);
  }
}

/**
 * Update existing manifest with new data
 *
 * @param {string} projectPath - Project root directory
 * @param {Object} updates - Updates to apply
 * @param {string} [updates.codex_version] - New CODEX version
 * @param {string} [updates.default_workflow] - New default workflow
 * @param {boolean} [updates.test_harness_included] - Test harness status
 * @param {string[]} [updates.ide_setup] - IDE integrations
 * @param {boolean} [updates.regenerate_files=false] - Regenerate file list with new hashes
 * @param {string} [updates.change_summary] - Description of changes
 * @returns {Promise<Object>} Updated manifest object
 */
export async function updateManifest(projectPath, updates = {}) {
  const manifest = readManifest(projectPath);

  if (!manifest) {
    throw new Error(`No manifest found at ${projectPath}. Use createManifest() first.`);
  }

  const {
    codex_version,
    default_workflow,
    test_harness_included,
    ide_setup,
    regenerate_files = false,
    change_summary
  } = updates;

  // Apply updates to manifest
  if (codex_version !== undefined) manifest.codex_version = codex_version;
  if (default_workflow !== undefined) manifest.default_workflow = default_workflow;
  if (test_harness_included !== undefined) manifest.test_harness_included = test_harness_included;
  if (ide_setup !== undefined) manifest.ide_setup = ide_setup;

  // Regenerate file list if requested
  if (regenerate_files) {
    manifest.files = await getCodexFiles(projectPath);
  }

  // Add update record
  const updateRecord = {
    timestamp: new Date().toISOString(),
    changes: {}
  };

  if (codex_version !== undefined) updateRecord.changes.codex_version = codex_version;
  if (default_workflow !== undefined) updateRecord.changes.default_workflow = default_workflow;
  if (test_harness_included !== undefined) updateRecord.changes.test_harness_included = test_harness_included;
  if (ide_setup !== undefined) updateRecord.changes.ide_setup = ide_setup;
  if (regenerate_files) updateRecord.changes.files_regenerated = true;
  if (change_summary) updateRecord.summary = change_summary;

  if (!manifest.updates) manifest.updates = [];
  manifest.updates.push(updateRecord);

  // Write updated manifest
  const manifestPath = join(projectPath, '.codex', 'install-manifest.yaml');
  const yamlContent = yaml.dump(manifest, {
    indent: 2,
    lineWidth: -1,
    noRefs: true
  });

  writeFileSync(manifestPath, yamlContent, 'utf8');

  return manifest;
}

/**
 * Verify manifest integrity
 *
 * Checks that all listed files exist and their hashes match.
 *
 * @param {string} projectPath - Project root directory
 * @returns {Object} Validation results
 * @returns {boolean} results.valid - Overall validity
 * @returns {number} results.totalFiles - Total files checked
 * @returns {number} results.missingFiles - Number of missing files
 * @returns {number} results.modifiedFiles - Number of modified files
 * @returns {Array<string>} results.missing - List of missing file paths
 * @returns {Array<{path: string, expected: string, actual: string}>} results.modified - Modified files with hash details
 * @returns {Array<string>} results.errors - Any errors encountered
 */
export function verifyManifest(projectPath) {
  const manifest = readManifest(projectPath);

  if (!manifest) {
    return {
      valid: false,
      error: 'No manifest found',
      totalFiles: 0,
      missingFiles: 0,
      modifiedFiles: 0,
      missing: [],
      modified: [],
      errors: ['Manifest file does not exist']
    };
  }

  const results = {
    valid: true,
    totalFiles: 0,
    missingFiles: 0,
    modifiedFiles: 0,
    missing: [],
    modified: [],
    errors: []
  };

  if (!manifest.files || !Array.isArray(manifest.files)) {
    results.valid = false;
    results.errors.push('Manifest has no files array');
    return results;
  }

  results.totalFiles = manifest.files.length;

  // Check each file
  for (const fileEntry of manifest.files) {
    const { path: filePath, hash: expectedHash } = fileEntry;
    const absolutePath = join(projectPath, filePath);

    // Check if file exists
    if (!existsSync(absolutePath)) {
      results.valid = false;
      results.missingFiles++;
      results.missing.push(filePath);
      continue;
    }

    // Verify hash
    try {
      const actualHash = generateFileHash(absolutePath);

      if (actualHash !== expectedHash) {
        results.valid = false;
        results.modifiedFiles++;
        results.modified.push({
          path: filePath,
          expected: expectedHash,
          actual: actualHash
        });

        // Update the modified flag in the manifest entry
        fileEntry.modified = true;
      }
    } catch (error) {
      results.valid = false;
      results.errors.push(`Failed to verify ${filePath}: ${error.message}`);
    }
  }

  return results;
}

/**
 * Get manifest summary information
 *
 * @param {string} projectPath - Project root directory
 * @returns {Object|null} Summary information or null if no manifest
 */
export function getManifestSummary(projectPath) {
  const manifest = readManifest(projectPath);

  if (!manifest) {
    return null;
  }

  return {
    codex_version: manifest.codex_version,
    schema_version: manifest.schema_version,
    installed_at: manifest.installed_at,
    default_workflow: manifest.default_workflow,
    test_harness_included: manifest.test_harness_included,
    ide_setup: manifest.ide_setup,
    file_count: manifest.files?.length || 0,
    update_count: manifest.updates?.length || 0,
    last_update: manifest.updates?.length > 0
      ? manifest.updates[manifest.updates.length - 1].timestamp
      : null
  };
}

export default {
  createManifest,
  readManifest,
  updateManifest,
  verifyManifest,
  getManifestSummary
};
