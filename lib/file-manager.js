/**
 * File Manager - Robust file operations for CODEX installer
 * Handles directory operations with error handling and exclude patterns
 */

import fs from 'fs-extra';
import path from 'path';

/**
 * Copy a directory from source to target with optional exclusion patterns
 * @param {string} source - Source directory path
 * @param {string} target - Target directory path
 * @param {Object} options - Copy options
 * @param {string[]} options.exclude - Array of patterns to exclude (supports glob-like patterns)
 * @returns {Promise<void>}
 * @throws {Error} If copy operation fails
 */
async function copyDirectory(source, target, options = {}) {
  const { exclude = [] } = options;

  try {
    // Ensure source exists
    const sourceExists = await fs.pathExists(source);
    if (!sourceExists) {
      throw new Error(`Source directory does not exist: ${source}`);
    }

    // Ensure target directory exists
    await ensureDirectory(target);

    // Copy with filter function for exclusions
    await fs.copy(source, target, {
      overwrite: true,
      errorOnExist: false,
      filter: (src) => {
        // Get relative path from source
        const relativePath = path.relative(source, src);

        // Check if path matches any exclude pattern
        for (const pattern of exclude) {
          // Simple pattern matching - supports wildcards and exact matches
          if (matchesPattern(relativePath, pattern)) {
            return false; // Exclude this file/directory
          }
        }

        return true; // Include this file/directory
      }
    });
  } catch (error) {
    throw new Error(`Failed to copy directory from ${source} to ${target}: ${error.message}`);
  }
}

/**
 * Simple pattern matching for exclude patterns
 * Supports wildcards (*) and exact matches
 * @param {string} filePath - File path to test
 * @param {string} pattern - Pattern to match against
 * @returns {boolean} True if path matches pattern
 */
function matchesPattern(filePath, pattern) {
  // Normalize paths for comparison
  const normalizedPath = filePath.replace(/\\/g, '/');
  const normalizedPattern = pattern.replace(/\\/g, '/');

  // Exact match
  if (normalizedPath === normalizedPattern) {
    return true;
  }

  // Check if pattern contains wildcards
  if (normalizedPattern.includes('*')) {
    // Convert glob pattern to regex
    const regexPattern = normalizedPattern
      .replace(/\./g, '\\.')
      .replace(/\*\*/g, '.*')
      .replace(/\*/g, '[^/]*');

    const regex = new RegExp(`^${regexPattern}$`);
    return regex.test(normalizedPath);
  }

  // Check if path starts with pattern (for directory matches)
  if (normalizedPath.startsWith(normalizedPattern + '/') ||
      normalizedPath.startsWith(normalizedPattern)) {
    return true;
  }

  return false;
}

/**
 * Ensure a directory exists, creating it if necessary
 * @param {string} dirPath - Directory path to ensure
 * @returns {Promise<void>}
 * @throws {Error} If directory creation fails
 */
async function ensureDirectory(dirPath) {
  try {
    await fs.ensureDir(dirPath);
  } catch (error) {
    throw new Error(`Failed to ensure directory ${dirPath}: ${error.message}`);
  }
}

/**
 * Remove a directory and all its contents recursively
 * @param {string} dirPath - Directory path to remove
 * @returns {Promise<void>}
 * @throws {Error} If removal fails
 */
async function removeDirectory(dirPath) {
  try {
    const exists = await fs.pathExists(dirPath);
    if (exists) {
      await fs.remove(dirPath);
    }
  } catch (error) {
    throw new Error(`Failed to remove directory ${dirPath}: ${error.message}`);
  }
}

/**
 * Check if a file exists
 * @param {string} filePath - File path to check
 * @returns {Promise<boolean>} True if file exists
 */
async function fileExists(filePath) {
  try {
    return await fs.pathExists(filePath);
  } catch (error) {
    // If there's an error checking existence, consider it non-existent
    return false;
  }
}

/**
 * Read a JSON file and parse it
 * @param {string} filePath - Path to JSON file
 * @returns {Promise<Object>} Parsed JSON object
 * @throws {Error} If file read or parse fails
 */
async function readJsonFile(filePath) {
  try {
    return await fs.readJson(filePath);
  } catch (error) {
    throw new Error(`Failed to read JSON file ${filePath}: ${error.message}`);
  }
}

/**
 * Write an object to a JSON file
 * @param {string} filePath - Path to JSON file
 * @param {Object} data - Data to write
 * @returns {Promise<void>}
 * @throws {Error} If file write fails
 */
async function writeJsonFile(filePath, data) {
  try {
    await fs.writeJson(filePath, data, { spaces: 2 });
  } catch (error) {
    throw new Error(`Failed to write JSON file ${filePath}: ${error.message}`);
  }
}

export {
  copyDirectory,
  ensureDirectory,
  removeDirectory,
  fileExists,
  readJsonFile,
  writeJsonFile
};
