# Repository Instructions for Agents

## Purpose & Scope
- **Distribution collection**, not a runnable application. Skills are copied into user harnesses (`opencode`, `claude-code`, `cursor`, etc.) via installers.
- Python tools (`tools/`) are standalone LangChain `@tool` modules. Import them directly in your own code; don't try to run this repo as a service.

## Quick Reference Commands
| Task | Command |
|------|---------|
| Install skills (auto-detect runtime) | `./installers/install.sh` |
| Install for specific platform | `./installers/install-<platform>.sh` (opencode, claude-code, codex, cursor, openwebui) |
| Dev environment | `pip install -e ".[dev]"` |
| Lint / Format / Test | `ruff check .` → `ruff format .` → `pytest` |
| Use Python tools locally | `pip install -e ".[tools]"`, then `from tools.<name> import <module>` |

## Directory Layout
- `skills/<name>/SKILL.md` — Agent Skills standard. Each directory is self-contained; optional subdirs: `scripts/`, `references/`, `assets/`.
- `tools/<name>.py` — LangChain Core `@tool` decorated modules. No package structure; each file is independent.
- `installers/*.sh` — Copy scripts that read `$SKILLS_DIR` and paste into harness config paths (e.g., `~/.config/opencode/skills/`).
- `docs/PLATFORMS.md` — Exact install paths per harness. Check here if unsure where skills land.

## Work Constraints
- **Do not** run skills directly from this repo. They are meant to be installed into external agent configurations.
- **Do not** modify installer scripts unless explicitly tasked with adding platform support or changing copy logic.
- When editing `SKILL.md` files, preserve YAML frontmatter (`name`, `description`). Changes to the body only.
- Python tools use LangChain's `@tool` decorator. Keep signatures explicit and type-safe. No hidden state or global mutability.

## Gotchas & Defaults
- **License**: Repo is MIT. Most skills are originally Apache-2.0 (compatible). Check individual `SKILL.md` frontmatter for exceptions.
- **Python version**: Requires 3.12+. Enforced in `pyproject.toml`.
- **Testing**: `pytest` has no special fixtures or parallel runs. Run tests from the project root after installing deps.
- **Git**: `.user-profile.md`, `.venv/`, `.idea/`, and build artifacts are ignored. Commit only installer scripts, skills, tools, docs, and config files.

## Where to Look First
1. `README.md` — Complete skill/tool catalog and install paths.
2. `installers/install.sh` — Universal auto-detection logic (bash).
3. `pyproject.toml` — Exact dependencies, dev tooling, and build backend.
4. `docs/PLATFORMS.md` — Platform-specific path mappings for skills and tools.