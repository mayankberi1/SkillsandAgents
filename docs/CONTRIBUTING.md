# Contributing to Skills & Agents Collection

Thank you for your interest in contributing! This document explains how to add new skills and tools to this collection.

## Adding a New Skill

Skills follow the [Agent Skills open standard](https://github.com/anthropics/agent-skills). Each skill is a directory under `skills/` containing at minimum a `SKILL.md` file.

### Steps

1. **Create a new directory** under `skills/`:
   ```bash
   mkdir skills/my-new-skill
   ```

2. **Create `SKILL.md`** with the following structure:
   ```markdown
   # My New Skill

   A brief description of what this skill does (1-1024 characters).

   ## When to Use

   Describe when the agent should apply this skill. Be specific about triggers
   and context that indicate this skill is relevant.

   ## Instructions

   Step-by-step instructions for the agent to follow when using this skill.
   Be thorough and cover common scenarios, edge cases, and best practices.

   ## Constraints

   Any constraints or guidelines the agent should observe.
   ```

3. **Optional: add supporting files**:
   ```bash
   skills/my-new-skill/
   ├── SKILL.md          # Required — skill definition
   ├── scripts/          # Optional — helper scripts the skill may invoke
   │   └── helper.sh
   ├── references/       # Optional — reference documents, templates, schemas
   │   └── template.md
   └── assets/           # Optional — images, icons, other static assets
       └── logo.png
   ```

4. **Update `README.md`**: Add your skill to the skills table with a description.

5. **License compliance**: If deriving from Anthropic's skills (Apache-2.0), note this in your SKILL.md and keep attribution.

### Naming Rules

- 1–64 characters
- Lowercase letters, numbers, and hyphens only
- Must match the directory name exactly

## Adding a New Tool

Tools are LangChain Core `@tool`-decorated Python modules under `tools/`.

### Steps

1. **Create a new file** under `tools/`:
   ```bash
   touch tools/my_new_tool.py
   ```

2. **Implement the tool**:
   ```python
   from langchain_core.tools import tool

   @tool
   def my_function(input: str) -> str:
       """Description of what this tool does."""
       # Implementation here
       return result
   ```

3. **Update `README.md`**: Add your tool to the tools table.

4. **Update `pyproject.toml`** if new runtime dependencies are needed.

## Code Standards

- Follow existing project conventions (see `main.py` and existing tools for style)
- Use descriptive function and variable names
- Keep functions focused and cohesive
- Add docstrings to all public functions
- Run `ruff check .` before committing

## Commit Message Format

Use conventional commits:
- `feat: add new-skill skill for X`
- `fix: correct tool description in Y.py`
- `docs: update README with Z`
- `chore: update version to 0.2.0`
