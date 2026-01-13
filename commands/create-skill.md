---
name: create-skill
description: |
  MANDATORY skill generator - converts GitHub repositories to Claude skills compatible with Anthropic ecosystem.

  ACTIVATE when user says: "create skill", "generate skill from [repo]", "make a skill for [url]",
  "convert [repo] to skill", "skill for [library]", or provides GitHub URLs with skill creation intent.

  Supports single or multiple repository URLs for parallel processing via sub-agents.
argument-hint: "<github_url> [github_url2 ...] [--name <skill-name>] [--output <path>] [--package [<path>]]"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebFetch
  - WebSearch
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Create Skill from GitHub Repository

Convert public GitHub repositories into ready-to-commit Claude skills following Anthropic skills ecosystem conventions. When multiple URLs are provided, spawn parallel sub-agents for concurrent processing.

## Argument Parsing

Parse the provided arguments:
- **Required**: `<github_url>` - One or more GitHub repository URLs
  - Multiple URLs can be provided, separated by spaces
  - Example: `/create-skill https://github.com/axios/axios https://github.com/lodash/lodash`
- **Optional**: `--name <skill-name>` - Override the generated skill name (only for single URL)
- **Optional**: `--output <path>` - Output directory (default: `.claude/skills/`)
- **Optional**: `--package [<path>]` - Package into a `.skill` file after generation

If no URL is provided, prompt the user for one.

## Multi-URL Detection and Parallel Processing

**CRITICAL**: Before proceeding with the standard pipeline, detect if multiple GitHub URLs are provided.

### Step 0: Detect Multiple URLs

1. Parse arguments and extract all GitHub URLs matching patterns:
   - `https://github.com/owner/repo`
   - `github.com/owner/repo`
   - `http://github.com/owner/repo`

2. Count valid URLs found

### Parallel Sub-Agent Spawning (2+ URLs)

If **2 or more URLs** are detected:

1. **Do NOT proceed with the single-skill pipeline below**
2. **Spawn parallel sub-agents using the Task tool**

For each URL, use the Task tool with these parameters:
- `subagent_type`: `"skill-generator:skill-generator-worker"`
- `description`: `"Generate skill from {repo_name}"`
- `prompt`: A detailed prompt containing the github_url, output directory, package options, and any API keys from config

**IMPORTANT**: Call ALL Task tools in a SINGLE message to enable parallel execution.

Example prompt for each sub-agent:
```
Generate a Claude skill from the GitHub repository: {github_url}

Configuration:
- Output directory: {output_path or ".claude/skills/"}
- Package skill: {true/false}
- Firecrawl API key: {key or "not configured"}
- GitHub token: {token or "not configured"}

Follow the skill-generator-worker pipeline and return the results.
```

After all sub-agents complete, aggregate and report:
- Summary of all skills created
- Any failures with resolution steps
- File tree for each skill
- Verification instructions

**STOP HERE if multiple URLs detected** - do not continue to the single-skill pipeline below.

---

## Single-Skill Pipeline (1 URL)

The following steps apply only when a single GitHub URL is provided.

## Configuration Check (API Keys)

Before starting the pipeline, check for API keys in this order:

### Step 0: Check for API Keys

Check these locations in order:

**1. Check `.claude/config.json`:**
```json
{
  "firecrawl_api_key": "fc-xxx",
  "github_token": "ghp-xxx"
}
```

**2. Check `.env` file in working directory:**
```
FIRECRAWL_API_KEY=fc-xxx
GITHUB_TOKEN=ghp-xxx
```

**3. Check environment variables:**
- `FIRECRAWL_API_KEY`
- `GITHUB_TOKEN`

**4. If keys not found, prompt user:**

Use AskUserQuestion:
- Question: "Would you like to configure API keys for enhanced features?"
- Options:
  - "Yes, I have a Firecrawl API key" → Ask for the key
  - "Yes, I have a GitHub token" → Ask for the token
  - "No, continue without" → Proceed with WebFetch only

**4. If user provides keys:**
- Create/update `.claude/config.json` with the keys:
```json
{
  "firecrawl_api_key": "user-provided-key",
  "github_token": "user-provided-token"
}
```
- Set environment variables for current session using Bash:
```bash
export FIRECRAWL_API_KEY="user-provided-key"
export GITHUB_TOKEN="user-provided-token"
```

**5. If user declines:**
- Proceed with WebFetch (no Firecrawl)
- Use unauthenticated GitHub API (rate limited)

## Execution Pipeline

Execute the following steps in order. If any step fails, report the error and stop.

### Step 1: Verify Repository

Run the GitHub verification script:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/github_utils.py full "<github_url>"
```

Parse the JSON output:
- If `success: false`, report the error and stop
- Extract: `owner`, `repo`, `metadata`, `codewiki_url`
- Note if repository is `archived` or a `fork`

### Step 2: Ingest Documentation

#### Primary: Fetch from Codewiki
Use WebFetch to get documentation from the Codewiki URL:

```
URL: https://codewiki.google/github.com/{owner}/{repo}
Prompt: Extract complete documentation including README, API references,
installation instructions, usage examples, and code snippets.
Preserve all code examples with their language annotations.
```

#### Fallback: Direct README
If Codewiki fails, fetch the raw README:

```
URL: https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/README.md
```

#### Enhanced: Firecrawl (if configured)
If `firecrawl_api_key` was found in Step 0 (from config.json or env var):

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/firecrawl_utils.py scrape "<codewiki_url>" --max-chars 200000 --output ".claude/tmp/firecrawl/{owner}-{repo}.md"
```

Parse the JSON output:
- If `success: true`, use the `content` field (markdown, possibly truncated)
- If `content_truncated: true`, read the full `content_path` in chunks (iterate with offset/limit until EOF) and assemble a complete doc before analysis
- If `success: false`, fall back to WebFetch

This provides better extraction than WebFetch for complex documentation sites.

#### Also fetch official docs if available

If GitHub metadata includes a `homepage` URL or the README links to official docs, fetch those pages too. Prefer official docs over mirrors for API signatures, examples, and usage notes.

### Step 3: Collect Target Tasks (if needed)

If documentation is sparse or the repo purpose is ambiguous, ask for 2-3 concrete tasks and example user prompts. Use AskUserQuestion:
- Question: "What 2-3 tasks should this skill handle? Share example user prompts if possible."

Use the answers to:
- Add trigger phrases to the `description`
- Build realistic Examples sections
- Decide what should be in `references/`, `scripts/`, or `assets/`

### Step 4: Web Search Enrichment

Run these WebSearch queries:
1. `"{repo_name}" tutorial getting started`
2. `"{repo_name}" documentation examples`
3. `"{repo_name}" common issues limitations`

Extract:
- Official documentation URL
- Common usage patterns
- Known limitations
- Community examples

### Step 5: Analyze Repository

Synthesize documentation into a technical understanding:
- Purpose and primary use cases
- Key APIs/functions/commands
- Installation requirements
- Platform support
- Common pitfalls

### Step 5.5: Classify Skill Type and Companion Skills

Determine what kind of skill this is (library, CLI tool, framework, spec, UI component set, integration, etc.). Use that classification to pick any companion skills that would materially help the user.

Rules:
- Only add companion skills if there is a clear, practical benefit.
- Limit to 1-3 companion skills.
- Use skill names from the Anthropic skills ecosystem (e.g., `frontend-design`, `web-artifacts-builder`, `webapp-testing`, `mcp-builder`, `docx`, `pdf`, `pptx`, `xlsx`, `brand-guidelines`, `theme-factory`, `internal-comms`, `slack-gif-creator`, `algorithmic-art`).
- If no companion skills are relevant, omit the section.

### Step 6: Check Skills Ecosystem

Search for existing similar skills:
- Check if a skill for this library already exists
- Identify potential naming conflicts
- Note any related skills

### Step 7: Select Skill Structure

Choose a structure that matches the repo and target tasks:
- **Workflow-based** for sequential processes
- **Task-based** for tool collections
- **Reference/guidelines** for standards or specs
- **Capabilities-based** for integrated systems

State the chosen structure in SKILL.md headings and keep it consistent.

### Step 8: Generate Skill Files

Read the skill template:
```bash
cat ${CLAUDE_PLUGIN_ROOT}/skills/skill-generator/references/skill-template.md
```

Generate the skill following these requirements:

**Directory Structure:**
```
{skill-name}/
├── SKILL.md
├── references/
│   └── api-reference.md (if API is complex)
├── examples/
│   └── basic-usage.{ext} (if helpful)
├── scripts/ (optional, for repeatable transforms)
└── assets/ (optional, for templates or bundled files)
```

**SKILL.md Requirements:**
- YAML frontmatter with `name` and `description` only (add other fields only if explicitly requested)
- `name`: max 64 chars, lowercase + hyphens only, no "anthropic"/"claude"
- `description`: max 1024 chars, include trigger phrases and "when to use" details
- Body: concise and task-focused, imperative form
- Use a structure that matches the repo (task-based, workflow-based, reference/guidelines, or capabilities-based)
- Add a Companion Skills section only when relevant (1-3 skills, with reasons)
- Progressive disclosure:
  - Keep SKILL.md under ~500 lines; move details to `references/`
  - Avoid deep reference chains (link only one level from SKILL.md)
  - Add a table of contents to reference files longer than 100 lines
  - If a reference file exceeds ~10k words, include grep search patterns

### Step 9: Validate Generated Skill

Run validation:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/validate_skill.py <skill_directory>
```

Fix any errors before proceeding.

### Step 10: Write Files

Write all skill files to the output directory using the Write tool.

### Step 11: Package Skill (optional)

If `--package` is provided, run:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/package_skill.py <skill_directory> [output-directory]
```

## Output Format

After successful generation, provide:

1. **Summary**: Brief description of what was created

2. **File Tree**:
```
{skill-name}/
├── SKILL.md
└── [other files]
```

3. **GitHub URL**: Original repository URL
4. **Codewiki URL**: Generated Codewiki URL
5. **Package Output** (if `--package` used): Path to the `.skill` file

6. **Verification Instructions**:
```
To test this skill:
1. The skill is created in .claude/skills/ by default (ready to use)
2. Start a new Claude Code session
3. Ask a question that should trigger the skill
4. Verify the skill loads and provides helpful guidance
```

## Error Handling

If any step fails, report:
- **Step**: Which step failed (1-11)
- **Error**: Exact error message
- **Resolution**: Specific steps to fix

Common errors:
- Invalid GitHub URL → Check URL format
- Repository not found → Verify URL and that repo is public
- Rate limited → Wait or use GitHub token
- Empty documentation → Repository may lack README

## Tips

- For large repositories, focus on the most commonly used APIs
- Include 2-5 task examples or workflow steps with short, working snippets when applicable
- Test code examples for syntax correctness
- Add `scripts/` or `assets/` when the repo includes repeatable transforms or templates
- Cite sources in your reasoning but not in the skill files
