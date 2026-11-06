# Skills & Agents Collection

A curated collection of **21 AI agent skills** (following the [Agent Skills open standard](https://github.com/anthropics/agent-skills)) and **25 LangChain-compatible Python tools** for integration with major AI coding agents.

## Contents

### Skills (`skills/`)
Each subdirectory follows the Agent Skills open standard: a top-level `SKILL.md` defines the skill's purpose, triggers, and instructions. Optional subdirectories include `scripts/`, `references/`, and `assets/`.

| # | Skill | Description |
|---|---|---|
| 1 | `academy-guide` | Academy onboarding and course guidance |
| 2 | `algorithmic-art` | Algorithmic art generation |
| 3 | `financial-history` | Import and reconcile statements; query saved financial history for spending, income, balances, recurring payments, and forecasts |
| 4 | `bank-transaction-tagging` | Tag saved transactions with vendor names, categories and user rules |
| 5 | `brand-guidelines` | Brand consistency checks and guidelines |
| 6 | `canvas-design` | Canvas-based visual design |
| 7 | `discernment-nudge` | Quality review nudges and discernment prompts |
| 8 | `doc-coauthoring` | Collaborative document co-authoring workflows |
| 9 | `docx` | Microsoft Word (.docx) document handling |
| 10 | `frontend-design` | Front-end UI/UX design patterns |
| 11 | `internal-comms` | Internal communications drafting and templates |
| 12 | `mcp-builder` | MCP (Model Context Protocol) server builder |
| 13 | `rss-reader` | rss aggregation and summarisation |
| 14 | `pdf` | PDF reading, extraction and generation |
| 15 | `pptx` | Microsoft PowerPoint (.pptx) presentation handling |
| 16 | `skill-creator` | Create new agent skills (SKILL.md format) |
| 17 | `slack-gif-creator` | Slack GIF creation workflows |
| 18 | `theme-factory` | Theme generation and customization |
| 19 | `web-artifacts-builder` | Web-based artifact builders |
| 20 | `webapp-testing` | Web application testing workflows |
| 21 | `xlsx` | Microsoft Excel (.xlsx) spreadsheet handling |

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

Use the skills and command prompts for the coding workflow. The main chat runs each stage and shows its result, evidence, open issues and next step. It stops at each approval gate. The command prompts do not assign work to specialist agents. Existing skill installers do not automatically register command prompts; add them to your harness as commands for the main agent.

- `/backlog <direction>`: load `software-development-workflow` and `software-development-requirements` to inspect project evidence, research sources and prepare a ranked backlog. Show the draft and exact revision for approval before requirements work.
- `/plan <feature or backlog ID>`: load `software-development-workflow` and `software-development-requirements` to match or save the requested feature, then prepare requirements, applicable designs and an iteration plan in visible stages. Wait for approval at each gate.
- `/plan next backlog item` or `/plan next feature`: process the approved queue sequentially through development and verification, stopping for existing approvals.
- `/implement <iteration ID>`: load `software-development-coding` after the user approves the iteration.
- `/review <iteration ID>`: load `software-development-testing`, `software-development-code-review`, `software-development-code-simplification` and `software-development-security` in the main chat. These checks are not independent reviews.

The target project's `docs/product-backlog.md` stores feature IDs, rank, scope, evidence, approvals, status, stage and lifecycle links. The main chat maintains the record when its tool access permits. Backlog approval does not replace later approvals. A direct feature request handles only that feature; saved queue state resumes through the approval, next and resume commands. Test, code and security checks run in the main chat. They are not independent reviews.

The shared rules live in `skills/software-development-workflow/SKILL.md`. Each command names the task skills to load. Task skills describe how to do their work; command prompts set the task and order. Tool permissions remain in the harness and are not enforced by skills.

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
