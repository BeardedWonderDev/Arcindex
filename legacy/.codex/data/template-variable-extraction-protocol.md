# Template Variable Extraction Protocol

## Purpose

Define the protocol for parsing `.codex/state/discovery-summary.json` and extracting template variables that can be used to auto-populate template sections across the CODEX workflow. This enables consistent variable usage from discovery through architect phases.

## Overview

Template variables enable:
1. **Consistency**: Same project name, platform, language used across all documents
2. **Automation**: Auto-populate template sections reducing manual entry
3. **Traceability**: Variables link back to discovery decisions
4. **Validation**: Ensure required context is captured during discovery

## Variable Reference Syntax

Templates can reference variables using:
```
{{var:variable_name}}
```

Examples:
- `{{var:project_name}}` → "TaskHub"
- `{{var:target_platform}}` → "Web"
- `{{var:primary_language}}` → "TypeScript"

## Extraction Mapping

### Source: discovery-summary.json → Output: template-variables.json

```yaml
# CORE PROJECT VARIABLES

project_name:
  source: discovery-summary.json → project_scope → extracted from first sentence
  extraction_rule: "Extract proper noun/project name from project_scope content"
  example: "TaskHub" (from "Building TaskHub, a task management app...")
  required: true
  validation: "Non-empty string, 1-50 characters"

project_description:
  source: discovery-summary.json → project_scope → content (first paragraph)
  extraction_rule: "First 1-2 sentences summarizing the project"
  example: "A task management app for remote teams that solves scattered communication."
  required: true
  validation: "Non-empty string, max 500 characters"

# PLATFORM & TECHNOLOGY VARIABLES

target_platform:
  source: discovery-summary.json → technical_constraints → platforms (array)
  extraction_rule: "Primary platform (first in array), or comma-separated list if multiple"
  example: "Web" or "Web, iOS, Android"
  required: true
  validation: "One of: Web, iOS, Android, Backend, Desktop, or comma-separated combination"

primary_language:
  source: discovery-summary.json → technical_constraints → languages (array)
  extraction_rule: "Primary language (first in array)"
  example: "TypeScript"
  required: true
  validation: "Non-empty string, common programming language name"

secondary_languages:
  source: discovery-summary.json → technical_constraints → languages (array, skip first)
  extraction_rule: "Remaining languages as comma-separated string"
  example: "JavaScript, Python"
  required: false
  validation: "Comma-separated language names or null"

frameworks:
  source: discovery-summary.json → technical_constraints → frameworks (array)
  extraction_rule: "Join array as comma-separated string"
  example: "Next.js, Express.js, React Native"
  required: false
  validation: "Comma-separated framework names or empty string"

organizational_standards:
  source: discovery-summary.json → technical_constraints → organizational_standards
  extraction_rule: "Copy verbatim"
  example: "SOC 2 compliance required, SSO integration mandatory"
  required: false
  validation: "String or null"

# USER & MARKET VARIABLES

target_users:
  source: discovery-summary.json → target_users → primary_users (array)
  extraction_rule: "Join as comma-separated string or take first if multiple"
  example: "Engineering Managers, Senior Engineers"
  required: true
  validation: "Non-empty string describing user personas"

user_pain_points:
  source: discovery-summary.json → target_users → key_pain_points (array)
  extraction_rule: "Join first 3 as bullet list or comma-separated"
  example: "Context switching costs 2-3 hours/day, Missing critical updates, No single source of truth"
  required: true
  validation: "Non-empty string with pain point descriptions"

competitors:
  source: discovery-summary.json → competitive_landscape → competitors (array)
  extraction_rule: "Extract competitor names, join as comma-separated"
  example: "Linear, Asana, ClickUp"
  required: false
  validation: "Comma-separated names or empty string"

differentiation:
  source: discovery-summary.json → competitive_landscape → differentiation
  extraction_rule: "Copy verbatim, condense if > 200 chars"
  example: "Developer-first design with deep tool integrations and intelligent notification filtering"
  required: false
  validation: "String describing unique value proposition"

# INTEGRATION & TECHNICAL VARIABLES

required_integrations:
  source: discovery-summary.json → integration_requirements → systems (array)
  extraction_rule: "Extract system names, join as comma-separated"
  example: "GitHub, Slack, Jira"
  required: false
  validation: "Comma-separated integration names or empty string"

integration_protocols:
  source: discovery-summary.json → integration_requirements → systems → protocols (arrays)
  extraction_rule: "Extract unique protocols across all systems"
  example: "REST, Webhooks, OAuth 2.0"
  required: false
  validation: "Comma-separated protocol names or empty string"

# SUCCESS & CONSTRAINTS VARIABLES

success_metrics:
  source: discovery-summary.json → success_criteria → metrics (array)
  extraction_rule: "Join first 3 metrics as bullet list or comma-separated"
  example: "30% reduction in context switching, 80% reduction in missed updates, 50+ teams onboarded"
  required: false
  validation: "String describing measurable success metrics"

timeline_constraint:
  source: discovery-summary.json → business_goals → constraints → timeline
  extraction_rule: "Copy verbatim"
  example: "MVP in 4 months, beta in 6 months"
  required: false
  validation: "String describing timeline or null"

budget_constraint:
  source: discovery-summary.json → business_goals → constraints → budget
  extraction_rule: "Copy verbatim if present"
  example: "Seed stage funding, $500K runway"
  required: false
  validation: "String or null"

regulatory_constraints:
  source: discovery-summary.json → business_goals → constraints → regulatory
  extraction_rule: "Copy verbatim"
  example: "SOC 2 Type 1 compliance required, GDPR compliance for EU"
  required: false
  validation: "String or null"

# RESEARCH & VALIDATION VARIABLES

user_research_completed:
  source: discovery-summary.json → user_research_status → research_completed (array)
  extraction_rule: "Join as comma-separated string"
  example: "User interviews (15), Developer survey (90 responses)"
  required: false
  validation: "String or empty"

user_research_planned:
  source: discovery-summary.json → user_research_status → research_planned (array)
  extraction_rule: "Join as comma-separated string"
  example: "Prototype usability testing, Beta testing with 3 pilot teams"
  required: false
  validation: "String or empty"

validation_approach:
  source: discovery-summary.json → user_research_status → validation_approach
  extraction_rule: "Copy verbatim"
  example: "Beta program with 3 pilot teams to validate core workflow improvements"
  required: false
  validation: "String or null"

# MARKET CONTEXT VARIABLES

market_trends:
  source: discovery-summary.json → market_opportunities → trends (array)
  extraction_rule: "Join first 3 as comma-separated"
  example: "Remote work normalization, Developer tool consolidation, Async-first communication"
  required: false
  validation: "String or empty"

market_timing:
  source: discovery-summary.json → market_opportunities → timing_rationale
  extraction_rule: "Copy verbatim, condense if > 200 chars"
  example: "Post-pandemic remote work is permanent. Companies investing in productivity tools."
  required: false
  validation: "String or null"
```

## template-variables.json Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CODEX Template Variables",
  "description": "Extracted variables from discovery for use in templates",
  "type": "object",

  "required": [
    "project_name",
    "project_description",
    "target_platform",
    "primary_language",
    "target_users",
    "user_pain_points"
  ],

  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "extracted_at": {"type": "string", "format": "date-time"},
        "source_file": {"type": "string"},
        "workflow_id": {"type": "string"},
        "extraction_version": {"type": "string", "const": "1.0"}
      }
    },

    "core_project": {
      "type": "object",
      "required": ["project_name", "project_description"],
      "properties": {
        "project_name": {"type": "string", "minLength": 1, "maxLength": 50},
        "project_description": {"type": "string", "minLength": 1, "maxLength": 500}
      }
    },

    "platform_technology": {
      "type": "object",
      "required": ["target_platform", "primary_language"],
      "properties": {
        "target_platform": {"type": "string", "minLength": 1},
        "primary_language": {"type": "string", "minLength": 1},
        "secondary_languages": {"type": ["string", "null"]},
        "frameworks": {"type": ["string", "null"]},
        "organizational_standards": {"type": ["string", "null"]}
      }
    },

    "users_market": {
      "type": "object",
      "required": ["target_users", "user_pain_points"],
      "properties": {
        "target_users": {"type": "string", "minLength": 1},
        "user_pain_points": {"type": "string", "minLength": 1},
        "competitors": {"type": ["string", "null"]},
        "differentiation": {"type": ["string", "null"]}
      }
    },

    "integration_technical": {
      "type": "object",
      "properties": {
        "required_integrations": {"type": ["string", "null"]},
        "integration_protocols": {"type": ["string", "null"]}
      }
    },

    "success_constraints": {
      "type": "object",
      "properties": {
        "success_metrics": {"type": ["string", "null"]},
        "timeline_constraint": {"type": ["string", "null"]},
        "budget_constraint": {"type": ["string", "null"]},
        "regulatory_constraints": {"type": ["string", "null"]}
      }
    },

    "research_validation": {
      "type": "object",
      "properties": {
        "user_research_completed": {"type": ["string", "null"]},
        "user_research_planned": {"type": ["string", "null"]},
        "validation_approach": {"type": ["string", "null"]}
      }
    },

    "market_context": {
      "type": "object",
      "properties": {
        "market_trends": {"type": ["string", "null"]},
        "market_timing": {"type": ["string", "null"]}
      }
    }
  }
}
```

## Extraction Algorithm

### Step 1: Load Discovery Summary
```python
import json

# Load discovery summary
with open('.codex/state/discovery-summary.json', 'r') as f:
    discovery = json.load(f)
```

### Step 2: Extract Core Variables

```python
def extract_project_name(discovery):
    """Extract project name from project_scope content"""
    content = discovery.get('project_scope', '')

    # Try to extract from first sentence
    # Pattern: "Building [ProjectName]," or "[ProjectName] is a..."
    import re

    # Pattern 1: "Building X" or "Creating X"
    match = re.search(r'(?:Building|Creating)\s+([A-Z][a-zA-Z0-9]+)', content)
    if match:
        return match.group(1)

    # Pattern 2: "[Name] is a" at start
    match = re.search(r'^([A-Z][a-zA-Z0-9]+)\s+is\s+a', content)
    if match:
        return match.group(1)

    # Fallback: Ask user or use "MyProject"
    return "MyProject"

def extract_platforms(discovery):
    """Extract target platforms from technical_constraints"""
    platforms = discovery.get('technical_constraints', {}).get('platforms', [])

    if not platforms:
        return "Web"  # Default

    if len(platforms) == 1:
        return platforms[0]

    return ", ".join(platforms)

def extract_languages(discovery):
    """Extract primary and secondary languages"""
    languages = discovery.get('technical_constraints', {}).get('languages', [])

    if not languages:
        return "TypeScript", None

    primary = languages[0]
    secondary = ", ".join(languages[1:]) if len(languages) > 1 else None

    return primary, secondary
```

### Step 3: Build Variables Object

```python
def build_template_variables(discovery):
    """Build complete template variables object"""

    project_name = extract_project_name(discovery)
    primary_lang, secondary_langs = extract_languages(discovery)

    variables = {
        "metadata": {
            "extracted_at": datetime.utcnow().isoformat() + "Z",
            "source_file": ".codex/state/discovery-summary.json",
            "workflow_id": discovery.get('discovery_metadata', {}).get('workflow_id', 'unknown'),
            "extraction_version": "1.0"
        },

        "core_project": {
            "project_name": project_name,
            "project_description": extract_description(discovery['project_scope'])
        },

        "platform_technology": {
            "target_platform": extract_platforms(discovery),
            "primary_language": primary_lang,
            "secondary_languages": secondary_langs,
            "frameworks": join_array(discovery, 'technical_constraints.frameworks'),
            "organizational_standards": discovery.get('technical_constraints', {}).get('organizational_standards')
        },

        "users_market": {
            "target_users": join_array(discovery, 'target_users.primary_users'),
            "user_pain_points": join_array(discovery, 'target_users.key_pain_points', limit=3),
            "competitors": extract_competitor_names(discovery),
            "differentiation": discovery.get('competitive_landscape', {}).get('differentiation')
        },

        "integration_technical": {
            "required_integrations": extract_integration_names(discovery),
            "integration_protocols": extract_unique_protocols(discovery)
        },

        "success_constraints": {
            "success_metrics": join_array(discovery, 'success_criteria.metrics', limit=3),
            "timeline_constraint": discovery.get('business_goals', {}).get('constraints', {}).get('timeline'),
            "budget_constraint": discovery.get('business_goals', {}).get('constraints', {}).get('budget'),
            "regulatory_constraints": discovery.get('business_goals', {}).get('constraints', {}).get('regulatory')
        },

        "research_validation": {
            "user_research_completed": join_array(discovery, 'user_research_status.research_completed'),
            "user_research_planned": join_array(discovery, 'user_research_status.research_planned'),
            "validation_approach": discovery.get('user_research_status', {}).get('validation_approach')
        },

        "market_context": {
            "market_trends": join_array(discovery, 'market_opportunities.trends', limit=3),
            "market_timing": condense(discovery.get('market_opportunities', {}).get('timing_rationale'), 200)
        }
    }

    return variables
```

### Step 4: Save to State

```python
def save_template_variables(variables):
    """Save to .codex/state/template-variables.json"""

    # Validate against schema
    validate_schema(variables, schema)

    # Write to file
    output_path = '.codex/state/template-variables.json'
    with open(output_path, 'w') as f:
        json.dump(variables, f, indent=2)

    # Update workflow.json
    update_workflow_state({
        'template_variables_extracted': True,
        'template_variables_path': output_path
    })
```

## Template Usage

### In YAML Templates

Templates can reference variables in their sections:

```yaml
# project-brief-template.yaml

- id: project-overview
  title: Project Overview
  type: structured
  elicit: true
  content: |
    Project Name: {{var:project_name}}
    Description: {{var:project_description}}

    Target Platform: {{var:target_platform}}
    Primary Language: {{var:primary_language}}

    Target Users: {{var:target_users}}
    Key Pain Points:
    {{var:user_pain_points}}
```

### Variable Substitution Engine

```python
def substitute_variables(template_content, variables):
    """Replace {{var:name}} with actual values"""

    import re

    def replace_var(match):
        var_path = match.group(1)  # e.g., "project_name"

        # Navigate nested structure
        value = get_nested_value(variables, var_path)

        if value is None:
            return f"[{var_path} NOT FOUND]"

        return str(value)

    # Replace all {{var:...}} patterns
    result = re.sub(r'\{\{var:([a-z_\.]+)\}\}', replace_var, template_content)

    return result

def get_nested_value(obj, path):
    """Get value from nested dict using dot notation"""
    # e.g., "core_project.project_name"
    parts = path.split('.')

    for part in parts:
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            return None

    return obj
```

## Integration Points

### 1. Discovery Phase → Extract Variables

After `persist-discovery-summary.md` executes:
```yaml
discovery_finalize:
  - Execute persist-discovery-summary.md
  - Discovery-summary.json created
  - Execute template-variable-extraction
  - Template-variables.json created
  - Update workflow.json
```

### 2. Analyst Phase → Use Variables

When analyst creates project-brief:
```yaml
analyst_create_brief:
  - Load template-variables.json
  - Load project-brief-template.yaml
  - Substitute {{var:...}} with actual values
  - Present pre-populated template to user
  - User reviews and refines via elicitation
```

### 3. PM Phase → Use Variables

When PM creates PRD:
```yaml
pm_create_prd:
  - Load template-variables.json
  - Auto-populate PRD sections:
    - Project name
    - Target users
    - Success metrics
    - Platform constraints
  - User refines via elicitation
```

### 4. Architect Phase → Use Variables

When architect creates architecture document:
```yaml
architect_create_arch:
  - Load template-variables.json
  - Auto-populate architecture sections:
    - Technology stack (languages, frameworks)
    - Platform targets
    - Integration requirements
    - Constraints
  - User refines via elicitation
```

## Execution Timing

**When to Extract Variables:**
1. After discovery finalization (Task 12: persist-discovery-summary)
2. Before analyst phase begins
3. Can be re-executed if discovery is updated

**State Updates:**
```json
{
  "workflow.json": {
    "template_variables_extracted": true,
    "template_variables_path": ".codex/state/template-variables.json",
    "template_variables_timestamp": "2025-10-07T23:55:00Z"
  }
}
```

## Validation Rules

### Required Variables Validation
```python
required_vars = [
    'core_project.project_name',
    'core_project.project_description',
    'platform_technology.target_platform',
    'platform_technology.primary_language',
    'users_market.target_users',
    'users_market.user_pain_points'
]

def validate_required(variables):
    """Ensure all required variables are present and non-empty"""
    for var_path in required_vars:
        value = get_nested_value(variables, var_path)
        if not value or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"Required variable {var_path} is missing or empty")
```

### Schema Validation
```python
import jsonschema

def validate_schema(variables, schema):
    """Validate against JSON schema"""
    try:
        jsonschema.validate(variables, schema)
    except jsonschema.ValidationError as e:
        raise ValueError(f"Template variables schema validation failed: {e.message}")
```

## Example Output

```json
{
  "metadata": {
    "extracted_at": "2025-10-07T23:55:00Z",
    "source_file": ".codex/state/discovery-summary.json",
    "workflow_id": "codex-20251007-235000",
    "extraction_version": "1.0"
  },

  "core_project": {
    "project_name": "TaskHub",
    "project_description": "A task management app for remote teams that solves the problem of scattered communication across multiple tools."
  },

  "platform_technology": {
    "target_platform": "Web, iOS, Android",
    "primary_language": "TypeScript",
    "secondary_languages": "Swift, Kotlin",
    "frameworks": "Next.js, Express.js, React Native",
    "organizational_standards": "SOC 2 compliance required, SSO integration mandatory"
  },

  "users_market": {
    "target_users": "Engineering Managers, Senior Engineers, Remote Team Leads",
    "user_pain_points": "Critical updates buried in Slack threads, Context switching costs 2-3 hours/day, No single source of truth for task status",
    "competitors": "Linear, Asana, ClickUp",
    "differentiation": "Developer-first design with deep tool integrations and intelligent notification filtering"
  },

  "integration_technical": {
    "required_integrations": "GitHub, Slack, Jira",
    "integration_protocols": "REST, Webhooks, OAuth 2.0"
  },

  "success_constraints": {
    "success_metrics": "30% reduction in context switching, 80% reduction in missed updates, 50+ teams onboarded in 6 months",
    "timeline_constraint": "MVP in 4 months, beta in 6 months, enterprise-ready in 9 months",
    "budget_constraint": "Seed stage funding, $500K runway",
    "regulatory_constraints": "SOC 2 Type 1 before enterprise sales, GDPR compliance for EU"
  },

  "research_validation": {
    "user_research_completed": "User interviews (15), Developer survey (90 responses)",
    "user_research_planned": "Prototype usability testing with 20 users, Beta testing with 3 pilot teams",
    "validation_approach": "Beta program with 3 pilot teams to validate core workflow improvements"
  },

  "market_context": {
    "market_trends": "Remote work normalization, Developer tool consolidation, Async-first communication",
    "market_timing": "Post-pandemic remote work is permanent. Companies investing in productivity tools."
  }
}
```

## Success Criteria

- [ ] Protocol documented in `.codex/data/template-variable-extraction-protocol.md`
- [ ] Variable mapping from discovery-summary.json to template-variables.json defined
- [ ] JSON schema for template-variables.json specified
- [ ] Extraction algorithm documented with code examples
- [ ] Template usage syntax defined ({{var:name}})
- [ ] Integration points with workflow phases specified
- [ ] Validation rules defined
- [ ] Example output provided

---

**Implementation Time**: 3 hours (PRP estimate)
**Dependencies**: Task 12 (persist-discovery-summary.md), discovery-summary.json
**Enables**: Task 14 (project-brief-template restoration with auto-population)
