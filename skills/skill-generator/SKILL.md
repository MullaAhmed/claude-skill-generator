---
name: skill-generator
description: This skill should be used when the user asks to "create a skill for [github-url]", "convert a GitHub repo to a skill", "generate a Claude skill from GitHub", "make a skill from this repository", or mentions converting GitHub libraries/tools into Anthropic skills. Provides comprehensive guidance for the GitHub-to-skill conversion pipeline.
---

# Skill Generator

Convert public GitHub repositories into Claude skills compatible with the Anthropic skills ecosystem. This skill guides the complete pipeline from URL verification through skill generation.

## Pipeline Overview

The conversion follows a deterministic 12-step pipeline:

1. **URL Parsing & Validation** - Extract owner/repo, validate format
2. **Repository Verification** - Verify via GitHub API, collect metadata
3. **Codewiki URL Generation** - Create documentation URL
4. **Documentation Ingestion** - Fetch docs via WebFetch/Firecrawl
5. **Target Task Collection** - Ask for example tasks if docs are thin
6. **Web Search Enrichment** - Find additional context and examples
7. **Repository Analysis** - Understand purpose, APIs, usage patterns
8. **Skills Ecosystem Check** - Verify no duplicates exist
9. **Skill Structure Selection** - Choose workflow/task/reference/capabilities layout
10. **Skill Generation** - Create ready-to-commit skill files
11. **Validation** - Validate against conventions
12. **Packaging (optional)** - Create a `.skill` file if requested

## Step-by-Step Execution

### Step 1: Parse and Validate GitHub URL

Use the Python utility script for deterministic URL parsing:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/github_utils.py parse "<github_url>"
```

Expected output on success:
```json
{
  "success": true,
  "owner": "juliangarnier",
  "repo": "anime",
  "normalized_url": "https://github.com/juliangarnier/anime"
}
```

Handle common URL issues:
- Missing `https://` prefix
- Trailing slashes or `.git` suffix
- URLs pointing to specific files/branches (reject these)

### Step 2: Verify Repository via GitHub API

Run full verification to check repository exists and collect metadata:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/github_utils.py full "<github_url>"
```

This returns:
- `full_name`, `description`, `default_branch`
- `topics`, `license`, `homepage`
- `stargazers_count`, `fork`, `archived`
- `language`, `created_at`, `updated_at`

**Important metadata checks:**
- If `archived: true`, warn user the repo is archived
- If `fork: true`, note this is a fork of another repository
- Record `license` for attribution in generated skill

### Step 3: Generate Codewiki URL

The Codewiki URL is generated deterministically:

```
https://codewiki.google/github.com/{owner}/{repo}
```

Both URLs (GitHub and Codewiki) must appear in the final output.

### Step 4: Documentation Ingestion

#### Primary: WebFetch from Codewiki

Use WebFetch to extract documentation from the Codewiki URL:

```
WebFetch URL: https://codewiki.google/github.com/{owner}/{repo}
Prompt: Extract all documentation including: README content, API references,
installation instructions, usage examples, and any docs/ content.
Preserve code examples and configuration snippets.
```

#### Fallback: Direct GitHub README

If Codewiki fails, fetch the raw README:

```
WebFetch URL: https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/README.md
Prompt: Extract the complete README documentation.
```

#### Alternative: Firecrawl MCP (if configured)

If Firecrawl MCP server is available, use it for more comprehensive scraping:

```
firecrawl_scrape URL: https://codewiki.google/github.com/{owner}/{repo}
```

#### Also fetch official docs if available

If the GitHub metadata includes a `homepage` or the README links to official documentation, fetch those pages too:
- Prefer the official docs site over mirrors
- Extract API signatures, examples, and usage notes
- Keep the official docs URL for the Resources section

### Step 5: Collect Target Tasks (if needed)

If documentation is sparse or the repo purpose is ambiguous, ask for 2-3 concrete tasks and example user prompts. Use the answers to:
- Add trigger phrases to the `description`
- Build realistic Examples sections
- Decide what should be in `references/`, `scripts/`, or `assets/`

### Step 6: Web Search Enrichment

Use WebSearch to find additional context:

**Search queries to run:**
1. `"{repo_name}" tutorial example usage`
2. `"{repo_name}" documentation official`
3. `"{repo_name}" common issues pitfalls`
4. `"{repo_name}" integration example`

**Extract from search results:**
- Official documentation site URL (if different from GitHub)
- Common usage patterns and best practices
- Known limitations or caveats
- Community examples and integrations
- Framework-specific integration guides

**Store sources for citation** in reasoning notes.

### Step 7: Repository Analysis

Synthesize collected information into a technical understanding:

**For libraries:**
```markdown
## Technical Summary
- **Purpose**: [What the library does]
- **Primary Use Cases**: [3-5 bullet points]
- **Key APIs/Functions**: [Main exports and methods]
- **Platforms**: [Supported environments]
- **Dependencies**: [Required packages]
- **Inputs/Outputs**: [What it accepts and returns]
- **Common Pitfalls**: [Known gotchas or constraints]

## Minimal Working Example
[Show import + basic usage]
```

**For CLI tools:**
```markdown
## Technical Summary
- **Purpose**: [What the tool does]
- **Installation**: [How to install]
- **Key Commands**: [Main CLI commands]
- **Configuration**: [Config files/env vars]

## Minimal Working Example
[Show installation + basic command]
```

### Step 7.5: Classify Skill Type and Companion Skills

Determine what kind of skill this is (library, CLI tool, framework, spec, UI component set, integration, etc.). Use that classification to pick any companion skills that would materially help the user.

Rules:
- Only add companion skills if there is a clear, practical benefit.
- Limit to 1-3 companion skills.
- Use skill names from the Anthropic skills ecosystem (e.g., `frontend-design`, `web-artifacts-builder`, `webapp-testing`, `mcp-builder`, `docx`, `pdf`, `pptx`, `xlsx`, `brand-guidelines`, `theme-factory`, `internal-comms`, `slack-gif-creator`, `algorithmic-art`).
- If no companion skills are relevant, omit the section.

### Step 8: Skills Ecosystem Analysis

Before generating, check the Anthropic skills ecosystem:

1. Search existing skills for similar functionality
2. Review `anthropics/skills` repository structure
3. Determine if this should be:
   - A new skill
   - An enhancement to existing skill
   - Potentially duplicative (warn user)

### Step 9: Select Skill Structure

Choose a structure that matches the repo and target tasks:
- **Workflow-based** for sequential processes
- **Task-based** for tool collections
- **Reference/guidelines** for standards or specs
- **Capabilities-based** for integrated systems

State the chosen structure in SKILL.md headings and keep it consistent.

### Step 10: Generate Skill Files

Create skill files following Anthropic conventions. See `references/skill-template.md` for the complete template.

**Required structure:**
```
skill-name/
├── SKILL.md           # Required: Main skill file
├── references/        # Optional: Detailed docs
│   └── api-reference.md
├── examples/          # Optional: Working examples
│   └── basic-usage.md
├── scripts/           # Optional: Repeatable helpers
└── assets/            # Optional: Templates or bundled files
```

Include `scripts/` or `assets/` only when docs or user-provided inputs provide repeatable transforms or templates.

**SKILL.md requirements:**
- YAML frontmatter with `name` and `description` only (add other fields only if explicitly requested)
- `description` must include trigger phrases and "when to use" details
- Name: lowercase letters, numbers, hyphens only
- No reserved words: "anthropic", "claude"
- No XML tags in name or description
- Keep SKILL.md concise and task-focused; do not rely on a "When to Use" section for triggering
- Add a Companion Skills section only when relevant (1-3 skills, with reasons)
- Progressive disclosure:
  - Keep SKILL.md under ~500 lines; move details to `references/`
  - Avoid deep reference chains (link only one level from SKILL.md)
  - Add a table of contents to reference files longer than 100 lines
  - If a reference file exceeds ~10k words, include grep search patterns

### Step 11: Validate Skill

After generating, validate the skill:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_skill.py <skill_directory>
```

Validation checks:
- Frontmatter format and required fields
- Name/description length limits
- Naming conventions
- Content structure

### Step 12: Package Skill (optional)

If packaging is requested, run:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/package_skill.py <skill_directory> [output-directory]
```

## Output Format

The final output must include:

1. **Summary** - Brief description of what was created
2. **File Tree** - Directory structure showing all files
3. **File Contents** - Complete content of each file
4. **Package Output** - Path to the `.skill` file if packaged
5. **Verification Instructions** - How to test the skill

## Error Handling

If any step fails, report:
- Which step failed
- Exact error message
- Specific remediation steps

Common errors:
- **URL Parse Error**: Invalid GitHub URL format
- **404 Not Found**: Repository doesn't exist or is private
- **403 Forbidden**: Private repo or rate limited
- **Documentation Empty**: No README or docs found

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/skill-template.md`** - Complete skill file template
- **`references/anthropic-conventions.md`** - Anthropic skills conventions

### Example Files

Working examples in `examples/`:
- **`examples/example-anime-skill.md`** - Example skill for anime.js library
