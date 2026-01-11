# Skill Generator Plugin

Convert public GitHub repositories into Claude skills compatible with the Anthropic skills ecosystem.

## Features

- **Automated Pipeline**: Parse URL → Verify repo → Fetch docs → Analyze → Generate skill
- **Deterministic Verification**: Python scripts for reliable GitHub API interaction
- **Documentation Ingestion**: WebFetch from Codewiki + optional Firecrawl MCP
- **Web Search Enrichment**: Find additional context and examples
- **Example-Driven Triggers**: Ask for 2-3 target tasks when docs are thin
- **Full Validation**: Verify generated skills meet Anthropic conventions
- **Progressive Disclosure Guardrails**: Keep SKILL.md lean with structured references
- **Ready-to-Commit Output**: Complete skill files written to disk
- **Optional Packaging**: Create a `.skill` file on request

## Installation

### From Plugin Directory

```bash
claude --plugin-dir /path/to/skill-generator
```

### Copy to Claude Plugins

```bash
# Copy to global plugins
cp -r skill-generator ~/.claude/plugins/

# Or copy to project plugins
cp -r skill-generator .claude/plugins/
```

## Usage

### Command

```bash
/create-skill https://github.com/juliangarnier/anime
```

With options:
```bash
/create-skill https://github.com/juliangarnier/anime --name custom-name --output ./custom-path --package ./dist
```

### Natural Language

Simply ask Claude:

```
create a skill for https://github.com/juliangarnier/anime
```

Or:

```
generate a Claude skill from the axios GitHub repo
```

## Pipeline Steps

1. **URL Parsing**: Extract owner/repo, validate format
2. **GitHub API Verification**: Check repo exists, get metadata
3. **Codewiki URL Generation**: Create documentation URL
4. **Documentation Ingestion**: Fetch via WebFetch or Firecrawl
5. **Target Task Collection**: Ask for example tasks when docs are thin
6. **Web Search Enrichment**: Find tutorials, examples, limitations
7. **Repository Analysis**: Understand APIs and use cases
8. **Skills Ecosystem Check**: Verify no duplicates
9. **Structure Selection**: Choose workflow/task/reference/capabilities layout
10. **Skill Generation**: Create SKILL.md and supporting files
11. **Validation**: Verify against Anthropic conventions
12. **Packaging (optional)**: Create a `.skill` file
13. **Output**: Write files to disk

## Configuration

The plugin checks for API keys in this order:
1. `.claude/config.json` in your project
2. `.env` file in your working directory
3. Environment variables

### Option 1: Interactive Setup (Recommended)

Simply run `/create-skill` - if no API keys are found, the plugin will prompt you to configure them and save to `.claude/config.json` automatically.

### Option 2: Config File

Create `.claude/config.json` in your project:

```json
{
  "firecrawl_api_key": "fc-your-api-key",
  "github_token": "ghp_your-token"
}
```

Add `.claude/config.json` to your `.gitignore` to keep keys private.

### Option 3: .env File

Create a `.env` file in your working directory:

```
FIRECRAWL_API_KEY=fc-your-api-key
GITHUB_TOKEN=ghp_your-token
```

Add `.env` to your `.gitignore` to keep keys private.

### Option 4: Environment Variables

**macOS/Linux:**
```bash
export FIRECRAWL_API_KEY=fc-your-api-key
export GITHUB_TOKEN=ghp_your-token
```

**Windows (PowerShell):**
```powershell
$env:FIRECRAWL_API_KEY = "fc-your-api-key"
$env:GITHUB_TOKEN = "ghp_your-token"
```

### API Keys

| Key | Purpose | Get it at |
|-----|---------|-----------|
| `firecrawl_api_key` | Enhanced documentation scraping | https://firecrawl.dev |
| `github_token` | Higher GitHub API rate limits | https://github.com/settings/tokens |

Without these keys, the plugin uses WebFetch and unauthenticated GitHub API (rate limited).

## Components

### Commands

- **`/create-skill`**: Main command to convert a GitHub repo to a skill

### Agents

- **`skill-generator`**: Autonomous agent handling the full conversion pipeline

### Skills

- **`skill-generator`**: Knowledge about Anthropic skills conventions and templates

### Scripts

- **`github_utils.py`**: URL parsing, GitHub API verification, Codewiki URL generation
- **`validate_skill.py`**: Skill validation against Anthropic conventions
- **`package_skill.py`**: Package skills into distributable `.skill` files
- **`firecrawl_utils.py`**: Enhanced web scraping using Firecrawl API

## Output Format

Generated skills follow this structure:

```
skill-name/
├── SKILL.md           # Main skill file with frontmatter
├── references/        # Detailed documentation (optional)
│   └── api-reference.md
├── examples/          # Working code examples (optional)
│   └── basic-usage.js
├── scripts/           # Utility scripts (optional)
└── assets/            # Templates or bundled files (optional)
```

### SKILL.md Format

```yaml
---
name: skill-name
description: Comprehensive description with trigger phrases...
---

# Skill Title

## When to Use This Skill
...

## Installation
...

## Quick Start
...

## Examples
...

## Limitations
...
```

## Packaging Skills

To create a distributable `.skill` file, either pass `--package` to `/create-skill` or run manually:

```bash
python scripts/package_skill.py ./generated-skill-name
```

With custom output directory:

```bash
python scripts/package_skill.py ./generated-skill-name ./dist
```

The packager automatically validates before creating the `.skill` file.

## Requirements

- Python 3.11+ (for utility scripts)
- Internet access (for GitHub API and documentation fetching)
- Claude Code with WebFetch and WebSearch tools

## Troubleshooting

### "Repository not found"

- Verify the URL is correct
- Ensure the repository is public
- Check for typos in owner/repo names

### "Rate limit exceeded"

- Wait for rate limit reset (usually 60 requests/hour for unauthenticated)
- Set `GITHUB_TOKEN` for higher limits

### "Empty documentation"

- Some repos have minimal READMEs
- The plugin will still generate a basic skill
- Consider contributing documentation to the original repo

### "Validation errors"

- Check the error message for specific issues
- Common: name too long, invalid characters, missing description
- The plugin will report exactly what needs fixing

## Examples

### Basic Usage

```
User: create a skill for https://github.com/juliangarnier/anime

Claude: [Runs full pipeline and generates anime-js skill]
```

### With Custom Name

```
User: /create-skill https://github.com/axios/axios --name http-client
```

### Library Skill

```
User: make a skill for lodash

Claude: I'll create a skill for the lodash utility library...
[Generates lodash-utils skill with common utility functions]
```

## Contributing

Contributions welcome! Key areas:

- Additional documentation sources
- Better API extraction patterns
- Support for more repository types
- Improved validation rules

## License

MIT

## Credits

- [Anthropic Skills Ecosystem](https://github.com/anthropics/skills)
- [Codewiki](https://codewiki.google) for documentation
- [Firecrawl](https://firecrawl.dev) for optional enhanced scraping
