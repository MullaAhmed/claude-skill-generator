# Skill Generator Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blueviolet.svg)](https://claude.ai)

> Convert public GitHub repositories into Claude skills compatible with the Anthropic skills ecosystem.

Transform any GitHub library or tool into a ready-to-use Claude skill with automated documentation ingestion, API analysis, and skill generation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Pipeline Steps](#pipeline-steps)
- [Configuration](#configuration)
- [Components](#components)
- [Output Format](#output-format)
- [Packaging Skills](#packaging-skills)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

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

### From Marketplace (Recommended)

```bash
# Step 1: Add the marketplace
/plugin marketplace add MullaAhmed/skill-generator-marketplace

# Step 2: Install the skill-generator plugin
/plugin install skill-generator@skill-generator-marketplace 
```

Alternatively, install directly from the marketplace URL:
```bash
/plugin marketplace add https://raw.githubusercontent.com/MullaAhmed/skill-generator-marketplace/main/.claude-plugin/marketplace.json
```

### From GitHub 

```bash
# Clone and install globally
git clone https://github.com/MullaAhmed/skill-generator-marketplace.git
cp -r skill-generator-marketplace ~/.claude/plugins/skill-generator

# Or install to current project
cp -r skill-generator-marketplace .claude/plugins/skill-generator
```

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

## Quick Start

```bash
# 1. Install the plugin (choose one method above)

# 2. Generate a skill from any GitHub repo
/create-skill https://github.com/juliangarnier/anime

# 3. Find your generated skill in ./skills/anime-js/
```

That's it! The plugin handles URL parsing, documentation fetching, API analysis, and skill generation automatically.

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
8. **Skills Ecosystem Check**: Verify no duplicates, identify companion skills
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

## Quick Start
...

## Core Tasks
...

## Pitfalls and Limits
...

## Resources
...
```

Structure varies by repo type; the description carries the "when to use" triggers.

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

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Built with:
- [Anthropic Claude](https://anthropic.com) - AI backbone
- [Anthropic Skills Ecosystem](https://github.com/anthropics/skills) - Skills format and conventions
- [Codewiki](https://codewiki.google) - Documentation source
- [Firecrawl](https://firecrawl.dev) - Optional enhanced web scraping

## Author

**Ahmed Mulla** - [GitHub](https://github.com/MullaAhmed)

---

<p align="center">Made with Claude Code</p>
