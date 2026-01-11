# Workflow Patterns

Use these patterns when skills involve multi-step processes.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Provide an overview at the beginning:

```markdown
Creating a skill from a GitHub repo involves these steps:

1. Parse and verify URL (run github_utils.py)
2. Fetch documentation (WebFetch from Codewiki)
3. Collect target tasks if docs are thin (ask for 2-3 examples)
4. Enrich with web search (find tutorials, limitations)
5. Analyze repository (identify APIs, use cases)
6. Select skill structure (workflow/task/reference/capabilities)
7. Generate skill files (create SKILL.md)
8. Validate output (run validate_skill.py)
9. Package if needed (run package_skill.py)
```

## Conditional Workflows

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the repository type:
   **JavaScript library?** → Follow "JS Library workflow" below
   **Python package?** → Follow "Python workflow" below
   **CLI tool?** → Follow "CLI Tool workflow" below

2. JS Library workflow:
   - Check for package.json
   - Extract npm install command
   - Look for TypeScript types

3. Python workflow:
   - Check for setup.py or pyproject.toml
   - Extract pip install command
   - Look for type hints

4. CLI Tool workflow:
   - Identify installation method
   - Document key commands and flags
   - Include configuration options
```

## Structure Selection

Use the repo and target tasks to choose a primary layout:

```markdown
1. Choose the skill structure:
   **Workflow-based?** -> use numbered steps and decision points
   **Task-based?** -> create task sections and quick starts
   **Reference/guidelines?** -> emphasize rules, standards, and constraints
   **Capabilities-based?** -> list capabilities with sub-sections
```

## Error Recovery Workflows

For tasks that may fail, include recovery steps:

```markdown
## If documentation fetch fails

1. Try fallback: raw README from GitHub
2. If still empty, use web search to find docs
3. If no docs found, generate minimal skill with warning

## If validation fails

1. Read the specific error message
2. Fix the identified issue
3. Re-run validation
4. Repeat until all errors resolved
```

## Parallel vs Sequential

**Run in parallel** when steps are independent:
- Fetching documentation AND running web searches
- Reading multiple reference files

**Run sequentially** when steps depend on previous output:
- Parse URL → then verify with GitHub API
- Generate skill → then validate → then package
