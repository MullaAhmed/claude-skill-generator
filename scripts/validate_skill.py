#!/usr/bin/env python3
"""
Skill Validation Utility for github-to-skill plugin.

Validates generated skills against Anthropic skills conventions:
- YAML frontmatter presence and format
- Required fields (name, description)
- Field length limits (name: 64 chars, description: 1024 chars)
- Naming conventions (lowercase, hyphens only)
- Reserved word checking
- Content structure verification

Usage:
    python validate_skill.py <path_to_SKILL.md>
    python validate_skill.py <path_to_skill_directory>
"""

import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class ValidationIssue:
    """A single validation issue."""
    level: str  # "error" or "warning"
    field: str
    message: str


@dataclass
class ValidationResult:
    """Result of skill validation."""
    valid: bool
    skill_path: str
    name: Optional[str]
    description: Optional[str]
    issues: list
    warnings: list


# Anthropic skills constraints
NAME_MAX_LENGTH = 64
DESCRIPTION_MAX_LENGTH = 1024
RESERVED_WORDS = ["anthropic", "claude"]
NAME_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$')

# Allowed frontmatter properties (per Anthropic's skill-creator)
ALLOWED_FRONTMATTER_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}


def _normalize_yaml_value(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _parse_simple_frontmatter(frontmatter_lines: list[str]) -> dict:
    """Fallback parser for simple key: value frontmatter."""
    frontmatter = {}
    current_key = None
    current_value_lines = []

    for line in frontmatter_lines:
        key_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$', line)
        if key_match:
            if current_key:
                value = "\n".join(current_value_lines)
                frontmatter[current_key] = _normalize_yaml_value(value)
            current_key = key_match.group(1)
            current_value_lines = [key_match.group(2)]
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            current_value_lines.append(line.strip())

    if current_key:
        value = "\n".join(current_value_lines)
        frontmatter[current_key] = _normalize_yaml_value(value)

    return frontmatter


def extract_frontmatter(content: str) -> tuple[Optional[dict], Optional[str], Optional[str]]:
    """
    Extract YAML frontmatter from markdown content.

    Args:
        content: Full markdown file content

    Returns:
        Tuple of (frontmatter_dict, body_content, error_message)
    """
    if not content.strip().startswith("---"):
        return None, content, "Missing YAML frontmatter (file must start with ---)"

    # Find the closing ---
    lines = content.split("\n")
    frontmatter_end = -1

    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            frontmatter_end = i
            break

    if frontmatter_end == -1:
        return None, content, "Invalid YAML frontmatter (missing closing ---)"

    frontmatter_lines = lines[1:frontmatter_end]
    frontmatter_text = "\n".join(frontmatter_lines)

    if yaml:
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            return None, content, f"Invalid YAML in frontmatter: {e}"
        if frontmatter is None:
            frontmatter = {}
        if not isinstance(frontmatter, dict):
            return None, content, "Frontmatter must be a YAML mapping"
    else:
        frontmatter = _parse_simple_frontmatter(frontmatter_lines)

    body = "\n".join(lines[frontmatter_end + 1:])

    return frontmatter, body, None


def validate_frontmatter_properties(frontmatter: dict) -> list[ValidationIssue]:
    """Validate that frontmatter only contains allowed properties."""
    issues = []

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_PROPERTIES
    if unexpected_keys:
        issues.append(ValidationIssue(
            "error",
            "frontmatter",
            f"Unexpected frontmatter properties: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_FRONTMATTER_PROPERTIES))}"
        ))

    return issues


def validate_name(name: Optional[str]) -> list[ValidationIssue]:
    """Validate the skill name field."""
    issues = []

    if not name:
        issues.append(ValidationIssue("error", "name", "Required field 'name' is missing"))
        return issues

    if not isinstance(name, str):
        issues.append(ValidationIssue("error", "name", f"Field 'name' must be a string, got {type(name).__name__}"))
        return issues

    # Length check
    if len(name) > NAME_MAX_LENGTH:
        issues.append(ValidationIssue("error", "name", f"Field 'name' exceeds {NAME_MAX_LENGTH} characters (got {len(name)})"))

    # Format check
    if not NAME_PATTERN.match(name):
        if name != name.lower():
            issues.append(ValidationIssue("error", "name", "Field 'name' must be lowercase"))
        elif " " in name:
            issues.append(ValidationIssue("error", "name", "Field 'name' cannot contain spaces (use hyphens)"))
        elif "_" in name:
            issues.append(ValidationIssue("warning", "name", "Field 'name' uses underscores (prefer hyphens for consistency)"))
        elif not re.match(r'^[a-z0-9-]+$', name):
            issues.append(ValidationIssue("error", "name", "Field 'name' must contain only lowercase letters, numbers, and hyphens"))

    # Reserved words check
    for reserved in RESERVED_WORDS:
        if reserved in name.lower():
            issues.append(ValidationIssue("error", "name", f"Field 'name' cannot contain reserved word '{reserved}'"))

    # XML tag check
    if "<" in name or ">" in name:
        issues.append(ValidationIssue("error", "name", "Field 'name' cannot contain XML tags"))

    return issues


def validate_description(description: Optional[str]) -> list[ValidationIssue]:
    """Validate the skill description field."""
    issues = []

    if not description:
        issues.append(ValidationIssue("error", "description", "Required field 'description' is missing"))
        return issues

    if not isinstance(description, str):
        issues.append(ValidationIssue("error", "description", f"Field 'description' must be a string, got {type(description).__name__}"))
        return issues

    # Empty check
    if not description.strip():
        issues.append(ValidationIssue("error", "description", "Field 'description' cannot be empty"))
        return issues

    # Length check
    if len(description) > DESCRIPTION_MAX_LENGTH:
        issues.append(ValidationIssue("error", "description", f"Field 'description' exceeds {DESCRIPTION_MAX_LENGTH} characters (got {len(description)})"))

    # XML tag check
    if "<" in description or ">" in description:
        issues.append(ValidationIssue("error", "description", "Field 'description' cannot contain XML tags"))

    # Quality checks (warnings)
    if len(description) < 50:
        issues.append(ValidationIssue("warning", "description", "Field 'description' is quite short - consider adding more detail"))

    # Check for trigger phrases (best practice)
    trigger_indicators = ["when", "use this", "should be used", "helps with", "for"]
    has_trigger = any(indicator in description.lower() for indicator in trigger_indicators)
    if not has_trigger:
        issues.append(ValidationIssue("warning", "description", "Description lacks trigger phrases - consider explaining when to use this skill"))

    return issues


def validate_body(body: str) -> list[ValidationIssue]:
    """Validate the markdown body content."""
    issues = []

    if not body or not body.strip():
        issues.append(ValidationIssue("error", "body", "Skill body content is empty"))
        return issues

    # Word count check
    word_count = len(body.split())
    if word_count < 100:
        issues.append(ValidationIssue("warning", "body", f"Skill body is quite short ({word_count} words) - consider adding more detail"))
    elif word_count > 5000:
        issues.append(ValidationIssue("warning", "body", f"Skill body is very long ({word_count} words) - consider moving details to references/"))

    # Check for examples or task/workflow guidance
    body_lower = body.lower()
    example_markers = [
        "## example",
        "### example",
        "example:",
        "examples",
        "core tasks",
        "workflow"
    ]
    if not any(marker in body_lower for marker in example_markers):
        issues.append(ValidationIssue(
            "warning",
            "body",
            "No examples or task/workflow guidance found - consider adding short examples or task steps"
        ))

    return issues


def validate_skill_file(file_path: str) -> ValidationResult:
    """
    Validate a SKILL.md file.

    Args:
        file_path: Path to the SKILL.md file

    Returns:
        ValidationResult with all findings
    """
    issues = []
    warnings = []

    # Check file exists
    if not os.path.exists(file_path):
        return ValidationResult(
            valid=False,
            skill_path=file_path,
            name=None,
            description=None,
            issues=[ValidationIssue("error", "file", f"File not found: {file_path}")],
            warnings=[]
        )

    # Read file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return ValidationResult(
            valid=False,
            skill_path=file_path,
            name=None,
            description=None,
            issues=[ValidationIssue("error", "file", f"Failed to read file: {e}")],
            warnings=[]
        )

    # Parse frontmatter
    frontmatter, body, fm_error = extract_frontmatter(content)
    if fm_error:
        return ValidationResult(
            valid=False,
            skill_path=file_path,
            name=None,
            description=None,
            issues=[ValidationIssue("error", "frontmatter", fm_error)],
            warnings=[]
        )

    if yaml is None:
        warnings.append(ValidationIssue(
            "warning",
            "frontmatter",
            "PyYAML not installed; using simplified parser. Install PyYAML for full YAML support."
        ))

    # Validate frontmatter properties
    fm_property_issues = validate_frontmatter_properties(frontmatter)

    # Validate name
    name = frontmatter.get("name")
    name_issues = validate_name(name)

    # Validate description
    description = frontmatter.get("description")
    desc_issues = validate_description(description)

    # Validate body
    body_issues = validate_body(body or "")

    # Separate errors and warnings
    all_issues = fm_property_issues + name_issues + desc_issues + body_issues
    for issue in all_issues:
        if issue.level == "error":
            issues.append(issue)
        else:
            warnings.append(issue)

    return ValidationResult(
        valid=len(issues) == 0,
        skill_path=file_path,
        name=name,
        description=description[:100] + "..." if description and len(description) > 100 else description,
        issues=issues,
        warnings=warnings
    )


def validate_skill_directory(dir_path: str) -> ValidationResult:
    """
    Validate a skill directory.

    Args:
        dir_path: Path to the skill directory

    Returns:
        ValidationResult with all findings
    """
    skill_md_path = os.path.join(dir_path, "SKILL.md")

    if not os.path.exists(skill_md_path):
        return ValidationResult(
            valid=False,
            skill_path=dir_path,
            name=None,
            description=None,
            issues=[ValidationIssue("error", "structure", f"No SKILL.md found in {dir_path}")],
            warnings=[]
        )

    result = validate_skill_file(skill_md_path)

    # Additional directory checks
    additional_warnings = []

    # Check for common directories
    has_references = os.path.isdir(os.path.join(dir_path, "references"))
    has_examples = os.path.isdir(os.path.join(dir_path, "examples"))
    has_scripts = os.path.isdir(os.path.join(dir_path, "scripts"))

    # Check if SKILL.md references files that don't exist
    try:
        with open(skill_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for references to files
        file_refs = re.findall(r'`([^`]+\.(md|py|sh|json))`', content)
        for ref, _ in file_refs:
            ref_path = os.path.join(dir_path, ref)
            if not os.path.exists(ref_path):
                additional_warnings.append(
                    ValidationIssue("warning", "references", f"Referenced file not found: {ref}")
                )
    except Exception:
        pass

    result.warnings.extend(additional_warnings)
    return result


def result_to_json(result: ValidationResult) -> str:
    """Convert ValidationResult to JSON string."""
    return json.dumps({
        "valid": result.valid,
        "skill_path": result.skill_path,
        "name": result.name,
        "description": result.description,
        "errors": [
            {"field": i.field, "message": i.message}
            for i in result.issues
        ],
        "warnings": [
            {"field": i.field, "message": i.message}
            for i in result.warnings
        ]
    }, indent=2)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]

    if os.path.isfile(path):
        result = validate_skill_file(path)
    elif os.path.isdir(path):
        result = validate_skill_directory(path)
    else:
        print(json.dumps({
            "valid": False,
            "error": f"Path not found: {path}"
        }))
        sys.exit(1)

    print(result_to_json(result))
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
