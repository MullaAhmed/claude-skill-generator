# Skill Template for Generated Skills

Use these templates when generating Claude skills from GitHub repositories. Choose the structure that fits the repo and the target tasks.

## Progressive Disclosure Principle

Keep SKILL.md lean. The description drives triggering, so include "when to use" information in the description itself. Put long API details, extended examples, or exhaustive references in `references/` and link to them.

Key rules:
- Keep SKILL.md under 500 lines; shorter is better.
- Prefer task instructions and decision points over full API dumps.
- Avoid duplicate information across SKILL.md and reference files.
- For long references, add a table of contents at the top.

## Structure Selection

Pick the structure that matches the repo and the tasks:
- **Task-based** for libraries and SDKs (default).
- **Workflow-based** for sequential, multi-step processes.
- **Reference/guidelines** for standards or specs.
- **Capabilities-based** for systems with multiple independent abilities.

## Companion Skills (optional)

If the repo clearly overlaps with an existing Anthropic skill, add a short "Companion Skills" section that points to 1-3 relevant skills and explains why they help. Only include this section when there is a clear, practical benefit.

Quick mapping hints:
- Frontend/UI work: `frontend-design`, `web-artifacts-builder`, `webapp-testing`
- MCP servers or tool integrations: `mcp-builder`
- Document workflows: `docx`, `pdf`, `pptx`, `xlsx`
- Branding or themes: `brand-guidelines`, `theme-factory`
- Internal comms/content templates: `internal-comms`
- GIF/animation assets: `slack-gif-creator`
- Generative art: `algorithmic-art`

## SKILL.md Templates

### Task-based (recommended default for libraries and SDKs)

```markdown
---
name: {skill-name}
description: {What it does + when to use + 4-6 trigger phrases in quotes. Max 1024 chars.}
---

# {Library/Tool Name}

{1-2 sentence overview of purpose and scope.}

## Quick Start

{Install command or prerequisite setup, then minimal working example.}

## Core Tasks

### Task: {Task name}
Goal: {What this task accomplishes.}
Steps:
1. {Step 1}
2. {Step 2}
3. {Step 3}

Example:
```{language}
{Minimal, working example}
```

### Task: {Task name}
{Repeat for 2-5 tasks total.}

## API Cheat Sheet (optional)
- `{functionOrClass}`: {What it does and key params}
- `{functionOrClass}`: {What it does and key params}

## Pitfalls and Limits
- {Limitation or common pitfall}
- {Performance or platform constraint}

## Companion Skills (optional)
- `{skill-name}`: {Why it helps}
- `{skill-name}`: {Why it helps}

## Resources
- {Link to references/ files if created}
- {Official docs URL}
- {GitHub repo URL}
- {License if needed}
```

### Workflow-based

```markdown
---
name: {skill-name}
description: {What it does + when to use + trigger phrases.}
---

# {Skill Name}

{Brief overview.}

## Workflow
1. {Step 1}
2. {Step 2}
3. {Step 3}

## Decision Points
- If {condition}, then {action}
- If {condition}, then {action}

## Examples
{1-3 short examples that map to the workflow}

## Pitfalls and Limits
- {Known issue}

## Companion Skills (optional)
- `{skill-name}`: {Why it helps}

## Resources
- {References and links}
```

### Reference/guidelines

```markdown
---
name: {skill-name}
description: {What it does + when to use + trigger phrases.}
---

# {Skill Name}

## Scope
{What this covers and what it does not cover.}

## Rules and Guidelines
- {Rule 1}
- {Rule 2}

## Examples
- {Example 1}
- {Example 2}

## Companion Skills (optional)
- `{skill-name}`: {Why it helps}

## Resources
- {References and links}
```

### Capabilities-based

```markdown
---
name: {skill-name}
description: {What it does + when to use + trigger phrases.}
---

# {Skill Name}

## Capabilities
- {Capability 1}
- {Capability 2}
- {Capability 3}

## How to Choose
{Guidance for selecting which capability to use.}

## Examples
{1-3 short examples}

## Companion Skills (optional)
- `{skill-name}`: {Why it helps}

## Resources
- {References and links}
```

## Description Guidelines

The description is the trigger. Include concrete phrases users would say.

Good:
```yaml
description: Create smooth JavaScript animations with anime.js. Use when asked to "animate elements", "tween properties", "build timelines", "animate SVG", or "create motion graphics" in web apps.
```

Bad:
```yaml
description: Animation library.
```

## Content Guidelines

- Focus on tasks and workflows, not exhaustive API coverage.
- Provide 2-5 concrete tasks with working examples.
- Keep Quick Start runnable and minimal.
- Add an API cheat sheet only for the most-used functions.
- Move deep API docs to `references/api-reference.md`.
- Avoid large "When to Use" sections in the body; triggering comes from description.
- Add a Companion Skills section only when it materially helps the user.

## Quality Checklist

- [ ] `name` is valid (kebab-case, max 64 chars)
- [ ] Description includes clear "when to use" triggers
- [ ] SKILL.md is concise and task-focused
- [ ] Examples are minimal and syntactically correct
- [ ] Limitations and pitfalls are documented
- [ ] References are linked if created
- [ ] Companion skills listed when clearly relevant
