/**
 * Compatibility Checker - Validates compatibility between installed and target CODEX versions
 * Checks schema versions, active workflows, and determines upgrade/downgrade safety
 */

import semver from 'semver';
import { detectExistingInstallation, detectActiveWorkflow, fetchPackageInfo } from './detector.js';

/**
 * Check compatibility between current installation and target version
 * @param {string} projectPath - Path to the project
 * @param {string} targetVersion - Target version to check compatibility with
 * @returns {Promise<Object>} Compatibility result
 */
async function checkCompatibility(projectPath, targetVersion) {
  try {
    // Step 1: Detect existing installation
    const installation = await detectExistingInstallation(projectPath);

    if (!installation.exists) {
      // No existing installation, always compatible for fresh install
      return {
        compatible: true,
        reason: null,
        severity: null,
        currentVersion: null,
        targetVersion: targetVersion,
        currentSchema: null,
        targetSchema: null,
        message: 'No existing installation detected. Fresh installation is compatible.',
        action: null,
        requiresConfirmation: false
      };
    }

    // Step 2: Check for active workflows
    const workflow = await detectActiveWorkflow(projectPath);

    if (workflow.active) {
      return {
        compatible: false,
        reason: 'workflow-in-progress',
        severity: 'critical',
        currentVersion: installation.version,
        targetVersion: targetVersion,
        currentSchema: installation.schemaVersion,
        targetSchema: null,
        message: `Cannot upgrade: Active workflow in progress (Phase: ${workflow.phase}, Type: ${workflow.workflowType}). Please complete or cancel the current workflow before upgrading.`,
        action: 'BLOCKED',
        requiresConfirmation: false,
        workflowDetails: {
          phase: workflow.phase,
          type: workflow.workflowType
        }
      };
    }

    // Step 3: Fetch target package information
    let targetPackageInfo;
    try {
      targetPackageInfo = await fetchPackageInfo('create-codex-project', targetVersion);
    } catch (error) {
      return {
        compatible: false,
        reason: 'fetch-error',
        severity: 'critical',
        currentVersion: installation.version,
        targetVersion: targetVersion,
        currentSchema: installation.schemaVersion,
        targetSchema: null,
        message: `Cannot verify compatibility: ${error.message}`,
        action: 'BLOCKED',
        requiresConfirmation: false
      };
    }

    // Extract target schema version from package.json
    const targetSchema = targetPackageInfo.codex?.schemaVersion || null;

    // Step 4: Compare schema versions
    const currentSchema = installation.schemaVersion;

    if (currentSchema === null || targetSchema === null) {
      return {
        compatible: false,
        reason: 'schema-unknown',
        severity: 'warning',
        currentVersion: installation.version,
        targetVersion: targetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: 'Cannot determine schema compatibility. Upgrade may cause issues.',
        action: 'WARNING',
        requiresConfirmation: true
      };
    }

    if (currentSchema !== targetSchema) {
      // Schema mismatch - this is a breaking change
      const upgrading = targetSchema > currentSchema;

      return {
        compatible: false,
        reason: 'schema-mismatch',
        severity: 'critical',
        currentVersion: installation.version,
        targetVersion: targetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: upgrading
          ? `Incompatible schema version. Upgrading from schema v${currentSchema} to v${targetSchema} requires manual migration. This is a breaking change.`
          : `Incompatible schema version. Downgrading from schema v${currentSchema} to v${targetSchema} is not supported.`,
        action: 'BLOCKED',
        requiresConfirmation: false,
        schemaChange: {
          direction: upgrading ? 'upgrade' : 'downgrade',
          from: currentSchema,
          to: targetSchema
        }
      };
    }

    // Step 5: Check semantic version compatibility
    const currentVersion = installation.version;

    // Validate versions
    if (!semver.valid(currentVersion)) {
      return {
        compatible: false,
        reason: 'invalid-version',
        severity: 'warning',
        currentVersion: currentVersion,
        targetVersion: targetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: `Current version "${currentVersion}" is not a valid semantic version. Upgrade may cause issues.`,
        action: 'WARNING',
        requiresConfirmation: true
      };
    }

    if (!semver.valid(targetVersion) && targetVersion !== 'latest') {
      return {
        compatible: false,
        reason: 'invalid-version',
        severity: 'warning',
        currentVersion: currentVersion,
        targetVersion: targetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: `Target version "${targetVersion}" is not a valid semantic version.`,
        action: 'WARNING',
        requiresConfirmation: true
      };
    }

    // Normalize 'latest' to actual version
    const normalizedTargetVersion = targetVersion === 'latest'
      ? targetPackageInfo.version
      : targetVersion;

    // Check if versions are the same
    if (semver.eq(currentVersion, normalizedTargetVersion)) {
      return {
        compatible: true,
        reason: null,
        severity: null,
        currentVersion: currentVersion,
        targetVersion: normalizedTargetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: `Already running version ${currentVersion}. Reinstallation will refresh files.`,
        action: null,
        requiresConfirmation: true,
        versionStatus: 'same'
      };
    }

    // Check if downgrading
    if (semver.lt(normalizedTargetVersion, currentVersion)) {
      return {
        compatible: true,
        reason: null,
        severity: 'warning',
        currentVersion: currentVersion,
        targetVersion: normalizedTargetVersion,
        currentSchema: currentSchema,
        targetSchema: targetSchema,
        message: `Downgrading from ${currentVersion} to ${normalizedTargetVersion}. Same schema version, but may lose newer features.`,
        action: 'WARNING',
        requiresConfirmation: true,
        versionStatus: 'downgrade'
      };
    }

    // Upgrading to a newer version with same schema
    return {
      compatible: true,
      reason: null,
      severity: null,
      currentVersion: currentVersion,
      targetVersion: normalizedTargetVersion,
      currentSchema: currentSchema,
      targetSchema: targetSchema,
      message: `Upgrading from ${currentVersion} to ${normalizedTargetVersion}. Same schema version, should be compatible.`,
      action: null,
      requiresConfirmation: false,
      versionStatus: 'upgrade'
    };

  } catch (error) {
    return {
      compatible: false,
      reason: 'check-error',
      severity: 'critical',
      currentVersion: null,
      targetVersion: targetVersion,
      currentSchema: null,
      targetSchema: null,
      message: `Compatibility check failed: ${error.message}`,
      action: 'BLOCKED',
      requiresConfirmation: false,
      error: error.message
    };
  }
}

export {
  checkCompatibility
};

export default {
  checkCompatibility
};
