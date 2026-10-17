# Platform Integration Guide

This document details how each supported AI coding agent platform loads and uses skills from this collection.

## OpenCode

**Skill Discovery Paths:**

| Scope | Path | Notes |
|---|---|---|
| Global config | `~/.config/opencode/skills/` | Skills here are available to all projects |
| User profile | `~/.claude/skills/` | Shared with Claude Code |
| Project-local | `.opencode/skills/` | Active for the current project |
| Project-local | `.claude/skills/` | Alternative project-local path |
| Project-local | `.agents/skills/` | Fallback project-local path |

**Configuration:** OpenCode scans all configured skill directories at startup. Skills are loaded by reading each `SKILL.md` file. Optional subdirectories (`scripts/`, `references/`, `assets/`) are mounted alongside the skill.

**Installation:**
```bash
./installers/install-opencode.sh
```

## Claude Code

**Skill Discovery Paths:**

| Scope | Path | Notes |
|---|---|---|
| Global config | `~/.claude/skills/` | Available in all sessions |
| Project-local | `.claude/skills/` | Active in the project root |
| Fallback | `.agents/skills/` | Secondary fallback |

**Configuration:** Claude Code (anthropic-cli) reads skills from its configured paths. Skills are loaded when a session starts and are available as context for tool use.

**Installation:**
```bash
./installers/install-claude-code.sh
```

## OpenAI Codex (CLI)

**Skill Discovery Paths:**

| Scope | Path | Notes |
|---|---|---|
| Global config | `$HOME/.agents/skills/` | Available to all projects |
| Project-local | `.agents/skills/` (repo root and above) | Walks up the directory tree |

**Configuration:** OpenAI Codex looks for skills in `.agents/skills/` starting from the current working directory and walking upward. This means placing a symlink or copy of skills at your project root will make them available to Codex sessions in that project.

**Installation:**
```bash
./installers/install-codex.sh
```

## Cursor

**Skill Discovery Paths:**

| Scope | Path | Notes |
|---|---|---|
| Global config | `~/.agents/skills/` | Available globally |
| Project-local | `.agents/skills/` | Per-project skills |
| Workspace settings | Custom path via Cursor config | Set in Cursor's workspace settings |

**Configuration:** Cursor supports multiple approaches:
1. **File-based**: Drop skills into `.agents/skills/` at your project root
2. **Settings-based**: Configure a custom skill directory in Cursor's workspace or user settings that points to this collection's `skills/` directory

**Installation:**
```bash
./installers/install-cursor.sh
```

## GitHub Copilot CLI (Codex)

**Skill Discovery Paths:**

| Scope | Path | Notes |
|---|---|---|
| Global config | `~/.agents/skills/` | Available everywhere |
| Project-local | `.agents/skills/` | Per-project |

Same as OpenAI Codex — both use the `.agents/skills/` convention.

## Open WebUI / LibreChat

These platforms differ from CLI agents in how they load skills:

**Open WebUI:**
- Skills are typically loaded by the **Computer** agent tool via a local path configuration
- Configure the Computer agent to point at `skills/` or `.agents/skills/` within your Open WebUI project directory
- No global user path — skills must be available in the deployment's filesystem

**LibreChat:**
- Skills may be loaded through the Agent plugin's configuration
- Point the plugin's skill directory config at this collection's `skills/` folder
- Or copy skills into a local `.agents/skills/` within your LibreChat project

**Setup for Open WebUI:**
```bash
# Copy skills into your Open WebUI deployment
cp -r ./skills/* /path/to/open-webui/.agents/skills/
```

**Setup for LibreChat:**
```bash
# Point Agent plugin config at this collection's skills directory
# Or copy locally:
cp -r ./skills/* /path/to/librechat/.agents/skills/
```

## LangChain Python Tools (`tools/`)

The Python tools in `tools/` are **not** platform-specific. They work with any LangChain-based agent harness:

```bash
# Install the package
pip install -e ".[tools]"

# Use in your own code
from tools.maths import calculator
from tools.weather import weather_query

# Or load all tools dynamically
import importlib, pkgutil, tools

all_tools = []
for importer, modname, ispkg in pkgutil.iter_modules(tools.__path__):
    if modname != "mcp_server" and not modname.startswith("_"):
        mod = importlib.import_module(f"tools.{modname}")
        # Extract @tool-decorated functions from the module
```

## Cross-Platform Tips

1. **Use the universal installer** to install to all detected platforms:
   ```bash
   ./installers/install.sh
   ```

2. **Symlink for multi-platform access:** If you want skills available across multiple platforms without duplicating files, symlink from one location:
   ```bash
   ln -s /path/to/SkillsandAgents/skills ~/.agents/skills/
   ```

3. **Keep `SKILL.md` up to date** — this is the only file each platform reads at a minimum. All other behavior derives from what's in that file.
