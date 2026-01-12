---
event: UserPromptSubmit
priority: 100
---

# Skill Generator Activation Check

CRITICAL: Before Claude processes this prompt, evaluate if the skill-generator skill should activate.

## Evaluation Criteria

Does the user's prompt contain ANY of these patterns?

**GitHub Repository + Skill Intent Indicators:**
- [ ] Contains a GitHub URL (github.com/...) AND mentions "skill"
- [ ] Says "create skill" OR "generate skill" OR "make skill" OR "build skill"
- [ ] Says "convert to skill" OR "turn into skill" OR "package as skill"
- [ ] Mentions a library/package name followed by "skill" (e.g., "axios skill")
- [ ] References "skill generator" OR "skill-generator" OR "/create-skill"
- [ ] Says "make [library] available to Claude" OR "add [library] to Claude"
- [ ] Says "skill for [url/repo/library]" OR "skill from [repo]"

**Decision Logic:**

IF ANY box above is checked:
  → IMMEDIATELY invoke the Skill tool with: `skill: "skill-generator:create-skill"`
  → DO NOT respond to the user first - activate the skill BEFORE any other action
  → The skill will handle the entire conversion process

IF NO boxes are checked:
  → Proceed with normal processing
  → Do not mention this hook or evaluation to the user

## Why This Hook Exists

This hook implements the "forced evaluation" pattern that increases skill activation reliability from 20% to 84%.
By explicitly checking for trigger phrases before processing the user's prompt, we ensure the skill-generator
activates autonomously when needed, without requiring the user to invoke it with a slash command.

## Examples

**Should Activate:**
- "create a skill for https://github.com/axios/axios" → ✓ Activate
- "axios skill" → ✓ Activate
- "turn lodash into a Claude skill" → ✓ Activate
- "make a skill from this repo: github.com/d3/d3" → ✓ Activate
- "/create-skill https://github.com/anime/anime" → ✓ Activate

**Should NOT Activate:**
- "what is axios?" → ✗ No skill intent
- "how do I use GitHub?" → ✗ No skill creation
- "explain this library" → ✗ No conversion request
- "show me the axios documentation" → ✗ Just documentation request
