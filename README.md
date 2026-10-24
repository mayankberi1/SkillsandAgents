# Skills & Agents Collection

A curated collection of **19 AI agent skills** (following the [Agent Skills open standard](https://github.com/anthropics/agent-skills)) and **25 LangChain-compatible Python tools** for integration with major AI coding agents.

## Contents

### Skills (`skills/`)
Each subdirectory follows the Agent Skills open standard: a top-level `SKILL.md` defines the skill's purpose, triggers, and instructions. Optional subdirectories include `scripts/`, `references/`, and `assets/`.

| # | Skill | Description |
|---|-------|-------------|
| 1 | `academy-guide` | Academy onboarding and course guidance |
| 2 | `algorithmic-art` | Algorithmic art generation |
| 3 | `brand-guidelines` | Brand consistency checks and guidelines |
| 4 | `canvas-design` | Canvas-based visual design |
| 5 | `discernment-nudge` | Quality review nudges and discernment prompts |
| 6 | `doc-coauthoring` | Collaborative document co-authoring workflows |
| 7 | `docx` | Microsoft Word (.docx) document handling |
| 8 | `frontend-design` | Front-end UI/UX design patterns |
| 9 | `internal-comms` | Internal communications drafting and templates |
| 10 | `mcp-builder` | MCP (Model Context Protocol) server builder |
| 11 | `rss-reader` | rss aggregation and summarisation |
| 12 | `pdf` | PDF reading, extraction and generation |
| 13 | `pptx` | Microsoft PowerPoint (.pptx) presentation handling |
| 14 | `skill-creator` | Create new agent skills (SKILL.md format) |
| 15 | `slack-gif-creator` | Slack GIF creation workflows |
| 16 | `theme-factory` | Theme generation and customization |
| 17 | `web-artifacts-builder` | Web-based artifact builders |
| 18 | `webapp-testing` | Web application testing workflows |
| 19 | `xlsx` | Microsoft Excel (.xlsx) spreadsheet handling |

> **Note:** Most skills in this collection originate from [Anthropic's official skills repository](https://github.com/anthropics/agent-skills). They are licensed under Apache-2.0, which is MIT-compatible for redistribution with attribution.

### Tools (`tools/`)
LangChain Core `@tool`-decorated Python modules compatible with any LangChain-based agent harness.

| # | Tool | Description |
|---|------|-------------|
| 1 | `api.py` | Generic API calling tool |
| 2 | `authentication.py` | Authentication and login helpers |
| 3 | `calendar.py` | Calendar operations (create, list, query) |
| 4 | `data.py` | General data manipulation |
| 5 | `database.py` | Database query interface |
| 6 | `fetch_text_from_url.py` | Fetch plain text from a URL |
| 7 | `finance.py` | Financial data and calculations |
| 8 | `flights.py` | Flight search and booking queries |
| 9 | `generic.py` | General-purpose utility tool |
| 10 | `gmail.py` | Gmail operations |
| 11 | `hotels.py` | Hotel search and booking |
| 12 | `map.py` | Map and geolocation queries |
| 13 | `maths.py` | Mathematical calculations |
| 14 | `mcp_client.py` | MCP client for tool calling |
| 15 | `mcp_server.py` | MCP server implementation |
| 16 | `media_organiser.py` | Media file organisation |
| 17 | `memory.py` | Agent memory operations |
| 18 | `password.py` | Password management helpers |
| 19 | `payments.py` | Payment processing queries |
| 20 | `rss_reader.py` | RSS feed reading |
| 21 | `tasks.py` | Task management |
| 22 | `text_summariser.py` | Text summarisation |
| 23 | `user_profile.py` | User profile operations |
| 24 | `weather.py` | Weather data queries |

### Installers (`installers/`)
Platform-specific installer scripts for deploying skills to various agent runtimes. See [docs/PLATFORMS.md](docs/PLATFORMS.md) for details.

- `install.sh` — Universal installer (auto-detects platform)
- `install-opencode.sh` — Installs to OpenCode skill paths
- `install-claude-code.sh` — Installs to Claude Code skill paths
- `install-codex.sh` — Installs to OpenAI Codex paths
- `install-cursor.sh` — Installs to Cursor paths
- `install-openwebui.sh` — Guides for Open WebUI / LibreChat setup

## Backlog-driven development

Configure the definitions in `agents/` and `commands/` in your harness to use this workflow. Existing skill installers do not automatically register these definitions.

- `/backlog <direction>`: Product Owner inspects the project, researches sources and brainstorms a ranked backlog with you. Drafts are saved before approval.
- `/plan <feature or backlog ID>`: reuse an existing item or save a new requested feature before requirements work. Ambiguous/completed matches and switching active work require clarification.
- `/plan next backlog item` or `/plan next feature`: process the approved queue sequentially through development and verification, stopping for existing approvals.

The target project's `docs/product-backlog.md` stores feature IDs, rank, scope, evidence, approvals, status, stage and lifecycle links. Product Owner owns content; specialists report progress; Coordinator persists checkpoints. Backlog approval does not replace lifecycle approvals. Explicit feature requests handle only that feature; saved queue state resumes through existing approval, next and resume commands.

## Installation

### Quick Install (Universal)

```bash
./installers/install.sh
```

This script detects your available agent runtime and installs skills to the appropriate global or project-local paths.

### Per-Platform Installation

```bash
# OpenCode
./installers/install-opencode.sh

# Claude Code
./installers/install-claude-code.sh

# OpenAI Codex
./installers/install-codex.sh

# Cursor
./installers/install-cursor.sh

# Open WebUI / LibreChat
./installers/install-openwebui.sh
```

## Platform-Specific Skill Paths

| Platform | Project Local Paths | Global User Paths |
|---|---|---|
| **OpenCode** | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` |
| **Claude Code** | `.claude/skills/`, `.agents/skills/` | `~/.claude/skills/`, `~/.agents/skills/` |
| **OpenAI Codex** | `.agents/skills/` (repo root and above) | `$HOME/.agents/skills/` |
| **Cursor** | `.agents/skills/` or workspace settings | User's `.agents/skills/` |
| **GitHub Copilot CLI** | `.agents/skills/` | `~/.agents/skills/` |
| **Open WebUI / LibreChat** | Project-local via Computer agent config | Depends on Computer deployment |

## Using the Python Tools

Install the package and its dependencies:

```bash
pip install -e ".[tools]"
```

Then import any tool module directly:

```python
from tools.maths import calculator
from tools.weather import weather_query
# Use with your LangChain-based agent harness
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Lint
ruff check .

# Format
ruff format .

# Test
pytest
```

## License

MIT — except where noted (most skills are Apache-2.0, which is MIT-compatible). See individual skill `SKILL.md` files for their specific license terms.
