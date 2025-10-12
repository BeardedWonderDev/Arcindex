/**
 * Installation Detector - Detects existing CODEX installations and active workflows
 * Provides utilities for checking installation state and workflow status
 */

import fs from 'fs-extra';
import path from 'path';
import yaml from 'js-yaml';

/**
 * Detect if CODEX is already installed in the given path
 * @param {string} projectPath - Path to check for CODEX installation
 * @returns {Promise<Object>} Installation detection result
 * @returns {boolean} result.exists - Whether CODEX is installed
 * @returns {string|null} result.version - Installed version if exists
 * @returns {number|null} result.schemaVersion - Schema version if exists
 * @returns {Object|null} result.manifest - Full manifest object if exists
 */
async function detectExistingInstallation(projectPath) {
  const manifestPath = path.join(projectPath, '.codex', 'install-manifest.yaml');

  try {
    // Check if manifest file exists
    const exists = await fs.pathExists(manifestPath);

    if (!exists) {
      return {
        exists: false,
        version: null,
        schemaVersion: null,
        manifest: null
      };
    }

    // Read and parse the manifest file
    const manifestContent = await fs.readFile(manifestPath, 'utf8');
    const manifest = yaml.load(manifestContent);

    return {
      exists: true,
      version: manifest.codex_version || null,
      schemaVersion: manifest.schema_version || null,
      manifest: manifest
    };
  } catch (error) {
    // If we can't read the manifest, treat as not installed
    return {
      exists: false,
      version: null,
      schemaVersion: null,
      manifest: null,
      error: `Failed to read installation manifest: ${error.message}`
    };
  }
}

/**
 * Detect if there's an active workflow in progress
 * @param {string} projectPath - Path to check for active workflow
 * @returns {Promise<Object>} Workflow detection result
 * @returns {boolean} result.active - Whether a workflow is active
 * @returns {string|null} result.phase - Current phase if active
 * @returns {string|null} result.workflowType - Type of workflow if active
 * @returns {Object|null} result.workflowState - Full workflow state if active
 */
async function detectActiveWorkflow(projectPath) {
  const workflowPath = path.join(projectPath, '.codex', 'state', 'workflow.json');

  try {
    // Check if workflow state file exists
    const exists = await fs.pathExists(workflowPath);

    if (!exists) {
      return {
        active: false,
        phase: null,
        workflowType: null,
        workflowState: null
      };
    }

    // Read and parse the workflow state
    const workflowState = await fs.readJson(workflowPath);

    // Check if workflow is active (current_phase is not 'completed')
    const isActive = workflowState.current_phase &&
                     workflowState.current_phase !== 'completed' &&
                     workflowState.status !== 'completed';

    return {
      active: isActive,
      phase: isActive ? workflowState.current_phase : null,
      workflowType: isActive ? workflowState.workflow_type : null,
      workflowState: isActive ? workflowState : null
    };
  } catch (error) {
    // If we can't read the workflow state, treat as no active workflow
    return {
      active: false,
      phase: null,
      workflowType: null,
      workflowState: null,
      error: `Failed to read workflow state: ${error.message}`
    };
  }
}

/**
 * Fetch package.json information from npm registry
 * @param {string} packageName - Name of the package
 * @param {string} version - Version to fetch (e.g., 'latest', '1.0.0')
 * @returns {Promise<Object>} Package information
 * @throws {Error} If fetch fails or package not found
 */
async function fetchPackageInfo(packageName, version = 'latest') {
  const registryUrl = `https://registry.npmjs.org/${packageName}/${version}`;

  try {
    // Dynamically import node-fetch for ESM compatibility
    const fetch = (await import('node-fetch')).default;

    const response = await fetch(registryUrl);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Package ${packageName}@${version} not found in npm registry`);
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const packageData = await response.json();

    // The response is the package.json data for the specified version
    return packageData;
  } catch (error) {
    if (error.code === 'ENOTFOUND' || error.code === 'EAI_AGAIN') {
      throw new Error(`Network error: Unable to reach npm registry. Check your internet connection.`);
    }

    throw new Error(`Failed to fetch package info for ${packageName}@${version}: ${error.message}`);
  }
}

export {
  detectExistingInstallation,
  detectActiveWorkflow,
  fetchPackageInfo
};

export default {
  detectExistingInstallation,
  detectActiveWorkflow,
  fetchPackageInfo
};
