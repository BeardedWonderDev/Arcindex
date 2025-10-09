/**
 * Hash Manager - File and directory hashing utilities for CODEX installer
 * Provides SHA-256 hashing for integrity verification
 */

const crypto = require('crypto');
const fs = require('fs-extra');
const path = require('path');

/**
 * Create SHA-256 hash of a file
 * @param {string} filePath - Path to file to hash
 * @returns {Promise<string>} Hex-encoded SHA-256 hash
 * @throws {Error} If file cannot be read or hashed
 */
async function hashFile(filePath) {
  try {
    // Check if file exists
    const exists = await fs.pathExists(filePath);
    if (!exists) {
      throw new Error(`File does not exist: ${filePath}`);
    }

    // Create hash stream
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);

    // Return promise that resolves with hash
    return new Promise((resolve, reject) => {
      stream.on('data', (data) => {
        hash.update(data);
      });

      stream.on('end', () => {
        resolve(hash.digest('hex'));
      });

      stream.on('error', (error) => {
        reject(new Error(`Failed to hash file ${filePath}: ${error.message}`));
      });
    });
  } catch (error) {
    throw new Error(`Failed to hash file ${filePath}: ${error.message}`);
  }
}

/**
 * Create hash manifest of all files in a directory
 * @param {string} dirPath - Path to directory to hash
 * @param {Object} options - Hashing options
 * @param {string[]} options.exclude - Array of patterns to exclude
 * @returns {Promise<Object>} Hash manifest object with file paths and hashes
 * @throws {Error} If directory cannot be read or hashed
 */
async function hashDirectory(dirPath, options = {}) {
  const { exclude = [] } = options;

  try {
    // Check if directory exists
    const exists = await fs.pathExists(dirPath);
    if (!exists) {
      throw new Error(`Directory does not exist: ${dirPath}`);
    }

    const manifest = {};

    // Recursively walk directory
    await walkDirectory(dirPath, dirPath, manifest, exclude);

    return manifest;
  } catch (error) {
    throw new Error(`Failed to hash directory ${dirPath}: ${error.message}`);
  }
}

/**
 * Recursively walk directory and hash all files
 * @param {string} dirPath - Current directory path
 * @param {string} basePath - Base directory path for relative paths
 * @param {Object} manifest - Manifest object to populate
 * @param {string[]} exclude - Exclusion patterns
 * @returns {Promise<void>}
 */
async function walkDirectory(dirPath, basePath, manifest, exclude) {
  const entries = await fs.readdir(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const relativePath = path.relative(basePath, fullPath);

    // Check if path should be excluded
    if (shouldExclude(relativePath, exclude)) {
      continue;
    }

    if (entry.isDirectory()) {
      // Recursively process subdirectories
      await walkDirectory(fullPath, basePath, manifest, exclude);
    } else if (entry.isFile()) {
      // Hash file and add to manifest
      const hash = await hashFile(fullPath);
      // Normalize path separators for cross-platform consistency
      const normalizedPath = relativePath.replace(/\\/g, '/');
      manifest[normalizedPath] = hash;
    }
  }
}

/**
 * Check if path should be excluded based on patterns
 * @param {string} filePath - File path to check
 * @param {string[]} exclude - Exclusion patterns
 * @returns {boolean} True if path should be excluded
 */
function shouldExclude(filePath, exclude) {
  const normalizedPath = filePath.replace(/\\/g, '/');

  for (const pattern of exclude) {
    const normalizedPattern = pattern.replace(/\\/g, '/');

    // Exact match
    if (normalizedPath === normalizedPattern) {
      return true;
    }

    // Wildcard pattern match
    if (normalizedPattern.includes('*')) {
      const regexPattern = normalizedPattern
        .replace(/\./g, '\\.')
        .replace(/\*\*/g, '.*')
        .replace(/\*/g, '[^/]*');

      const regex = new RegExp(`^${regexPattern}$`);
      if (regex.test(normalizedPath)) {
        return true;
      }
    }

    // Directory prefix match
    if (normalizedPath.startsWith(normalizedPattern + '/') ||
        normalizedPath.startsWith(normalizedPattern)) {
      return true;
    }
  }

  return false;
}

/**
 * Compare two hash values or hash manifests
 * @param {string|Object} hash1 - First hash or manifest
 * @param {string|Object} hash2 - Second hash or manifest
 * @returns {boolean} True if hashes match
 */
function compareHashes(hash1, hash2) {
  // If both are strings, simple comparison
  if (typeof hash1 === 'string' && typeof hash2 === 'string') {
    return hash1 === hash2;
  }

  // If both are objects (manifests), deep comparison
  if (typeof hash1 === 'object' && typeof hash2 === 'object') {
    return compareManifests(hash1, hash2);
  }

  // Type mismatch
  return false;
}

/**
 * Compare two hash manifests
 * @param {Object} manifest1 - First manifest
 * @param {Object} manifest2 - Second manifest
 * @returns {boolean} True if manifests match
 */
function compareManifests(manifest1, manifest2) {
  const keys1 = Object.keys(manifest1).sort();
  const keys2 = Object.keys(manifest2).sort();

  // Check if same number of files
  if (keys1.length !== keys2.length) {
    return false;
  }

  // Check if all keys match
  for (let i = 0; i < keys1.length; i++) {
    if (keys1[i] !== keys2[i]) {
      return false;
    }
  }

  // Check if all hashes match
  for (const key of keys1) {
    if (manifest1[key] !== manifest2[key]) {
      return false;
    }
  }

  return true;
}

/**
 * Get differences between two hash manifests
 * @param {Object} manifest1 - First manifest (old)
 * @param {Object} manifest2 - Second manifest (new)
 * @returns {Object} Object with added, removed, and modified files
 */
function getManifestDiff(manifest1, manifest2) {
  const diff = {
    added: [],
    removed: [],
    modified: []
  };

  const keys1 = new Set(Object.keys(manifest1));
  const keys2 = new Set(Object.keys(manifest2));

  // Find added files
  for (const key of keys2) {
    if (!keys1.has(key)) {
      diff.added.push(key);
    }
  }

  // Find removed files
  for (const key of keys1) {
    if (!keys2.has(key)) {
      diff.removed.push(key);
    }
  }

  // Find modified files
  for (const key of keys1) {
    if (keys2.has(key) && manifest1[key] !== manifest2[key]) {
      diff.modified.push(key);
    }
  }

  return diff;
}

module.exports = {
  hashFile,
  hashDirectory,
  compareHashes,
  getManifestDiff
};
