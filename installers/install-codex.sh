#!/usr/bin/env bash
# Installer for OpenAI Codex — installs skills to Codex paths.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PROJECT_DIR/skills"

if [[ ! -d "$SKILLS_DIR" ]]; then
    echo "Error: skills/ directory not found." >&2
    exit 1
fi

echo "=== OpenAI Codex Skill Installer ==="

# OpenAI Codex looks for skills in .agents/skills/ at the repo root and above.
# We install globally to ~/agents/skills/ and optionally project-local.

TARGET_DIRS=(
    "$HOME/.agents/skills"
    "$PROJECT_DIR/.agents/skills"
)

count=0
for target in "${TARGET_DIRS[@]}"; do
    parent="$(dirname "$target")"
    [[ ! -d "$parent" ]] && continue

    label="$([ "$target" = "$HOME/.agents/skills" ] && echo 'global' || echo 'project-local')"
    echo "Installing to ($label): $target"
    mkdir -p "$target"
    for skill_dir in "$SKILLS_DIR"/*/; do
        local_name="$(basename "$skill_dir")"
        if [[ -f "$skill_dir/SKILL.md" ]]; then
            cp -r "$skill_dir" "$target/$local_name/" 2>/dev/null || true
            echo "  ✓ $local_name"
        fi
    done
    count=$((count + 1))
done

if [[ $count -eq 0 ]]; then
    echo "No writable Codex paths found." >&2
    echo "Run: mkdir -p ~/.agents/skills && $0" >&2
fi

echo ""
echo "=== Done — OpenAI Codex skills installed ==="
