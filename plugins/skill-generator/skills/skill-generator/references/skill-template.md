# Skill Template for Generated Skills

Use this template when generating Claude skills from GitHub repositories.

## Progressive Disclosure Principle

**Keep SKILL.md lean.** The context window is a shared resource. Only include what Claude truly needs.

**Three-level loading:**
1. **Metadata** (name + description) - Always loaded (~100 tokens)
2. **SKILL.md body** - Loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** - Loaded as needed (references/, examples/, scripts/, assets/)

**Key rules:**
- Challenge each paragraph: "Does Claude really need this?"
- Keep SKILL.md under 500 lines - move details to `references/`
- Prefer concise examples over verbose explanations
- Don't duplicate info between SKILL.md and reference files
- For complex APIs, put detailed docs in `references/api-reference.md`
- Avoid deep reference chains (link only one level from SKILL.md)
- Add a table of contents to reference files longer than 100 lines
- If a reference file exceeds ~10k words, include grep search patterns
- Use `scripts/` for repeatable transforms and `assets/` for templates when needed

## Structure Selection

Choose the primary layout based on the repo and target tasks:
- **Workflow-based** for sequential processes
- **Task-based** for tool collections
- **Reference/guidelines** for standards or specs
- **Capabilities-based** for integrated systems

## SKILL.md Template

```markdown
---
name: {skill-name}
description: {Comprehensive description explaining what this skill does and when to use it. Include specific trigger phrases like "use {library} to", "create {thing} with", etc. Max 1024 characters.}
---

# {Library/Tool Name}

{One-paragraph overview of what this library/tool does and its primary value proposition.}

## When to Use This Skill

Use this skill when:
- {Specific use case 1}
- {Specific use case 2}
- {Specific use case 3}
- {Additional use cases...}

## Installation

{Platform-specific installation instructions}

### npm/yarn (for JS libraries)
\`\`\`bash
npm install {package-name}
# or
yarn add {package-name}
\`\`\`

### pip (for Python libraries)
\`\`\`bash
pip install {package-name}
\`\`\`

### CDN (for browser libraries)
\`\`\`html
<script src="{cdn-url}"></script>
\`\`\`

## Quick Start

### Basic Usage

\`\`\`{language}
{Minimal working example showing import and basic usage}
\`\`\`

### Common Workflow

\`\`\`{language}
{More complete example showing typical real-world usage}
\`\`\`

## Core API Reference

### {Main Function/Class 1}

\`\`\`{language}
{Function signature or class definition}
\`\`\`

**Parameters:**
- `{param1}` ({type}): {Description}
- `{param2}` ({type}, optional): {Description}. Default: `{default}`

**Returns:** {Return type and description}

**Example:**
\`\`\`{language}
{Usage example}
\`\`\`

### {Main Function/Class 2}

{Repeat pattern for other key APIs}

## Examples

### Example 1: {Basic Use Case}

{Description of what this example demonstrates}

\`\`\`{language}
{Complete working code}
\`\`\`

### Example 2: {Real-World Workflow}

{Description of practical application}

\`\`\`{language}
{Complete working code}
\`\`\`

### Example 3: {Troubleshooting/Edge Case}

{Description of handling common issues}

\`\`\`{language}
{Code showing error handling or edge case}
\`\`\`

## Configuration Options

{If the library has configuration:}

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `{option1}` | {type} | `{default}` | {Description} |
| `{option2}` | {type} | `{default}` | {Description} |

## Safety and Limitations

### Limitations
- {Limitation 1}
- {Limitation 2}

### Known Issues
- {Known issue 1}
- {Known issue 2}

### Best Practices
- {Best practice 1}
- {Best practice 2}

## How It Works

{High-level explanation of the library's approach/architecture, 2-3 paragraphs max}

## Required Tools and Permissions

- **Tools needed**: {List of Claude tools required - Bash, Write, etc.}
- **Environment**: {Runtime requirements - Node.js version, Python version, etc.}
- **Permissions**: {Any special permissions needed}

## Additional Resources

- [Official Documentation]({docs-url})
- [GitHub Repository]({github-url})
- [Examples]({examples-url})
```

Only include `name` and `description` in frontmatter unless the user explicitly requests additional fields.

## Naming Conventions

### Skill Name
- Use kebab-case: `anime-js`, `lodash-utils`, `python-requests`
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- Must not contain: "anthropic", "claude"
- Should be recognizable to users

### Good Examples
- `anime-js` - Clear library name
- `pdf-processing` - Descriptive purpose
- `react-testing-library` - Full library name

### Bad Examples
- `anime` - Too generic, could conflict
- `AnimeJS` - Wrong case
- `anime_js` - Underscores not allowed
- `my-cool-animation-library-for-claude` - Too long

## Description Guidelines

### Structure
```
{What it does} + {When to use it with trigger phrases}
```

### Good Example
```yaml
description: Create smooth JavaScript animations with anime.js. Use this skill when the user asks to "animate elements", "create CSS animations", "tween properties", "build animation sequences", or work with motion graphics in web applications.
```

### Bad Example
```yaml
description: Animation library.
```

### Trigger Phrase Patterns
- "use {library} to"
- "create {thing} with"
- "how to {action} using"
- "help me {task}"
- "{specific feature}"

## Content Guidelines

### Use Cases Section
List 3-8 specific use cases with bullet points. Be concrete:
- Good: "Animate DOM element properties (opacity, transform, colors)"
- Bad: "Do animations"

### Examples Section
Include at least 3 examples:
1. **Basic** - Minimal working code
2. **Real-world** - Practical application
3. **Troubleshooting** - Error handling or edge case

### API Reference
- Focus on most-used APIs (80/20 rule)
- Include type signatures
- Show brief examples for each

### Limitations Section
Be honest about:
- What the library can't do
- Known bugs or issues
- Performance considerations
- Platform limitations

## Quality Checklist

Before finalizing a generated skill:

- [ ] Name is valid (kebab-case, max 64 chars, no reserved words)
- [ ] Description is comprehensive (max 1024 chars)
- [ ] Description includes trigger phrases
- [ ] Frontmatter uses only `name` and `description` unless explicitly requested
- [ ] Installation instructions are correct
- [ ] Quick start example works
- [ ] At least 3 examples included
- [ ] API reference covers main functions
- [ ] Limitations are documented
- [ ] References have TOC if long and no deep reference chains
- [ ] All code examples are syntactically correct
- [ ] External links are valid
