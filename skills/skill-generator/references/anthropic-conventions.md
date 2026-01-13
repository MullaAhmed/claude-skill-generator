# Anthropic Skills Ecosystem Conventions

Comprehensive reference for creating skills compatible with the Anthropic skills ecosystem.

## Skill Architecture

### Three-Level Progressive Disclosure

Skills use progressive loading to manage context efficiently:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| **Level 1: Metadata** | Always (at startup) | ~100 tokens | `name` and `description` from YAML frontmatter |
| **Level 2: Instructions** | When skill triggers | <5k tokens | SKILL.md body with instructions |
| **Level 3: Resources** | As needed | Unlimited | Bundled files (references/, examples/, scripts/) |

### Directory Structure

```
skill-name/
├── SKILL.md           # Required: Main skill file
├── references/        # Optional: Detailed documentation
│   ├── api-reference.md
│   └── advanced-usage.md
├── examples/          # Optional: Working code examples
│   ├── basic-example.js
│   └── advanced-example.js
├── scripts/           # Optional: Utility scripts
│   └── helper.py
└── assets/            # Optional: Template files, images
    └── template.html
```

## YAML Frontmatter Requirements

### Required Fields

```yaml
---
name: skill-name
description: Skill description with trigger phrases
---
```

Default to only `name` and `description`. Only include optional fields if the user explicitly requests them or the target platform requires them.
The `description` is the primary trigger mechanism, so include "when to use" details here instead of relying on body sections.

### Field Constraints

#### `name` Field
- **Max length**: 64 characters
- **Format**: Lowercase letters, numbers, hyphens only
- **Pattern**: `^[a-z0-9][a-z0-9-]*[a-z0-9]$` or single character `^[a-z0-9]$`
- **Forbidden**: XML tags (`<`, `>`)
- **Reserved words**: Cannot contain "anthropic" or "claude"

#### `description` Field
- **Max length**: 1024 characters
- **Format**: Non-empty string
- **Forbidden**: XML tags (`<`, `>`)
- **Best practice**: Include specific trigger phrases

### Optional Fields (only if explicitly requested)

```yaml
---
name: skill-name
description: Skill description
version: 1.0.0
author: Author Name
category: Development & Technical
tags:
  - javascript
  - animation
  - frontend
---
```

Avoid adding optional fields by default; most generated skills should include only `name` and `description`.
If a license needs to be captured, prefer referencing it in the body or resources unless the user explicitly requests a frontmatter field.

## Skill Categories

Official categories in the Anthropic skills ecosystem:

1. **Creative & Design** - Art, music, design tasks
2. **Development & Technical** - Testing, MCP server generation, coding
3. **Enterprise & Communication** - Business workflows, branding
4. **Document Skills** - Document creation and editing (DOCX, PDF, PPTX, XLSX)

## Markdown Body Guidelines

### Writing Style
- Use **imperative/infinitive form** (verb-first instructions)
- Avoid second person ("you should")
- Be objective and instructional

### Good Examples
```markdown
Install the package using npm.
Configure the animation properties.
Call the animate() function with target elements.
```

### Bad Examples
```markdown
You should install the package using npm.
You need to configure the animation properties.
You can call the animate() function.
```

### Recommended Sections

```markdown
# Skill Name

{Overview paragraph}

## Quick Start
{Minimal working example}

## Core Workflows or Tasks
{Step-by-step guidance or task recipes}

## Examples
{Multiple working examples}

## Limitations
{Known limitations and caveats}

## Companion Skills (optional)
{1-3 related skills from the Anthropic skills ecosystem and why they help}

## Additional Resources
{Links to references/ and examples/}
```

Choose sections that fit the task. "When to Use This Skill" can be included for readability, but it does not drive triggering.

### Length Guidelines
- **Target**: Keep SKILL.md concise and task-focused (often 300-1200 words)
- **Maximum**: 5,000 words
- **If longer**: Move detailed content to `references/`

## File Naming Conventions

### Skill Directory
- Use kebab-case: `anime-js`, `pdf-processing`
- Match the `name` field in frontmatter

### Supporting Files
- Use kebab-case with appropriate extensions
- Be descriptive: `api-reference.md`, not `ref.md`
- Group related files in subdirectories

### Reserved Names
Avoid these patterns:
- Starting with `.` (hidden files)
- `node_modules/`
- `__pycache__/`
- `.git/`

## Platform Support

### Claude.ai
- Custom skills uploaded as ZIP files
- Pre-built skills available automatically
- Individual user scope (not shared)

### Claude API
- Skills specified via `skill_id` parameter
- Organization-wide sharing
- Requires beta headers

### Claude Code
- Filesystem-based skills in `.claude/skills/`
- Auto-discovered by Claude Code
- Can be bundled with plugins

### Claude Agent SDK
- Skills in `.claude/skills/` directory
- Enable via `allowed_tools` configuration
- Auto-discovered at runtime

## Validation Rules

### Critical Errors (Skill Rejected)
- Missing SKILL.md file
- Missing/invalid frontmatter
- Missing `name` field
- Missing `description` field
- `name` exceeds 64 characters
- `description` exceeds 1024 characters
- Invalid `name` format (uppercase, spaces, underscores)
- Reserved words in `name`
- XML tags in `name` or `description`

### Warnings (Skill Accepted)
- Short description (<50 chars)
- No trigger phrases in description
- Very short body (<100 words)
- Very long body (>5000 words)
- Missing examples or task guidance
- Unreferenced files in directories

## Best Practices

### Description Quality
Include specific trigger phrases that users would say:

```yaml
# Good
description: Create smooth JavaScript animations with anime.js. Use when
  the user asks to "animate elements", "create CSS animations", "tween
  properties", or work with motion graphics.

# Bad
description: Animation library for JavaScript.
```

### Example Quality
Provide complete, runnable examples:

```javascript
// Good - Complete example
import anime from 'animejs';

anime({
  targets: '.element',
  translateX: 250,
  duration: 1000,
  easing: 'easeInOutQuad'
});

// Bad - Incomplete
anime({ targets: '.el' });
```

### Progressive Disclosure
Keep SKILL.md focused; move details to references/:

```
skill-name/
├── SKILL.md                    # Core concepts, quick start
└── references/
    ├── api-reference.md        # Detailed API docs
    ├── advanced-patterns.md    # Complex use cases
    └── troubleshooting.md      # Common issues
```

Additional guardrails:
- Avoid deep reference chains (link only one level from SKILL.md)
- Add a table of contents to reference files longer than 100 lines
- If a reference file exceeds ~10k words, include grep search patterns

### Avoid Extra Files
Do not add README, changelogs, or setup guides. Only include files that help Claude execute the task.

### Resource References
Clearly reference supporting files in SKILL.md:

```markdown
## Additional Resources

For detailed API documentation, see `references/api-reference.md`.
Working examples are available in `examples/`.
```

## Security Considerations

### What to Include
- Public API documentation
- Open-source code examples
- General best practices

### What to Avoid
- API keys or secrets
- Internal URLs or endpoints
- Proprietary algorithms
- Personal data

### External Resources
- Only reference HTTPS URLs
- Prefer official documentation
- Avoid URL shorteners
- Note that skills cannot make network requests in Claude API

## Quality Checklist

Before publishing a skill:

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name` is valid (lowercase, hyphens, max 64 chars)
- [ ] `description` is comprehensive (max 1024 chars)
- [ ] Frontmatter uses only `name` and `description` unless explicitly requested
- [ ] Description includes trigger phrases
- [ ] Body uses imperative form (not "you should")
- [ ] Body is concise and task-focused
- [ ] References have TOC if long and avoid deep reference chains
- [ ] Examples or task steps included where applicable
- [ ] Companion skills listed when clearly relevant
- [ ] All referenced files exist
- [ ] No sensitive data included
- [ ] Code examples are syntactically correct
